"""Textual interface for concurrent local agent tasks."""

from __future__ import annotations

import asyncio
from pathlib import Path
import threading

from textual import events, on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, DataTable, Footer, Header, Log, Select, Static, TextArea
from .agent_runner import AgentRunner
from .clipboard import copy_to_system_clipboard, paste_from_system_clipboard
from .config import (
    CodingStatisticsSettings,
    TuiSettings,
    load_coding_statistics_settings,
    load_orchestration_settings,
    load_tui_settings,
)
from .debug_log import LOGGER, close_fault_handler, configure_debug_logging, install_fault_handler, log_exception
from .memory import DEFAULT_MEMORY_FILE, TaskMemoryStore
from .projects import DaedalusProject, discover_projects
from .plan import (
    CUSTOM_ANSWER_OPTION_ID,
    PlanQuestion,
    custom_answer_text,
    encode_custom_answer,
    plan_answer_options,
)
from .task_coordinator import TaskCoordinator, TaskRecord
from .transcript import TranscriptLog
from .token_usage import calculate_token_usage, merge_usage_entries, task_usage_entry, usage_entries_from_memory
from .vim_text_area import DaedalusVimTextArea


_THREAD_EXIT_APPS: dict[int, "DaedalusTuiApp"] = {}
_THREAD_EXIT_APPS_LOCK = threading.Lock()
_THREAD_EXIT_HOOK_REGISTERED = False


def _shutdown_apps_before_thread_join() -> None:
    """Pause active agents before ThreadPoolExecutor joins its workers.

    CPython executes ``threading._register_atexit`` callbacks before the
    executor's own thread join. Ordinary ``atexit`` callbacks are too late:
    the executor is already waiting for an agent process by then.
    """
    with _THREAD_EXIT_APPS_LOCK:
        apps = tuple(_THREAD_EXIT_APPS.values())
    for app in apps:
        try:
            app._shutdown_before_thread_join()
        except BaseException as error:
            log_exception("Pre-thread-shutdown coordinator cleanup failed", error)


def _register_app_for_thread_exit(app: "DaedalusTuiApp") -> None:
    global _THREAD_EXIT_HOOK_REGISTERED
    with _THREAD_EXIT_APPS_LOCK:
        _THREAD_EXIT_APPS[id(app)] = app
        if _THREAD_EXIT_HOOK_REGISTERED:
            return
        register = getattr(threading, "_register_atexit", None)
        if not callable(register):
            LOGGER.warning("Python does not provide a pre-thread-shutdown hook.")
            return
        register(_shutdown_apps_before_thread_join)
        _THREAD_EXIT_HOOK_REGISTERED = True


def _unregister_app_for_thread_exit(app: "DaedalusTuiApp") -> None:
    with _THREAD_EXIT_APPS_LOCK:
        _THREAD_EXIT_APPS.pop(id(app), None)


GLOBAL_SHORTCUTS = (
    ("Ctrl+Enter", "Send prompt", "submit_prompt"),
    ("Ctrl+C", "Copy selected text", "copy_selection"),
    ("Ctrl+Alt+S", "Copy selection", "copy_selection"),
    ("Ctrl+P", "Pause task", "pause_task"),
    ("Ctrl+R", "Resume task", "resume_task"),
    ("Ctrl+X", "Cancel task", "cancel_task"),
    ("Ctrl+Q", "Quit", "quit"),
    ("Ctrl+K", "Show keyboard shortcuts", "show_shortcuts"),
    ("Ctrl+T", "Show coding statistics", "show_statistics"),
)

SHORTCUT_SECTIONS = (
    (
        "Global shortcuts",
        tuple((shortcut, description) for shortcut, description, _ in GLOBAL_SHORTCUTS),
    ),
    (
        "Output navigation",
        (
            ("j / k", "Scroll output down / up"),
            ("gg / G", "Scroll to output start / end"),
            ("Ctrl+D / Ctrl+U", "Scroll one page down / up"),
            ("y", "Copy selected text"),
            ("p", "Paste into the prompt"),
            ("i", "Focus the prompt"),
        ),
    ),
    (
        "Prompt (Vim mode)",
        (
            ("Esc", "Enter Normal mode"),
            ("i / a / o", "Enter Insert mode"),
            ("h / j / k / l", "Move the cursor"),
            ("w / e / 0 / $", "Move by word or line"),
            ("gg / G", "Move to document start / end"),
            ("d / u", "Delete / undo"),
            ("y / p", "Yank / paste"),
            ("V", "Select whole lines"),
            ("Enter", "Insert a newline"),
        ),
    ),
)


class PlanAnswerSelect(Select):
    """Initialize dynamic plan selectors after their nested children mount."""

    @on(events.Mount)
    def _on_plan_answer_mount(self, event: events.Mount) -> None:
        # Textual 8.2.x can dispatch a dynamically mounted Select's mount
        # handler before SelectCurrent has mounted its internal ``#label``.
        # The base Select handler is a naming-convention handler and would
        # otherwise also run after this method, so prevent its default action.
        event.prevent_default()
        self.call_after_refresh(self._initialize_after_mount)

    def _initialize_after_mount(self) -> None:
        if self.is_attached and not self._closing:
            self._setup_options_renderables()
            self._init_selected_option(self._value)


class KeyboardShortcutsScreen(ModalScreen[None]):
    """Modal reference for the app and prompt editor keyboard shortcuts."""

    BINDINGS = [
        ("escape", "close_shortcuts", "Close"),
        ("ctrl+k", "close_shortcuts", "Close"),
    ]

    def compose(self) -> ComposeResult:
        with Vertical(id="shortcuts-dialog"):
            yield Static("Keyboard shortcuts", id="shortcuts-title")
            yield Static("Press Esc or Ctrl+K to close", id="shortcuts-subtitle")
            for heading, shortcuts in SHORTCUT_SECTIONS:
                yield Static(heading, classes="shortcut-section")
                for shortcut, description in shortcuts:
                    yield Static(f"{shortcut:<18}{description}", classes="shortcut-row")

    def action_close_shortcuts(self) -> None:
        self.dismiss(None)


class CodingStatisticsScreen(ModalScreen[None]):
    """Show token or task usage history and derived coding statistics."""

    BINDINGS = [
        ("escape", "close_statistics", "Close"),
        ("ctrl+t", "close_statistics", "Close"),
    ]

    def __init__(
        self,
        entries,
        settings: CodingStatisticsSettings | None = None,
    ) -> None:
        super().__init__()
        self.settings = settings or CodingStatisticsSettings()
        self.stats = calculate_token_usage(
            entries,
            recent_window_hours=self.settings.recent_window_hours,
            forecast_days=self.settings.forecast_days,
            thirty_day_forecast_days=self.settings.thirty_day_forecast_days,
        )
        self.unit = "tokens"

    def compose(self) -> ComposeResult:
        with Vertical(id="coding-statistics-dialog"):
            yield Static("Coding statistics", id="coding-statistics-title")
            with Horizontal(id="coding-statistics-controls"):
                yield Static("Measure", id="statistics-unit-label")
                yield Select(
                    [("Tokens", "tokens"), ("Tasks", "tasks")],
                    value="tokens",
                    allow_blank=False,
                    id="statistics-unit-select",
                )
            yield Static("Token usage from recorded local tasks", id="coding-statistics-subtitle")
            with Horizontal(id="coding-statistics-summary"):
                yield Static(id="cumulative-metric", classes="usage-metric")
                yield Static(id="daily-metric", classes="usage-metric")
                yield Static(id="thirty-day-metric", classes="usage-metric")
            with Horizontal(id="coding-statistics-body"):
                with Vertical(id="usage-history-panel"):
                    yield Static("Task usage", classes="statistics-heading")
                    yield DataTable(id="usage-table", cursor_type="row")
                with Vertical(id="usage-breakdown-panel"):
                    yield Static("Statistics", classes="statistics-heading")
                    yield Static(id="average-metric", classes="statistics-value")
                    yield Static(id="recent-metric", classes="statistics-value")
                    yield Static(id="seven-day-metric", classes="statistics-value")
                    yield Static(id="thirty-day-statistic", classes="statistics-value")
                    yield Static(id="provider-split", classes="statistics-value")
            yield Static("Press Esc or Ctrl+T to close", id="coding-statistics-footer")

    def on_mount(self) -> None:
        self._refresh_statistics_view()

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id != "statistics-unit-select" or event.value in (Select.BLANK, ""):
            return
        self.unit = str(event.value)
        self._refresh_statistics_view()

    def _refresh_statistics_view(self) -> None:
        unit = self.unit
        is_tasks = unit == "tasks"
        suffix = "tasks" if is_tasks else "tokens"
        cumulative = self.stats.cumulative_tasks if is_tasks else self.stats.cumulative_tokens
        daily = self.stats.daily_tasks if is_tasks else self.stats.daily_tokens
        recent = self.stats.last_hour_tasks if is_tasks else self.stats.last_hour_tokens
        seven_day = self.stats.seven_day_expected_tasks if is_tasks else self.stats.seven_day_expected_tokens
        thirty_day = self.stats.thirty_day_expected_tasks if is_tasks else self.stats.thirty_day_expected_tokens
        average = self.stats.average_tasks_per_prompt if is_tasks else self.stats.average_tokens_per_prompt
        self.query_one("#coding-statistics-subtitle", Static).update(
            f"{suffix.capitalize()} from recorded local tasks"
        )
        self.query_one("#cumulative-metric", Static).update(
            f"Cumulative {suffix}\n{_format_count(cumulative)}"
        )
        self.query_one("#daily-metric", Static).update(
            f"Today's {suffix}\n{_format_count(daily)}"
        )
        self.query_one("#thirty-day-metric", Static).update(
            f"{self.settings.thirty_day_forecast_days}-day expected {suffix}\n{_format_count(thirty_day)}"
        )
        self.query_one("#average-metric", Static).update(
            f"Average {suffix} per prompt\n{average:,.0f}"
        )
        self.query_one("#recent-metric", Static).update(
            f"Last hour {suffix} usage\n{_format_count(recent)}"
        )
        self.query_one("#seven-day-metric", Static).update(
            f"{self.settings.forecast_days}-day expected {suffix}\n{_format_count(seven_day)}"
        )
        self.query_one("#thirty-day-statistic", Static).update(
            f"{self.settings.thirty_day_forecast_days}-day expected {suffix}\n{_format_count(thirty_day)}"
        )
        self.query_one("#provider-split", Static).update(self._provider_split_text())

        table = self.query_one("#usage-table", DataTable)
        table.clear(columns=True)
        rows = [
            (
                entry.timestamp.astimezone().strftime("%Y-%m-%d %H:%M"),
                entry.provider,
                "1" if is_tasks else _format_tokens(entry.tokens),
            )
            for entry in self.stats.entries
        ]
        if not rows:
            rows = [("—", "No recorded tasks", "0")]

        # Set widths before adding rows so DataTable doesn't render once with
        # header-only auto widths and cache clipped cell content.
        table.add_column(
            "Timestamp", width=max(len("Timestamp"), *(len(row[0]) for row in rows))
        )
        table.add_column(
            "Provider", width=max(len("Provider"), *(len(row[1]) for row in rows))
        )
        table.add_column(
            suffix.capitalize(), width=max(len(suffix), *(len(row[2]) for row in rows))
        )
        for row in rows:
            table.add_row(*row)

    def action_close_statistics(self) -> None:
        self.dismiss(None)

    def _provider_split_text(self) -> str:
        lines = ["Provider split"]
        split = self.stats.provider_split(self.unit)
        suffix = "tasks" if self.unit == "tasks" else "tokens"
        if not split:
            lines.append(f"No {suffix} recorded")
        else:
            lines.extend(
                f"{provider}: {percentage:.1f}% ({_format_count(count)} {suffix})"
                for provider, count, percentage in split
            )
        return "\n".join(lines)


def _format_tokens(tokens: int) -> str:
    return f"{tokens:,}"


def _format_count(value: int) -> str:
    return f"{value:,}"


class DaedalusTuiApp(App[None]):
    TITLE = "Daedalus TUI"
    CSS_PATH = "app.tcss"
    # Keep Textual's arbitrary text selection enabled for labels, logs, and
    # other non-editor widgets. TextArea has its own native selection model.
    ALLOW_SELECT = True
    BINDINGS = [(shortcut.lower(), action, description) for shortcut, description, action in GLOBAL_SHORTCUTS]

    def __init__(
        self,
        runner: AgentRunner | None = None,
        directory: Path | None = None,
        settings: TuiSettings | None = None,
        coordinator: TaskCoordinator | None = None,
        statistics_settings: CodingStatisticsSettings | None = None,
    ) -> None:
        super().__init__()
        self.launch_root = (directory or Path.cwd()).resolve()
        self.memory = TaskMemoryStore(self.launch_root / DEFAULT_MEMORY_FILE)
        self.settings = settings or load_tui_settings()
        self.statistics_settings = statistics_settings or load_coding_statistics_settings()
        self.orchestration_settings = load_orchestration_settings()
        self.debug_log_path = self.launch_root / self.orchestration_settings.debug_log_filename
        self._fault_log_file = None
        self.runner = runner or AgentRunner()
        discovered = list(discover_projects(self.launch_root))
        if not discovered:
            # Keep the app usable when launched in a new or test directory;
            # orchestration will provide the actionable Git error if needed.
            discovered = [DaedalusProject(self.launch_root, self.launch_root)]
        discovered_paths = {project.path.resolve() for project in discovered}
        remembered_project = self._remembered_project()
        if remembered_project in discovered_paths:
            active_project = remembered_project
        else:
            active_project = discovered[0].path.resolve()
        if coordinator is not None and active_project not in discovered_paths:
            discovered.insert(0, DaedalusProject(active_project, self.launch_root))
        self.projects = tuple(discovered)
        self._coordinators: dict[Path, TaskCoordinator] = {}
        self._external_coordinator = coordinator
        self._active_project_path = active_project
        self.directory = active_project
        self._remember_project(active_project)
        self.coordinator = self._coordinator_for(active_project)
        self._selected_task_id: str | None = None
        # The task inbox spans all discovered projects. Row keys include the
        # project path because task IDs are only unique within a coordinator.
        self._task_rows: dict[str, tuple[Path, str]] = {}
        self._updated_task_rows: set[str] = set()
        self._new_task_mode = True
        self._vim_pending_g = False
        self._plan_review_generation = 0
        self._accept_task_events = False
        self._shutdown_lock = threading.Lock()
        self._shutdown_started = False
        self._textual_unmounted = False
        self._previous_asyncio_exception_handler = None
        self._rendered_plan_question_signature: tuple[object, ...] | None = None

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="screen"):
            with Horizontal(id="workspace"):
                with Vertical(id="task-sidebar"):
                    yield Static("Task updates", id="task-label")
                    yield DataTable(id="task-list", cursor_type="row")
                with Vertical(id="project-main"):
                    yield Static("Local agent orchestration", id="title")
                    with Horizontal(id="task-bar"):
                        yield Static("Project", id="project-label")
                        yield Select(
                            [(project.display_name, str(project.path)) for project in self.projects],
                            value=self._project_select_value(),
                            id="project-select",
                        )
                        yield Button("New Task", id="new-task-button", variant="primary")
                    with Horizontal(id="settings"):
                        yield Select(
                            [(option.label, option.value) for option in self.settings.providers],
                            value=self.settings.default_provider,
                            id="provider-select",
                        )
                        yield Select(
                            [(option.label, option.value) for option in self.settings.codex_models],
                            value=self.settings.default_model,
                            id="model-select",
                        )
                        yield Select(
                            [(option.label, option.value) for option in self.settings.codex_reasoning],
                            value=self.settings.default_reasoning,
                            id="reasoning-select",
                        )
                        yield Select(
                            [(option.label, option.value) for option in self.settings.modes],
                            value="coding",
                            id="mode-select",
                        )
                    yield Static(self._directory_text(), id="directory")
                    yield Static("Phase: Idle", id="phase")
                    yield Static("Task branch: —    Worktree: —", id="task-context")
                    # Keep diagnostics on the same selectable Log surface as
                    # the transcript so mouse selection, y, and Ctrl+C all
                    # use Textual's screen-selection clipboard path.
                    yield Log(id="task-error", auto_scroll=False)
                    # Log supports Textual click-drag selection; RichLog does not.
                    yield TranscriptLog(id="output", auto_scroll=True)
                    with Vertical(id="plan-review"):
                        yield Static("", id="plan-display")
                        with Vertical(id="plan-questions"):
                            yield Static("", id="plan-questions-empty")
                        with Horizontal(id="plan-actions"):
                            yield Button("Submit Answers", id="answer-plan-button", disabled=True)
                            yield Button("Implement", id="implement-button", disabled=True, variant="primary")
                    with Vertical(id="composer"):
                        yield DaedalusVimTextArea(
                            id="prompt-input",
                            placeholder="Describe the change for the local agent...",
                        )
                        with Vertical(id="resume-notes-panel"):
                            yield Static("Optional notes for resuming this task", id="resume-notes-label")
                            yield TextArea(
                                id="resume-notes",
                                placeholder="Tell the agent what it missed or what to update next...",
                            )
                        with Horizontal(id="actions"):
                            yield Button("Send", id="send-button", variant="primary")
                            yield Button("Continue Plan", id="continue-plan-button", disabled=True)
                            yield Button("Start Coding", id="start-coding-button", disabled=True, variant="primary")
                            yield Button("Pause", id="pause-button", disabled=True)
                            yield Button("Resume", id="resume-button", disabled=True)
                            yield Button("Cancel", id="cancel-button", disabled=True, variant="error")
                            yield Button("Retry", id="retry-button", disabled=True)
                            yield Static("Idle", id="status")
        yield Footer()

    def on_mount(self) -> None:
        self.debug_log_path = configure_debug_logging(self.debug_log_path)
        self._fault_log_file = install_fault_handler(self.debug_log_path)
        self._install_exit_diagnostics()
        self._accept_task_events = True
        self._refresh_task_list()
        prompt = self.query_one("#prompt-input", DaedalusVimTextArea)
        prompt.enter_insert_mode()
        prompt.focus()

    def on_key(self, event: events.Key) -> None:
        """Add Vim-like navigation without changing TextArea insert behavior."""
        if isinstance(self.focused, TextArea):
            self._vim_pending_g = False
            return

        key = event.key
        if self._vim_pending_g:
            self._vim_pending_g = False
            if key == "g":
                self._scroll_output("home")
            else:
                self._handle_vim_key(key)
            event.stop()
            return

        if key == "g":
            self._vim_pending_g = True
            self._set_status("g-")
            event.stop()
            return
        if key in {"j", "k", "G", "ctrl+d", "ctrl+u", "y", "p", "i"}:
            self._handle_vim_key(key)
            event.stop()

    def on_unmount(self) -> None:
        self._textual_unmounted = True
        _unregister_app_for_thread_exit(self)
        shutdown_complete = self._shutdown_coordinators("Textual app unmount")
        if shutdown_complete:
            close_fault_handler(self._fault_log_file)
        self._remove_exit_diagnostics()

    def exit(self, *args, **kwargs) -> None:
        """Stop agents before an explicit Textual exit begins."""
        self._shutdown_coordinators("explicit Textual exit")
        super().exit(*args, **kwargs)

    def _handle_exception(self, error: Exception) -> None:
        """Persist Textual failures that would otherwise only flash on screen."""
        log_exception("Unhandled Textual application exception", error)
        self._shutdown_coordinators("unhandled Textual application exception")
        super()._handle_exception(error)

    def _install_exit_diagnostics(self) -> None:
        """Cover terminal and event-loop exits that bypass Textual unmount."""
        _register_app_for_thread_exit(self)
        loop = asyncio.get_running_loop()
        self._previous_asyncio_exception_handler = loop.get_exception_handler()
        loop.set_exception_handler(self._log_asyncio_exception)
        LOGGER.info("Installed pre-thread-shutdown and asyncio diagnostics for Textual lifecycle.")

    def _remove_exit_diagnostics(self) -> None:
        try:
            asyncio.get_running_loop().set_exception_handler(self._previous_asyncio_exception_handler)
        except RuntimeError:
            pass
        self._previous_asyncio_exception_handler = None

    def _log_asyncio_exception(self, loop: asyncio.AbstractEventLoop, context: dict) -> None:
        error = context.get("exception")
        if isinstance(error, BaseException):
            log_exception("Unhandled asyncio exception in the Textual loop", error)
        else:
            LOGGER.error("Unhandled asyncio exception in the Textual loop: %s", context.get("message", context))
        if self._previous_asyncio_exception_handler is not None:
            self._previous_asyncio_exception_handler(loop, context)
        else:
            loop.default_exception_handler(context)

    def _shutdown_before_thread_join(self) -> None:
        """Run before ThreadPoolExecutor's internal interpreter-exit join."""
        if self._textual_unmounted:
            return
        LOGGER.error("Python is exiting while the Textual unmount hook was not observed.")
        self._shutdown_coordinators("Python pre-thread shutdown")

    def shutdown_after_run(self) -> None:
        """Clean up if Textual's run loop returns without its unmount hook."""
        if self._textual_unmounted:
            return
        LOGGER.error("Textual run loop returned without the unmount hook.")
        self._shutdown_coordinators("Textual run loop returned")

    def _shutdown_coordinators(self, reason: str) -> bool:
        """Idempotently detach task callbacks and request child-process shutdown."""
        with self._shutdown_lock:
            if self._shutdown_started:
                return True
            self._shutdown_started = True
        LOGGER.info("%s; requesting coordinator shutdown.", reason)
        self._accept_task_events = False
        shutdown_complete = True
        for coordinator in self._coordinators.values():
            if hasattr(coordinator, "set_event_callback"):
                coordinator.set_event_callback(None)
            try:
                shutdown_complete = coordinator.shutdown() is not False and shutdown_complete
            except Exception as error:
                shutdown_complete = False
                log_exception("Coordinator shutdown failed", error)
        if not shutdown_complete:
            LOGGER.error("Leaving fault handler active because a task worker is still running.")
        return shutdown_complete

    def action_submit_prompt(self) -> None:
        self._submit_prompt()

    def action_new_task(self) -> None:
        self._start_new_task()

    def action_copy_selection(self) -> None:
        self._copy_selection()

    def action_pause_task(self) -> None:
        self._pause_task()

    def action_resume_task(self) -> None:
        self._resume_task()

    def action_continue_plan(self) -> None:
        self._continue_plan()

    def action_start_coding(self) -> None:
        self._start_coding()

    def action_cancel_task(self) -> None:
        self._cancel_task()

    def action_retry_task(self) -> None:
        self._retry_task()

    def action_show_shortcuts(self) -> None:
        self.push_screen(KeyboardShortcutsScreen())

    def action_show_statistics(self) -> None:
        self.push_screen(CodingStatisticsScreen(self._usage_entries(), self.statistics_settings))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "send-button":
            self._submit_prompt()
        elif event.button.id == "new-task-button":
            self._start_new_task()
        elif event.button.id == "continue-plan-button":
            self._continue_plan()
        elif event.button.id == "start-coding-button":
            self._start_coding()
        elif event.button.id == "pause-button":
            self._pause_task()
        elif event.button.id == "resume-button":
            self._resume_task()
        elif event.button.id == "cancel-button":
            self._cancel_task()
        elif event.button.id == "retry-button":
            self._retry_task()
        elif event.button.id == "answer-plan-button":
            self._answer_plan()
        elif event.button.id == "implement-button":
            self._implement_plan()

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id == "project-select":
            if event.value not in (Select.BLANK, ""):
                self._switch_project(Path(str(event.value)))
            return
        if event.select.id and event.select.id.startswith("plan-question-"):
            self._update_plan_custom_answer_visibility(event.select.id, event.value)
            self._update_plan_action_buttons()
            return
        if event.select.id != "provider-select":
            return
        is_cursor = event.value == "cursor"
        model_select = self.query_one("#model-select", Select)
        reasoning_select = self.query_one("#reasoning-select", Select)
        if is_cursor:
            model_select.set_options([(self.settings.cursor_model.label, self.settings.cursor_model.value)])
            model_select.value = self.settings.cursor_model.value
            model_select.disabled = True
            reasoning_select.set_options([("Not applicable", "")])
            reasoning_select.value = ""
            reasoning_select.disabled = True
        else:
            model_select.set_options([(option.label, option.value) for option in self.settings.codex_models])
            model_select.value = self.settings.default_model
            model_select.disabled = False
            reasoning_select.set_options([(option.label, option.value) for option in self.settings.codex_reasoning])
            reasoning_select.value = self.settings.default_reasoning
            reasoning_select.disabled = False

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        if event.text_area.id and event.text_area.id.startswith("plan-custom-answer-"):
            self._update_plan_action_buttons()

    def _submit_prompt(self) -> None:
        prompt_widget = self.query_one("#prompt-input", TextArea)
        if prompt_widget.read_only:
            self._set_status("Press New Task first")
            return
        prompt = prompt_widget.text.strip()
        if not prompt:
            self._set_error("Prompt cannot be empty.")
            self._set_status("Error")
            prompt_widget.focus()
            return

        project_value = self.query_one("#project-select", Select).value
        if project_value in (Select.BLANK, "", getattr(Select, "NULL", None)):
            self._set_error("Select a project before sending.")
            self._set_status("Error")
            return
        selected_project = Path(str(project_value)).expanduser().resolve()
        if selected_project not in {project.path.resolve() for project in self.projects}:
            self._set_error("The selected project is no longer available.")
            self._set_status("Error")
            return
        if selected_project != self._active_project_path:
            draft = prompt_widget.text
            self._switch_project(selected_project)
            # A project switch renders the idle view and clears its prompt;
            # restore the draft so a selection made immediately before Send
            # cannot discard the user's new-task text.
            self._set_prompt_text(draft, editable=True)

        provider = str(self.query_one("#provider-select", Select).value)
        model = str(self.query_one("#model-select", Select).value)
        reasoning_value = self.query_one("#reasoning-select", Select).value
        reasoning = "" if reasoning_value is Select.BLANK else str(reasoning_value)
        mode = str(self.query_one("#mode-select", Select).value)
        try:
            record = self.coordinator.submit(prompt, provider, model, reasoning, mode)
        except (RuntimeError, ValueError) as error:
            self._set_error(str(error))
            self._set_status("Error")
            return
        self._selected_task_id = record.task_id
        self._new_task_mode = False
        self._clear_task_update(self._task_row_key(self._active_project_path, record.task_id))
        self._refresh_task_list()
        self._render_selected_task_safely("prompt submission")

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Focus a task from the cross-project update inbox."""
        row_key = str(event.row_key.value)
        task_target = self._task_rows.get(row_key)
        if task_target is None:
            return
        project_path, task_id = task_target
        self._focus_task(project_path, task_id)

    def _on_task_event(self, record: TaskRecord, phase: str, message: str, kind: str) -> None:
        LOGGER.debug(
            "Task event task=%s phase=%s kind=%s message_length=%d",
            record.task_id,
            phase,
            kind,
            len(message),
        )
        if not self._accept_task_events:
            LOGGER.debug("Dropped late task event because the app is closing.")
            return
        if threading.current_thread() is threading.main_thread():
            self._apply_task_event(record, phase, message, kind)
        else:
            try:
                self.call_from_thread(self._apply_task_event, record, phase, message, kind)
            except RuntimeError as error:
                # A worker can race with Textual's final shutdown transition.
                # Do not let a late event print an exception after the UI closes.
                if "App is not running" not in str(error):
                    log_exception("Could not forward task event into Textual", error)
                    raise
                LOGGER.info("Dropped task event after Textual stopped task=%s", record.task_id)

    def _apply_task_event(self, record: TaskRecord, phase: str, message: str, kind: str) -> None:
        try:
            project_path = self._project_for_record(record)
            if project_path is None:
                return
            row_key = self._task_row_key(project_path, record.task_id)
            is_selected = (
                project_path == self._active_project_path
                and self._selected_task_id == record.task_id
            )
            if not is_selected and self._should_promote_task_update(record, phase):
                self._updated_task_rows.add(row_key)
            elif is_selected:
                self._updated_task_rows.discard(row_key)
            self._refresh_project_selector()
            self._refresh_task_list()
            if is_selected:
                self._render_selected_task_safely(f"task event phase={phase}")
        except Exception as error:
            log_exception(f"Could not render task event task={record.task_id} phase={phase}", error)
            if not self._accept_task_events:
                return
            try:
                self._set_error(f"Task update could not be rendered: {error}")
                self._set_status("Error")
            except Exception as display_error:
                log_exception("Could not show task rendering error", display_error)

    @staticmethod
    def _should_promote_task_update(record: TaskRecord, phase: str) -> bool:
        """Promote only events that need the user's attention in the inbox."""
        normalized_phase = phase.lower()
        if normalized_phase in {"completed", "failed"}:
            return True
        return record.mode == "plan" and normalized_phase == "questions"

    def _coordinator_for(self, project_path: Path) -> TaskCoordinator:
        project_path = project_path.resolve()
        if project_path in self._coordinators:
            return self._coordinators[project_path]
        coordinator = self._external_coordinator if self._external_coordinator is not None else TaskCoordinator(
            project_path,
            self.runner,
            self.orchestration_settings,
            self._on_task_event,
            memory_path=self.launch_root / DEFAULT_MEMORY_FILE,
        )
        self._external_coordinator = None
        if hasattr(coordinator, "set_event_callback"):
            coordinator.set_event_callback(self._on_task_event)
        self._coordinators[project_path] = coordinator
        return coordinator

    def _usage_entries(self):
        try:
            persisted = usage_entries_from_memory(self.memory)
        except (OSError, ValueError):
            persisted = ()
        live = tuple(
            entry
            for coordinator in self._coordinators.values()
            for record in coordinator.tasks()
            for entry in (task_usage_entry(record),)
            if entry is not None
        )
        return merge_usage_entries(persisted, live)

    def _remembered_project(self) -> Path | None:
        try:
            return self.memory.get_last_opened_project()
        except (OSError, ValueError):
            return None

    def _remember_project(self, project_path: Path) -> None:
        try:
            self.memory.set_last_opened_project(project_path)
        except (OSError, ValueError):
            # Project navigation should remain usable if local memory is unavailable.
            pass

    def _switch_project(self, project_path: Path) -> None:
        project_path = project_path.expanduser().resolve()
        if project_path == self._active_project_path:
            return
        if project_path not in {project.path.resolve() for project in self.projects}:
            return
        self._active_project_path = project_path
        self.directory = project_path
        # Persist after the active focus changes so the marker mirrors the
        # project that is currently visible in the TUI.
        self._remember_project(project_path)
        self.coordinator = self._coordinator_for(project_path)
        self._selected_task_id = None
        self._new_task_mode = False
        self._updated_task_rows = {
            row_key for row_key in self._updated_task_rows if row_key in self._task_rows
        }
        self.query_one("#directory", Static).update(self._directory_text())
        self._refresh_task_list()
        self._render_selected_task_safely("project switch")
        self._set_status("Project switched")

    def _refresh_project_selector(self) -> None:
        project_select = self.query_one("#project-select", Select)
        options = []
        for project in self.projects:
            project_path = project.path.resolve()
            task_count = (
                len(self._coordinators[project_path].tasks())
                if project_path in self._coordinators
                else 0
            )
            suffix = f" · {task_count} tasks" if task_count else ""
            options.append((f"{project.display_name}{suffix}", str(project.path)))
        project_select.set_options(options)
        project_select.value = self._project_select_value()

    def _project_select_value(self) -> str:
        for project in self.projects:
            if project.path.resolve() == self._active_project_path:
                return str(project.path)
        return str(self._active_project_path)

    def _directory_text(self) -> str:
        return f"Launch root: {self.launch_root}    Active project: {self.directory}"

    def _refresh_task_list(self) -> None:
        """Render every known task, promoting rows with unseen updates."""
        task_list = self.query_one("#task-list", DataTable)
        task_list.clear(columns=True)
        task_list.add_columns("", "Project", "Task", "Status")
        self._task_rows.clear()

        project_names = {
            project.path.resolve(): project.display_name
            for project in self.projects
        }
        rows: list[tuple[Path, TaskRecord]] = []
        for project_path in project_names:
            coordinator = self._coordinators.get(project_path)
            if coordinator is None:
                continue
            rows.extend((project_path, record) for record in coordinator.tasks())
        rows.sort(
            key=lambda item: (
                self._task_row_key(item[0], item[1].task_id) not in self._updated_task_rows,
                -item[1].submission_sequence,
            )
        )

        current_row_keys = {
            self._task_row_key(project_path, record.task_id)
            for project_path, record in rows
        }
        self._updated_task_rows.intersection_update(current_row_keys)
        for project_path, record in rows:
            row_key = self._task_row_key(project_path, record.task_id)
            self._task_rows[row_key] = (project_path, record.task_id)
            project_name = project_names.get(project_path, project_path.name)
            summary = " ".join(record.prompt.split())
            if len(summary) > 38:
                summary = summary[:35] + "..."
            marker = "!" if row_key in self._updated_task_rows else ""
            task_list.add_row(marker, project_name, summary, record.status, key=row_key)

        if self._selected_task_id:
            selected_key = self._task_row_key(self._active_project_path, self._selected_task_id)
            if selected_key in self._task_rows:
                task_list.move_cursor(row=list(self._task_rows).index(selected_key), column=0)

    @staticmethod
    def _task_row_key(project_path: Path, task_id: str) -> str:
        return f"{project_path.resolve()}::{task_id}"

    def _project_for_record(self, record: TaskRecord) -> Path | None:
        for project_path, coordinator in self._coordinators.items():
            if coordinator.get(record.task_id) is record:
                return project_path
        return None

    def _clear_task_update(self, row_key: str) -> None:
        self._updated_task_rows.discard(row_key)

    def _focus_task(self, project_path: Path, task_id: str) -> None:
        """Switch the project context and focus a row selected in the inbox."""
        project_path = project_path.resolve()
        record_coordinator = self._coordinators.get(project_path)
        if record_coordinator is None or record_coordinator.get(task_id) is None:
            return
        self._active_project_path = project_path
        self.directory = project_path
        self._remember_project(project_path)
        self.coordinator = record_coordinator
        self._selected_task_id = task_id
        self._new_task_mode = False
        self._clear_task_update(self._task_row_key(project_path, task_id))
        self.query_one("#project-select", Select).value = self._project_select_value()
        self.query_one("#directory", Static).update(self._directory_text())
        self._refresh_task_list()
        self._render_selected_task_safely("task selection")

    def _render_selected_task_safely(self, source: str) -> None:
        """Keep one bad dynamic widget update from closing the entire TUI."""
        try:
            self._render_selected_task()
        except Exception as error:
            log_exception(f"Could not render selected task during {source}", error)
            try:
                self._set_error(f"Task view could not be rendered: {error}")
                self._set_status("Error")
            except Exception as display_error:
                log_exception("Could not show selected-task rendering error", display_error)

    def _render_selected_task(self) -> None:
        record = self.coordinator.get(self._selected_task_id or "")
        self._plan_review_generation += 1
        plan_review_generation = self._plan_review_generation
        output = self.query_one("#output", TranscriptLog)
        output.clear()
        if record is None:
            self._rendered_plan_question_signature = None
            self._set_prompt_text("", editable=True)
            self.query_one("#output", TranscriptLog).styles.display = "block"
            self.query_one("#task-context", Static).update("Task branch: —    Worktree: —")
            self.query_one("#phase", Static).update("Phase: Idle")
            self._set_error("")
            self.query_one("#pause-button", Button).disabled = True
            self.query_one("#resume-button", Button).disabled = True
            self.query_one("#cancel-button", Button).disabled = True
            self.query_one("#retry-button", Button).disabled = True
            self.query_one("#continue-plan-button", Button).disabled = True
            self.query_one("#start-coding-button", Button).disabled = True
            self.query_one("#resume-notes-panel", Vertical).styles.display = "none"
            self.query_one("#plan-review", Vertical).styles.display = "none"
            return
        # Use Textual's resolved Rich color rather than the raw CSS variable:
        # the default `$text` value is CSS syntax (`auto 87%`), not a Rich
        # color string, and selecting an existing task has made the prompt
        # read-only by this point.
        output.set_final_color(self.screen.rich_style.color)
        self._set_prompt_text(record.prompt, editable=False)
        plan_review = self.query_one("#plan-review", Vertical)
        plan_review.styles.display = "block" if record.mode == "plan" else "none"
        output.styles.display = "none" if record.mode == "plan" else "block"
        if record.mode == "plan":
            self._render_plan_review(record, plan_review_generation)
        else:
            self._rendered_plan_question_signature = None
            for index, message in enumerate(record.messages):
                output.write_message(
                    message,
                    final=record.status == "completed" and index == len(record.messages) - 1,
                )
        worktree = str(record.worktree_path) if record.worktree_path else "—"
        branch = record.branch_name or "—"
        reasoning = record.reasoning or "not applicable"
        self.query_one("#task-context", Static).update(
            f"Mode: {record.mode} · Provider: {record.provider} · Model: {record.model} · Thinking: {reasoning}\n"
            f"Task branch: {branch}    Worktree: {worktree}"
        )
        self.query_one("#phase", Static).update(f"Phase: {record.phase}")
        self._set_error(record.error or "")
        self._set_status(record.status.capitalize())
        active = record.status in {
            "queued",
            "planning",
            "running",
            "verifying",
            "ready",
            "integrating",
            "resolving",
        }
        self.query_one("#pause-button", Button).disabled = not active
        self.query_one("#resume-button", Button).disabled = record.status != "paused"
        self.query_one("#cancel-button", Button).disabled = not active and record.status != "questioning"
        self.query_one("#retry-button", Button).disabled = record.status != "failed"
        self.query_one("#continue-plan-button", Button).disabled = record.status != "questioning"
        self.query_one("#start-coding-button", Button).disabled = record.status != "questioning"
        self.query_one("#resume-notes-panel", Vertical).styles.display = (
            "block" if record.status in {"paused", "questioning"} else "none"
        )
        self.query_one("#resume-notes-label", Static).update(
            "Plan follow-up or question" if record.status == "questioning" else "Optional notes for resuming this task"
        )

    def _render_plan_review(self, record: TaskRecord, generation: int) -> None:
        plan_display = self.query_one("#plan-display", Static)
        plan_display.update(record.plan_text or "Waiting for the agent to return a structured plan.")
        questions = tuple(record.plan_questions)
        answers = dict(record.plan_answers)
        question_signature = (
            record.task_id,
            tuple(
                (
                    question.question_id,
                    question.text,
                    tuple((option.option_id, option.label) for option in question.options),
                )
                for question in questions
            ),
        )

        async def rebuild_questions() -> None:
            try:
                await self._rebuild_plan_questions(record, questions, answers, generation, question_signature)
            except asyncio.CancelledError:
                raise
            except Exception as error:
                # A stale dynamic widget must never terminate the whole TUI.
                # Textual workers exit the app on uncaught errors by default.
                if generation == self._plan_review_generation:
                    self._set_error(f"Plan review could not be rendered: {error}")
                    self._set_status("Error")

        if self._rendered_plan_question_signature != question_signature:
            self.run_worker(
                rebuild_questions,
                exclusive=True,
                group="plan-questions",
                exit_on_error=False,
            )
        answer_button = self.query_one("#answer-plan-button", Button)
        # The button stays disabled until the asynchronous controls have been
        # mounted, so a fast click cannot query widgets that do not exist yet.
        answer_button.disabled = True
        self._update_plan_action_buttons()

    def _update_plan_action_buttons(self) -> None:
        record = self.coordinator.get(self._selected_task_id or "")
        if record is None or record.mode != "plan":
            return
        selected = {
            index: self.query_one(f"#plan-question-{index}", Select).value
            for index, question in enumerate(record.plan_questions)
            if self.query(f"#plan-question-{index}").nodes
        }
        all_answered = all(
            self._has_plan_answer(selected.get(index), self._plan_custom_answer_text(index))
            for index in range(len(record.plan_questions))
        )
        self.query_one("#answer-plan-button", Button).disabled = not (
            bool(record.plan_questions)
            and record.status in {"completed", "awaiting_answers"}
            and len(selected) == len(record.plan_questions)
            and all_answered
            and not record.plan_confirmed
        )
        implement_button = self.query_one("#implement-button", Button)
        implemented = record.plan_implemented
        implement_button.disabled = implemented or not (
            record.plan_confirmed
            and all(not question.required or question.question_id in record.plan_answers for question in record.plan_questions)
        )
        implement_button.set_class(implemented, "implemented")
        implement_button.label = "Implemented" if implemented else "Implement"

    @staticmethod
    def _has_plan_answer(value, custom_text: str = "") -> bool:
        if value in (Select.BLANK, "", getattr(Select, "NULL", object())):
            return False
        return value != CUSTOM_ANSWER_OPTION_ID or bool(custom_text.strip())

    def _plan_custom_answer_text(self, index: int) -> str:
        nodes = self.query(f"#plan-custom-answer-{index}").nodes
        return nodes[0].text if nodes else ""

    def _update_plan_custom_answer_visibility(self, select_id: str, value) -> None:
        index = select_id.removeprefix("plan-question-")
        nodes = self.query(f"#plan-custom-answer-{index}").nodes
        if nodes:
            nodes[0].styles.display = "block" if value == CUSTOM_ANSWER_OPTION_ID else "none"

    async def _rebuild_plan_questions(
        self,
        record: TaskRecord,
        questions: tuple[PlanQuestion, ...],
        answers: dict[str, str],
        generation: int,
        question_signature: tuple[object, ...],
    ) -> None:
        """Replace question controls after Textual has completed child removal."""
        if not self._is_current_plan_review(record, generation):
            return
        question_container = self.query_one("#plan-questions", Vertical)
        await question_container.remove_children()
        if not self._is_current_plan_review(record, generation):
            return
        if not questions:
            await question_container.mount(Static("No questions from the agent."))
        else:
            widgets = [Static("Questions", classes="plan-questions-heading")]
            for index, question in enumerate(questions):
                saved_answer = answers.get(question.question_id)
                saved_custom_text = custom_answer_text(saved_answer)
                selected_value = CUSTOM_ANSWER_OPTION_ID if saved_custom_text else saved_answer or Select.NULL
                widgets.extend(
                    (
                        Static(question.text, classes="plan-question"),
                        PlanAnswerSelect(
                            [(option.label, option.option_id) for option in plan_answer_options(question)],
                            value=selected_value,
                            allow_blank=True,
                            id=f"plan-question-{index}",
                        ),
                        TextArea(
                            saved_custom_text or "",
                            id=f"plan-custom-answer-{index}",
                            classes="plan-custom-answer",
                        ),
                    )
                )
            await question_container.mount(*widgets)
            for index, question in enumerate(questions):
                saved_answer = answers.get(question.question_id)
                saved_custom_text = custom_answer_text(saved_answer)
                self._update_plan_custom_answer_visibility(
                    f"plan-question-{index}",
                    CUSTOM_ANSWER_OPTION_ID if saved_custom_text else saved_answer or Select.NULL,
                )
        if self._is_current_plan_review(record, generation):
            self._rendered_plan_question_signature = question_signature
            self._update_plan_action_buttons()

    def _is_current_plan_review(self, record: TaskRecord, generation: int) -> bool:
        return (
            generation == self._plan_review_generation
            and self.coordinator.get(record.task_id) is record
            and self._selected_task_id == record.task_id
        )

    def _answer_plan(self) -> None:
        record = self.coordinator.get(self._selected_task_id or "")
        if record is None or record.mode != "plan":
            return
        answers: dict[str, str] = {}
        for index, question in enumerate(record.plan_questions):
            selection = self.query_one(f"#plan-question-{index}", Select).value
            custom_text = self._plan_custom_answer_text(index)
            if self._has_plan_answer(selection, custom_text):
                answers[question.question_id] = (
                    encode_custom_answer(custom_text)
                    if selection == CUSTOM_ANSWER_OPTION_ID
                    else str(selection)
                )
        if len(answers) != len(record.plan_questions):
            self._set_status("Answer every question first")
            return
        LOGGER.info(
            "Submitting plan answers task=%s answer_ids=%s",
            record.task_id,
            sorted(CUSTOM_ANSWER_OPTION_ID if custom_answer_text(answer) else answer for answer in answers.values()),
        )
        answer_plan = getattr(self.coordinator, "answer_plan", None)
        if answer_plan is None or not answer_plan(record.task_id, answers):
            self._set_status("Plan answers could not be submitted")
            return
        self._set_status("Reviewing answers")

    def _implement_plan(self) -> None:
        record = self.coordinator.get(self._selected_task_id or "")
        if record is None or record.mode != "plan":
            return
        implement_plan = getattr(self.coordinator, "implement_plan", None)
        coding_record = implement_plan(record.task_id) if implement_plan is not None else None
        if coding_record is None:
            self._set_status("The agent must confirm no more questions")
            return
        implement_button = self.query_one("#implement-button", Button)
        implement_button.disabled = True
        implement_button.add_class("implemented")
        implement_button.label = "Implemented"
        self._selected_task_id = coding_record.task_id
        self._new_task_mode = False
        self._refresh_task_list()
        self._render_selected_task_safely("plan implementation")
        self._set_status("Implementation queued")

    def _start_new_task(self) -> None:
        """Clear the selected task and unlock a fresh prompt editor."""
        self._selected_task_id = None
        self._new_task_mode = True
        self._refresh_task_list()
        self._render_selected_task_safely("new task")
        self._set_status("New task")

    def _set_prompt_text(self, text: str, *, editable: bool) -> None:
        prompt = self.query_one("#prompt-input", DaedalusVimTextArea)
        # Loading text is a programmatic operation, so temporarily make the
        # widget writable even when replacing a submitted task's immutable
        # prompt.
        prompt.read_only = False
        prompt.load_text(text)
        prompt.read_only = not editable
        self.query_one("#output", TranscriptLog).invalidate_render_cache()
        send_button = self.query_one("#send-button", Button)
        send_button.disabled = not editable
        if editable:
            prompt.enter_insert_mode()
            prompt.focus()

    def _copy_selection(self) -> None:
        selection = self._get_selected_text()
        if not selection:
            self._set_status("Select text first")
            return
        self._copy_text(selection)
        self._set_status("Selection copied")

    def _handle_vim_key(self, key: str) -> None:
        if key == "j":
            self._scroll_output("down")
        elif key == "k":
            self._scroll_output("up")
        elif key == "G":
            self._scroll_output("end")
        elif key == "ctrl+d":
            self._scroll_output("page_down")
        elif key == "ctrl+u":
            self._scroll_output("page_up")
        elif key == "y":
            self._copy_selection()
        elif key == "p":
            self._paste_into_prompt()
        elif key == "i":
            self.query_one("#prompt-input", TextArea).focus()
            self._set_status("Insert")

    def _scroll_output(self, direction: str) -> None:
        output = self.query_one("#output", Log)
        output.focus()
        scroll_methods = {
            "up": output.scroll_up,
            "down": output.scroll_down,
            "home": output.scroll_home,
            "end": output.scroll_end,
            "page_up": output.scroll_page_up,
            "page_down": output.scroll_page_down,
        }
        if direction in {"page_up", "page_down"}:
            scroll_methods[direction](animate=False)
        else:
            scroll_methods[direction](animate=False, immediate=True)
        self._set_status(f"Output {direction.replace('_', ' ')}")

    def _paste_into_prompt(self) -> None:
        text = paste_from_system_clipboard()
        if text is None:
            self._set_status("Clipboard unavailable")
            return
        prompt = self.query_one("#prompt-input", TextArea)
        if prompt.read_only:
            self._set_status("Press New Task first")
            return
        if isinstance(prompt, DaedalusVimTextArea):
            prompt.enter_insert_mode()
        prompt.focus()
        prompt.insert(text)
        self._set_status("Pasted")

    def _get_selected_text(self) -> str | None:
        """Return a TextArea selection or the active screen selection."""
        focused = self.focused
        if isinstance(focused, TextArea):
            selected_text = focused.selected_text
            if selected_text:
                return selected_text
        # A read-only diagnostic TextArea may retain its selection while focus
        # is returned to the prompt. Check the other editors before falling
        # back to Textual's arbitrary widget-selection model.
        for text_area in self.query(TextArea):
            if text_area is focused:
                continue
            selected_text = text_area.selected_text
            if selected_text:
                return selected_text
        return self.screen.get_selected_text()

    def copy_to_clipboard(self, text: str) -> None:
        """Use Textual's OSC 52 path and a native clipboard fallback."""
        super().copy_to_clipboard(text)
        copy_to_system_clipboard(text)

    def _copy_text(self, text: str) -> None:
        self.copy_to_clipboard(text)

    def _pause_task(self) -> None:
        record = self.coordinator.get(self._selected_task_id or "")
        if record is not None and self.coordinator.pause(record.task_id):
            self._set_status("Pausing")

    def _resume_task(self) -> None:
        record = self.coordinator.get(self._selected_task_id or "")
        notes_widget = self.query_one("#resume-notes", TextArea)
        notes = notes_widget.text.strip()
        if record is not None and self.coordinator.resume(record.task_id, notes):
            notes_widget.clear()
            self._set_status("Resuming")

    def _continue_plan(self) -> None:
        record = self.coordinator.get(self._selected_task_id or "")
        notes_widget = self.query_one("#resume-notes", TextArea)
        notes = notes_widget.text.strip()
        if record is not None and self.coordinator.continue_plan(record.task_id, notes):
            notes_widget.clear()
            self._set_status("Continuing plan")

    def _start_coding(self) -> None:
        record = self.coordinator.get(self._selected_task_id or "")
        notes_widget = self.query_one("#resume-notes", TextArea)
        notes = notes_widget.text.strip()
        if record is not None and self.coordinator.start_coding(record.task_id, notes):
            notes_widget.clear()
            self._set_status("Starting coding")

    def _cancel_task(self) -> None:
        record = self.coordinator.get(self._selected_task_id or "")
        if record is not None and self.coordinator.cancel(record.task_id):
            self._set_status("Cancelling")

    def _retry_task(self) -> None:
        record = self.coordinator.get(self._selected_task_id or "")
        retry = getattr(self.coordinator, "retry", None)
        if record is None or retry is None or not retry(record.task_id):
            self._set_status("Retry unavailable")
            return
        self._set_status("Retrying")

    def _set_status(self, status: str) -> None:
        self.query_one("#status", Static).update(status)

    def _set_error(self, error: str) -> None:
        error_widget = self.query_one("#task-error", Log)
        error_widget.clear()
        if error:
            error_widget.write(error)
