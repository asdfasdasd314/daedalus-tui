import json
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from textual import events
from textual.geometry import Offset
from textual.selection import Selection as ScreenSelection
from textual.widgets import Button, DataTable, Log, Select, Static, TextArea
from textual.widgets.text_area import Selection
from vimkeys_input import VimMode

from tui.app import CodingStatisticsScreen, DaedalusTuiApp, KeyboardShortcutsScreen
from tui.config import ModelOption, TuiSettings
from tui.projects import DaedalusProject
from tui.plan import PlanOption, PlanQuestion
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
        self.plan_actions = []
        self.retry_actions = []

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

    def continue_plan(self, task_id, notes=""):
        self.plan_actions.append(("continue", task_id, notes))
        return True

    def start_coding(self, task_id, notes=""):
        self.plan_actions.append(("coding", task_id, notes))
        return True

    def cancel(self, _task_id):
        return True

    def retry(self, task_id):
        self.retry_actions.append(task_id)
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
            self.assertIsInstance(app.query_one("#retry-button", Button), Button)
            self.assertIsInstance(app.query_one("#continue-plan-button", Button), Button)
            self.assertIsInstance(app.query_one("#start-coding-button", Button), Button)
            self.assertIsInstance(app.query_one("#new-task-button", Button), Button)
            await pilot.pause()

    @patch("tui.app.TaskCoordinator")
    @patch("tui.app.discover_projects")
    async def test_all_project_coordinators_share_the_launch_root_memory_file(self, discover, coordinator_class):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = root / "first"
            second = root / "second"
            discover.return_value = (
                DaedalusProject(first, root),
                DaedalusProject(second, root),
            )
            coordinator_class.return_value = FakeCoordinator()

            app = DaedalusTuiApp(
                runner=FakeRunner(),
                directory=root,
                settings=settings(),
            )
            app._coordinator_for(second)

            self.assertEqual(coordinator_class.call_count, 2)
            self.assertEqual(
                [call.kwargs["memory_path"] for call in coordinator_class.call_args_list],
                [root.resolve() / ".daedalus-memory.json"] * 2,
            )

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

    @patch("tui.app.discover_projects")
    async def test_initial_launch_records_default_project_and_each_switch_updates_it(self, discover):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = root / "first"
            second = root / "second"
            memory_path = root / ".daedalus-memory.json"
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

            self.assertEqual(
                json.loads(memory_path.read_text(encoding="utf-8")),
                [{"last_opened_project": str(first.resolve())}],
            )
            async with app.run_test() as pilot:
                project_select = app.query_one("#project-select", Select)
                project_select.value = str(second)
                await pilot.pause()
                self.assertEqual(
                    json.loads(memory_path.read_text(encoding="utf-8")),
                    [{"last_opened_project": str(second.resolve())}],
                )
                project_select.value = str(first)
                await pilot.pause()

            self.assertEqual(
                json.loads(memory_path.read_text(encoding="utf-8")),
                [{"last_opened_project": str(first.resolve())}],
            )

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
            self.assertIn("Ctrl+T", shortcut_text)
            self.assertIn("gg / G", shortcut_text)

            await pilot.press("escape")
            await pilot.pause()
            self.assertNotIsInstance(app.screen, KeyboardShortcutsScreen)

    async def test_ctrl_t_opens_coding_statistics_with_usage_columns_and_metrics(self):
        app, coordinator = self.make_app()
        async with app.run_test() as pilot:
            prompt = app.query_one("#prompt-input", DaedalusVimTextArea)
            prompt.insert("Track my token usage")
            app.action_submit_prompt()
            coordinator.records[0].tokens_consumed = 165
            await pilot.press("ctrl+t")
            await pilot.pause()

            self.assertIsInstance(app.screen, CodingStatisticsScreen)
            self.assertEqual(app.screen.query_one("#usage-table", DataTable).row_count, 1)
            summary_text = "\n".join(str(widget.render()) for widget in app.screen.query(".usage-metric"))
            statistics_text = "\n".join(
                str(widget.render()) for widget in app.screen.query(".statistics-value")
            )
            self.assertIn("Cumulative tokens", summary_text)
            self.assertIn("Average tokens per prompt", statistics_text)

            await pilot.press("escape")
            await pilot.pause()
            self.assertNotIsInstance(app.screen, CodingStatisticsScreen)

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

    async def test_failed_task_exposes_retry_action(self):
        app, coordinator = self.make_app()
        async with app.run_test() as pilot:
            app.query_one("#prompt-input", TextArea).insert("Retry this task")
            app.action_submit_prompt()
            record = coordinator.records[0]
            record.status = "failed"
            record.phase = "Failed"
            record.error = "Agent timed out; check your internet connection and retry."
            coordinator.emit(record, "failed", record.error, "error")
            await pilot.pause()

            retry_button = app.query_one("#retry-button", Button)
            self.assertFalse(retry_button.disabled)
            self.assertIn("internet connection", app.query_one("#task-error", TextArea).text)
            retry_button.press()
            await pilot.pause()
            self.assertEqual(coordinator.retry_actions, [record.task_id])

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

    async def test_prompt_e_advances_to_the_end_of_each_word(self):
        app, _ = self.make_app()
        async with app.run_test() as pilot:
            prompt = app.query_one("#prompt-input", DaedalusVimTextArea)
            prompt.insert("first second")
            prompt.cursor_location = (0, 0)

            await pilot.press("escape")
            await pilot.press("e")
            self.assertEqual(prompt.cursor_location, (0, 4))
            await pilot.press("e")
            self.assertEqual(prompt.cursor_location, (0, 11))

    async def test_escape_clears_visual_line_highlighting_and_cursor_does_not_blink(self):
        app, _ = self.make_app()
        async with app.run_test() as pilot:
            prompt = app.query_one("#prompt-input", DaedalusVimTextArea)
            prompt.insert("first line\nsecond line")
            prompt.cursor_location = (1, 3)

            await pilot.press("escape")
            await pilot.press("V")
            self.assertFalse(prompt.selection.is_empty)
            await pilot.press("escape")

            self.assertTrue(prompt.selection.is_empty)
            self.assertFalse(prompt.cursor_blink)

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

            self.assertEqual(prompt.yank_register, "copy this line\n")
            clipboard.assert_called_once_with("copy this line\n")

    async def test_prompt_cursor_shape_follows_insert_command_and_yank_pending(self):
        app, _ = self.make_app()
        async with app.run_test() as pilot:
            prompt = app.query_one("#prompt-input", DaedalusVimTextArea)
            prompt.insert("copy this line")

            self.assertEqual(prompt.vim_mode, VimMode.INSERT)
            self.assertEqual(prompt.cursor_shape, "bar")
            self.assertTrue(prompt.has_class("insert-mode"))
            self.assertFalse(prompt.has_class("operator-pending"))

            await pilot.press("escape")
            self.assertEqual(prompt.vim_mode, VimMode.COMMAND)
            self.assertEqual(prompt.cursor_shape, "block")
            self.assertTrue(prompt.has_class("command-mode"))

            await pilot.press("y")
            self.assertTrue(prompt.operator_pending.is_pending())
            self.assertEqual(prompt.cursor_shape, "underline")
            self.assertTrue(prompt.has_class("operator-pending"))

            await pilot.press("y")
            self.assertFalse(prompt.operator_pending.is_pending())
            self.assertEqual(prompt.cursor_shape, "block")
            self.assertFalse(prompt.has_class("operator-pending"))
            self.assertEqual(prompt.yank_register, "copy this line\n")

    async def test_insert_cursor_sits_left_of_text_at_a_middle_position(self):
        app, _ = self.make_app()
        async with app.run_test() as pilot:
            prompt = app.query_one("#prompt-input", DaedalusVimTextArea)
            prompt.focus()
            await pilot.pause()
            prompt.insert("beforeafter")
            self.assertTrue(prompt.has_focus)
            self.assertEqual(prompt.cursor_shape, "bar")
            prompt.cursor_location = (0, len("before"))

            rendered = prompt.render_line(0)

            self.assertIn("before", rendered.text)
            self.assertIn("▏", rendered.text)
            self.assertIn("after", rendered.text)
            self.assertLess(rendered.text.index("▏"), rendered.text.index("a"))

    async def test_prompt_dollar_moves_to_line_end_in_command_mode(self):
        app, _ = self.make_app()
        async with app.run_test() as pilot:
            prompt = app.query_one("#prompt-input", DaedalusVimTextArea)
            prompt.insert("hello world")
            prompt.cursor_location = (0, 0)

            await pilot.press("escape")
            await pilot.press("$")

            self.assertEqual(prompt.text, "hello world")
            self.assertEqual(prompt.cursor_location, prompt.get_cursor_line_end_location())
            self.assertEqual(prompt.vim_mode, VimMode.COMMAND)

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

    async def test_questioning_plan_is_selectable_and_can_continue_or_start_coding(self):
        app, coordinator = self.make_app()
        async with app.run_test() as pilot:
            app.query_one("#mode-select", Select).value = "plan"
            app.query_one("#prompt-input", TextArea).insert("Make a plan")
            app.action_submit_prompt()
            record = coordinator.records[0]
            record.status = "questioning"
            record.phase = "Questioning"
            record.messages.append("Plan output and open questions")
            coordinator.emit(record, "questioning", "Plan ready.", "status")
            await pilot.pause()

            self.assertEqual(str(app.query_one("#phase", Static).render()), "Phase: Questioning")
            self.assertFalse(app.query_one("#continue-plan-button", Button).disabled)
            self.assertFalse(app.query_one("#start-coding-button", Button).disabled)
            self.assertTrue(app.query_one("#pause-button", Button).disabled)
            self.assertFalse(app.query_one("#cancel-button", Button).disabled)

            app.query_one("#resume-notes", TextArea).insert("Please clarify the data flow.")
            app.action_continue_plan()
            self.assertEqual(
                coordinator.plan_actions[-1],
                ("continue", record.task_id, "Please clarify the data flow."),
            )

            record.status = "questioning"
            coordinator.emit(record, "questioning", "Plan ready again.", "status")
            app.query_one("#resume-notes", TextArea).insert("Use the smallest compatible change.")
            app._start_coding()
            self.assertEqual(
                coordinator.plan_actions[-1],
                ("coding", record.task_id, "Use the smallest compatible change."),
            )

    async def test_plan_review_renders_choices_and_keeps_implementation_locked(self):
        app, coordinator = self.make_app()
        async with app.run_test() as pilot:
            app.query_one("#mode-select", Select).value = "plan"
            app.query_one("#prompt-input", TextArea).insert("Choose a storage layer")
            app.action_submit_prompt()
            record = coordinator.records[0]
            record.status = "awaiting_answers"
            record.phase = "Questions"
            record.plan_text = "Use the selected storage layer."
            record.plan_questions = (
                PlanQuestion(
                    "q1",
                    "Which storage layer?",
                    (PlanOption("a", "SQLite"), PlanOption("b", "JSON")),
                ),
            )
            coordinator.emit(record, "questions", "", "status")
            await pilot.pause()

            self.assertEqual(app.query_one("#plan-display", Static).render().plain, record.plan_text)
            self.assertEqual(app.query_one("#output", Log).styles.display, "none")
            answer = app.query_one("#plan-question-0", Select)
            self.assertTrue(answer.query_one("#label"))
            self.assertTrue(app.query_one("#answer-plan-button", Button).disabled)
            self.assertTrue(app.query_one("#implement-button", Button).disabled)

            answer.value = "b"
            await pilot.pause()
            self.assertFalse(app.query_one("#answer-plan-button", Button).disabled)
            self.assertTrue(app.query_one("#implement-button", Button).disabled)

            record.plan_questions = ()
            record.plan_confirmed = True
            record.plan_answers = {"q1": "b"}
            record.status = "completed"
            coordinator.emit(record, "completed", "", "status")
            await pilot.pause()
            self.assertFalse(app.query_one("#implement-button", Button).disabled)

    async def test_plan_review_can_mount_a_preselected_answer(self):
        app, coordinator = self.make_app()
        async with app.run_test() as pilot:
            app.query_one("#mode-select", Select).value = "plan"
            app.query_one("#prompt-input", TextArea).insert("Choose a velocity model")
            app.action_submit_prompt()
            record = coordinator.records[0]
            record.status = "awaiting_answers"
            record.phase = "Questions"
            record.plan_text = "Use the selected velocity model."
            record.plan_questions = (
                PlanQuestion(
                    "q1",
                    "Which model?",
                    (
                        PlanOption("a", "GUIDED body-frame velocity (Recommended)"),
                        PlanOption("b", "World-frame velocity"),
                    ),
                ),
            )
            record.plan_answers = {"q1": "a"}
            coordinator.emit(record, "questions", "", "status")
            await pilot.pause()

            answer = app.query_one("#plan-question-0", Select)
            self.assertEqual(answer.value, "a")
            self.assertTrue(answer.query_one("#label"))
            self.assertIsNone(app._exception)

    async def test_plan_review_survives_streamed_completion_event(self):
        app, coordinator = self.make_app()
        async with app.run_test() as pilot:
            app.query_one("#mode-select", Select).value = "plan"
            app.query_one("#prompt-input", TextArea).insert("Plan the storage change")
            app.action_submit_prompt()
            record = coordinator.records[0]
            response = (
                'BEGIN_DAEDALUS_PLAN{"plan":"Use the selected storage layer.",'
                '"questions":[{"id":"q1","question":"Which storage layer?",'
                '"options":[{"id":"a","label":"SQLite"},{"id":"b","label":"JSON"}]},'
                '{"id":"q2","question":"Which format?",'
                '"options":[{"id":"a","label":"Compact"},{"id":"b","label":"Readable"}]}],'
                '"no_more_questions":false}END_DAEDALUS_PLAN'
            )

            def emit_realistic_plan_events() -> None:
                record.messages.append(response)
                record.status = "planning"
                record.phase = "Planning"
                coordinator.emit(record, "agent", response, "message")
                record.status = "awaiting_answers"
                record.phase = "Questions"
                record.plan_text = "Use the selected storage layer."
                record.plan_questions = (
                    PlanQuestion(
                        "q1",
                        "Which storage layer?",
                        (PlanOption("a", "SQLite"), PlanOption("b", "JSON")),
                    ),
                    PlanQuestion(
                        "q2",
                        "Which format?",
                        (PlanOption("a", "Compact"), PlanOption("b", "Readable")),
                    ),
                )
                coordinator.emit(record, "questions", "", "status")

            event_thread = threading.Thread(target=emit_realistic_plan_events)
            event_thread.start()
            await pilot.pause()
            event_thread.join(timeout=1)
            await pilot.pause()

            self.assertFalse(event_thread.is_alive())
            self.assertEqual(
                [app.query_one(f"#plan-question-{index}", Select).value for index in range(2)],
                [Select.NULL, Select.NULL],
            )
            self.assertEqual(app.query_one("#phase", Static).render().plain, "Phase: Questions")

    async def test_plan_review_render_error_does_not_exit_tui(self):
        app, _coordinator = self.make_app()

        async def fail_rebuild(*_args):
            raise RuntimeError("synthetic plan widget failure")

        async with app.run_test() as pilot:
            with patch.object(app, "_rebuild_plan_questions", fail_rebuild):
                app.query_one("#mode-select", Select).value = "plan"
                app.query_one("#prompt-input", TextArea).insert("Plan safely")
                app.action_submit_prompt()
                await pilot.pause()

            self.assertIsNone(app._exception)
            self.assertEqual(str(app.query_one("#status", Static).render()), "Error")
            self.assertIn("synthetic plan widget failure", app.query_one("#task-error", TextArea).text)

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

    async def test_final_assistant_message_uses_brighter_transcript_tone(self):
        app, coordinator = self.make_app()
        async with app.run_test() as pilot:
            app.query_one("#prompt-input", TextArea).insert("Build the feature")
            app.action_submit_prompt()
            record = coordinator.records[0]
            record.messages.extend(["I am inspecting the worktree.", "The feature is complete."])
            record.status = "completed"
            record.phase = "Completed"
            coordinator.emit(record, "completed", "", "status")
            await pilot.pause()

            output = app.query_one("#output", Log)
            self.assertEqual(output.line_tones[:2], ("generic", "final"))

    async def test_final_assistant_message_renders_with_resolved_theme_color(self):
        app, coordinator = self.make_app()
        async with app.run_test() as pilot:
            app.query_one("#prompt-input", TextArea).insert("Build the feature")
            app.action_submit_prompt()
            record = coordinator.records[0]
            record.messages.extend(["I am inspecting the worktree.", "The feature is complete."])
            record.status = "completed"
            record.phase = "Completed"
            coordinator.emit(record, "completed", "", "status")
            await pilot.pause()

            output = app.query_one("#output", Log)
            output._render_line_strip(1, output.rich_style)

    async def test_submitted_prompt_uses_faded_read_only_text_style(self):
        app, _ = self.make_app()
        async with app.run_test() as pilot:
            prompt = app.query_one("#prompt-input", DaedalusVimTextArea)
            prompt.insert("Keep this task immutable")
            app.action_submit_prompt()
            await pilot.pause()

            self.assertTrue(prompt.read_only)
            self.assertTrue(prompt.has_class("-read-only"))

    async def test_output_selection_uses_prompt_selection_colors(self):
        app, _ = self.make_app()
        async with app.run_test():
            output_selection = app.screen.get_component_rich_style("screen--selection")
            prompt_selection = app.query_one("#prompt-input").get_component_rich_style(
                "text-area--selection"
            )

            self.assertEqual(output_selection.bgcolor, prompt_selection.bgcolor)
            self.assertEqual(output_selection.color, prompt_selection.color)

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

    async def test_background_events_do_not_choose_an_unselected_task(self):
        app, coordinator = self.make_app()
        async with app.run_test() as pilot:
            prompt = app.query_one("#prompt-input", TextArea)
            prompt.insert("First task")
            app.action_submit_prompt()

            app.action_new_task()
            prompt.insert("Second task")
            app.action_submit_prompt()
            second = coordinator.records[1]

            app._selected_task_id = None
            app._new_task_mode = False
            coordinator.emit(second, "agent", "A background update.", "message")
            await pilot.pause()

            self.assertIsNone(app._selected_task_id)
            self.assertEqual(app.query_one("#task-select", Select).value, "")


if __name__ == "__main__":
    unittest.main()
