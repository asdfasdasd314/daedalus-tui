#!/usr/bin/env python3
"""Render a top-down HTML call tree for a parameter-selected Python project."""

from __future__ import annotations

import sys
import tomllib
from pathlib import Path


SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from tui.call_graph_tree import CallGraphConfig, render_call_graph_tree


PARAMETER_FILENAME = "daedalus-tui-call-graph-visualization.toml"

# Fallbacks keep the imported module useful if the parameter file is absent.
# Normal execution reads the values from parameter_files/ instead.
CONFIG: dict = {
    "source_globs": ["src/**/*.py"],
    "exclude": ["tests/**", "**/test_*.py", ".venv/**"],
    "entry_points": [],
    "output_path": "call-graph-out/call-tree.html",
    "max_tree_depth": 12,
    "pyan_depth": 2,
    "similarity_enabled": True,
    "embedding_backend": "sklearn-tfidf",
    "max_neighbors_in_descriptor": 20,
    "max_sibling_pairs_per_parent": 50,
    "feature_similarity_threshold": 0.55,
    "similarity_display_low": 0.25,
    "similarity_display_high": 0.55,
    "similarity_tint_siblings": False,
    "write_similarity_json": True,
    "variable_lineage_enabled": True,
    "write_variable_lineage_json": True,
    "variable_stats_row_limit": 200,
}

_PROJECT_METADATA_KEYS = frozenset(
    {"analysis_project", "projects_root", "projects", "project_defaults", "profiles"}
)


def load_runner_parameters() -> dict:
    """Load the runner-owned parameter file, if it is available."""
    parameter_path = SCRIPT_ROOT / "parameter_files" / PARAMETER_FILENAME
    return _load_parameter_values(parameter_path) if parameter_path.is_file() else {}


def _project_table(parameters: dict, project_name: str) -> dict:
    """Return optional settings for *project_name* after validating the table."""
    projects = parameters.get("projects", {})
    if not isinstance(projects, dict):
        raise ValueError("The projects parameter must be a TOML table.")
    settings = projects.get(project_name, {})
    if not isinstance(settings, dict):
        raise ValueError(f"Project settings for {project_name!r} must be a TOML table.")
    return settings


def _project_root_setting(parameters: dict) -> str | None:
    projects_root = parameters.get("projects_root")
    if projects_root is None:
        return None
    if not isinstance(projects_root, str) or not projects_root.strip():
        raise ValueError("projects_root must be a non-empty path string.")
    return projects_root


def resolve_project_root(
    project_name: str,
    *,
    working_directory: Path | None = None,
    projects_root: str | Path | None = None,
    projects: dict | None = None,
) -> Path:
    """Resolve ``current`` or a named project from parameterized path rules.

    Named projects use an explicit ``projects.<name>.root`` when provided;
    otherwise they resolve to ``projects_root/<name>``.  This keeps adding a
    sibling checkout a parameter-only operation while still supporting
    projects stored elsewhere.
    """
    working_directory = (working_directory or Path.cwd()).absolute()
    if project_name == "current":
        # Preserve the caller's path spelling.  On macOS, ``resolve()`` turns
        # paths such as /var/folders into /private/var/folders, which makes a
        # supplied working directory compare unequal to the resolved result.
        return working_directory

    settings = (projects or {}).get(project_name, {})
    if not isinstance(settings, dict):
        raise ValueError(f"Project settings for {project_name!r} must be a TOML table.")
    configured_root = settings.get("root")
    if configured_root is None:
        configured_root = (projects_root or Path.home() / "Projects")
        configured_root = Path(configured_root).expanduser() / project_name
    elif not isinstance(configured_root, str) or not configured_root.strip():
        raise ValueError(f"Project root for {project_name!r} must be a non-empty path string.")

    project_root = Path(configured_root).expanduser()
    if not project_root.is_absolute():
        project_root = working_directory / project_root
    project_root = project_root.resolve()
    if not project_root.is_dir():
        raise FileNotFoundError(
            f"Configured root for {project_name!r} does not exist: {project_root}"
        )
    return project_root


def _flat_parameter_values(values: dict) -> dict:
    """Return call-graph settings while keeping routing tables out of config."""
    return {
        key: value
        for key, value in values.items()
        if key not in _PROJECT_METADATA_KEYS and key != "root"
    }


def _load_parameter_values(path: Path) -> dict:
    with path.open("rb") as source:
        return tomllib.load(source)


def load_config(
    project_root: Path,
    project_name: str = "current",
) -> CallGraphConfig:
    """Load runner defaults, project settings, and target-local overrides."""
    parameter_path = project_root / "parameter_files" / PARAMETER_FILENAME
    runner_parameter_path = SCRIPT_ROOT / "parameter_files" / PARAMETER_FILENAME
    runner_parameters = load_runner_parameters()
    project_defaults = runner_parameters.get("project_defaults", {})
    if not isinstance(project_defaults, dict):
        raise ValueError(f"{runner_parameter_path} project_defaults must be a table.")
    project_settings = _project_table(runner_parameters, project_name)

    # For an arbitrary project selected as ``current``, retain the generic
    # project defaults unless that project is this checkout.  Otherwise this
    # repository's ``tui/**/*.py`` source glob would hide an external project
    # that has no local parameter file yet.
    is_runner_checkout = project_root.resolve() == SCRIPT_ROOT.resolve()
    values = {**CONFIG}
    if project_name == "current" and is_runner_checkout:
        values.update(_flat_parameter_values(runner_parameters))
    else:
        values.update(_flat_parameter_values(project_defaults))
        values.update(_flat_parameter_values(project_settings))

        # Keep older parameter files readable while projects migrate from
        # profiles.<name> to projects.<name>.
        projects = runner_parameters.get("projects", {})
        profiles = runner_parameters.get("profiles", {})
        if (
            isinstance(projects, dict)
            and project_name not in projects
            and isinstance(profiles, dict)
        ):
            legacy_profile = profiles.get(project_name)
            if isinstance(legacy_profile, dict):
                values.update(_flat_parameter_values(legacy_profile))

    # A target repository may provide its own flat parameter file.  The
    # runner's file is already included above, so avoid applying it twice when
    # analyzing this checkout itself.
    if parameter_path.is_file() and parameter_path.resolve() != runner_parameter_path.resolve():
        values.update(_flat_parameter_values(_load_parameter_values(parameter_path)))

    return CallGraphConfig(
        source_globs=list(values["source_globs"]),
        exclude=list(values["exclude"]),
        entry_points=list(values.get("entry_points", [])),
        output_path=str(values["output_path"]),
        max_tree_depth=int(values["max_tree_depth"]),
        pyan_depth=int(values["pyan_depth"]),
        similarity_enabled=bool(values.get("similarity_enabled", True)),
        embedding_backend=str(values.get("embedding_backend", "sklearn-tfidf")),
        max_neighbors_in_descriptor=int(values.get("max_neighbors_in_descriptor", 20)),
        max_sibling_pairs_per_parent=int(values.get("max_sibling_pairs_per_parent", 50)),
        feature_similarity_threshold=float(values.get("feature_similarity_threshold", 0.55)),
        similarity_display_low=float(values.get("similarity_display_low", 0.25)),
        similarity_display_high=float(values.get("similarity_display_high", 0.55)),
        similarity_tint_siblings=bool(values.get("similarity_tint_siblings", False)),
        write_similarity_json=bool(values.get("write_similarity_json", True)),
        variable_lineage_enabled=bool(values.get("variable_lineage_enabled", True)),
        write_variable_lineage_json=bool(
            values.get("write_variable_lineage_json", True)
        ),
        variable_stats_row_limit=int(values.get("variable_stats_row_limit", 200)),
    )


def main() -> None:
    runner_parameters = load_runner_parameters()
    analysis_project = runner_parameters.get("analysis_project", "current")
    if not isinstance(analysis_project, str) or not analysis_project.strip():
        raise ValueError("analysis_project must be a non-empty project name.")
    analysis_project = analysis_project.strip()
    projects = runner_parameters.get("projects", {})
    if not isinstance(projects, dict):
        raise ValueError("The projects parameter must be a TOML table.")
    project_root = resolve_project_root(
        analysis_project,
        projects_root=_project_root_setting(runner_parameters),
        projects=projects,
    )
    config = load_config(project_root, analysis_project)
    output_path = render_call_graph_tree(project_root, config)
    print(output_path)


if __name__ == "__main__":
    main()
