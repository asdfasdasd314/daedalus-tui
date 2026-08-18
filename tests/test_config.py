import tempfile
import unittest
from pathlib import Path

from tui.config import load_coding_statistics_settings, load_orchestration_settings, load_tui_settings


class ConfigTests(unittest.TestCase):
    def test_loads_all_provider_and_orchestration_settings(self):
        root = Path(__file__).resolve().parents[1]
        settings = load_tui_settings(root / "parameter_files" / "daedalus-tui.toml")
        orchestration = load_orchestration_settings(root / "parameter_files" / "daedalus-tui-orchestration.toml")

        self.assertEqual(settings.default_model, "gpt-5.6-luna")
        self.assertEqual(settings.default_reasoning, "high")
        self.assertEqual([item.value for item in settings.codex_models], [
            "gpt-5.6-luna", "gpt-5.6-terra", "gpt-5.6-sol",
        ])
        self.assertEqual([item.value for item in settings.codex_reasoning], [
            "light", "medium", "high", "extra-high",
        ])
        self.assertEqual([item.value for item in settings.modes], ["coding", "ask", "plan"])
        self.assertEqual(orchestration.primary_branch, "main")
        self.assertEqual(orchestration.resolver_attempt_limit, 3)
        self.assertEqual(orchestration.max_concurrent_tasks, 4)
        self.assertEqual(orchestration.agent_timeout_seconds, 450)
        self.assertTrue(orchestration.graphify_update_enabled)
        self.assertEqual(orchestration.graphify_executable, "graphify")

    def test_loads_coding_statistics_forecast_settings(self):
        root = Path(__file__).resolve().parents[1]
        statistics = load_coding_statistics_settings(
            root / "parameter_files" / "daedalus-tui-coding-statistics.toml"
        )

        self.assertEqual(statistics.recent_window_hours, 1)
        self.assertEqual(statistics.forecast_days, 7)
        self.assertEqual(statistics.thirty_day_forecast_days, 30)


if __name__ == "__main__":
    unittest.main()
