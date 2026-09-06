#!/usr/bin/env python3
"""Render a top-down HTML call tree for the current working directory project."""

from __future__ import annotations

import sys
import tomllib
from pathlib import Path


SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from tui.call_graph_tree import CallGraphConfig, render_call_graph_tree


PARAMETER_FILENAME = "daedalus-tui-call-graph-visualization.toml"

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
    "similarity_display_low": 0.25,
    "similarity_display_high": 0.55,
    "similarity_tint_siblings": False,
    "write_similarity_json": True,
}


def load_config(project_root: Path) -> CallGraphConfig:
    parameter_path = project_root / "parameter_files" / PARAMETER_FILENAME
    values = CONFIG
    if parameter_path.is_file():
        with parameter_path.open("rb") as source:
            values = {**CONFIG, **tomllib.load(source)}

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
        similarity_display_low=float(values.get("similarity_display_low", 0.25)),
        similarity_display_high=float(values.get("similarity_display_high", 0.55)),
        similarity_tint_siblings=bool(values.get("similarity_tint_siblings", False)),
        write_similarity_json=bool(values.get("write_similarity_json", True)),
    )


def main() -> None:
    project_root = Path.cwd().resolve()
    config = load_config(project_root)
    output_path = render_call_graph_tree(project_root, config)
    print(output_path)


if __name__ == "__main__":
    main()
