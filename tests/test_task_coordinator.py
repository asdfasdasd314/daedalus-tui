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
            coordinator.shutdown()

    def test_persists_tokens_only_after_a_task_completes(self):
        class TokenReportingOrchestrator:
            def __init__(self, *_args, **_kwargs):
                pass

            def run(self, prompt, _provider, _model, _reasoning, task_id=None, **_kwargs):
                if prompt == "bad":
                    return OrchestrationResult(False, task_id, error="failed")
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
            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0]["tokens"], 42)
            self.assertEqual(
                entries[0]["timestamp"],
                datetime.fromtimestamp(succeeded.submitted_at, timezone.utc)
                .isoformat()
                .replace("+00:00", "Z"),
            )
            self.assertEqual(
                {key: entries[0][key] for key in ("provider", "model", "reasoning")},
                {"provider": "codex", "model": "luna", "reasoning": "medium"},
            )

    def test_persists_null_model_and_reasoning_for_cursor_usage(self):
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

            self.assertEqual(
                json.loads(memory_path.read_text(encoding="utf-8")),
                [
                    {
                        "timestamp": datetime.fromtimestamp(record.submitted_at, timezone.utc)
                        .isoformat()
                        .replace("+00:00", "Z"),
                        "tokens": 17,
                        "provider": "cursor",
                        "model": None,
                        "reasoning": None,
                    }
                ],
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


if __name__ == "__main__":
    unittest.main()
