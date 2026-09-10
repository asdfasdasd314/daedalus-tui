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
    def test_any_named_project_uses_recursive_generic_defaults(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            lotus = RUNNER.load_config(root, "lotus")
            another_project = RUNNER.load_config(root, "another-project")

            self.assertEqual(lotus.source_globs, ["**/*.py"])
            self.assertEqual(another_project.source_globs, ["**/*.py"])
            self.assertIn("tests/**", lotus.exclude)
            self.assertIn("vendor/**", another_project.exclude)
            self.assertEqual(lotus.entry_points, [])
            self.assertEqual(another_project.entry_points, [])

    def test_external_current_project_keeps_generic_defaults_without_local_config(self):
        with tempfile.TemporaryDirectory() as directory:
            config = RUNNER.load_config(Path(directory), "current")

            self.assertEqual(config.source_globs, ["**/*.py"])

    def test_target_local_parameters_override_generic_project_defaults(self):
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

    def test_resolve_project_root_supports_current_and_named_projects(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(RUNNER.resolve_project_root("current", working_directory=root), root)

            projects_root = root / "projects"
            named_root = projects_root / "lotus"
            named_root.mkdir(parents=True)
            self.assertEqual(
                RUNNER.resolve_project_root("lotus", projects_root=projects_root),
                named_root.resolve(),
            )

            explicit_root = root / "elsewhere" / "project"
            explicit_root.mkdir(parents=True)
            self.assertEqual(
                RUNNER.resolve_project_root(
                    "custom",
                    projects_root=projects_root,
                    projects={"custom": {"root": str(explicit_root)}},
                ),
                explicit_root.resolve(),
            )


if __name__ == "__main__":
    unittest.main()
