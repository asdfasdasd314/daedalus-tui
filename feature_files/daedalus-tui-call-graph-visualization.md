# Daedalus TUI Call Graph Visualization

## Summary
Standalone tooling that statically analyzes a target Python project with pyan3 and writes a self-contained, top-down HTML call tree for import and feature-boundary workflows. The analyzed project is whichever directory is current when the runner script is invoked.

## Key Points
- **CWD-based target selection**: `cd` into the project to analyze, then run `scripts/render_call_graph_tree.py` from the Daedalus TUI checkout.
- **Parameter-file tunables**: `source_globs`, `exclude`, `entry_points`, `output_path`, `max_tree_depth`, and `pyan_depth` live in `parameter_files/daedalus-tui-call-graph-visualization.toml` when analyzing this repo.
- **Evidence, not intent**: Static analysis misses dynamic dispatch and non-Python code; cycles and partial graphs are expected and marked inline.
- **Custom HTML tree**: pyan supplies edges only; rendering uses an SVG top-down tree diagram with connector lines (not pyan's Graphviz HTML output or a nested file-tree list).

## Relevant Files
- `tui/call_graph_tree.py`: Source discovery, pyan analysis, tree building, and HTML rendering.
- `scripts/render_call_graph_tree.py`: Runnable entrypoint; loads the parameter file from the target project when present.
- `parameter_files/daedalus-tui-call-graph-visualization.toml`: Tunables for analyzing this TUI repository.
- `tests/test_call_graph_tree.py`: Unit tests against a small fixture package.
- `tests/fixtures/call_graph_sample/`: Minimal package with known call edges and a cycle.

## Dev Mode
HACKING

## State Log
- 2026-09-01: Added pyan3-backed call-graph discovery and top-down HTML tree rendering for import workflow evidence gathering.
- 2026-09-01: Repaired verification by lazy-loading pyan3, fixing max_tree_depth traversal semantics, and bootstrapping the test dependency when missing.
- 2026-09-01: Guarded pyan collapse_inner against anonymous nodes with namespace=None so real projects (including this TUI) no longer crash during analysis.
- 2026-09-01: Replaced nested-list file-tree HTML with an SVG top-down tree diagram supporting n-ary branches and multiple roots.
