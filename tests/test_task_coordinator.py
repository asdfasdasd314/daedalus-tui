from datetime import datetime, timezone
import json
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from tui.orchestrator import OrchestrationResult, OrchestrationSettings
from tui.git_worktree import WorktreeContext
from tui.plan import PlanOption, PlanQuestion, encode_custom_answer
from tui.task_coordinator import TASK_STATUSES, IntegrationCoordinator, TaskCoordinator, TaskRecord


class FakeOrchestrator:
    active = 0
    maximum = 0
    lock = threading.Lock()
    starts = []
    release = None

    def __init__(self, _repository, _runner, _settings, on_event, integration_gate=None):
        self.on_event = on_event
        self.integration_gate = integration_gate

    def run(self, prompt, provider, model, reasoning, task_id=None, submission_sequence=0, mode="coding", control=None, existing_context=None, resume_notes=()):
        with self.lock:
            type(self).active += 1
            type(self).maximum = max(type(self).maximum, type(self).active)
            type(self).starts.append((prompt, provider, model, reasoning))
        self.on_event("worktree", f"Created agent/task-{task_id} at /tmp/{task_id}.", "status")
        self.on_event("agent", f"Completed {prompt}", "message")
        if type(self).release is not None:
            type(self).release.wait(timeout=5)

        def integrate():
            self.on_event("integration", "Integrating task.", "status")

        self.on_event("ready", "Ready.", "status")
        self.integration_gate(submission_sequence, integrate)
        with self.lock:
            type(self).active -= 1
        return OrchestrationResult(True, task_id, f"agent/task-{task_id}", Path(f"/tmp/{task_id}"))


class TaskCoordinatorTests(unittest.TestCase):
    def setUp(self):
        FakeOrchestrator.active = 0
        FakeOrchestrator.maximum = 0
        FakeOrchestrator.starts = []
        FakeOrchestrator.release = threading.Event()

    def test_executor_limits_concurrent_agent_tasks_and_snapshots_settings(self):
        self.assertIn("blocked", TASK_STATUSES)
        with tempfile.TemporaryDirectory() as directory:
            coordinator = TaskCoordinator(
                Path(directory),
                object(),
                OrchestrationSettings(max_concurrent_tasks=2),
            )
            with patch("tui.task_coordinator.LocalOrchestrator", FakeOrchestrator):
                records = [
                    coordinator.submit(f"Task {index}", "codex", f"model-{index}", "medium")
                    for index in range(5)
                ]
                deadline = time.time() + 2
                while len(FakeOrchestrator.starts) < 2 and time.time() < deadline:
                    time.sleep(0.01)
                self.assertEqual(len(FakeOrchestrator.starts), 2)
                self.assertLessEqual(FakeOrchestrator.maximum, 2)
                self.assertEqual(records[0].status, "running")
                self.assertEqual(records[2].status, "queued")
                FakeOrchestrator.release.set()
                for record in records:
                    record.future.result(timeout=5)
            self.assertLessEqual(FakeOrchestrator.maximum, 2)
            self.assertEqual(
                [(record.model, record.reasoning) for record in records[:2]],
                [("model-0", "medium"), ("model-1", "medium")],
            )
            coordinator.shutdown()

    def test_plan_task_stays_questioning_until_started_as_coding(self):
        class PlanningOrchestrator:
            calls = []

            def __init__(self, *_args, **_kwargs):
                pass

            def run(self, prompt, _provider, _model, _reasoning, task_id=None, mode="coding", **kwargs):
                type(self).calls.append((mode, kwargs.get("existing_context"), kwargs.get("resume_notes", ())))
                context = kwargs.get("existing_context") or WorktreeContext(
                    Path(directory), task_id, "base", f"agent/task-{task_id}", Path(directory) / "worktree"
                )
                return OrchestrationResult(
                    True,
                    task_id,
                    context.branch_name,
                    context.path,
                    context=context,
                    awaiting_plan=mode == "plan",
                )

        with tempfile.TemporaryDirectory() as directory:
            coordinator = TaskCoordinator(Path(directory), object(), OrchestrationSettings(max_concurrent_tasks=1))
            with patch("tui.task_coordinator.LocalOrchestrator", PlanningOrchestrator):
                record = coordinator.submit("plan this", "codex", "luna", "medium", mode="plan")
                record.future.result(timeout=5)

                self.assertEqual(record.status, "questioning")
                self.assertEqual(record.phase, "Questioning")
                self.assertTrue(coordinator.continue_plan(record.task_id, "What about the API boundary?"))
                record.future.result(timeout=5)
                self.assertEqual(record.status, "questioning")

                self.assertTrue(coordinator.start_coding(record.task_id, "Proceed with the minimal design."))
                record.future.result(timeout=5)

            self.assertEqual(record.mode, "coding")
            self.assertEqual(record.status, "completed")
            self.assertEqual([call[0] for call in PlanningOrchestrator.calls], ["plan", "plan", "coding"])
            self.assertIs(PlanningOrchestrator.calls[1][1], record.context)
            self.assertIn("What about the API boundary?", PlanningOrchestrator.calls[1][2])
            coordinator.shutdown()

    def test_first_ready_integration_is_serialized(self):
        coordinator = IntegrationCoordinator()
        started = threading.Event()
        release = threading.Event()
        order = []

        def first_operation():
            order.append(2)
            started.set()
            release.wait(timeout=5)

        thread_two = threading.Thread(target=coordinator.run_when_ready, args=(2, first_operation))
        thread_two.start()
        self.assertTrue(started.wait(timeout=2))

        thread_one = threading.Thread(
            target=coordinator.run_when_ready,
            args=(1, lambda: order.append(1)),
        )
        thread_one.start()
        time.sleep(0.05)
        self.assertEqual(order, [2])
        release.set()
        thread_two.join(timeout=2)
        thread_one.join(timeout=2)
        self.assertEqual(order, [2, 1])

    def test_shutdown_cancels_an_active_worker_without_waiting_indefinitely(self):
        class CancellableOrchestrator:
            started = threading.Event()

            def __init__(self, *_args, **_kwargs):
                pass

            def run(self, _prompt, _provider, _model, _reasoning, task_id=None, control=None, **_kwargs):
                type(self).started.set()
                control.cancel_requested.wait(timeout=1)
                return OrchestrationResult(False, task_id, cancelled=True)

        with tempfile.TemporaryDirectory() as directory:
            coordinator = TaskCoordinator(
                Path(directory),
                object(),
                OrchestrationSettings(max_concurrent_tasks=1, shutdown_grace_seconds=0.5),
            )
            with patch("tui.task_coordinator.LocalOrchestrator", CancellableOrchestrator):
                record = coordinator.submit("stop", "codex", "luna", "medium")
                self.assertTrue(CancellableOrchestrator.started.wait(timeout=1))
                self.assertTrue(coordinator.shutdown())

            self.assertTrue(record.future.done())

    def test_failed_task_does_not_block_later_task(self):
        class FailingOrchestrator(FakeOrchestrator):
            def run(self, prompt, provider, model, reasoning, task_id=None, submission_sequence=0, mode="coding", control=None, existing_context=None, resume_notes=()):
                if prompt == "bad":
                    self.on_event("failed", "Task failed but worktree is preserved.", "error")
                    return OrchestrationResult(False, task_id, f"agent/task-{task_id}", Path(f"/tmp/{task_id}"), "preserved")
                return OrchestrationResult(True, task_id, f"agent/task-{task_id}", Path(f"/tmp/{task_id}"))

        with tempfile.TemporaryDirectory() as directory:
            coordinator = TaskCoordinator(Path(directory), object(), OrchestrationSettings(max_concurrent_tasks=2))
            with patch("tui.task_coordinator.LocalOrchestrator", FailingOrchestrator):
                failed = coordinator.submit("bad", "codex", "luna", "medium")
                succeeded = coordinator.submit("good", "codex", "terra", "high")
                failed.future.result(timeout=5)
                succeeded.future.result(timeout=5)
            self.assertEqual(failed.status, "failed")
            self.assertEqual(failed.error, "Task failed but worktree is preserved.")
            self.assertEqual(succeeded.status, "completed")
            tasks = next(
                item["tasks"]
                for item in json.loads(coordinator.memory.path.read_text(encoding="utf-8"))
                if "tasks" in item
            )
            self.assertEqual(tasks[failed.worktree_path.name]["state"], "failed")
            self.assertEqual(tasks[failed.worktree_path.name]["error"], failed.error)
            coordinator.shutdown()

    def test_persists_task_details_for_failed_and_completed_tasks(self):
        class TokenReportingOrchestrator:
            def __init__(self, *_args, **_kwargs):
                pass

            def run(self, prompt, _provider, _model, _reasoning, task_id=None, **_kwargs):
                if prompt == "bad":
                    return OrchestrationResult(False, task_id, error="failed", tokens_consumed=99)
                return OrchestrationResult(True, task_id, tokens_consumed=42)

        with tempfile.TemporaryDirectory() as directory:
            memory_path = Path(directory) / ".daedalus-memory.json"
            coordinator = TaskCoordinator(
                Path(directory),
                object(),
                OrchestrationSettings(max_concurrent_tasks=2),
                memory_path=memory_path,
            )
            with patch("tui.task_coordinator.LocalOrchestrator", TokenReportingOrchestrator):
                failed = coordinator.submit("bad", "codex", "luna", "medium")
                succeeded = coordinator.submit("good", "codex", "luna", "medium")
                failed.future.result(timeout=5)
                succeeded.future.result(timeout=5)
            coordinator.shutdown()

            self.assertEqual(failed.status, "failed")
            self.assertEqual(succeeded.status, "completed")
            entries = json.loads(memory_path.read_text(encoding="utf-8"))
            tasks = next(entry["tasks"] for entry in entries if "tasks" in entry)
            failed_task = tasks[f"task-{failed.task_id}"]
            succeeded_task = tasks[f"task-{succeeded.task_id}"]
            self.assertEqual(failed_task["state"], "failed")
            self.assertEqual(succeeded_task["state"], "completed")
            self.assertEqual(failed_task["prompt"], "bad")
            self.assertEqual(succeeded_task["prompt"], "good")
            self.assertEqual(
                succeeded_task["timestamp"],
                datetime.fromtimestamp(succeeded.submitted_at, timezone.utc)
                .isoformat()
                .replace("+00:00", "Z"),
            )
            self.assertEqual(
                {key: succeeded_task[key] for key in ("provider", "model", "reasoning", "mode")},
                {"provider": "codex", "model": "luna", "reasoning": "medium", "mode": "coding"},
            )
            self.assertEqual(succeeded_task["tokens"], 42)
            self.assertEqual(succeeded_task["project"], str(Path(directory).resolve()))
            self.assertEqual(failed_task["tokens"], 0)
            self.assertEqual(failed_task["project"], str(Path(directory).resolve()))

    def test_failed_agent_can_be_retried_with_the_same_request(self):
        class RetryOrchestrator:
            calls = []
            attempts = 0

            def __init__(self, _repository, _runner, _settings, on_event, integration_gate=None):
                self.on_event = on_event

            def run(self, prompt, _provider, _model, _reasoning, task_id=None, resume_notes=(), **_kwargs):
                type(self).calls.append((prompt, resume_notes))
                type(self).attempts += 1
                if type(self).attempts == 1:
                    self.on_event("agent", "I was inspecting the existing implementation.", "message")
                    return OrchestrationResult(False, task_id, error="Agent timed out; retry later.")
                return OrchestrationResult(True, task_id, awaiting_plan=True)

        with tempfile.TemporaryDirectory() as directory:
            coordinator = TaskCoordinator(Path(directory), object(), OrchestrationSettings(max_concurrent_tasks=1))
            with patch("tui.task_coordinator.LocalOrchestrator", RetryOrchestrator):
                record = coordinator.submit("retryable plan", "codex", "luna", "medium", mode="plan")
                record.future.result(timeout=5)
                self.assertEqual(record.status, "failed")
                self.assertIn("timed out", record.error)

                self.assertTrue(coordinator.retry(record.task_id))
                record.future.result(timeout=5)

            self.assertEqual(record.status, "questioning")
            self.assertEqual(RetryOrchestrator.calls[0], ("retryable plan", ()))
            self.assertEqual(RetryOrchestrator.calls[1][0], "retryable plan")
            self.assertEqual(
                RetryOrchestrator.calls[1][1],
                ("Previous visible AI output from the failed attempt:\n"
                 "I was inspecting the existing implementation.",),
            )
            coordinator.shutdown()

    def test_repeated_retries_replace_previous_output_context_instead_of_duplicating_it(self):
        class RetryOrchestrator:
            attempts = 0
            resume_notes = []

            def __init__(self, _repository, _runner, _settings, on_event, integration_gate=None):
                self.on_event = on_event

            def run(self, _prompt, _provider, _model, _reasoning, task_id=None, resume_notes=(), **_kwargs):
                type(self).resume_notes.append(resume_notes)
                type(self).attempts += 1
                self.on_event("agent", f"Attempt {type(self).attempts} output.", "message")
                if type(self).attempts < 3:
                    return OrchestrationResult(False, task_id, error="Agent failed; retry later.")
                return OrchestrationResult(True, task_id)

        with tempfile.TemporaryDirectory() as directory:
            coordinator = TaskCoordinator(Path(directory), object(), OrchestrationSettings(max_concurrent_tasks=1))
            with patch("tui.task_coordinator.LocalOrchestrator", RetryOrchestrator):
                record = coordinator.submit("retry this", "codex", "luna", "medium")
                record.future.result(timeout=5)
                self.assertTrue(coordinator.retry(record.task_id))
                record.future.result(timeout=5)
                self.assertTrue(coordinator.retry(record.task_id))
                record.future.result(timeout=5)

            self.assertEqual(RetryOrchestrator.resume_notes[0], ())
            self.assertEqual(
                RetryOrchestrator.resume_notes[1],
                ("Previous visible AI output from the failed attempt:\nAttempt 1 output.",),
            )
            self.assertEqual(
                RetryOrchestrator.resume_notes[2],
                ("Previous visible AI output from the failed attempt:\n"
                 "Attempt 1 output.\n\nAttempt 2 output.",),
            )
            coordinator.shutdown()

    def test_persists_null_model_and_reasoning_for_cursor_task(self):
        class CursorOrchestrator:
            def __init__(self, *_args, **_kwargs):
                pass

            def run(self, prompt, _provider, _model, _reasoning, task_id=None, **_kwargs):
                return OrchestrationResult(True, task_id, tokens_consumed=17)

        with tempfile.TemporaryDirectory() as directory:
            memory_path = Path(directory) / ".daedalus-memory.json"
            coordinator = TaskCoordinator(
                Path(directory),
                object(),
                OrchestrationSettings(max_concurrent_tasks=1),
                memory_path=memory_path,
            )
            with patch("tui.task_coordinator.LocalOrchestrator", CursorOrchestrator):
                record = coordinator.submit("cursor task", "cursor", "cursor", "")
                record.future.result(timeout=5)
            coordinator.shutdown()

            entries = json.loads(memory_path.read_text(encoding="utf-8"))
            tasks = next(entry["tasks"] for entry in entries if "tasks" in entry)
            self.assertEqual(
                tasks[f"task-{record.task_id}"],
                {
                    "timestamp": datetime.fromtimestamp(record.submitted_at, timezone.utc)
                        .isoformat()
                        .replace("+00:00", "Z"),
                    "prompt": "cursor task",
                    "provider": "cursor",
                    "model": None,
                    "reasoning": None,
                    "mode": "coding",
                    "state": "completed",
                    "outputs": [],
                    "error": None,
                    "tokens": 17,
                    "project": str(Path(directory).resolve()),
                },
            )

    def test_pause_preserves_context_and_resume_reuses_same_worktree(self):
        class PausableOrchestrator:
            started = threading.Event()
            calls = []

            def __init__(self, repository, _runner, _settings, _on_event, integration_gate=None):
                self.repository = repository

            def run(self, prompt, provider, model, reasoning, task_id=None, submission_sequence=0, mode="coding", control=None, existing_context=None, resume_notes=()):
                type(self).calls.append((existing_context, resume_notes))
                type(self).started.set()
                context = existing_context or WorktreeContext(
                    self.repository,
                    task_id,
                    "base",
                    f"agent/task-{task_id}",
                    self.repository / "worktree",
                )
                if existing_context is None:
                    control.pause_requested.wait(timeout=2)
                    return OrchestrationResult(False, task_id, context.branch_name, context.path, context=context, paused=True)
                return OrchestrationResult(True, task_id, context.branch_name, context.path, context=context)

        with tempfile.TemporaryDirectory() as directory:
            coordinator = TaskCoordinator(Path(directory), object(), OrchestrationSettings(max_concurrent_tasks=1))
            with patch("tui.task_coordinator.LocalOrchestrator", PausableOrchestrator):
                record = coordinator.submit("continue", "codex", "luna", "medium")
                self.assertTrue(PausableOrchestrator.started.wait(timeout=2))
                self.assertTrue(coordinator.pause(record.task_id))
                record.future.result(timeout=5)
                self.assertEqual(record.status, "paused")
                preserved_context = record.context
                self.assertIsNotNone(preserved_context)

                PausableOrchestrator.started.clear()
                self.assertTrue(coordinator.resume(record.task_id, "The API already exists here."))
                record.future.result(timeout=5)

            self.assertEqual(record.status, "completed")
            self.assertIs(PausableOrchestrator.calls[1][0], preserved_context)
            self.assertEqual(PausableOrchestrator.calls[1][1], ("The API already exists here.",))
            coordinator.shutdown()

    def test_cancel_paused_task_removes_preserved_worktree(self):
        with tempfile.TemporaryDirectory() as directory:
            coordinator = TaskCoordinator(Path(directory), object(), OrchestrationSettings(max_concurrent_tasks=1))
            record = TaskRecord("paused-task", 1, "pause me", "codex", "luna", "medium", status="paused")
            record.context = WorktreeContext(
                Path(directory), record.task_id, "base", "agent/task-paused", Path(directory) / "worktree"
            )
            with coordinator._lock:
                coordinator._tasks[record.task_id] = record
            with patch("tui.task_coordinator.GitWorktreeManager") as manager_class:
                self.assertTrue(coordinator.cancel(record.task_id))
                manager_class.return_value.remove_cancelled.assert_called_once_with(record.context)
            self.assertEqual(record.status, "cancelled")
            coordinator.shutdown()

    def test_plan_answers_require_agent_confirmation_before_implementation(self):
        class PlanOrchestrator:
            responses = [
                '{"plan":"Add the selected store.","questions":[{"id":"q1",'
                '"question":"Which store?","options":[{"id":"a","label":"SQLite"},'
                '{"id":"b","label":"JSON"}]}],"no_more_questions":false}',
                '{"plan":"Add the JSON store.","questions":[],"no_more_questions":true}',
                "Implemented the approved plan.",
            ]
            prompts = []

            def __init__(self, _repository, _runner, _settings, on_event, integration_gate=None):
                self.on_event = on_event

            def run(self, prompt, _provider, _model, _reasoning, task_id=None, **_kwargs):
                type(self).prompts.append(prompt)
                response = type(self).responses.pop(0)
                self.on_event("agent", response, "message")
                return OrchestrationResult(True, task_id)

        with tempfile.TemporaryDirectory() as directory:
            coordinator = TaskCoordinator(Path(directory), object(), OrchestrationSettings(max_concurrent_tasks=1))
            with patch("tui.task_coordinator.LocalOrchestrator", PlanOrchestrator):
                plan_record = coordinator.submit("Choose a store", "codex", "luna", "medium", mode="plan")
                plan_record.future.result(timeout=5)

                self.assertEqual(plan_record.status, "awaiting_answers")
                self.assertFalse(plan_record.plan_confirmed)
                self.assertFalse(
                    coordinator.implement_plan(plan_record.task_id)
                )
                self.assertTrue(coordinator.answer_plan(plan_record.task_id, {"q1": "b"}))
                plan_record.future.result(timeout=5)

                self.assertTrue(plan_record.plan_confirmed)
                self.assertEqual(plan_record.plan_questions, ())
                persisted = coordinator.memory.get_tasks()[plan_record.memory_task_id]
                self.assertEqual(persisted["prompt_history"][0], "Choose a store")
                self.assertIn("User answers:", persisted["prompt_history"][1])
                coding_record = coordinator.implement_plan(plan_record.task_id)
                self.assertIsNotNone(coding_record)
                coding_record.future.result(timeout=5)
                self.assertTrue(plan_record.plan_implemented)
                self.assertIsNone(coordinator.implement_plan(plan_record.task_id))

            self.assertEqual(coding_record.mode, "coding")
            self.assertIn("Add the JSON store", coding_record.prompt)
            self.assertIn("Original user request", coding_record.prompt)
            self.assertIn("q1: b (Which store?: JSON)", coding_record.prompt)
            coordinator.shutdown()

    def test_plan_answers_accept_ui_owned_custom_text(self):
        class PlanOrchestrator:
            prompts = []
            responses = [
                '{"plan":"Choose the store.","questions":[{"id":"q1",'
                '"question":"Which store?","options":[{"id":"a","label":"SQLite"},'
                '{"id":"b","label":"JSON"}]}],"no_more_questions":false}',
                '{"plan":"Use the custom store.","questions":[],"no_more_questions":true}',
            ]

            def __init__(self, _repository, _runner, _settings, on_event, integration_gate=None):
                self.on_event = on_event

            def run(self, prompt, _provider, _model, _reasoning, task_id=None, **_kwargs):
                type(self).prompts.append(prompt)
                self.on_event("agent", type(self).responses.pop(0), "message")
                return OrchestrationResult(True, task_id)

        custom_answer = encode_custom_answer("A user-defined store")
        with tempfile.TemporaryDirectory() as directory:
            coordinator = TaskCoordinator(Path(directory), object(), OrchestrationSettings(max_concurrent_tasks=1))
            with patch("tui.task_coordinator.LocalOrchestrator", PlanOrchestrator):
                record = coordinator.submit("Choose a store", "codex", "luna", "medium", mode="plan")
                record.future.result(timeout=5)

                self.assertTrue(coordinator.answer_plan(record.task_id, {"q1": custom_answer}))
                record.future.result(timeout=5)

            self.assertTrue(record.plan_confirmed)
            self.assertIn("Custom answer: A user-defined store", PlanOrchestrator.prompts[1])
            self.assertEqual(
                record.plan_answer_details["q1"],
                "Which store?: Custom answer: A user-defined store",
            )
            coordinator.shutdown()

    def test_invalid_confirmation_preserves_answers_for_a_safe_retry(self):
        class PlanOrchestrator:
            responses = [
                '{"plan":"Add the selected store.","questions":[{"id":"q1",'
                '"question":"Which store?","options":[{"id":"a","label":"SQLite"},'
                '{"id":"b","label":"JSON"}]}],"no_more_questions":false}',
                "The final plan is JSON somewhere else.",
                '{"plan":"Add the JSON store.","questions":[],"no_more_questions":true}',
            ]

            def __init__(self, _repository, _runner, _settings, on_event, integration_gate=None):
                self.on_event = on_event

            def run(self, _prompt, _provider, _model, _reasoning, task_id=None, **_kwargs):
                self.on_event("agent", type(self).responses.pop(0), "message")
                return OrchestrationResult(True, task_id)

        with tempfile.TemporaryDirectory() as directory:
            coordinator = TaskCoordinator(Path(directory), object(), OrchestrationSettings(max_concurrent_tasks=1))
            with patch("tui.task_coordinator.LocalOrchestrator", PlanOrchestrator):
                record = coordinator.submit("Choose a store", "codex", "luna", "medium", mode="plan")
                record.future.result(timeout=5)
                self.assertTrue(coordinator.answer_plan(record.task_id, {"q1": "b"}))
                record.future.result(timeout=5)

                self.assertEqual(record.status, "awaiting_answers")
                self.assertEqual(record.plan_text, "Add the selected store.")
                self.assertEqual(record.plan_answers, {"q1": "b"})
                self.assertIn("required format", record.error)

                self.assertTrue(coordinator.answer_plan(record.task_id, {"q1": "b"}))
                record.future.result(timeout=5)

            self.assertTrue(record.plan_confirmed)
            coordinator.shutdown()

    def test_revised_question_drops_only_its_invalid_saved_answer(self):
        class PlanOrchestrator:
            responses = [
                '{"plan":"Choose storage.","questions":[{"id":"q1","question":"Which store?",'
                '"options":[{"id":"a","label":"SQLite"},{"id":"b","label":"JSON"}]}],'
                '"no_more_questions":false}',
                '{"plan":"Choose hosting.","questions":[{"id":"q1","question":"Which host?",'
                '"options":[{"id":"cloud","label":"Cloud"},{"id":"local","label":"Local"}]}],'
                '"no_more_questions":false}',
            ]

            def __init__(self, _repository, _runner, _settings, on_event, integration_gate=None):
                self.on_event = on_event

            def run(self, _prompt, _provider, _model, _reasoning, task_id=None, **_kwargs):
                self.on_event("agent", type(self).responses.pop(0), "message")
                return OrchestrationResult(True, task_id)

        with tempfile.TemporaryDirectory() as directory:
            coordinator = TaskCoordinator(Path(directory), object(), OrchestrationSettings(max_concurrent_tasks=1))
            with patch("tui.task_coordinator.LocalOrchestrator", PlanOrchestrator):
                record = coordinator.submit("Choose deployment", "codex", "luna", "medium", mode="plan")
                record.future.result(timeout=5)
                self.assertTrue(coordinator.answer_plan(record.task_id, {"q1": "b"}))
                record.future.result(timeout=5)

            self.assertEqual(record.status, "awaiting_answers")
            self.assertEqual(record.plan_answers, {})
            coordinator.shutdown()

    def test_implementation_discards_the_clean_planning_worktree(self):
        with tempfile.TemporaryDirectory() as directory:
            coordinator = TaskCoordinator(Path(directory), object(), OrchestrationSettings(max_concurrent_tasks=1))
            record = TaskRecord("plan-task", 1, "Plan it", "codex", "luna", "medium", mode="plan")
            record.status = "completed"
            record.plan_confirmed = True
            record.context = WorktreeContext(
                Path(directory), record.task_id, "base", "agent/task-plan-task", Path(directory) / "plan-worktree"
            )
            record.worktree_path = record.context.path
            with coordinator._lock:
                coordinator._tasks[record.task_id] = record
            with patch("tui.task_coordinator.GitWorktreeManager") as manager_class:
                coding_record = coordinator.implement_plan(record.task_id)

            self.assertIsNotNone(coding_record)
            manager_class.return_value.remove_successful.assert_called_once_with(
                WorktreeContext(Path(directory), record.task_id, "base", "agent/task-plan-task", Path(directory) / "plan-worktree")
            )
            self.assertIsNone(record.context)
            self.assertIsNone(record.worktree_path)
            coordinator.shutdown()


if __name__ == "__main__":
    unittest.main()
