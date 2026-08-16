"""Concurrent task state and serialized local integration."""

from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from threading import Condition, Lock
import time
import uuid
from typing import Callable

from .agent_runner import AgentControl, AgentRunner
from .git_worktree import GitWorktreeError, GitWorktreeManager, WorktreeContext
from .memory import DEFAULT_MEMORY_FILE, TokenUsageStore
from .orchestrator import LocalOrchestrator, OrchestrationResult, OrchestrationSettings


TaskEventCallback = Callable[["TaskRecord", str, str, str], None]
TASK_STATUSES = (
    "queued",
    "running",
    "verifying",
    "ready",
    "integrating",
    "resolving",
    "completed",
    "failed",
    "blocked",
    "paused",
    "cancelled",
)


@dataclass
class TaskRecord:
    task_id: str
    submission_sequence: int
    prompt: str
    provider: str
    model: str
    reasoning: str
    mode: str = "coding"
    status: str = "queued"
    phase: str = "Queued"
    branch_name: str = ""
    worktree_path: Path | None = None
    messages: list[str] = field(default_factory=list)
    error: str | None = None
    submitted_at: float = field(default_factory=time.time)
    started_at: float | None = None
    finished_at: float | None = None
    resume_notes: list[str] = field(default_factory=list)
    context: WorktreeContext | None = field(default=None, repr=False, compare=False)
    control: AgentControl = field(default_factory=AgentControl, repr=False, compare=False)
    future: Future | None = field(default=None, repr=False, compare=False)
    tokens_consumed: int = 0


class IntegrationCoordinator:
    """Run ready integration operations one at a time in ready order."""

    def __init__(self) -> None:
        self._condition = Condition()
        self._ready: list[tuple[int, int, Callable[[], None]]] = []
        self._ready_counter = 0
        self._active = False

    def run_when_ready(self, sequence: int, operation: Callable[[], None]) -> None:
        with self._condition:
            self._ready_counter += 1
            entry = (self._ready_counter, sequence, operation)
            self._ready.append(entry)
            self._ready.sort(key=lambda item: (item[0], item[1]))
            while self._active or self._ready[0] is not entry:
                self._condition.wait()
            self._ready.pop(0)
            self._active = True

        try:
            operation()
        finally:
            with self._condition:
                self._active = False
                self._condition.notify_all()


class TaskCoordinator:
    """Submit independent prompts while sharing a serialized integration gate."""

    def __init__(
        self,
        repository: Path,
        runner: AgentRunner,
        settings: OrchestrationSettings,
        on_event: TaskEventCallback | None = None,
        memory_path: Path | None = None,
    ) -> None:
        if settings.max_concurrent_tasks < 1:
            raise ValueError("max_concurrent_tasks must be positive")
        self.repository = repository.resolve()
        self.runner = runner
        self.settings = settings
        self.on_event = on_event
        self.integration = IntegrationCoordinator()
        self.executor = ThreadPoolExecutor(max_workers=settings.max_concurrent_tasks)
        self._lock = Lock()
        self._next_sequence = 1
        self._tasks: dict[str, TaskRecord] = {}
        self._closed = False
        self.memory = TokenUsageStore(memory_path or self.repository / DEFAULT_MEMORY_FILE)

    def set_event_callback(self, callback: TaskEventCallback | None) -> None:
        self.on_event = callback

    def submit(self, prompt: str, provider: str, model: str, reasoning: str, mode: str = "coding") -> TaskRecord:
        with self._lock:
            if self._closed:
                raise RuntimeError("Task coordinator is shut down.")
            sequence = self._next_sequence
            self._next_sequence += 1
            task_id = f"{sequence:03d}-{uuid.uuid4().hex[:8]}"
            record = TaskRecord(task_id, sequence, prompt, provider, model, reasoning, mode=mode)
            self._tasks[task_id] = record
            record.future = self.executor.submit(self._run, record)
        self._notify(record, "queued", "Task queued.", "status")
        return record

    def tasks(self) -> tuple[TaskRecord, ...]:
        with self._lock:
            return tuple(sorted(self._tasks.values(), key=lambda task: task.submission_sequence))

    def get(self, task_id: str) -> TaskRecord | None:
        with self._lock:
            return self._tasks.get(task_id)

    def shutdown(self) -> None:
        with self._lock:
            if self._closed:
                return
            self._closed = True
            for record in self._tasks.values():
                if record.status in {"queued", "running", "verifying", "ready", "integrating", "resolving"}:
                    record.control.request_cancel()
        self.executor.shutdown(wait=False, cancel_futures=True)

    def pause(self, task_id: str) -> bool:
        record = self.get(task_id)
        if record is None or record.status in {"completed", "failed", "blocked", "paused", "cancelled"}:
            return False
        if record.status == "queued" and record.future is not None and record.future.cancel():
            record.status = "paused"
            record.phase = "Paused"
            record.finished_at = time.time()
            self._notify(record, "paused", "Task paused before execution.", "status")
            return True
        record.control.request_pause()
        record.phase = "Pausing"
        self._notify(record, "pausing", "Stopping the active agent and preserving progress.", "status")
        return True

    def resume(self, task_id: str, notes: str = "") -> bool:
        with self._lock:
            record = self._tasks.get(task_id)
            if record is None or record.status != "paused" or self._closed:
                return False
            record.control.clear_pause()
            record.status = "queued"
            record.phase = "Queued (resuming)"
            record.error = None
            record.finished_at = None
            if notes.strip():
                record.resume_notes.append(notes.strip())
            record.future = self.executor.submit(self._run, record)
        self._notify(record, "queued", "Task queued to resume in its existing worktree.", "status")
        return True

    def cancel(self, task_id: str) -> bool:
        record = self.get(task_id)
        if record is None or record.status in {"completed", "failed", "blocked", "cancelled"}:
            return False
        if record.status == "paused":
            if record.context is not None:
                try:
                    GitWorktreeManager(
                        self.repository,
                        self.settings.primary_branch,
                        self.settings.worktree_root,
                    ).remove_cancelled(record.context)
                except GitWorktreeError as error:
                    record.status = "failed"
                    record.phase = "Failed"
                    record.error = f"Cancelled task cleanup failed: {error}"
                    self._notify(record, "failed", record.error, "error")
                    return False
            record.status = "cancelled"
            record.phase = "Cancelled"
            record.error = "Task cancelled and its worktree was removed."
            record.finished_at = time.time()
            self._notify(record, "cancelled", record.error, "error")
            return True
        if record.status == "queued" and record.future is not None and record.future.cancel():
            record.status = "cancelled"
            record.phase = "Cancelled"
            record.error = "Task cancelled before execution."
            record.finished_at = time.time()
            self._notify(record, "cancelled", record.error, "error")
            return True
        record.control.request_cancel()
        record.phase = "Cancelling"
        self._notify(record, "cancelling", "Stopping the active agent and removing its worktree.", "status")
        return True

    def _run(self, record: TaskRecord) -> None:
        record.started_at = time.time()
        orchestrator = LocalOrchestrator(
            self.repository,
            self.runner,
            self.settings,
            lambda phase, message, kind="status": self._handle_event(record, phase, message, kind),
            integration_gate=self.integration.run_when_ready,
        )
        try:
            result = orchestrator.run(
                record.prompt,
                record.provider,
                record.model,
                record.reasoning,
                task_id=record.task_id,
                submission_sequence=record.submission_sequence,
                mode=record.mode,
                control=record.control,
                existing_context=record.context,
                resume_notes=tuple(record.resume_notes),
            )
        except Exception as error:  # Keep one unexpected task failure isolated from the pool.
            record.finished_at = time.time()
            record.status = "failed"
            record.phase = "Failed"
            record.error = str(error)
            self._notify(record, "failed", str(error), "error")
            return
        record.finished_at = time.time()
        record.branch_name = result.branch_name or record.branch_name
        record.worktree_path = result.worktree or record.worktree_path
        record.context = result.context or record.context
        if result.paused:
            record.status = "paused"
            record.phase = "Paused"
            record.error = None
            self._notify(record, "paused", "Task paused; progress preserved.", "status")
            return
        if result.cancelled:
            record.status = "cancelled"
            record.phase = "Cancelled"
            record.error = result.error or "Task cancelled."
            self._notify(record, "cancelled", record.error, "error")
            return
        if result.succeeded:
            record.status = "completed"
            record.phase = "Completed"
            record.tokens_consumed = result.tokens_consumed
            try:
                self.memory.record(record.submitted_at, record.tokens_consumed)
            except (OSError, ValueError):
                # Telemetry must never turn an otherwise completed task into a failure.
                pass
        else:
            record.status = "failed"
            record.phase = "Failed"
            record.error = record.error or result.error or "Task failed."
        self._notify(record, "completed" if result.succeeded else "failed", "", "status")

    def _handle_event(self, record: TaskRecord, phase: str, message: str, kind: str) -> None:
        record.phase = phase.replace("_", " ").capitalize()
        status = {
            "worktree": "running",
            "agent": "running",
            "verification": "verifying",
            "repairing": "verifying",
            "ready": "ready",
            "integration": "integrating",
            "resolving": "resolving",
            "completed": "completed",
            "failed": "failed",
            "paused": "paused",
            "cancelled": "cancelled",
        }.get(phase)
        if status:
            record.status = status
        if kind == "message" and message:
            record.messages.append(message)
        if kind == "error" and message:
            record.error = message
        if phase == "worktree" and message.startswith("Created "):
            branch, _, worktree = message.removeprefix("Created ").rstrip(".").partition(" at ")
            if branch and worktree:
                record.branch_name = branch
                record.worktree_path = Path(worktree)
        self._notify(record, phase, message, kind)

    def _notify(self, record: TaskRecord, phase: str, message: str, kind: str) -> None:
        if self.on_event is not None:
            self.on_event(record, phase, message, kind)
