"""Textual interface for concurrent local agent tasks."""

from __future__ import annotations

from pathlib import Path
import threading

from textual import events
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Footer, Header, RichLog, Select, Static, TextArea
from .agent_runner import AgentRunner
from .clipboard import copy_to_system_clipboard, paste_from_system_clipboard
from .config import TuiSettings, load_orchestration_settings, load_tui_settings
from .memory import DEFAULT_MEMORY_FILE, TokenUsageStore
from .projects import DaedalusProject, discover_projects
from .task_coordinator import TaskCoordinator, TaskRecord
from .vim_text_area import DaedalusVimTextArea


GLOBAL_SHORTCUTS = (
    ("Ctrl+Enter", "Send prompt", "submit_prompt"),
    ("Ctrl+C", "Copy selected text", "copy_selection"),
    ("Ctrl+Alt+S", "Copy selection", "copy_selection"),
    ("Ctrl+P", "Pause task", "pause_task"),
    ("Ctrl+R", "Resume task", "resume_task"),
    ("Ctrl+X", "Cancel task", "cancel_task"),
    ("Ctrl+Q", "Quit", "quit"),
    ("Ctrl+K", "Show keyboard shortcuts", "show_shortcuts"),
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
    ) -> None:
        super().__init__()
        self.launch_root = (directory or Path.cwd()).resolve()
        self.memory = TokenUsageStore(self.launch_root / DEFAULT_MEMORY_FILE)
        self.settings = settings or load_tui_settings()
        self.orchestration_settings = load_orchestration_settings()
        self.runner = runner or AgentRunner()
        discovered = list(discover_projects(self.launch_root))
        if not discovered:
            # Keep the app usable when launched in a new or test directory;
            # orchestration will provide the actionable Git error if needed.
            discovered = [DaedalusProject(self.launch_root, self.launch_root)]
        discovered_paths = {project.path for project in discovered}
        remembered_project = self._remembered_project()
        if remembered_project in discovered_paths:
            active_project = remembered_project
        else:
            active_project = discovered[0].path
        if coordinator is not None and active_project not in {project.path for project in discovered}:
            discovered.insert(0, DaedalusProject(active_project, self.launch_root))
        self.projects = tuple(discovered)
        self._coordinators: dict[Path, TaskCoordinator] = {}
        self._external_coordinator = coordinator
        self._active_project_path = active_project
        self.directory = active_project
        self._remember_project(active_project)
        self.coordinator = self._coordinator_for(active_project)
        self._selected_task_id: str | None = None
        self._new_task_mode = True
        self._vim_pending_g = False

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="screen"):
            with Horizontal(id="workspace"):
                with Vertical(id="project-sidebar"):
                    yield Static("Projects", id="project-label")
                    yield Select(
                        [(project.display_name, str(project.path)) for project in self.projects],
                        value=str(self._active_project_path),
                        id="project-select",
                    )
                with Vertical(id="project-main"):
                    yield Static("Local agent orchestration", id="title")
                    with Horizontal(id="task-bar"):
                        yield Static("Tasks", id="task-label")
                        yield Select([("No tasks", "")], value="", disabled=True, id="task-select")
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
                    yield TextArea("", read_only=True, show_line_numbers=False, id="task-error")
                    yield RichLog(id="output", markup=False, wrap=True, highlight=False, auto_scroll=True)
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
                            yield Button("Pause", id="pause-button", disabled=True)
                            yield Button("Resume", id="resume-button", disabled=True)
                            yield Button("Cancel", id="cancel-button", disabled=True, variant="error")
                            yield Static("Idle", id="status")
        yield Footer()

    def on_mount(self) -> None:
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
        for coordinator in self._coordinators.values():
            coordinator.shutdown()

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

    def action_cancel_task(self) -> None:
        self._cancel_task()

    def action_show_shortcuts(self) -> None:
        self.push_screen(KeyboardShortcutsScreen())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "send-button":
            self._submit_prompt()
        elif event.button.id == "new-task-button":
            self._start_new_task()
        elif event.button.id == "pause-button":
            self._pause_task()
        elif event.button.id == "resume-button":
            self._resume_task()
        elif event.button.id == "cancel-button":
            self._cancel_task()

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id == "project-select":
            if event.value not in (Select.BLANK, ""):
                self._switch_project(Path(str(event.value)))
            return
        if event.select.id == "task-select":
            if event.value not in (Select.BLANK, ""):
                self._selected_task_id = str(event.value)
                self._new_task_mode = False
                self._render_selected_task()
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
        self._refresh_task_selector()
        self._render_selected_task()

    def _on_task_event(self, record: TaskRecord, phase: str, message: str, kind: str) -> None:
        if threading.current_thread() is threading.main_thread():
            self._apply_task_event(record, phase, message, kind)
        else:
            self.call_from_thread(self._apply_task_event, record, phase, message, kind)

    def _apply_task_event(self, record: TaskRecord, phase: str, message: str, kind: str) -> None:
        self._refresh_project_selector()
        if self.coordinator.get(record.task_id) is record:
            self._refresh_task_selector()
        if self.coordinator.get(record.task_id) is record and self._selected_task_id == record.task_id:
            self._render_selected_task()

    def _coordinator_for(self, project_path: Path) -> TaskCoordinator:
        project_path = project_path.resolve()
        if project_path in self._coordinators:
            return self._coordinators[project_path]
        coordinator = self._external_coordinator if self._external_coordinator is not None else TaskCoordinator(
            project_path,
            self.runner,
            self.orchestration_settings,
            self._on_task_event,
        )
        self._external_coordinator = None
        if hasattr(coordinator, "set_event_callback"):
            coordinator.set_event_callback(self._on_task_event)
        self._coordinators[project_path] = coordinator
        return coordinator

    def _remembered_project(self) -> Path | None:
        try:
            return self.memory.get_last_opened_project()
        except (OSError, ValueError):
            return None

    def _remember_project(self, project_path: Path) -> None:
        try:
            self.memory.record_last_opened_project(project_path)
        except (OSError, ValueError):
            # Project navigation should remain usable if local memory is unavailable.
            pass

    def _switch_project(self, project_path: Path) -> None:
        if project_path == self._active_project_path:
            return
        if project_path not in {project.path for project in self.projects}:
            return
        self._remember_project(project_path)
        self._active_project_path = project_path
        self.directory = project_path
        self.coordinator = self._coordinator_for(project_path)
        self._selected_task_id = None
        self._new_task_mode = False
        self.query_one("#directory", Static).update(self._directory_text())
        self._refresh_task_selector()
        self._render_selected_task()
        self._set_status("Project switched")

    def _refresh_project_selector(self) -> None:
        project_select = self.query_one("#project-select", Select)
        options = []
        for project in self.projects:
            task_count = len(self._coordinator_for(project.path).tasks()) if project.path in self._coordinators else 0
            suffix = f" · {task_count} tasks" if task_count else ""
            options.append((f"{project.display_name}{suffix}", str(project.path)))
        project_select.set_options(options)
        project_select.value = str(self._active_project_path)

    def _directory_text(self) -> str:
        return f"Launch root: {self.launch_root}    Active project: {self.directory}"

    def _refresh_task_selector(self) -> None:
        task_select = self.query_one("#task-select", Select)
        records = self.coordinator.tasks()
        options = [("Select a task", "")] if records else []
        for record in records:
            summary = " ".join(record.prompt.split())
            if len(summary) > 42:
                summary = summary[:39] + "..."
            options.append((f"{record.task_id} · {record.status} · {summary}", record.task_id))
        task_select.set_options(options or [("No tasks", "")])
        task_select.disabled = not bool(options)
        if records and not self._new_task_mode and self._selected_task_id not in {record.task_id for record in records}:
            self._selected_task_id = records[-1].task_id
        if self._selected_task_id:
            task_select.value = self._selected_task_id
        else:
            task_select.value = ""

    def _render_selected_task(self) -> None:
        record = self.coordinator.get(self._selected_task_id or "")
        output = self.query_one("#output", RichLog)
        output.clear()
        if record is None:
            self._set_prompt_text("", editable=True)
            self.query_one("#task-context", Static).update("Task branch: —    Worktree: —")
            self.query_one("#phase", Static).update("Phase: Idle")
            self._set_error("")
            self.query_one("#pause-button", Button).disabled = True
            self.query_one("#resume-button", Button).disabled = True
            self.query_one("#cancel-button", Button).disabled = True
            self.query_one("#resume-notes-panel", Vertical).styles.display = "none"
            return
        self._set_prompt_text(record.prompt, editable=False)
        for message in record.messages:
            output.write(message)
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
        active = record.status in {"queued", "running", "verifying", "ready", "integrating", "resolving"}
        self.query_one("#pause-button", Button).disabled = not active
        self.query_one("#resume-button", Button).disabled = record.status != "paused"
        self.query_one("#cancel-button", Button).disabled = not active
        self.query_one("#resume-notes-panel", Vertical).styles.display = (
            "block" if record.status == "paused" else "none"
        )

    def _start_new_task(self) -> None:
        """Clear the selected task and unlock a fresh prompt editor."""
        self._selected_task_id = None
        self._new_task_mode = True
        self._refresh_task_selector()
        self._render_selected_task()
        self._set_status("New task")

    def _set_prompt_text(self, text: str, *, editable: bool) -> None:
        prompt = self.query_one("#prompt-input", DaedalusVimTextArea)
        # Loading text is a programmatic operation, so temporarily make the
        # widget writable even when replacing a submitted task's immutable
        # prompt.
        prompt.read_only = False
        prompt.load_text(text)
        prompt.read_only = not editable
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
        output = self.query_one("#output", RichLog)
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

    def _cancel_task(self) -> None:
        record = self.coordinator.get(self._selected_task_id or "")
        if record is not None and self.coordinator.cancel(record.task_id):
            self._set_status("Cancelling")

    def _set_status(self, status: str) -> None:
        self.query_one("#status", Static).update(status)

    def _set_error(self, error: str) -> None:
        error_widget = self.query_one("#task-error", TextArea)
        error_widget.load_text(error)
