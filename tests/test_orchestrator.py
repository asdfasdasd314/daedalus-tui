import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from tui.agent_runner import AgentResult
from tui.git_worktree import GitWorktreeError, WorktreeContext
from tui.graphify import GraphifyResult
from tui.orchestrator import LocalOrchestrator, OrchestrationSettings
from tui.verification import VerificationResult


class OrchestratorTests(unittest.TestCase):
    def test_graphify_failure_is_reported_without_failing_promotion(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            (repository / "graphify-out").mkdir()
            events = []
            orchestrator = LocalOrchestrator(
                repository,
                Mock(),
                OrchestrationSettings(),
                lambda phase, message, channel="status": events.append((phase, message, channel)),
            )
            manager = Mock()
            manager.discard_graphify_changes = Mock()
            with patch(
                "tui.orchestrator.update_repository",
                return_value=GraphifyResult(True, False, "Operation not permitted"),
            ):
                orchestrator.refresh_graphify(manager, "task-1")

        manager.commit_graphify_changes.assert_not_called()
        manager.discard_graphify_changes.assert_called_once_with(repository.resolve())
        self.assertTrue(any(phase == "graphify" and "Operation not permitted" in message for phase, message, _ in events))

    def test_successful_graphify_changes_are_committed_after_promotion(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            (repository / "graphify-out").mkdir()
            orchestrator = LocalOrchestrator(repository, Mock(), OrchestrationSettings(), lambda *_: None)
            manager = Mock()
            manager.commit_graphify_changes.return_value = True
            with patch(
                "tui.orchestrator.update_repository",
                return_value=GraphifyResult(True, True, "updated"),
            ):
                orchestrator.refresh_graphify(manager, "task-1")

        manager.commit_graphify_changes.assert_called_once_with("Daedalus graphify update after task task-1")
        manager.discard_graphify_changes.assert_not_called()

    def test_merge_failure_deploys_resolver_and_retries_verification(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            runner = Mock()
            runner.run.return_value = AgentResult("codex", 0, "done")
            events = []
            orchestrator = LocalOrchestrator(
                repository,
                runner,
                OrchestrationSettings(verification_commands=(("true",),), resolver_attempt_limit=2),
                lambda phase, message, channel: events.append((phase, message, channel)),
            )
            context = WorktreeContext(repository, "task", "base", "agent/task-task", repository / "worktree")
            manager = Mock()
            manager.create.return_value = context
            manager.head.return_value = "changed"
            manager.has_unmerged_paths.return_value = False
            with (
                patch("tui.orchestrator.GitWorktreeManager", return_value=manager),
                patch("tui.orchestrator.run_verification", side_effect=[VerificationResult(True, ""), VerificationResult(True, ""), VerificationResult(True, "")]),
                patch.object(orchestrator, "integrate", wraps=orchestrator.integrate) as integrate,
            ):
                manager.merge_primary_into_task.side_effect = GitWorktreeError("merge conflict")
                result = orchestrator.run("Build it", "codex", "gpt-5.6-luna", "medium")

        self.assertTrue(result.succeeded)
        self.assertTrue(any(phase == "resolving" for phase, _, _ in events))
        self.assertGreaterEqual(runner.run.call_count, 2)
        integrate.assert_called_once()
        manager.promote.assert_called_once()
        manager.remove_successful.assert_called_once()

    def test_failed_resolver_preserves_worktree(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            runner = Mock()
            runner.run.side_effect = [
                AgentResult("codex", 0, "done"),
                AgentResult("codex", 1, "", "resolver failed"),
            ]
            context = WorktreeContext(repository, "task", "base", "agent/task-task", repository / "worktree")
            manager = Mock()
            manager.create.return_value = context
            manager.head.return_value = "changed"
            manager.merge_primary_into_task.side_effect = GitWorktreeError("merge conflict")
            events = []
            orchestrator = LocalOrchestrator(
                repository,
                runner,
                OrchestrationSettings(verification_commands=(("true",),), resolver_attempt_limit=1),
                lambda phase, message, channel: events.append((phase, message, channel)),
            )
            with patch("tui.orchestrator.GitWorktreeManager", return_value=manager), patch(
                "tui.orchestrator.run_verification", return_value=VerificationResult(True, "")
            ):
                result = orchestrator.run("Build it", "codex", "gpt-5.6-luna", "medium")

        self.assertFalse(result.succeeded)
        self.assertEqual(result.worktree, context.path)
        manager.remove_successful.assert_not_called()
        self.assertTrue(any(phase == "failed" for phase, _, _ in events))

    def test_failed_task_verification_runs_repair_agent(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            runner = Mock()
            runner.run.return_value = AgentResult("codex", 0, "done")
            context = WorktreeContext(repository, "task", "base", "agent/task-task", repository / "worktree")
            manager = Mock()
            manager.create.return_value = context
            manager.head.return_value = "changed"
            events = []
            orchestrator = LocalOrchestrator(
                repository,
                runner,
                OrchestrationSettings(verification_commands=(("true",),), task_verification_attempt_limit=2),
                lambda phase, message, channel: events.append((phase, message, channel)),
            )
            with (
                patch("tui.orchestrator.GitWorktreeManager", return_value=manager),
                patch("tui.orchestrator.run_verification", side_effect=[
                    VerificationResult(False, "tests failed"),
                    VerificationResult(True, ""),
                    VerificationResult(True, ""),
                ]),
            ):
                result = orchestrator.run("Build it", "codex", "gpt-5.6-luna", "medium")

        self.assertTrue(result.succeeded)
        self.assertEqual(runner.run.call_count, 2)
        self.assertTrue(any(phase == "repairing" for phase, _, _ in events))

    def test_cancelled_agent_removes_unintegrated_worktree(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            runner = Mock()
            runner.run.return_value = AgentResult("codex", -15, "", stopped_reason="cancelled")
            context = WorktreeContext(repository, "task", "base", "agent/task-task", repository / "worktree")
            manager = Mock()
            manager.create.return_value = context
            events = []
            orchestrator = LocalOrchestrator(
                repository,
                runner,
                OrchestrationSettings(),
                lambda phase, message, channel: events.append((phase, message, channel)),
            )
            with patch("tui.orchestrator.GitWorktreeManager", return_value=manager):
                from tui.agent_runner import AgentControl
                control = AgentControl()
                control.request_cancel()
                result = orchestrator.run("Build it", "codex", "gpt-5.6-luna", "medium", control=control)

        self.assertFalse(result.succeeded)
        self.assertTrue(result.cancelled)
        manager.remove_cancelled.assert_called_once_with(context)
        self.assertTrue(any(phase == "cancelled" for phase, _, _ in events))


if __name__ == "__main__":
    unittest.main()
