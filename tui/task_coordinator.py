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
from .debug_log import LOGGER, log_exception
from .git_worktree import GitWorktreeError, GitWorktreeManager, WorktreeContext
from .memory import DEFAULT_MEMORY_FILE, TaskMemoryStore
from .orchestrator import LocalOrchestrator, OrchestrationResult, OrchestrationSettings
from .plan import (
    PlanQuestion,
    build_implementation_prompt,
    build_plan_followup_prompt,
    parse_plan_response,
)


TaskEventCallback = Callable[["TaskRecord", str, str, str], None]
TASK_STATUSES = (
    "queued",
    "planning",
    "questioning",
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
    "awaiting_answers",
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
    tokens_consumed: int = 0
    submitted_at: float = field(default_factory=time.time)
    started_at: float | None = None
    finished_at: float | None = None
    resume_notes: list[str] = field(default_factory=list)
    context: WorktreeContext | None = field(default=None, repr=False, compare=False)
    control: AgentControl = field(default_factory=AgentControl, repr=False, compare=False)
    future: Future | None = field(default=None, repr=False, compare=False)
    memory_task_id: str | None = field(default=None, repr=False, compare=False)
    plan_text: str = ""
    plan_questions: tuple[PlanQuestion, ...] = ()
    plan_answers: dict[str, str] = field(default_factory=dict)
    plan_answer_details: dict[str, str] = field(default_factory=dict)
    plan_confirmed: bool = False
    plan_implemented: bool = False
    plan_error: str | None = None
    prompt_history: list[str] = field(default_factory=list, repr=False, compare=False)
    plan_followup_prompt: str | None = field(default=None, repr=False, compare=False)
    retry_prompt: str | None = field(default=None, repr=False, compare=False)
    retry_output_context: str | None = field(default=None, repr=False, compare=False)


class IntegrationCoordinator:
    """Run ready integration operations one at a time in ready order."""

    def __init__(self) -> None:
        self._condition = Condition()
        self._ready: list[tuple[int, int, Callable[[], None]]] = []
        self._ready_counter = 0
        self._active = False
        self._closed = False

    def shutdown(self) -> None:
        with self._condition:
            self._closed = True
            self._condition.notify_all()

    def run_when_ready(self, sequence: int, operation: Callable[[], None]) -> None:
        with self._condition:
            if self._closed:
                raise RuntimeError("Integration coordinator is shut down.")
            self._ready_counter += 1
            entry = (self._ready_counter, sequence, operation)
            self._ready.append(entry)
            self._ready.sort(key=lambda item: (item[0], item[1]))
            while self._active or self._ready[0] is not entry:
                self._condition.wait(timeout=0.1)
                if self._closed:
                    self._ready.remove(entry)
                    self._condition.notify_all()
                    raise RuntimeError("Integration coordinator is shut down.")
            if self._closed:
                self._ready.remove(entry)
                self._condition.notify_all()
                raise RuntimeError("Integration coordinator is shut down.")
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
        self.memory = TaskMemoryStore(memory_path or self.repository / DEFAULT_MEMORY_FILE)

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
            record.prompt_history = [prompt]
            record.memory_task_id = f"task-{task_id}"
            self._tasks[task_id] = record
            self._persist_task(record)
            record.future = self.executor.submit(self._run, record)
        self._notify(record, "queued", "Task queued.", "status")
        return record

    def answer_plan(self, task_id: str, answers: dict[str, str]) -> bool:
        """Send selected plan answers back to the planning agent for confirmation."""
        with self._lock:
            record = self._tasks.get(task_id)
            if (
                record is None
                or record.mode != "plan"
                or record.plan_confirmed
                or record.status not in {"completed", "awaiting_answers"}
            ):
                return False
            question_ids = {question.question_id for question in record.plan_questions}
            if not question_ids.issubset(answers):
                return False
            valid_answers = {
                question.question_id: answer
                for question in record.plan_questions
                for answer in [answers.get(question.question_id)]
                if answer is not None and any(option.option_id == answer for option in question.options)
            }
            if question_ids - valid_answers.keys():
                return False
            record.plan_answers.update(valid_answers)
            for question in record.plan_questions:
                answer_id = valid_answers.get(question.question_id)
                if answer_id is None:
                    continue
                option = next(option for option in question.options if option.option_id == answer_id)
                record.plan_answer_details[question.question_id] = f"{question.text}: {option.label}"
            record.plan_followup_prompt = build_plan_followup_prompt(
                record.prompt, record.plan_text, record.plan_questions, record.plan_answers
            )
            record.prompt_history.append(record.plan_followup_prompt)
            record.status = "queued"
            record.phase = "Queued (reviewing answers)"
            record.error = None
            record.plan_error = None
            self._persist_task(record)
            record.future = self.executor.submit(self._run, record)
            LOGGER.info("Plan answers queued task=%s answer_ids=%s", record.task_id, sorted(valid_answers))
        self._notify(record, "queued", "Plan answers queued for agent confirmation.", "status")
        return True

    def implement_plan(self, task_id: str) -> TaskRecord | None:
        """Create a new coding task from a confirmed plan review."""
        with self._lock:
            record = self._tasks.get(task_id)
            if (
                record is None
                or record.mode != "plan"
                or record.status != "completed"
                or not record.plan_confirmed
                or record.plan_implemented
            ):
                return None
            if any(question.question_id not in record.plan_answers for question in record.plan_questions):
                return None
            # Claim the one-shot transition before submitting so concurrent UI
            # events cannot create more than one coding task.
            record.plan_implemented = True
        try:
            coding_record = self.submit(
                build_implementation_prompt(
                    record.prompt,
                    record.plan_text,
                    record.plan_answers,
                    record.plan_answer_details,
                ),
                record.provider,
                record.model,
                record.reasoning,
                mode="coding",
            )
        except Exception:
            with self._lock:
                record.plan_implemented = False
            raise
        self._discard_plan_worktree(record)
        return coding_record

    def tasks(self) -> tuple[TaskRecord, ...]:
        with self._lock:
            return tuple(sorted(self._tasks.values(), key=lambda task: task.submission_sequence))

    def get(self, task_id: str) -> TaskRecord | None:
        with self._lock:
            return self._tasks.get(task_id)

    def shutdown(self) -> bool:
        with self._lock:
            if self._closed:
                return True
            self._closed = True
            self.integration.shutdown()
            for record in self._tasks.values():
                if record.status in {
                    "queued",
                    "planning",
                    "running",
                    "verifying",
                    "ready",
                    "integrating",
                    "resolving",
                }:
                    record.control.request_cancel()
                    LOGGER.info("Shutdown requested task=%s status=%s", record.task_id, record.status)
        # Do not hold Textual's unmount path indefinitely. Active agent process
        # groups receive cancellation above and the executor will finish as they
        # return; any survivor is recorded for inspection in the debug log.
        self.executor.shutdown(wait=False, cancel_futures=True)
        deadline = time.monotonic() + self.settings.shutdown_grace_seconds
        pending: list[TaskRecord] = []
        while time.monotonic() < deadline:
            pending = [
                record
                for record in self._tasks.values()
                if record.future is not None and not record.future.done()
            ]
            if not pending:
                LOGGER.info("Coordinator shutdown completed repository=%s", self.repository)
                return True
            time.sleep(0.05)
        pending_ids = ", ".join(record.task_id for record in pending)
        LOGGER.error("Coordinator shutdown grace period expired pending_tasks=%s", pending_ids or "unknown")
        return False

    def pause(self, task_id: str) -> bool:
        record = self.get(task_id)
        if record is None or record.status in {"completed", "failed", "blocked", "paused", "cancelled"}:
            return False
        if record.status == "questioning":
            return False
        if record.status == "queued" and record.future is not None and record.future.cancel():
            record.status = "paused"
            record.phase = "Paused"
            record.finished_at = time.time()
            self._persist_task(record)
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
            self._persist_task(record)
            record.future = self.executor.submit(self._run, record)
        self._notify(record, "queued", "Task queued to resume in its existing worktree.", "status")
        return True

    def continue_plan(self, task_id: str, notes: str = "") -> bool:
        """Run another planning pass while keeping the task in questioning."""
        with self._lock:
            record = self._tasks.get(task_id)
            if record is None or record.status != "questioning" or self._closed:
                return False
            planning_output = "\n\n".join(message for message in record.messages if message.strip()).strip()
            if planning_output:
                record.resume_notes.append("Review this previous planning output:\n" + planning_output)
            if notes.strip():
                record.resume_notes.append(notes.strip())
            record.status = "queued"
            record.phase = "Queued (continuing plan)"
            record.error = None
            self._persist_task(record)
            record.future = self.executor.submit(self._run, record)
        self._notify(record, "queued", "Task queued for another planning pass.", "status")
        return True

    def start_coding(self, task_id: str, notes: str = "") -> bool:
        """Promote a reviewed plan into the normal coding and verification route."""
        with self._lock:
            record = self._tasks.get(task_id)
            if record is None or record.status != "questioning" or self._closed:
                return False
            planning_output = "\n\n".join(message for message in record.messages if message.strip()).strip()
            if planning_output:
                record.resume_notes.append(
                    "Carry this planning context into implementation:\n" + planning_output
                )
            if notes.strip():
                record.resume_notes.append(notes.strip())
            record.mode = "coding"
            record.status = "queued"
            record.phase = "Queued (starting coding)"
            record.error = None
            self._persist_task(record)
            record.future = self.executor.submit(self._run, record)
        self._notify(record, "queued", "Task queued to start coding from its plan.", "status")
        return True

    def retry(self, task_id: str) -> bool:
        """Retry a failed agent request after connectivity or service recovery."""
        with self._lock:
            record = self._tasks.get(task_id)
            if record is None or record.status != "failed" or self._closed:
                return False
            visible_output = "\n\n".join(message.strip() for message in record.messages if message.strip())
            record.retry_output_context = (
                "Previous visible AI output from the failed attempt:\n" + visible_output
                if visible_output
                else None
            )
            record.control = AgentControl()
            record.status = "queued"
            record.phase = "Queued (retrying)"
            record.error = None
            record.finished_at = None
            self._persist_task(record)
            record.future = self.executor.submit(self._run, record)
        self._notify(record, "queued", "Task queued for retry.", "status")
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
                    self._persist_task(record)
                    self._notify(record, "failed", record.error, "error")
                    return False
            record.status = "cancelled"
            record.phase = "Cancelled"
            record.error = "Task cancelled and its worktree was removed."
            record.finished_at = time.time()
            self._persist_task(record)
            self._notify(record, "cancelled", record.error, "error")
            return True
        if record.status == "questioning":
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
                    record.error = f"Cancelled plan cleanup failed: {error}"
                    self._persist_task(record)
                    self._notify(record, "failed", record.error, "error")
                    return False
            record.status = "cancelled"
            record.phase = "Cancelled"
            record.error = "Plan cancelled and its worktree was removed."
            record.finished_at = time.time()
            self._persist_task(record)
            self._notify(record, "cancelled", record.error, "error")
            return True
        if record.status == "queued" and record.future is not None and record.future.cancel():
            record.status = "cancelled"
            record.phase = "Cancelled"
            record.error = "Task cancelled before execution."
            record.finished_at = time.time()
            self._persist_task(record)
            self._notify(record, "cancelled", record.error, "error")
            return True
        record.control.request_cancel()
        record.phase = "Cancelling"
        self._notify(record, "cancelling", "Stopping the active agent and removing its worktree.", "status")
        return True

    def _run(self, record: TaskRecord) -> None:
        LOGGER.info("Task worker started task=%s mode=%s", record.task_id, record.mode)
        record.started_at = time.time()
        self._persist_task(record)
        message_start = len(record.messages)
        if record.mode == "plan" and record.plan_followup_prompt and record.provider == "cursor":
            # Cursor streams deltas by extending the last stored message. Give a
            # follow-up response its own transcript slot before starting it.
            record.messages.append("")
        prompt = record.plan_followup_prompt or record.retry_prompt or record.prompt
        record.retry_prompt = prompt
        record.plan_followup_prompt = None
        resume_notes = tuple(record.resume_notes)
        if record.retry_output_context:
            resume_notes += (record.retry_output_context,)
        record.retry_output_context = None
        orchestrator = LocalOrchestrator(
            self.repository,
            self.runner,
            self.settings,
            lambda phase, message, kind="status": self._handle_event(record, phase, message, kind),
            integration_gate=self.integration.run_when_ready,
        )
        try:
            result = orchestrator.run(
                prompt,
                record.provider,
                record.model,
                record.reasoning,
                task_id=record.task_id,
                submission_sequence=record.submission_sequence,
                mode=record.mode,
                control=record.control,
                existing_context=record.context,
                resume_notes=resume_notes,
            )
        except Exception as error:  # Keep one unexpected task failure isolated from the pool.
            log_exception(f"Task worker crashed task={record.task_id}", error)
            record.finished_at = time.time()
            record.status = "failed"
            record.phase = "Failed"
            record.error = str(error)
            self._persist_task(record)
            self._notify(record, "failed", str(error), "error")
            return
        record.finished_at = time.time()
        record.branch_name = result.branch_name or record.branch_name
        record.worktree_path = result.worktree or record.worktree_path
        record.context = result.context or record.context
        if result.succeeded:
            record.tokens_consumed += result.tokens_consumed
        if result.awaiting_plan:
            if record.mode == "plan":
                self._update_plan_state(record, record.messages[message_start:])
            if record.plan_confirmed:
                record.status = "completed"
                record.phase = "Completed"
            elif record.plan_questions:
                record.status = "awaiting_answers"
                record.phase = "Questions"
            else:
                # Keep malformed or prose-only responses in the selectable
                # planning loop so the user can request another pass.
                record.status = "questioning"
                record.phase = "Questioning"
            record.error = None
            if record.plan_error:
                record.error = record.plan_error
            self._persist_task(record)
            event_phase = {
                "completed": "completed",
                "awaiting_answers": "questions",
            }.get(record.status, "questioning")
            self._notify(
                record,
                event_phase,
                "Plan ready for review." if record.status != "completed" else "Plan confirmed.",
                "status",
            )
            LOGGER.info("Task worker finished task=%s status=%s", record.task_id, record.status)
            return
        if result.paused:
            record.status = "paused"
            record.phase = "Paused"
            record.error = None
            self._persist_task(record)
            self._notify(record, "paused", "Task paused; progress preserved.", "status")
            LOGGER.info("Task worker finished task=%s status=%s", record.task_id, record.status)
            return
        if result.cancelled:
            record.status = "cancelled"
            record.phase = "Cancelled"
            record.error = result.error or "Task cancelled."
            self._persist_task(record)
            self._notify(record, "cancelled", record.error, "error")
            LOGGER.info("Task worker finished task=%s status=%s", record.task_id, record.status)
            return
        if result.succeeded:
            if record.mode == "plan":
                self._update_plan_state(record, record.messages[message_start:])
            if record.mode == "plan" and not record.plan_confirmed:
                if record.plan_questions:
                    record.status = "awaiting_answers"
                    record.phase = "Questions"
                else:
                    record.status = "questioning"
                    record.phase = "Questioning"
            else:
                record.status = "completed"
                record.phase = "Completed"
        else:
            record.status = "failed"
            record.phase = "Failed"
            record.error = record.error or result.error or "Task failed."
        self._persist_task(record)
        self._notify(
            record,
            "questions" if result.succeeded and record.mode == "plan" and record.plan_questions and not record.plan_confirmed else
            ("completed" if result.succeeded else "failed"),
            "",
            "status",
        )
        LOGGER.info("Task worker finished task=%s status=%s", record.task_id, record.status)

    def _update_plan_state(self, record: TaskRecord, new_messages: list[str]) -> bool:
        response = "\n\n".join(new_messages).strip()
        parsed = parse_plan_response(response)
        if not parsed.valid:
            # A protocol error after the user answered questions must not erase
            # the last usable plan or make the choices impossible to resubmit.
            record.plan_confirmed = False
            record.plan_error = parsed.error
            record.error = parsed.error
            LOGGER.warning(
                "Rejected invalid plan payload task=%s response_length=%d error=%s",
                record.task_id,
                len(response),
                parsed.error,
            )
            return False
        record.plan_text = parsed.plan
        record.plan_questions = parsed.questions
        record.plan_confirmed = parsed.valid and parsed.no_more_questions and not parsed.questions
        record.plan_error = None
        record.error = None
        # An agent may revise a question while retaining its id. Do not mount a
        # Select with the now-invalid old value; retain decisions for questions
        # that disappeared because they remain useful implementation context.
        for question in parsed.questions:
            answer_id = record.plan_answers.get(question.question_id)
            if answer_id is not None and not any(option.option_id == answer_id for option in question.options):
                record.plan_answers.pop(question.question_id, None)
                record.plan_answer_details.pop(question.question_id, None)
        return True

    def _discard_plan_worktree(self, record: TaskRecord) -> None:
        """Remove the clean, read-only planning worktree after coding is queued."""
        if record.context is None:
            return
        try:
            manager = GitWorktreeManager(
                self.repository,
                self.settings.primary_branch,
                self.settings.worktree_root,
            )
            manager.remove_successful(record.context)
        except GitWorktreeError as error:
            # The coding task is already queued; a failed cleanup must not
            # prevent it from running or hide the planning result.
            LOGGER.warning("Could not remove plan worktree task=%s error=%s", record.task_id, error)
            return
        LOGGER.info("Removed clean plan worktree task=%s path=%s", record.task_id, record.context.path)
        record.context = None
        record.worktree_path = None
        self._persist_task(record)

    def _handle_event(self, record: TaskRecord, phase: str, message: str, kind: str) -> None:
        record.phase = phase.replace("_", " ").capitalize()
        status = {
            "worktree": "running",
            "planning": "planning",
            "questioning": "questioning",
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
            if record.provider == "cursor" and record.messages:
                record.messages[-1] += message
            else:
                record.messages.append(message)
        if kind == "error" and message:
            record.error = message
        if phase == "worktree" and message.startswith("Created "):
            branch, _, worktree = message.removeprefix("Created ").rstrip(".").partition(" at ")
            if branch and worktree:
                record.branch_name = branch
                record.worktree_path = Path(worktree)
        self._persist_task(record)
        self._notify(record, phase, message, kind)

    def _persist_task(self, record: TaskRecord) -> None:
        """Persist the latest task state without affecting task execution."""
        task_id = record.worktree_path.name if record.worktree_path is not None else f"task-{record.task_id}"
        previous_task_id = record.memory_task_id
        try:
            self.memory.record_task(
                task_id,
                record.prompt,
                record.provider,
                None if record.provider == "cursor" else record.model or None,
                None if record.provider == "cursor" else record.reasoning or None,
                record.mode,
                record.status,
                record.messages,
                record.error,
                previous_task_id=previous_task_id,
                submitted_at=record.submitted_at,
                tokens=record.tokens_consumed,
                project=self.repository,
                prompt_history=tuple(record.prompt_history or (record.prompt,)),
            )
        except (OSError, ValueError) as error:
            # Persistent task history must never change orchestration behavior.
            LOGGER.warning("Could not persist task task=%s error=%s", record.task_id, error)
            return
        record.memory_task_id = task_id

    def _notify(self, record: TaskRecord, phase: str, message: str, kind: str) -> None:
        if self.on_event is not None:
            self.on_event(record, phase, message, kind)
