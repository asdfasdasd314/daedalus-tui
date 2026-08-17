import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from textual import events
from textual.geometry import Offset
from textual.selection import Selection as ScreenSelection
from textual.widgets import Button, Log, Select, Static, TextArea
from textual.widgets.text_area import Selection
from vimkeys_input import VimMode

from tui.app import DaedalusTuiApp, KeyboardShortcutsScreen
from tui.config import ModelOption, TuiSettings
from tui.projects import DaedalusProject
from tui.task_coordinator import TaskRecord
from tui.vim_text_area import DaedalusVimTextArea


class FakeRunner:
    def __init__(self):
        self.requests = []


class FakeCoordinator:
    def __init__(self):
        self.callback = None
        self.records = []
        self.resume_notes = []

    def set_event_callback(self, callback):
        self.callback = callback

    def submit(self, prompt, provider, model, reasoning, mode="coding"):
        record = TaskRecord(
            f"task-{len(self.records) + 1}",
            len(self.records) + 1,
            prompt,
            provider,
            model,
            reasoning,
            mode=mode,
            status="running",
            phase="Agent",
            branch_name=f"agent/task-{len(self.records) + 1}",
            worktree_path=Path(f"/tmp/task-{len(self.records) + 1}"),
        )
        self.records.append(record)
        self.emit(record, "agent", "", "status")
        return record

    def tasks(self):
        return tuple(self.records)

    def get(self, task_id):
        return next((record for record in self.records if record.task_id == task_id), None)

    def emit(self, record, phase, message, kind):
        if self.callback:
            self.callback(record, phase, message, kind)

    def finish(self, record, message):
        record.messages.append(message)
        record.status = "completed"
        record.phase = "Completed"
        self.emit(record, "completed", "", "status")

    def shutdown(self):
        return None

    def pause(self, _task_id):
        return True

    def resume(self, _task_id, notes=""):
        self.resume_notes.append(notes)
        return True

    def cancel(self, _task_id):
        return True


def settings():
    return TuiSettings(
        "codex",
        "gpt-5.6-luna",
        "medium",
        (ModelOption("Codex", "codex"), ModelOption("Cursor CLI", "cursor")),
        (
            ModelOption("GPT-5.6 Luna", "gpt-5.6-luna"),
            ModelOption("GPT-5.6 Terra", "gpt-5.6-terra"),
            ModelOption("GPT-5.6 Sol", "gpt-5.6-sol"),
        ),
        (
            ModelOption("Light", "light"),
            ModelOption("Medium", "medium"),
            ModelOption("High", "high"),
            ModelOption("Extra high", "extra-high"),
        ),
        ModelOption("Cursor CLI", "cursor"),
    )


class TuiAppTests(unittest.IsolatedAsyncioTestCase):
    def make_app(self):
        coordinator = FakeCoordinator()
        app = DaedalusTuiApp(
            runner=FakeRunner(),
            directory=Path("/workspace/project"),
            settings=settings(),
            coordinator=coordinator,
        )
        return app, coordinator

    async def test_controls_and_launch_directory_are_visible(self):
        app, _ = self.make_app()
        async with app.run_test() as pilot:
            self.assertEqual(app.query_one("#provider-select", Select).value, "codex")
            self.assertEqual(app.query_one("#model-select", Select).value, "gpt-5.6-luna")
            self.assertEqual(app.query_one("#reasoning-select", Select).value, "medium")
            self.assertEqual(app.query_one("#mode-select", Select).value, "coding")
            self.assertIn("/workspace/project", str(app.query_one("#directory", Static).render()))
            self.assertIsInstance(app.query_one("#task-select", Select), Select)
            self.assertIsInstance(app.query_one("#prompt-input", TextArea), DaedalusVimTextArea)
            self.assertEqual(app.query_one("#prompt-input", DaedalusVimTextArea).vim_mode, VimMode.INSERT)
            self.assertEqual(app.query("#vim-mode").nodes, [])
            self.assertEqual(app.query("#vim-help").nodes, [])
            self.assertEqual(app.query("#copy-button, #copy-selection-button, #copy-error-button").nodes, [])
            self.assertIsInstance(app.query_one("#project-select", Select), Select)
            self.assertIsInstance(app.query_one("#pause-button", Button), Button)
            self.assertIsInstance(app.query_one("#resume-button", Button), Button)
            self.assertIsInstance(app.query_one("#cancel-button", Button), Button)
            self.assertIsInstance(app.query_one("#new-task-button", Button), Button)
            await pilot.pause()

    @patch("tui.app.discover_projects")
    async def test_restores_and_updates_last_opened_project(self, discover):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = root / "first"
            second = root / "second"
            memory_path = root / ".daedalus-memory.json"
            memory_path.write_text(
                json.dumps([{"last_opened_project": str(second)}]),
                encoding="utf-8",
            )
            discover.return_value = (
                DaedalusProject(first, root),
                DaedalusProject(second, root),
            )
            app = DaedalusTuiApp(
                runner=FakeRunner(),
                directory=root,
                settings=settings(),
                coordinator=FakeCoordinator(),
            )

            self.assertEqual(app.directory, second.resolve())
            async with app.run_test() as pilot:
                project_select = app.query_one("#project-select", Select)
                project_select.value = str(first)
                await pilot.pause()

            self.assertEqual(
                json.loads(memory_path.read_text(encoding="utf-8"))[-1],
                {"last_opened_project": str(first.resolve())},
            )

    @patch("tui.app.discover_projects")
    async def test_falls_back_to_first_project_when_memory_target_is_missing(self, discover):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = root / "first"
            second = root / "second"
            (root / ".daedalus-memory.json").write_text(
                json.dumps([{"last_opened_project": str(root / "missing")}]),
                encoding="utf-8",
            )
            discover.return_value = (
                DaedalusProject(first, root),
                DaedalusProject(second, root),
            )

            app = DaedalusTuiApp(
                runner=FakeRunner(),
                directory=root,
                settings=settings(),
                coordinator=FakeCoordinator(),
            )

            self.assertEqual(app.directory, first.resolve())

    async def test_ctrl_k_opens_shortcuts_menu_with_global_and_vim_keys(self):
        app, _ = self.make_app()
        async with app.run_test() as pilot:
            await pilot.press("ctrl+k")
            await pilot.pause()

            self.assertIsInstance(app.screen, KeyboardShortcutsScreen)
            shortcut_text = "\n".join(
                str(widget.render()) for widget in app.screen.query(".shortcut-row")
            )
            self.assertIn("Ctrl+Q", shortcut_text)
            self.assertIn("Ctrl+Enter", shortcut_text)
            self.assertIn("Ctrl+K", shortcut_text)
            self.assertIn("Ctrl+P", shortcut_text)
            self.assertIn("gg / G", shortcut_text)

            await pilot.press("escape")
            await pilot.pause()
            self.assertNotIsInstance(app.screen, KeyboardShortcutsScreen)

    @patch("tui.app.discover_projects")
    async def test_sidebar_switches_active_project_and_keeps_task_coordinators_separate(self, discover):
        root = Path("/workspace")
        first = root / "first"
        second = root / "second"
        discover.return_value = (
            DaedalusProject(first, root),
            DaedalusProject(second, root),
        )
        app, first_coordinator = self.make_app()
        app.launch_root = root
        app.projects = discover.return_value
        app._active_project_path = first
        app.directory = first
        app.coordinator = first_coordinator
        app._coordinators = {first: first_coordinator}
        async with app.run_test() as pilot:
            project_select = app.query_one("#project-select", Select)
            project_select.value = str(second)
            await pilot.pause()

            self.assertEqual(app.directory, second)
            self.assertIsNot(app.coordinator, first_coordinator)
            self.assertIn("Active project: /workspace/second", str(app.query_one("#directory", Static).render()))
            self.assertEqual(len(first_coordinator.tasks()), 0)

            project_select.value = str(first)
            await pilot.pause()
            self.assertIs(app.coordinator, first_coordinator)

    async def test_cursor_disables_model_and_reasoning_controls(self):
        app, _ = self.make_app()
        async with app.run_test() as pilot:
            provider = app.query_one("#provider-select", Select)
            provider.value = "cursor"
            await pilot.pause()

            self.assertTrue(app.query_one("#model-select", Select).disabled)
            self.assertTrue(app.query_one("#reasoning-select", Select).disabled)
            self.assertEqual(app.query_one("#model-select", Select).value, "cursor")

    async def test_empty_prompt_is_rejected(self):
        app, _ = self.make_app()
        async with app.run_test() as pilot:
            app.action_submit_prompt()
            await pilot.pause()

            self.assertEqual(str(app.query_one("#status", Static).render()), "Error")
            self.assertIn("cannot be empty", app.query_one("#task-error", TextArea).text)
            self.assertFalse(app.query_one("#send-button", Button).disabled)

    async def test_submitted_prompt_is_visible_and_immutable(self):
        app, coordinator = self.make_app()
        async with app.run_test() as pilot:
            prompt = app.query_one("#prompt-input", DaedalusVimTextArea)
            prompt.insert("Keep this prompt available")
            app.action_submit_prompt()
            await pilot.pause()

            self.assertEqual(prompt.text, "Keep this prompt available")
            self.assertTrue(prompt.read_only)
            self.assertTrue(app.query_one("#send-button", Button).disabled)
            self.assertEqual(coordinator.records[0].prompt, prompt.text)

    async def test_new_task_unlocks_a_blank_prompt_after_viewing_submitted_task(self):
        app, _ = self.make_app()
        async with app.run_test() as pilot:
            prompt = app.query_one("#prompt-input", DaedalusVimTextArea)
            prompt.insert("The previous prompt")
            app.action_submit_prompt()
            await pilot.pause()

            app.query_one("#new-task-button", Button).press()
            await pilot.pause()

            self.assertEqual(prompt.text, "")
            self.assertFalse(prompt.read_only)
            self.assertFalse(app.query_one("#send-button", Button).disabled)
            self.assertEqual(str(app.query_one("#phase", Static).render()), "Phase: Idle")

    async def test_failed_task_selection_restores_its_prompt(self):
        app, coordinator = self.make_app()
        async with app.run_test() as pilot:
            prompt = app.query_one("#prompt-input", DaedalusVimTextArea)
            prompt.insert("A task that will fail")
            app.action_submit_prompt()
            record = coordinator.records[0]
            record.status = "failed"
            record.phase = "Failed"
            coordinator.emit(record, "failed", "The task failed.", "error")
            app.query_one("#new-task-button", Button).press()
            await pilot.pause()
            app.query_one("#task-select", Select).value = record.task_id
            await pilot.pause()

            self.assertEqual(prompt.text, "A task that will fail")
            self.assertTrue(prompt.read_only)
            self.assertTrue(app.query_one("#send-button", Button).disabled)

    async def test_prompt_supports_modal_vim_modes_and_multiline_insert(self):
        app, _ = self.make_app()
        async with app.run_test() as pilot:
            prompt = app.query_one("#prompt-input", DaedalusVimTextArea)
            await pilot.press("escape")
            self.assertEqual(prompt.vim_mode, VimMode.COMMAND)
            await pilot.press("i")
            self.assertEqual(prompt.vim_mode, VimMode.INSERT)
            prompt.insert("first line")
            await pilot.press("enter")
            prompt.insert("second line")
            self.assertEqual(prompt.text, "first line\nsecond line")

    async def test_shift_v_selects_complete_lines(self):
        app, _ = self.make_app()
        async with app.run_test() as pilot:
            prompt = app.query_one("#prompt-input", DaedalusVimTextArea)
            prompt.insert("first line\nsecond line\nthird line")
            prompt.cursor_location = (1, 3)
            await pilot.press("escape")
            await pilot.press("V")

            self.assertEqual(prompt.vim_mode, VimMode.VISUAL_LINE)
            self.assertEqual(prompt.selected_text, "second line\n")
            await pilot.press("j")
            self.assertEqual(prompt.selected_text, "second line\nthird line")

    @patch("tui.vim_text_area.paste_from_system_clipboard", return_value="system paste")
    async def test_prompt_paste_falls_back_to_system_clipboard(self, clipboard):
        app, _ = self.make_app()
        async with app.run_test() as pilot:
            prompt = app.query_one("#prompt-input", DaedalusVimTextArea)
            prompt.yank_register = ""
            await pilot.press("escape")
            await pilot.press("p")
            clipboard.assert_called_once_with()
            self.assertIn("system paste", prompt.text)

    @patch("tui.app.copy_to_system_clipboard")
    async def test_prompt_yank_mirrors_vim_register_to_system_clipboard(self, clipboard):
        app, _ = self.make_app()
        async with app.run_test() as pilot:
            prompt = app.query_one("#prompt-input", DaedalusVimTextArea)
            prompt.insert("copy this line")
            await pilot.press("escape")
            await pilot.press("y")
            await pilot.press("y")

            clipboard.assert_called_once_with("copy this line\n")

    async def test_plan_mode_is_snapshotted_and_task_controls_are_available(self):
        app, coordinator = self.make_app()
        async with app.run_test() as pilot:
            app.query_one("#mode-select", Select).value = "plan"
            app.query_one("#prompt-input", TextArea).insert("Make a plan")
            app.action_submit_prompt()
            await pilot.pause()

            self.assertEqual(coordinator.records[0].mode, "plan")
            self.assertFalse(app.query_one("#pause-button", Button).disabled)
            self.assertFalse(app.query_one("#cancel-button", Button).disabled)

    async def test_paused_task_exposes_optional_resume_notes(self):
        app, coordinator = self.make_app()
        async with app.run_test() as pilot:
            app.query_one("#prompt-input", TextArea).insert("Continue this task")
            app.action_submit_prompt()
            record = coordinator.records[0]
            record.status = "paused"
            record.phase = "Paused"
            coordinator.emit(record, "paused", "Progress preserved.", "status")
            await pilot.pause()

            notes_panel = app.query_one("#resume-notes-panel")
            self.assertEqual(notes_panel.styles.display, "block")
            app.query_one("#resume-notes", TextArea).insert("The API already exists here.")
            app.action_resume_task()

            self.assertEqual(coordinator.resume_notes, ["The API already exists here."])
            self.assertEqual(app.query_one("#resume-notes", TextArea).text, "")

    @patch("tui.app.copy_to_system_clipboard")
    async def test_copy_selection_uses_only_highlighted_text(self, native_clipboard):
        app, _ = self.make_app()
        async with app.run_test():
            app.screen.get_selected_text = Mock(return_value="only this selected section")
            app.action_copy_selection()

            native_clipboard.assert_called_once_with("only this selected section")

    @patch("tui.app.copy_to_system_clipboard")
    async def test_copy_selection_reads_focused_text_area_selection(self, native_clipboard):
        app, _ = self.make_app()
        async with app.run_test():
            error = app.query_one("#task-error", TextArea)
            error.load_text("only this diagnostic section")
            error.selection = Selection((0, 0), (0, 13))
            error.focus()

            self.assertEqual(error.selected_text, "only this dia")
            app.action_copy_selection()

            native_clipboard.assert_called_once_with("only this dia")

    @patch("tui.app.paste_from_system_clipboard", return_value="pasted notes")
    async def test_vim_paste_inserts_system_clipboard_into_prompt(self, _clipboard):
        app, _ = self.make_app()
        async with app.run_test():
            app.query_one("#output", Log).focus()
            app._handle_vim_key("p")

            self.assertEqual(app.query_one("#prompt-input", TextArea).text, "pasted notes")

    async def test_output_log_supports_textual_selection(self):
        app, coordinator = self.make_app()
        async with app.run_test() as pilot:
            app.query_one("#prompt-input", TextArea).insert("Capture selectable output")
            app.action_submit_prompt()
            coordinator.finish(coordinator.records[0], "Selectable assistant transcript line.")
            await pilot.pause()

            output = app.query_one("#output", Log)
            self.assertTrue(output.allow_select)
            selected = output.get_selection(
                ScreenSelection.from_offsets(Offset(0, 0), Offset(10, 0))
            )
            self.assertIsNotNone(selected)
            self.assertEqual(selected[0], "Selectable")

    async def test_vim_navigation_scrolls_output_and_keeps_prompt_typing_safe(self):
        app, _ = self.make_app()
        async with app.run_test() as pilot:
            output = app.query_one("#output", Log)
            output.focus()
            await pilot.pause()
            app._handle_vim_key("j")
            self.assertIs(app.focused, output)

            prompt = app.query_one("#prompt-input", TextArea)
            prompt.focus()
            await pilot.pause()
            app.on_key(events.Key("j", "j"))
            self.assertEqual(prompt.text, "")

    async def test_multiple_tasks_keep_independent_snapshots_and_transcripts(self):
        app, coordinator = self.make_app()
        async with app.run_test() as pilot:
            prompt = app.query_one("#prompt-input", TextArea)
            prompt.insert("First task")
            app.action_submit_prompt()
            first = coordinator.records[0]

            app.query_one("#model-select", Select).value = "gpt-5.6-terra"
            app.query_one("#reasoning-select", Select).value = "high"
            app.action_new_task()
            prompt.insert("Second task")
            app.action_submit_prompt()
            second = coordinator.records[1]

            self.assertTrue(app.query_one("#send-button", Button).disabled)
            self.assertFalse(prompt.disabled)
            self.assertEqual((first.model, first.reasoning), ("gpt-5.6-luna", "medium"))
            self.assertEqual((second.model, second.reasoning), ("gpt-5.6-terra", "high"))

            coordinator.finish(first, "Implemented the first task.")
            task_select = app.query_one("#task-select", Select)
            task_select.value = first.task_id
            await pilot.pause()

            first.error = "Cursor failed with exit code 1.\n\nDiagnostics:\nAuthentication failed."
            coordinator.emit(first, "failed", first.error, "error")

            task_select.value = second.task_id
            await pilot.pause()
            self.assertIn("Task branch: agent/task-2", str(app.query_one("#task-context", Static).render()))


if __name__ == "__main__":
    unittest.main()
