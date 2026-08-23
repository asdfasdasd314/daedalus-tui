import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, call, patch

from tui.agent_runner import AgentResult
from tui.git_worktree import GitWorktreeError, WorktreeContext
from tui.graphify import GraphifyResult
from tui.orchestrator import LocalOrchestrator, OrchestrationSettings
from tui.verification import VerificationResult


class OrchestratorTests(unittest.TestCase):
    def test_plan_waits_for_questions_and_preserves_worktree(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            runner = Mock()
            runner.run.return_value = AgentResult("codex", 0, "plan", tokens_consumed=12)
            context = WorktreeContext(repository, "task", "base", "agent/task-task", repository / "worktree")
            (context.path / ".agents" / "profiles").mkdir(parents=True)
            (context.path / ".agents" / "profiles" / "planning.md").write_text(
                "PLANNING_PROFILE_FROM_WORKTREE", encoding="utf-8"
            )
            manager = Mock()
            manager.create.return_value = context
            orchestrator = LocalOrchestrator(
                repository,
                runner,
                OrchestrationSettings(),
                lambda _phase, _message, _channel: None,
            )

            with patch("tui.orchestrator.GitWorktreeManager", return_value=manager):
                result = orchestrator.run("Make a plan", "codex", "luna", "high", mode="plan")

        self.assertTrue(result.succeeded)
        self.assertTrue(result.awaiting_plan)
        self.assertEqual(result.tokens_consumed, 12)
        manager.remove_successful.assert_not_called()
        manager.discard_graphify_changes.assert_called_once_with(context.path)
        manager.reset_task_to_base.assert_called_once_with(context)
        self.assertIn("PLANNING_PROFILE_FROM_WORKTREE", runner.run.call_args.args[0].prompt)

    def test_missing_profile_is_reported_without_changing_plan_lifecycle(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            runner = Mock()
            runner.run.return_value = AgentResult("codex", 0, "plan")
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
                result = orchestrator.run("Make a plan", "codex", "luna", "high", mode="plan")

        self.assertTrue(result.succeeded)
        self.assertTrue(result.awaiting_plan)
        self.assertTrue(any(phase == "profile" and channel == "error" for phase, _, channel in events))
        self.assertNotIn(".agents/profiles", runner.run.call_args.args[0].prompt)

    def test_planning_followup_uses_the_planning_profile_through_task_wrapper(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            runner = Mock()
            runner.run.return_value = AgentResult("codex", 0, "updated plan")
            context = WorktreeContext(repository, "task", "base", "agent/task-task", repository / "worktree")
            (context.path / ".agents" / "profiles").mkdir(parents=True)
            (context.path / ".agents" / "profiles" / "planning.md").write_text(
                "PLANNING_PROFILE_FOR_FOLLOWUP", encoding="utf-8"
            )
            manager = Mock()
            orchestrator = LocalOrchestrator(
                repository,
                runner,
                OrchestrationSettings(),
                lambda _phase, _message, _channel: None,
            )

            with patch("tui.orchestrator.GitWorktreeManager", return_value=manager):
                result = orchestrator.run(
                    "Re-evaluate the plan using the user's answers.",
                    "codex",
                    "luna",
                    "high",
                    mode="plan",
                    existing_context=context,
                )

        self.assertTrue(result.succeeded)
        self.assertIn("PLANNING_PROFILE_FOR_FOLLOWUP", runner.run.call_args.args[0].prompt)

    def test_failed_plan_does_not_report_agent_tokens(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            runner = Mock()
            runner.run.return_value = AgentResult("codex", 1, "", "plan failed", tokens_consumed=12)
            context = WorktreeContext(repository, "task", "base", "agent/task-task", repository / "worktree")
            manager = Mock()
            manager.create.return_value = context
            orchestrator = LocalOrchestrator(
                repository,
                runner,
                OrchestrationSettings(),
                lambda _phase, _message, _channel: None,
            )

            with patch("tui.orchestrator.GitWorktreeManager", return_value=manager):
                result = orchestrator.run("Make a plan", "codex", "luna", "high", mode="plan")

        self.assertFalse(result.succeeded)
        self.assertEqual(result.tokens_consumed, 0)

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
            manager.prepare_primary_checkout.return_value = (repository.resolve(), None)
            manager.discard_graphify_changes = Mock()
            with patch(
                "tui.orchestrator.update_repository",
                return_value=GraphifyResult(True, False, "Operation not permitted"),
            ):
                orchestrator.refresh_graphify(manager, "task-1")

        manager.commit_graphify_changes.assert_not_called()
        manager.discard_graphify_changes.assert_called_once_with(repository.resolve())
        manager.cleanup_temporary_checkout.assert_called_once_with(None)
        self.assertTrue(any(phase == "graphify" and "Operation not permitted" in message for phase, message, _ in events))

    def test_successful_graphify_changes_are_committed_after_promotion(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            (repository / "graphify-out").mkdir()
            orchestrator = LocalOrchestrator(repository, Mock(), OrchestrationSettings(), lambda *_: None)
            manager = Mock()
            manager.prepare_primary_checkout.return_value = (repository.resolve(), None)
            manager.commit_graphify_changes.return_value = True
            with patch(
                "tui.orchestrator.update_repository",
                return_value=GraphifyResult(True, True, "updated"),
            ):
                orchestrator.refresh_graphify(manager, "task-1")

        manager.commit_graphify_changes.assert_called_once_with(
            "Daedalus graphify update after task task-1",
            repository.resolve(),
        )
        manager.discard_graphify_changes.assert_not_called()
        manager.cleanup_temporary_checkout.assert_called_once_with(None)

    def test_merge_failure_deploys_resolver_and_retries_verification(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            runner = Mock()
            runner.run.return_value = AgentResult("codex", 0, "done")
            (repository / "worktree" / ".agents" / "profiles").mkdir(parents=True)
            (repository / "worktree" / ".agents" / "profiles" / "coding.md").write_text(
                "CODING_PROFILE_FOR_INITIAL", encoding="utf-8"
            )
            (repository / "worktree" / ".agents" / "profiles" / "integrating.md").write_text(
                "INTEGRATING_PROFILE_FOR_RESOLVER", encoding="utf-8"
            )
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
        manager.stage_changes.assert_called_once_with(context.path)
        stage_call = call.stage_changes(context.path)
        unmerged_call = call.has_unmerged_paths(context.path)
        self.assertLess(manager.method_calls.index(stage_call), manager.method_calls.index(unmerged_call))
        manager.promote.assert_called_once()
        manager.remove_successful.assert_called_once()
        self.assertIn("CODING_PROFILE_FOR_INITIAL", runner.run.call_args_list[0].args[0].prompt)
        self.assertIn("INTEGRATING_PROFILE_FOR_RESOLVER", runner.run.call_args_list[1].args[0].prompt)

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
            context = WorktreeContext(repository, "task", "base", "agent/task-task", repository / "worktree")
            (context.path / ".agents" / "profiles").mkdir(parents=True)
            profile_path = context.path / ".agents" / "profiles" / "coding.md"
            profile_path.write_text(
                "CODING_PROFILE_FOR_INITIAL_AND_REPAIR", encoding="utf-8"
            )

            def run_agent(request, _on_event):
                if "CODING_PROFILE_FOR_INITIAL" in request.prompt:
                    profile_path.write_text("CODING_PROFILE_FOR_REPAIR", encoding="utf-8")
                    return AgentResult("codex", 0, "done", tokens_consumed=10)
                return AgentResult("codex", 0, "repaired", tokens_consumed=5)

            runner.run.side_effect = run_agent
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
        self.assertEqual(result.tokens_consumed, 15)
        self.assertTrue(any(phase == "repairing" for phase, _, _ in events))
        self.assertIn("CODING_PROFILE_FOR_INITIAL_AND_REPAIR", runner.run.call_args_list[0].args[0].prompt)
        self.assertIn("CODING_PROFILE_FOR_REPAIR", runner.run.call_args_list[1].args[0].prompt)

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
