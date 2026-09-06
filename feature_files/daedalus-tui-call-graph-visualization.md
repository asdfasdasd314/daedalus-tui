# Daedalus TUI Call Graph Visualization

## Summary
Standalone tooling that statically analyzes a target Python project with pyan3 and writes a self-contained, top-down HTML call tree for import and feature-boundary workflows. The analyzed project is whichever directory is current when the runner script is invoked. Related call-graph symbols also receive exploratory TF-IDF cosine similarity scores so reviewers can judge whether high similarity tracks cohesive feature neighborhoods.

## Key Points
- **CWD-based target selection**: `cd` into the project to analyze, then run `scripts/render_call_graph_tree.py` from the Daedalus TUI checkout.
- **Parameter-file tunables**: `source_globs`, `exclude`, `entry_points`, `output_path`, `max_tree_depth`, `pyan_depth`, and similarity display/scoring knobs live in `parameter_files/daedalus-tui-call-graph-visualization.toml` when analyzing this repo.
- **Evidence, not intent**: Static analysis misses dynamic dispatch and non-Python code; cycles and partial graphs are expected and marked inline.
- **Custom HTML tree**: pyan supplies edges only; rendering uses an SVG top-down tree diagram with connector lines (not pyan's Graphviz HTML output or a nested file-tree list).
- **Edge semantic similarity**: Each symbol gets a descriptor from terminal symbol names, callers, callees, graph siblings, and docs/comments; sklearn TF-IDF + cosine scores parent→child edges (SVG labels/bands) and sibling pairs (sortable table + optional mean tint), with a JSON sidecar for threshold exploration. Full FQNs remain in graph relations and output metadata, but do not contribute shared module-path tokens to similarity.

## Relevant Files
- `tui/call_graph_tree.py`: Source discovery, pyan analysis, tree building, HTML/SVG rendering, and similarity wiring.
- `tui/call_graph_similarity.py`: Symbol context, descriptor formatting, TF-IDF cosine scoring, and JSON sidecar helpers.
- `scripts/render_call_graph_tree.py`: Runnable entrypoint; loads the parameter file from the target project when present.
- `parameter_files/daedalus-tui-call-graph-visualization.toml`: Tunables for analyzing this TUI repository.
- `tests/test_call_graph_tree.py`: Unit tests against a small fixture package.
- `tests/fixtures/call_graph_sample/`: Minimal package with known call edges, a cycle, and cohesive vs unrelated branches.

## Dev Mode
HACKING

## State Log
- 2026-09-01: Added pyan3-backed call-graph discovery and top-down HTML tree rendering for import workflow evidence gathering.
- 2026-09-01: Repaired verification by lazy-loading pyan3, fixing max_tree_depth traversal semantics, and bootstrapping the test dependency when missing.
- 2026-09-01: Guarded pyan collapse_inner against anonymous nodes with namespace=None so real projects (including this TUI) no longer crash during analysis.
- 2026-09-01: Replaced nested-list file-tree HTML with an SVG top-down tree diagram supporting n-ary branches and multiple roots.
- 2026-09-01: Call-tree HTML now renders at natural pixel size inside a scrollable viewport so nodes stay readable instead of shrinking to fit the page width.
- 2026-09-01: Call-tree layout now spaces siblings by subtree width and uses full-graph bounds with wider side margins so labels no longer overlap or clip at the edges.
- 2026-09-05: Added sklearn TF-IDF cosine similarity for parent/child and sibling relations with SVG edge scores, sibling table/histogram, and JSON sidecar; on the fixture, cohesive order siblings outrank cross-feature UI pairs, but absolute scores cluster mid (~0.33–0.50) so display bands stay exploratory at low 0.25 / high 0.55 pending larger-graph review.
- 2026-09-05: Similarity descriptors now use only terminal symbol names for the subject and graph neighbors, preventing parent/child pairs such as `tui.agent_runner.call` and `tui.agent_runner` from sharing module-path tokens; full FQNs remain relation identifiers.
