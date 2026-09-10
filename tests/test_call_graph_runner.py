import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


RUNNER_PATH = Path(__file__).resolve().parents[1] / "scripts" / "render_call_graph_tree.py"


def load_runner_module():
    spec = importlib.util.spec_from_file_location("render_call_graph_tree_runner", RUNNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {RUNNER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


RUNNER = load_runner_module()


class CallGraphRunnerTests(unittest.TestCase):
    def test_lotus_and_medley_profiles_discover_recursive_python_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            lotus = RUNNER.load_config(root, "lotus")
            medley = RUNNER.load_config(root, "medley")

            self.assertEqual(lotus.source_globs, ["**/*.py"])
            self.assertEqual(medley.source_globs, ["**/*.py"])
            self.assertIn("tests/**", lotus.exclude)
            self.assertIn("vendor/**", medley.exclude)
            self.assertEqual(lotus.entry_points, [])
            self.assertEqual(medley.entry_points, [])

    def test_external_current_project_keeps_generic_defaults_without_local_config(self):
        with tempfile.TemporaryDirectory() as directory:
            config = RUNNER.load_config(Path(directory), "current")

            self.assertEqual(config.source_globs, ["src/**/*.py"])

    def test_target_local_parameters_override_named_profile(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            parameter_directory = root / "parameter_files"
            parameter_directory.mkdir()
            (parameter_directory / RUNNER.PARAMETER_FILENAME).write_text(
                'source_globs = ["medley/**/*.py"]\n'
                'exclude = ["generated/**"]\n'
                'entry_points = ["medley.app.main"]\n'
                "max_tree_depth = 7\n",
                encoding="utf-8",
            )

            config = RUNNER.load_config(root, "medley")

            self.assertEqual(config.source_globs, ["medley/**/*.py"])
            self.assertEqual(config.exclude, ["generated/**"])
            self.assertEqual(config.entry_points, ["medley.app.main"])
            self.assertEqual(config.max_tree_depth, 7)

    def test_resolve_project_root_supports_current_and_rejects_unknown_names(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(RUNNER.resolve_project_root("current", working_directory=root), root)

        with self.assertRaisesRegex(ValueError, "Unknown ANALYSIS_PROJECT"):
            RUNNER.resolve_project_root("unknown")


if __name__ == "__main__":
    unittest.main()
