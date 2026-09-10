#!/usr/bin/env python3
"""Render a top-down HTML call tree for a manually selected Python project."""

from __future__ import annotations

import sys
import tomllib
from pathlib import Path


SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from tui.call_graph_tree import CallGraphConfig, render_call_graph_tree


PARAMETER_FILENAME = "daedalus-tui-call-graph-visualization.toml"

# Manual, intentionally non-CLI project selection.  ``current`` preserves the
# original behavior; the named projects resolve from the user's Projects
# directory and can be adjusted when a checkout lives elsewhere.
ANALYSIS_PROJECT = "current"
PROJECT_ROOTS: dict[str, Path] = {
    "lotus": Path.home() / "Projects" / "lotus",
    "medley": Path.home() / "Projects" / "medley",
}

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


def resolve_project_root(
    project_name: str,
    *,
    working_directory: Path | None = None,
) -> Path:
    """Resolve ``current`` or one of the manually configured project roots."""
    if project_name == "current":
        return (working_directory or Path.cwd()).resolve()
    try:
        configured_root = PROJECT_ROOTS[project_name]
    except KeyError as error:
        available = ", ".join(["current", *sorted(PROJECT_ROOTS)])
        raise ValueError(
            f"Unknown ANALYSIS_PROJECT {project_name!r}; choose one of: {available}."
        ) from error
    project_root = configured_root.expanduser().resolve()
    if not project_root.is_dir():
        raise FileNotFoundError(
            f"Configured root for {project_name!r} does not exist: {project_root}"
        )
    return project_root


def _flat_parameter_values(values: dict) -> dict:
    """Return runner settings while keeping named profiles out of the flat config."""
    return {key: value for key, value in values.items() if key != "profiles"}


def _load_parameter_values(path: Path) -> dict:
    with path.open("rb") as source:
        return tomllib.load(source)


def load_config(
    project_root: Path,
    profile_name: str = ANALYSIS_PROJECT,
) -> CallGraphConfig:
    """Load defaults, a named project profile, and target-local overrides."""
    parameter_path = project_root / "parameter_files" / PARAMETER_FILENAME
    runner_parameter_path = SCRIPT_ROOT / "parameter_files" / PARAMETER_FILENAME
    runner_parameters = (
        _load_parameter_values(runner_parameter_path)
        if runner_parameter_path.is_file()
        else {}
    )
    # For an arbitrary project selected as ``current``, retain the generic
    # runner defaults unless that project is this checkout.  Otherwise this
    # repository's ``tui/**/*.py`` source glob would hide an external project
    # that has no local parameter file yet.
    use_runner_parameters = (
        profile_name != "current"
        or project_root.resolve() == SCRIPT_ROOT.resolve()
    )
    values = {**CONFIG}
    if use_runner_parameters:
        values.update(_flat_parameter_values(runner_parameters))

    profiles = runner_parameters.get("profiles", {})
    if not isinstance(profiles, dict):
        raise ValueError(f"{runner_parameter_path} profiles must be a table.")
    if profile_name != "current":
        profile = profiles.get(profile_name)
        if not isinstance(profile, dict):
            available = ", ".join(sorted(str(name) for name in profiles)) or "none"
            raise ValueError(
                f"No call-graph profile named {profile_name!r}; available profiles: {available}."
            )
        values.update(profile)

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
    project_root = resolve_project_root(ANALYSIS_PROJECT)
    config = load_config(project_root, ANALYSIS_PROJECT)
    output_path = render_call_graph_tree(project_root, config)
    print(output_path)


if __name__ == "__main__":
    main()
