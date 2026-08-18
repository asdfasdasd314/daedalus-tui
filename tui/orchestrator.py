"""Single-run local agent orchestration without daemon or database dependencies."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import uuid
from typing import Callable

from .agent_runner import AgentControl, AgentRequest, AgentResult, AgentRunner
from .debug_log import LOGGER, log_exception
from .graphify import update_repository
from .git_worktree import GitWorktreeError, GitWorktreeManager, WorktreeContext
from .prompts import build_repair_prompt, build_resolver_prompt, build_task_prompt
from .verification import discover_commands, run_verification


EventCallback = Callable[[str, str, str], None]
IntegrationGate = Callable[[int, Callable[[], None]], None]
PROFILE_FILENAMES = {
    "coding": "coding.md",
    "plan": "planning.md",
    "integrating": "integrating.md",
}


@dataclass(frozen=True)
class OrchestrationSettings:
    primary_branch: str = "main"
    worktree_root: str = ".daedalus-worktrees"
    verification_commands: tuple[tuple[str, ...], ...] = ()
    task_verification_attempt_limit: int = 3
    resolver_attempt_limit: int = 3
    max_concurrent_tasks: int = 4
    agent_timeout_seconds: float = 450.0
    graphify_update_enabled: bool = True
    graphify_executable: str = "graphify"
    shutdown_grace_seconds: float = 8.0
    debug_log_filename: str = ".daedalus-debug.log"


@dataclass(frozen=True)
class OrchestrationResult:
    succeeded: bool
    task_id: str
    branch_name: str = ""
    worktree: Path | None = None
    error: str | None = None
    context: WorktreeContext | None = None
    paused: bool = False
    cancelled: bool = False
    tokens_consumed: int = 0
    awaiting_plan: bool = False


class AgentStopped(RuntimeError):
    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


class LocalOrchestrator:
    def __init__(
        self,
        repository: Path,
        runner: AgentRunner,
        settings: OrchestrationSettings,
        on_event: EventCallback,
        integration_gate: IntegrationGate | None = None,
    ):
        self.repository = repository.resolve()
        self.runner = runner
        self.settings = settings
        self.on_event = on_event
        self.integration_gate = integration_gate or (lambda _sequence, operation: operation())
        self._tokens_consumed = 0

    def run(
        self,
        prompt: str,
        provider: str,
        model: str,
        reasoning: str,
        task_id: str | None = None,
        submission_sequence: int = 0,
        mode: str = "coding",
        control: AgentControl | None = None,
        existing_context: WorktreeContext | None = None,
        resume_notes: tuple[str, ...] = (),
    ) -> OrchestrationResult:
        task_id = task_id or uuid.uuid4().hex[:12]
        LOGGER.info("Orchestration started task=%s mode=%s provider=%s", task_id, mode, provider)
        context: WorktreeContext | None = existing_context
        manager = GitWorktreeManager(
            self.repository,
            self.settings.primary_branch,
            self.settings.worktree_root,
        )
        try:
            self.emit("worktree", "Validating the primary Git worktree.")
            if context is None:
                context = manager.create(task_id)
                self.emit("worktree", f"Created {context.branch_name} at {context.path}.")
            else:
                manager.validate_primary()
                self.emit("worktree", f"Resuming {context.branch_name} at {context.path}.")
            self._raise_if_stopped(control)

            selection = (provider, model, reasoning)
            self.emit(
                "planning" if mode == "plan" else "agent",
                f"Planning with {provider} in the isolated worktree."
                if mode == "plan"
                else f"Running {provider} in the isolated worktree.",
            )
            profile_text = self.load_profile(context.path, mode)
            result = self.run_agent(
                manager,
                context,
                selection,
                build_task_prompt(
                    prompt,
                    mode,
                    resume_notes,
                    resumed=existing_context is not None,
                    profile_text=profile_text,
                ),
                control,
                event_phase="planning" if mode == "plan" else "agent",
            )
            if not result.succeeded:
                raise RuntimeError(result.error or "Agent execution failed.")

            if mode in {"ask", "plan"}:
                manager.discard_graphify_changes(context.path)
            if mode == "plan":
                manager.reset_task_to_base(context)
                self.emit("questioning", "Plan ready. Review it, answer questions, or start coding.")
                return OrchestrationResult(
                    True,
                    task_id,
                    context.branch_name,
                    context.path,
                    context=context,
                    awaiting_plan=True,
                    tokens_consumed=self._completed_tokens(),
                )
            if mode == "ask":
                manager.remove_successful(context)
                self.emit("completed", f"Completed {mode} task.")
                return OrchestrationResult(
                    True,
                    task_id,
                    context.branch_name,
                    context.path,
                    context=context,
                    tokens_consumed=self._completed_tokens(),
                )

            manager.discard_graphify_changes(context.path)
            manager.commit_changes(context.path, f"Daedalus task {task_id}")
            if manager.head(context.path) == context.base_commit:
                raise RuntimeError("Agent finished without creating a commit.")
            self.verify_with_repairs(manager, context, selection, prompt, control)

            def integrate_and_promote() -> None:
                self._raise_if_stopped(control)
                integration_base = manager.capture_primary()
                self.integrate(manager, context, selection, prompt, control)
                manager.promote(context, integration_base)
                self.refresh_graphify(manager, task_id)

            self.emit("ready", "Task is ready for serialized integration.")
            self.integration_gate(submission_sequence, integrate_and_promote)
            manager.remove_successful(context)
            self.emit("completed", f"Promoted {context.branch_name} into {self.settings.primary_branch}.")
            return OrchestrationResult(
                True,
                task_id,
                context.branch_name,
                context.path,
                context=context,
                tokens_consumed=self._completed_tokens(),
            )
        except AgentStopped as stopped:
            LOGGER.info("Orchestration stopped task=%s reason=%s", task_id, stopped.reason)
            if stopped.reason == "cancelled" and context is not None:
                manager.remove_cancelled(context)
                self.emit("cancelled", "Task cancelled and its worktree was removed.")
                return OrchestrationResult(
                    False,
                    task_id,
                    context.branch_name,
                    context.path,
                    "Task cancelled.",
                    cancelled=True,
                    tokens_consumed=self._completed_tokens(False),
                )
            self.emit("paused", "Task paused; its worktree and current progress were preserved.")
            return OrchestrationResult(
                False,
                task_id,
                context.branch_name if context else "",
                context.path if context else None,
                context=context,
                paused=True,
                tokens_consumed=self._completed_tokens(False),
            )
        except (GitWorktreeError, RuntimeError, ValueError) as error:
            log_exception(f"Orchestration failed task={task_id}", error)
            message = str(error)
            self.emit("failed", message, "error")
            return OrchestrationResult(
                False,
                task_id,
                context.branch_name if context else "",
                context.path if context else None,
                message,
                context=context,
                tokens_consumed=self._completed_tokens(False),
            )

    def run_agent(
        self,
        manager: GitWorktreeManager,
        context: WorktreeContext,
        selection: tuple[str, str, str],
        prompt: str,
        control: AgentControl | None = None,
        event_phase: str = "agent",
    ) -> AgentResult:
        provider, model, reasoning = selection
        request = AgentRequest(
            prompt=prompt,
            directory=context.path,
            provider=provider,
            model=model,
            reasoning=reasoning,
            writable_directories=(context.path,),
            environment_files=(self.repository / ".env",),
            control=control,
            timeout_seconds=self.settings.agent_timeout_seconds,
        )
        result = self.runner.run(
            request,
            lambda event: self.emit(event_phase, event.text, event.kind),
        )
        if result.tokens_consumed is not None:
            self._tokens_consumed += result.tokens_consumed
        if provider == "cursor" and result.succeeded and result.output and not result.output_streamed:
            self.emit(event_phase, result.output, "message")
        if result.stopped_reason:
            raise AgentStopped(result.stopped_reason)
        return result

    def verify_with_repairs(
        self,
        manager: GitWorktreeManager,
        context: WorktreeContext,
        selection: tuple[str, str, str],
        original: str,
        control: AgentControl | None = None,
    ) -> None:
        commands = discover_commands(
            context.path,
            [list(command) for command in self.settings.verification_commands],
        )
        attempts = 0
        while True:
            self.emit("verification", "Running verification checks.")
            self._raise_if_stopped(control)
            result = run_verification(context.path, commands)
            self._raise_if_stopped(control)
            if result.succeeded:
                return
            attempts += 1
            if attempts >= self.settings.task_verification_attempt_limit:
                raise RuntimeError(
                    f"Verification failed after {self.settings.task_verification_attempt_limit} attempts.\n\n"
                    f"{result.output}"
                )
            self.emit("repairing", f"Launching task repair attempt {attempts}/{self.settings.task_verification_attempt_limit}.")
            profile_text = self.load_profile(context.path, "coding")
            repair = self.run_agent(
                manager,
                context,
                selection,
                build_repair_prompt(
                    original,
                    result.output,
                    attempts,
                    self.settings.task_verification_attempt_limit,
                    profile_text=profile_text,
                ),
                control,
            )
            if not repair.succeeded:
                raise RuntimeError(repair.error or "Task repair agent failed.")
            manager.commit_changes(context.path, f"Daedalus task repair {attempts}")

    def integrate(
        self,
        manager: GitWorktreeManager,
        context: WorktreeContext,
        selection: tuple[str, str, str],
        original: str,
        control: AgentControl | None = None,
    ) -> None:
        failure = ""
        try:
            self._raise_if_stopped(control)
            self.emit("integration", f"Merging {self.settings.primary_branch} into {context.branch_name}.")
            manager.merge_primary_into_task(context)
        except GitWorktreeError as error:
            failure = str(error)

        if failure:
            self.resolve_integration(manager, context, selection, original, failure, control)

        commands = discover_commands(
            context.path,
            [list(command) for command in self.settings.verification_commands],
        )
        result = run_verification(context.path, commands)
        self._raise_if_stopped(control)
        if not result.succeeded:
            self.resolve_integration(manager, context, selection, original, result.output, control)

    def resolve_integration(
        self,
        manager: GitWorktreeManager,
        context: WorktreeContext,
        selection: tuple[str, str, str],
        original: str,
        failure: str,
        control: AgentControl | None = None,
    ) -> None:
        for attempt in range(1, self.settings.resolver_attempt_limit + 1):
            self._raise_if_stopped(control)
            self.emit("resolving", f"Launching resolver attempt {attempt}/{self.settings.resolver_attempt_limit}.")
            profile_text = self.load_profile(context.path, "integrating")
            result = self.run_agent(
                manager,
                context,
                selection,
                build_resolver_prompt(
                    original,
                    failure,
                    attempt,
                    self.settings.resolver_attempt_limit,
                    profile_text=profile_text,
                ),
                control,
            )
            if result.succeeded:
                manager.stage_changes(context.path)
                if manager.has_unmerged_paths(context.path):
                    failure = "Resolver left unmerged Git paths in the task worktree."
                    continue
                manager.discard_graphify_changes(context.path)
                manager.commit_changes(context.path, f"Daedalus resolver attempt {attempt}")
                commands = discover_commands(
                    context.path,
                    [list(command) for command in self.settings.verification_commands],
                )
                verification = run_verification(context.path, commands)
                self._raise_if_stopped(control)
                if verification.succeeded:
                    return
                failure = verification.output
            else:
                failure = result.error or "Resolver agent failed."
        raise RuntimeError(
            f"Integration failed after {self.settings.resolver_attempt_limit} resolver attempts.\n\n{failure}"
        )

    def load_profile(self, worktree: Path, route: str) -> str | None:
        """Load a repository-owned profile immediately before building a prompt."""
        filename = PROFILE_FILENAMES.get(route)
        if filename is None:
            return None
        profile_path = worktree / ".agents" / "profiles" / filename
        try:
            return profile_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            message = f"Could not load {route} profile from {profile_path}: {error}"
            LOGGER.warning(message)
            self.emit("profile", message, "error")
            return None

    def refresh_graphify(self, manager: GitWorktreeManager, task_id: str) -> None:
        """Refresh graph metadata after promotion without blocking the task."""
        if not self.settings.graphify_update_enabled:
            return
        if not (self.repository / "graphify-out").exists():
            self.emit("graphify", "Graph refresh skipped because graphify-out is not present.")
            return
        self.emit("graphify", "Refreshing the primary repository graph.")
        result = update_repository(self.repository, self.settings.graphify_executable)
        if not result.succeeded:
            # A failed or partial refresh must not dirty the primary worktree
            # and must never trigger a resolver attempt for the code task.
            try:
                manager.discard_graphify_changes(self.repository)
            except GitWorktreeError as cleanup_error:
                self.emit(
                    "graphify",
                    f"Graph refresh failed and cleanup also failed: {cleanup_error}",
                    "error",
                )
            self.emit("graphify", f"Graph refresh skipped: {result.output or 'unknown error'}")
            return
        try:
            committed = manager.commit_graphify_changes(f"Daedalus graphify update after task {task_id}")
        except GitWorktreeError as error:
            try:
                manager.discard_graphify_changes(self.repository)
            except GitWorktreeError as cleanup_error:
                self.emit("graphify", f"Graph refresh commit failed and cleanup also failed: {cleanup_error}", "error")
            self.emit("graphify", f"Graph refresh completed but could not be committed: {error}", "error")
            return
        self.emit("graphify", "Graph refresh committed." if committed else "Graph refresh completed with no changes.")

    def emit(self, phase: str, message: str, kind: str = "status") -> None:
        LOGGER.debug("Orchestration event phase=%s kind=%s message_length=%d", phase, kind, len(message))
        self.on_event(phase, message, kind)

    def _completed_tokens(self, completed: bool = True) -> int:
        """Expose usage only after the whole task reaches completion."""
        return self._tokens_consumed if completed else 0

    @staticmethod
    def _raise_if_stopped(control: AgentControl | None) -> None:
        if control is not None and control.stop_reason:
            raise AgentStopped(control.stop_reason)
