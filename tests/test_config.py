import tempfile
import unittest
from pathlib import Path

from tui.config import LayoutSettings, load_coding_statistics_settings, load_orchestration_settings, load_tui_settings


class ConfigTests(unittest.TestCase):
    def test_loads_all_provider_and_orchestration_settings(self):
        root = Path(__file__).resolve().parents[1]
        settings = load_tui_settings(root / "parameter_files" / "daedalus-tui.toml")
        orchestration = load_orchestration_settings(root / "parameter_files" / "daedalus-tui-orchestration.toml")

        self.assertEqual(settings.default_model, "gpt-6-astra")
        self.assertEqual(settings.default_reasoning, "high")
        self.assertEqual([item.value for item in settings.codex_models], [
            "gpt-6-astra", "gpt-5.6-luna", "gpt-5.6-terra", "gpt-5.6-sol",
        ])
        self.assertEqual([item.value for item in settings.codex_reasoning], [
            "light", "medium", "high", "extra-high",
        ])
        self.assertEqual([item.value for item in settings.modes], ["coding", "ask", "plan"])
        self.assertEqual(settings.output_width, "95%")
        self.assertEqual(settings.task_inbox_widths, (1, 9, 14, 7))
        self.assertEqual(settings.layout, LayoutSettings(100, 32, 8, 4))
        self.assertEqual(orchestration.primary_branch, "main")
        self.assertEqual(orchestration.resolver_attempt_limit, 3)
        self.assertEqual(orchestration.max_concurrent_tasks, 4)
        self.assertEqual(orchestration.agent_timeout_seconds, 450)
        self.assertTrue(orchestration.graphify_update_enabled)
        self.assertEqual(orchestration.graphify_executable, "graphify")
        self.assertTrue(orchestration.supabase_db_push_enabled)
        self.assertEqual(orchestration.supabase_executable, "supabase")
        self.assertTrue(orchestration.firebase_deploy_enabled)
        self.assertEqual(orchestration.firebase_executable, "firebase")

    def test_loads_claude_provider_models_effort_and_permission_mode(self):
        root = Path(__file__).resolve().parents[1]
        settings = load_tui_settings(root / "parameter_files" / "daedalus-tui.toml")

        self.assertIn("claude", [item.value for item in settings.providers])
        self.assertEqual(
            [item.value for item in settings.claude_models],
            ["claude-opus-5", "claude-sonnet-5", "claude-fable-5-1", "claude-haiku-4-5-20251001"],
        )
        # Claude Code exposes an effort level Codex has no equivalent for.
        self.assertIn("max", [item.value for item in settings.claude_reasoning])
        self.assertEqual(settings.claude.permission_mode, "acceptEdits")

    def test_provider_cascade_falls_back_to_a_legal_model_and_effort(self):
        root = Path(__file__).resolve().parents[1]
        settings = load_tui_settings(root / "parameter_files" / "daedalus-tui.toml")

        self.assertEqual(settings.default_model_for("codex"), "gpt-6-astra")
        # The Codex default is not a Claude model, so the first Claude one wins.
        self.assertEqual(settings.default_model_for("claude"), "claude-opus-5")
        self.assertEqual(settings.default_model_for("cursor"), "cursor")
        self.assertEqual(settings.default_reasoning_for("claude"), "high")
        self.assertEqual(settings.default_reasoning_for("cursor"), "")
        self.assertEqual(settings.reasoning_for("cursor"), ())

    def test_account_auth_mode_lists_provider_key_variables_to_strip(self):
        root = Path(__file__).resolve().parents[1]
        settings = load_tui_settings(root / "parameter_files" / "daedalus-tui.toml")

        self.assertTrue(settings.auth.uses_account_login)
        self.assertEqual(
            settings.auth.for_provider("claude").api_key_variables,
            ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"),
        )
        self.assertEqual(
            settings.auth.for_provider("claude").sign_in_command,
            ("claude", "auth", "login"),
        )
        policy = settings.auth.runner_policy()
        self.assertTrue(policy.account_login)
        self.assertEqual(policy.stripped_variables("cursor"), ("CURSOR_API_KEY",))
        self.assertEqual(policy.stripped_variables("codex"), ("OPENAI_API_KEY",))

    def test_api_key_mode_strips_nothing(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "auth.toml"
            path.write_text(
                """
                providers = [{ label = "Codex", value = "codex" }]
                codex_models = [{ label = "Model", value = "model" }]
                codex_reasoning = [{ label = "High", value = "high" }]

                [auth]
                mode = "api-key"

                [auth.codex]
                label = "Codex"
                api_key_variables = ["OPENAI_API_KEY"]
                """,
                encoding="utf-8",
            )
            policy = load_tui_settings(path).auth.runner_policy()

            self.assertFalse(policy.account_login)
            self.assertEqual(policy.stripped_variables("codex"), ())

    def test_rejects_an_unknown_auth_mode(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "auth.toml"
            path.write_text(
                """
                providers = [{ label = "Codex", value = "codex" }]
                codex_models = [{ label = "Model", value = "model" }]
                codex_reasoning = [{ label = "High", value = "high" }]

                [auth]
                mode = "oauth"
                """,
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "auth.mode"):
                load_tui_settings(path)

    def test_rejects_a_claude_provider_without_models(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "claude.toml"
            path.write_text(
                """
                providers = [
                  { label = "Codex", value = "codex" },
                  { label = "Claude Code", value = "claude" },
                ]
                codex_models = [{ label = "Model", value = "model" }]
                codex_reasoning = [{ label = "High", value = "high" }]
                """,
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "claude_models"):
                load_tui_settings(path)

    def test_loads_project_discovery_breadth(self):
        root = Path(__file__).resolve().parents[1]
        settings = load_tui_settings(root / "parameter_files" / "daedalus-tui.toml")

        self.assertTrue(settings.project_discovery.include_git_repositories)
        self.assertFalse(settings.project_discovery.include_all_directories)
        self.assertIn("node_modules", settings.project_discovery.skipped_directory_names)

    def test_loads_target_branch_and_primary_branch_alias(self):
        with tempfile.TemporaryDirectory() as directory:
            target_path = Path(directory) / "target.toml"
            target_path.write_text('target_branch = "develop"\nverification_commands = []\n', encoding="utf-8")
            alias_path = Path(directory) / "alias.toml"
            alias_path.write_text('primary_branch = "release"\nverification_commands = []\n', encoding="utf-8")

            self.assertEqual(load_orchestration_settings(target_path).primary_branch, "develop")
            self.assertEqual(load_orchestration_settings(alias_path).primary_branch, "release")

    def test_loads_coding_statistics_forecast_settings(self):
        root = Path(__file__).resolve().parents[1]
        statistics = load_coding_statistics_settings(
            root / "parameter_files" / "daedalus-tui-coding-statistics.toml"
        )

        self.assertEqual(statistics.recent_window_hours, 1)
        self.assertEqual(statistics.forecast_days, 7)
        self.assertEqual(statistics.thirty_day_forecast_days, 30)

    def test_rejects_non_positive_layout_settings(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "layout.toml"
            path.write_text(
                """
                providers = [{ label = "Codex", value = "codex" }]
                codex_models = [{ label = "Model", value = "model" }]
                codex_reasoning = [{ label = "High", value = "high" }]
                [layout]
                compact_width = 0
                """,
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "layout values must be positive"):
                load_tui_settings(path)

    def test_loads_custom_layout_settings(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "layout.toml"
            path.write_text(
                """
                providers = [{ label = "Codex", value = "codex" }]
                codex_models = [{ label = "Model", value = "model" }]
                codex_reasoning = [{ label = "High", value = "high" }]
                [layout]
                compact_width = 88
                wide_control_min_width = 14
                short_height = 24
                compact_task_sidebar_height = 6
                compact_prompt_height = 3
                """,
                encoding="utf-8",
            )

            self.assertEqual(
                load_tui_settings(path).layout,
                LayoutSettings(88, 24, 6, 3, 14),
            )


if __name__ == "__main__":
    unittest.main()
