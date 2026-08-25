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
from vimkeys_input import VimMode

from tui.app import CodingStatisticsScreen, DaedalusTuiApp, KeyboardShortcutsScreen
from tui.config import ModelOption, TuiSettings
from tui.projects import DaedalusProject
from tui.plan import CUSTOM_ANSWER_OPTION_ID, PlanOption, PlanQuestion, encode_custom_answer
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

    def answer_plan(self, task_id, answers):
        record = self.get(task_id)
        if record is None:
            return False
        record.plan_answers.update(answers)
        record.status = "queued"
        record.phase = "Queued (reviewing answers)"
        self.emit(record, "queued", "Plan answers queued for agent confirmation.", "status")
        return True

    def implement_plan(self, task_id):
        record = self.get(task_id)
        if record is None or record.plan_implemented:
            return None
        record.plan_implemented = True
        return self.submit("Approved implementation", record.provider, record.model, record.reasoning)

    def clarify_plan_question(self, task_id, question_id, user_question):
        record = self.get(task_id)
        if record is None:
            return False
        from tui.plan import PlanClarification

        clarification = PlanClarification(
            clarification_id=f"c{len(record.plan_clarifications.get(question_id, [])) + 1}",
            question_id=question_id,
            user_question=user_question,
            status="completed",
            answer=f"Clarified: {user_question}",
        )
        record.plan_clarifications.setdefault(question_id, []).append(clarification)
        self.plan_actions.append(("clarify", task_id, question_id, user_question))
        self.emit(record, "clarification", clarification.answer, "status")
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
            self.assertEqual(app.query_one("#target-branch-select", Select).value, "main")
            self.assertIn("/workspace/project", str(app.query_one("#directory", Static).render()))
            self.assertIsInstance(app.query_one("#task-list", DataTable), DataTable)
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

    async def test_task_list_keeps_failures_active_work_and_current_session_tasks(self):
        app, coordinator = self.make_app()
        historical_completed = TaskRecord(
            "001-completed",
            1,
            "An old completed task",
            "codex",
            "model",
            "medium",
            status="completed",
        )
        historical_failed = TaskRecord(
            "002-failed",
            2,
            "An old failed task",
            "codex",
            "model",
            "medium",
            status="failed",
        )
        historical_paused = TaskRecord(
            "003-paused",
            3,
            "An interrupted task",
            "codex",
            "model",
            "medium",
            status="paused",
        )
        historical_cancelled = TaskRecord(
            "004-cancelled",
            4,
            "An old cancelled task",
            "codex",
            "model",
            "medium",
            status="cancelled",
        )
        coordinator.records.extend(
            (historical_completed, historical_failed, historical_paused, historical_cancelled)
        )

        async with app.run_test() as pilot:
            await pilot.pause()
            visible_before_submit = set(app._task_rows)
            self.assertIn(app._task_row_key(app._active_project_path, historical_failed.task_id), visible_before_submit)
            self.assertIn(app._task_row_key(app._active_project_path, historical_paused.task_id), visible_before_submit)
            self.assertNotIn(
                app._task_row_key(app._active_project_path, historical_completed.task_id),
                visible_before_submit,
            )
            self.assertNotIn(
                app._task_row_key(app._active_project_path, historical_cancelled.task_id),
                visible_before_submit,
            )

            app.query_one("#prompt-input", TextArea).insert("A task from this session")
            app.action_submit_prompt()
            current = coordinator.records[-1]
            current.status = "completed"
            app._refresh_task_list()

            self.assertIn(app._task_row_key(app._active_project_path, current.task_id), app._task_rows)

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
            self.assertEqual(
                [call.args[2].primary_branch for call in coordinator_class.call_args_list],
                ["main", "main"],
            )

    @patch("tui.app.TaskCoordinator")
    @patch("tui.app.list_local_branches")
    @patch("tui.app.discover_projects")
    async def test_target_branch_select_persists_per_project_and_restores_on_switch(
        self, discover, list_branches, coordinator_class
    ):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = root / "wfinance"
            second = root / "other"
            memory_path = root / ".daedalus-memory.json"
            discover.return_value = (
                DaedalusProject(first, root),
                DaedalusProject(second, root),
            )
            list_branches.side_effect = lambda path: {
                first.resolve(): ["main", "james"],
                second.resolve(): ["main", "develop"],
            }.get(Path(path).resolve(), ["main"])
            coordinator_class.side_effect = lambda *args, **kwargs: FakeCoordinator()

            app = DaedalusTuiApp(
                runner=FakeRunner(),
                directory=root,
                settings=settings(),
                coordinator=FakeCoordinator(),
            )

            async with app.run_test() as pilot:
                branch_select = app.query_one("#target-branch-select", Select)
                self.assertEqual(branch_select.value, "main")
                branch_select.value = "james"
                await pilot.pause()
                self.assertEqual(app.coordinator.settings.primary_branch, "james")
                self.assertEqual(
                    json.loads(memory_path.read_text(encoding="utf-8")),
                    [
                        {"last_opened_project": str(first.resolve())},
                        {
                            "project_target_branches": {
                                str(first.resolve()): "james",
                            }
                        },
                    ],
                )

                project_select = app.query_one("#project-select", Select)
                project_select.value = str(second)
                await pilot.pause()
                self.assertEqual(app.query_one("#target-branch-select", Select).value, "main")
                self.assertEqual(app.coordinator.settings.primary_branch, "main")

                app.query_one("#target-branch-select", Select).value = "develop"
                await pilot.pause()
                project_select.value = str(first)
                await pilot.pause()

                self.assertEqual(app.query_one("#target-branch-select", Select).value, "james")
                self.assertEqual(app.coordinator.settings.primary_branch, "james")
                mapping = next(
                    entry["project_target_branches"]
                    for entry in json.loads(memory_path.read_text(encoding="utf-8"))
                    if "project_target_branches" in entry
                )
                self.assertEqual(
                    mapping,
                    {
                        str(first.resolve()): "james",
                        str(second.resolve()): "develop",
                    },
                )

    @patch("tui.app.list_local_branches")
    @patch("tui.app.discover_projects")
    async def test_stale_remembered_target_branch_clears_memory_and_falls_back(
        self, discover, list_branches
    ):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "wfinance"
            memory_path = root / ".daedalus-memory.json"
            memory_path.write_text(
                json.dumps(
                    [
                        {"last_opened_project": str(project.resolve())},
                        {
                            "project_target_branches": {
                                str(project.resolve()): "james",
                            }
                        },
                    ]
                ),
                encoding="utf-8",
            )
            discover.return_value = (DaedalusProject(project, root),)
            list_branches.return_value = ["main", "develop"]

            app = DaedalusTuiApp(
                runner=FakeRunner(),
                directory=root,
                settings=settings(),
                coordinator=FakeCoordinator(),
            )

            async with app.run_test() as pilot:
                await pilot.pause()
                self.assertEqual(app.query_one("#target-branch-select", Select).value, "main")
                self.assertEqual(app.coordinator.settings.primary_branch, "main")

            self.assertEqual(
                json.loads(memory_path.read_text(encoding="utf-8")),
                [{"last_opened_project": str(project.resolve())}],
            )

    @patch("tui.app.TaskCoordinator")
    @patch("tui.app.list_local_branches")
    @patch("tui.app.discover_projects")
    async def test_new_task_coordinator_uses_project_primary_branch(
        self, discover, list_branches, coordinator_class
    ):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "wfinance"
            memory_path = root / ".daedalus-memory.json"
            memory_path.write_text(
                json.dumps(
                    [
                        {
                            "project_target_branches": {
                                str(project.resolve()): "james",
                            }
                        }
                    ]
                ),
                encoding="utf-8",
            )
            discover.return_value = (DaedalusProject(project, root),)
            list_branches.return_value = ["main", "james"]
            coordinator_class.return_value = FakeCoordinator()

            app = DaedalusTuiApp(
                runner=FakeRunner(),
                directory=root,
                settings=settings(),
            )

            self.assertEqual(coordinator_class.call_args.args[2].primary_branch, "james")
            async with app.run_test() as pilot:
                await pilot.pause()
                self.assertEqual(app.coordinator.settings.primary_branch, "james")

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
            coordinator.records[0].status = "completed"
            await pilot.press("ctrl+t")
            await pilot.pause()

            self.assertIsInstance(app.screen, CodingStatisticsScreen)
            usage_table = app.screen.query_one("#usage-table", DataTable)
            self.assertEqual(usage_table.row_count, 1)
            self.assertEqual(
                [column.width for column in usage_table.columns.values()],
                [16, len("Provider"), len("Tokens")],
            )
            summary_text = "\n".join(str(widget.render()) for widget in app.screen.query(".usage-metric"))
            statistics_text = "\n".join(
                str(widget.render()) for widget in app.screen.query(".statistics-value")
            )
            self.assertIn("Cumulative tokens", summary_text)
            self.assertIn("Average tokens per prompt", statistics_text)
            self.assertIn("30-day expected tokens", summary_text)

            app.screen.query_one("#statistics-unit-select", Select).value = "tasks"
            await pilot.pause()
            task_summary = "\n".join(
                str(widget.render()) for widget in app.screen.query(".usage-metric")
            )
            task_statistics = "\n".join(
                str(widget.render()) for widget in app.screen.query(".statistics-value")
            )
            self.assertIn("Cumulative tasks", task_summary)
            self.assertIn("30-day expected tasks", task_summary)
            self.assertIn("Average tasks per prompt", task_statistics)
            self.assertEqual(
                [column.label.plain for column in app.screen.query_one("#usage-table", DataTable).columns.values()],
                ["Timestamp", "Provider", "Tasks"],
            )

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

    @patch("tui.app.discover_projects")
    async def test_project_switch_preserves_editable_prompt_draft(self, discover):
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
            prompt = app.query_one("#prompt-input", DaedalusVimTextArea)
            prompt.insert("Draft written for the wrong project")
            await pilot.pause()

            app.query_one("#project-select", Select).value = str(second)
            await pilot.pause()

            self.assertEqual(app.directory, second)
            self.assertEqual(prompt.text, "Draft written for the wrong project")
            self.assertFalse(prompt.read_only)
            self.assertFalse(app.query_one("#send-button", Button).disabled)

    @patch("tui.app.discover_projects")
    async def test_project_switch_does_not_keep_read_only_task_prompt(self, discover):
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
            prompt = app.query_one("#prompt-input", DaedalusVimTextArea)
            prompt.insert("Submitted task prompt")
            app.action_submit_prompt()
            await pilot.pause()
            self.assertTrue(prompt.read_only)

            app.query_one("#project-select", Select).value = str(second)
            await pilot.pause()

            self.assertEqual(app.directory, second)
            self.assertEqual(prompt.text, "")
            self.assertFalse(prompt.read_only)

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
            self.assertIn("cannot be empty", "\n".join(app.query_one("#task-error", Log)._lines))
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
            task_list = app.query_one("#task-list", DataTable)
            task_list.move_cursor(row=0, column=0)
            task_list.action_select_cursor()
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
            self.assertIn("internet connection", "\n".join(app.query_one("#task-error", Log)._lines))
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

    async def test_insert_cursor_keeps_the_character_at_a_middle_position_visible(self):
        app, _ = self.make_app()
        async with app.run_test() as pilot:
            prompt = app.query_one("#prompt-input", DaedalusVimTextArea)
            prompt.focus()
            await pilot.pause()
            prompt.insert("beforeafter")
            self.assertTrue(prompt.has_focus)
            self.assertEqual(prompt.cursor_shape, "bar")
            self.assertFalse(prompt.highlight_cursor_line)
            prompt.cursor_location = (0, len("before"))

            rendered = prompt.render_line(0)

            self.assertEqual(prompt.text, "beforeafter")
            self.assertEqual(rendered.cell_length, TextArea.render_line(prompt, 0).cell_length)
            self.assertEqual(rendered.text, TextArea.render_line(prompt, 0).text)
            self.assertEqual(rendered.text[len("before")], "a")
            self.assertEqual(rendered.text[len("before") + 1], "f")

            cursor_style = prompt._theme.cursor_style
            self.assertTrue(cursor_style.transparent_background)
            self.assertIsNone(cursor_style.bgcolor)
            self.assertTrue(cursor_style.underline)

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

    async def test_plan_review_renders_literal_markup_like_agent_text(self):
        """Agent plan text must not be parsed as Textual/Rich markup."""
        app, coordinator = self.make_app()
        markup_like_plan = (
            "[Q=1e-4`, measurement noise `R=1e-2` on price "
            "(or log-price — pick price-level for readability)"
        )
        markup_like_question = (
            "Keep process noise [Q=1e-4` and measurement noise `R=1e-2`?"
        )
        async with app.run_test() as pilot:
            app.query_one("#mode-select", Select).value = "plan"
            app.query_one("#prompt-input", TextArea).insert("Plan a Kalman filter")
            app.action_submit_prompt()
            record = coordinator.records[0]
            record.status = "awaiting_answers"
            record.phase = "Questions"
            record.plan_text = markup_like_plan
            record.plan_questions = (
                PlanQuestion(
                    "q1",
                    markup_like_question,
                    (
                        PlanOption("a", "Price-level (Recommended)"),
                        PlanOption("b", "Log-price"),
                    ),
                ),
            )
            coordinator.emit(record, "questions", "", "status")
            await pilot.pause()
            await pilot.pause()

            plan_display = app.query_one("#plan-display", Static)
            self.assertEqual(plan_display.render().plain, markup_like_plan)
            question = app.query_one(".plan-question", Static)
            self.assertEqual(question.render().plain, markup_like_question)
            self.assertIsNone(app._exception)
            self.assertNotEqual(str(app.query_one("#status", Static).render()), "Error")
            self.assertNotIn(
                "Expected markup value",
                "\n".join(app.query_one("#task-error", Log)._lines),
            )
            self.assertTrue(app.query_one("#plan-question-0", Select).query_one("#label"))

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

            app.query_one("#implement-button", Button).press()
            await pilot.pause()
            self.assertTrue(record.plan_implemented)
            implement_button = app.query_one("#implement-button", Button)
            self.assertTrue(implement_button.disabled)
            self.assertTrue(implement_button.has_class("implemented"))
            self.assertEqual(str(implement_button.label), "Implemented")

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

    async def test_submitting_plan_answers_keeps_mounted_selectors_in_place(self):
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
            await pilot.pause()

            answer = app.query_one("#plan-question-0", Select)
            answer.value = "b"
            await pilot.pause()
            with patch.object(app, "run_worker") as run_worker:
                app._answer_plan()
                await pilot.pause()

            self.assertEqual(record.status, "queued")
            self.assertEqual(record.plan_answers, {"q1": "b"})
            self.assertIs(app.query_one("#plan-question-0", Select), answer)
            run_worker.assert_not_called()
            self.assertIsNone(app._exception)

    async def test_plan_review_accepts_a_ui_owned_custom_answer(self):
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

            answer = app.query_one("#plan-question-0", Select)
            custom_input = app.query_one("#plan-custom-answer-0", TextArea)
            self.assertTrue(app.query_one("#answer-plan-button", Button).disabled)
            answer.value = CUSTOM_ANSWER_OPTION_ID
            await pilot.pause()
            self.assertEqual(custom_input.styles.display, "block")
            self.assertTrue(app.query_one("#answer-plan-button", Button).disabled)

            custom_input.insert("A user-defined storage layer")
            await pilot.pause()
            self.assertFalse(app.query_one("#answer-plan-button", Button).disabled)
            app._answer_plan()

            self.assertEqual(
                record.plan_answers,
                {"q1": encode_custom_answer("A user-defined storage layer")},
            )

    async def test_plan_answer_mount_suppresses_textual_select_default_handler(self):
        app, coordinator = self.make_app()
        async with app.run_test() as pilot:
            app.query_one("#mode-select", Select).value = "plan"
            app.query_one("#prompt-input", TextArea).insert("Choose a model")
            app.action_submit_prompt()
            record = coordinator.records[0]
            record.status = "awaiting_answers"
            record.phase = "Questions"
            record.plan_text = "Use the selected model."
            record.plan_questions = (
                PlanQuestion(
                    "q1",
                    "Which model?",
                    (PlanOption("a", "Local"), PlanOption("b", "Remote")),
                ),
            )

            def unexpected_default_mount(*_args, **_kwargs):
                raise AssertionError("Textual Select default mount handler ran")

            with patch.object(Select, "_on_mount", unexpected_default_mount):
                coordinator.emit(record, "questions", "", "status")
                await pilot.pause()
                await pilot.pause()

            self.assertEqual(app.query_one("#plan-question-0", Select).value, Select.NULL)
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

    async def test_plan_question_clarification_button_and_viewer(self):
        from tui.app import PlanClarificationScreen
        from tui.plan import PlanClarification

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
            await pilot.pause()

            clarify_button = app.query_one("#plan-clarify-0", Button)
            self.assertEqual(str(clarify_button.label), "?")

            with patch.object(app, "push_screen") as push_screen:
                clarify_button.press()
                await pilot.pause()
                self.assertEqual(push_screen.call_count, 1)
                screen = push_screen.call_args.args[0]
                self.assertIsInstance(screen, PlanClarificationScreen)
                callback = push_screen.call_args.args[1]
                callback("What does storage layer mean?")

            self.assertEqual(
                coordinator.plan_actions[-1],
                ("clarify", record.task_id, "q1", "What does storage layer mean?"),
            )
            await pilot.pause()
            await pilot.pause()

            self.assertEqual(
                app.query_one("#plan-clarification-select-0", Select).value,
                record.plan_clarifications["q1"][-1].clarification_id,
            )
            self.assertIn(
                "Clarified: What does storage layer mean?",
                app.query_one("#plan-clarification-answer-0", Static).render().plain,
            )

            record.plan_clarifications["q1"].append(
                PlanClarification(
                    clarification_id="c2",
                    question_id="q1",
                    user_question="Is JSON for config only?",
                    status="completed",
                    answer="Yes, keep JSON for config.",
                )
            )
            coordinator.emit(record, "clarification", "Yes, keep JSON for config.", "status")
            await pilot.pause()
            await pilot.pause()

            select = app.query_one("#plan-clarification-select-0", Select)
            select.value = "c2"
            await pilot.pause()
            self.assertIn(
                "Yes, keep JSON for config.",
                app.query_one("#plan-clarification-answer-0", Static).render().plain,
            )

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
            self.assertIn(
                "synthetic plan widget failure",
                "\n".join(app.query_one("#task-error", Log)._lines),
            )

    async def test_late_background_event_is_ignored_after_app_shutdown(self):
        app, coordinator = self.make_app()
        async with app.run_test() as pilot:
            record = coordinator.records[0] if coordinator.records else TaskRecord(
                "late-task", 1, "late", "codex", "luna", "medium"
            )
            app._accept_task_events = False
            app._on_task_event(record, "agent", "late output", "message")
            app._accept_task_events = True
            with patch.object(app, "call_from_thread", side_effect=RuntimeError("App is not running")):
                event_thread = threading.Thread(
                    target=app._on_task_event,
                    args=(record, "agent", "late output", "message"),
                )
                event_thread.start()
                event_thread.join(timeout=1)
                self.assertFalse(event_thread.is_alive())
            await pilot.pause()

        self.assertIsNone(app._exception)

    def test_run_loop_fallback_stops_coordinator_when_unmount_is_skipped(self):
        app, coordinator = self.make_app()

        app.shutdown_after_run()
        self.assertFalse(app._accept_task_events)
        self.assertIsNone(coordinator.callback)
        # The guard is idempotent because multiple lifecycle paths can observe
        # the same shutdown.
        self.assertTrue(app._shutdown_coordinators("repeat process exit"))

    async def test_task_render_failure_is_logged_without_exiting_the_app(self):
        app, coordinator = self.make_app()
        async with app.run_test() as pilot:
            app.query_one("#prompt-input", TextArea).insert("Keep rendering")
            app.action_submit_prompt()
            record = coordinator.records[0]
            await pilot.pause()
            with patch.object(app, "_render_selected_task", side_effect=RuntimeError("render failure")):
                app._apply_task_event(record, "agent", "output", "message")

            self.assertIsNone(app._exception)
            self.assertEqual(str(app.query_one("#status", Static).render()), "Error")
            self.assertIn("render failure", "\n".join(app.query_one("#task-error", Log)._lines))

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
    async def test_copy_selection_reads_selectable_error_log(self, native_clipboard):
        app, _ = self.make_app()
        async with app.run_test() as pilot:
            error = app.query_one("#task-error", Log)
            error.write("only this diagnostic section")
            error.focus()
            await pilot.pause()
            selected = error.get_selection(
                ScreenSelection.from_offsets(Offset(0, 0), Offset(10, 0))
            )
            self.assertTrue(selected)
            app.screen.get_selected_text = Mock(return_value=selected[0])

            self.assertTrue(error.allow_select)
            app._handle_vim_key("y")
            native_clipboard.assert_called_once_with(selected[0])

            native_clipboard.reset_mock()
            app.action_copy_selection()
            native_clipboard.assert_called_once_with(selected[0])

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
            final_line = output._lines.index("The feature is complete.")
            self.assertEqual(output.line_tones[final_line], "final")

    async def test_output_messages_are_separated_and_wrapped(self):
        app, coordinator = self.make_app()
        async with app.run_test() as pilot:
            app.query_one("#prompt-input", TextArea).insert("Show progress")
            app.action_submit_prompt()
            record = coordinator.records[0]
            record.messages.extend(
                [
                    "Deciphering things",
                    "Deciphering more things",
                    "Here is the final answer: " + ("a " * 200),
                ]
            )
            record.status = "completed"
            record.phase = "Completed"
            coordinator.emit(record, "completed", "", "status")
            await pilot.pause()

            output = app.query_one("#output", Log)
            self.assertEqual(output._lines[:3], [
                "Deciphering things",
                "",
                "Deciphering more things",
            ])
            self.assertGreater(len(output._lines), 5)
            self.assertTrue(all(len(line) <= output.size.width for line in output._lines))

    async def test_output_wraps_at_words_and_hyphenates_overlong_words(self):
        app, _ = self.make_app()
        async with app.run_test():
            output = app.query_one("#output", Log)

            self.assertEqual(
                output._wrap_line("Keep complete words together", 13),
                ["Keep complete", "words together"],
            )
            self.assertEqual(
                output._wrap_line("abcdefghijk", 6),
                ["abcde-", "fghij-", "k"],
            )

    async def test_output_rewraps_messages_when_the_content_width_changes(self):
        app, coordinator = self.make_app()
        async with app.run_test() as pilot:
            app.query_one("#prompt-input", TextArea).insert("Resize the output")
            app.action_submit_prompt()
            record = coordinator.records[0]
            record.messages.append("A long output line that should reflow when the output box changes width.")
            record.status = "running"
            record.phase = "Agent"
            coordinator.emit(record, "agent", "", "status")
            await pilot.pause()

            output = app.query_one("#output", Log)
            original_lines = tuple(output._lines)
            output.styles.width = 32
            await pilot.pause()

            self.assertNotEqual(tuple(output._lines), original_lines)
            content_width = output.content_region.width
            self.assertTrue(all(len(line) <= content_width for line in output._lines if line))

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
            output._render_line_strip(2, output.rich_style)

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
            task_list = app.query_one("#task-list", DataTable)
            first_row = app._task_row_key(app._active_project_path, first.task_id)
            task_list.move_cursor(row=list(app._task_rows).index(first_row), column=0)
            task_list.action_select_cursor()
            await pilot.pause()

            first.error = "Cursor failed with exit code 1.\n\nDiagnostics:\nAuthentication failed."
            coordinator.emit(first, "failed", first.error, "error")

            second_row = app._task_row_key(app._active_project_path, second.task_id)
            task_list.move_cursor(row=list(app._task_rows).index(second_row), column=0)
            task_list.action_select_cursor()
            await pilot.pause()
            self.assertIn("Task branch: agent/task-2", str(app.query_one("#task-context", Static).render()))

    async def test_background_progress_does_not_promote_an_unselected_task(self):
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
            row_key = app._task_row_key(app._active_project_path, second.task_id)
            self.assertNotIn(row_key, app._updated_task_rows)

    async def test_background_completion_promotes_an_unselected_task(self):
        app, coordinator = self.make_app()
        async with app.run_test() as pilot:
            prompt = app.query_one("#prompt-input", TextArea)
            prompt.insert("First task")
            app.action_submit_prompt()

            app.action_new_task()
            prompt.insert("Second task")
            app.action_submit_prompt()
            first = coordinator.records[0]
            app._selected_task_id = None

            coordinator.finish(first, "The task is complete.")
            await pilot.pause()

            row_key = app._task_row_key(app._active_project_path, first.task_id)
            self.assertIn(row_key, app._updated_task_rows)

    async def test_plan_questions_promote_an_unselected_task(self):
        app, coordinator = self.make_app()
        async with app.run_test() as pilot:
            app.query_one("#mode-select", Select).value = "plan"
            app.query_one("#prompt-input", TextArea).insert("Make a plan")
            app.action_submit_prompt()
            record = coordinator.records[0]
            app._selected_task_id = None
            record.status = "awaiting_answers"
            record.plan_questions = (
                PlanQuestion(
                    "q1",
                    "Which option?",
                    (PlanOption("a", "A"), PlanOption("b", "B")),
                ),
            )
            coordinator.emit(record, "questions", "", "status")
            await pilot.pause()

            row_key = app._task_row_key(app._active_project_path, record.task_id)
            self.assertIn(row_key, app._updated_task_rows)

            app._updated_task_rows.discard(row_key)
            record.status = "completed"
            record.plan_questions = ()
            record.plan_confirmed = True
            coordinator.emit(record, "completed", "", "status")
            await pilot.pause()

            self.assertIn(row_key, app._updated_task_rows)


if __name__ == "__main__":
    unittest.main()
