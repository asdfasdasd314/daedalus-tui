# Daedalus TUI Call Graph Visualization

## Summary
Standalone tooling that statically analyzes a target Python project with pyan3 and writes a self-contained, top-down HTML call tree for import and feature-boundary workflows. The runner can preserve current-directory analysis or select manually configured Lotus and Medley checkouts. Related call-graph symbols also receive exploratory TF-IDF cosine similarity scores so reviewers can judge whether high similarity tracks cohesive feature neighborhoods. A first-pass AST variable-lineage analysis adds scoped variable/attribute usage stats as additional import evidence for later resource and key-point detection.

## Key Points
- **Manual target selection**: `scripts/render_call_graph_tree.py` uses the `ANALYSIS_PROJECT` variable (`current`, `lotus`, or `medley`) instead of CLI arguments. Lotus and Medley roots default to `~/Projects/{name}` through `PROJECT_ROOTS`; adjust those variables for another checkout layout.
- **Project profiles and overrides**: Lotus and Medley profiles use recursive Python discovery with common generated/dependency/test exclusions. The runner loads these profiles from the TUI parameter file, then lets an analyzed project's own `parameter_files/daedalus-tui-call-graph-visualization.toml` override them when present.
- **Parameter-file tunables**: `source_globs`, `exclude`, `entry_points`, `output_path`, `max_tree_depth`, `pyan_depth`, similarity display/scoring knobs, and variable-lineage toggles (`variable_lineage_enabled`, `write_variable_lineage_json`, `variable_stats_row_limit`) live in `parameter_files/daedalus-tui-call-graph-visualization.toml`. `feature_similarity_threshold` defaults to `0.55` and is inclusive.
- **Evidence, not intent**: Static analysis misses dynamic dispatch and non-Python code; cycles and partial graphs are expected and marked inline.
- **Custom HTML tree**: pyan supplies edges only; rendering uses an SVG top-down tree diagram with connector lines (not pyan's Graphviz HTML output or a nested file-tree list).
- **Edge semantic similarity**: Each symbol gets a descriptor from terminal symbol names, callers, callees, graph siblings, and docs/comments; sklearn TF-IDF + cosine scores parent→child edges (SVG labels/bands) and sibling pairs (sortable table + optional mean tint), with a JSON sidecar for threshold exploration. Full FQNs remain in graph relations and output metadata, but do not contribute shared module-path tokens to similarity.
- **Candidate features**: Every parent→child or sibling relation at or above the inclusive `feature_similarity_threshold` participates in an undirected connected-component grouping. Qualifying chains form one deterministic candidate group, while a below-threshold link breaks connectivity; singleton symbols are excluded. Groups are exposed in JSON and a separate HTML widget, and applicable SVG nodes carry the stable feature ID. Sibling pairs are included subject to `max_sibling_pairs_per_parent`.
- **Variable lineage pass**: An AST `NodeVisitor` collects scoped Name/Attribute nodes (LEGB free-name binding; `global`/`nonlocal` aware), function summaries, and lineage edges (`DERIVED_FROM`, `ASSIGNED_FROM`, `PASSED_TO` when the callee is unique, `RETURNED_TO`, `READS`/`WRITES`/`MUTATES`). Per-variable stats (`function_count`, `read_count`, `mutation_count`, transitive `derived_count`) render in an HTML section after similarity/candidate panels, with a full `variable-lineage.json` sidecar for later resource/key-point detection during import.

## Relevant Files
- `tui/call_graph_tree.py`: Source discovery, pyan analysis, tree building, HTML/SVG rendering, similarity wiring, and variable-lineage panel integration.
- `tui/call_graph_similarity.py`: Symbol context, descriptor formatting, TF-IDF cosine scoring, and JSON sidecar helpers.
- `tui/variable_lineage.py`: AST variable-lineage visitor, graph/stats aggregation, JSON sidecar, and HTML panel renderer.
- `scripts/render_call_graph_tree.py`: Runnable entrypoint; resolves the manually selected target and merges the named profile with target-local parameters.
- `parameter_files/daedalus-tui-call-graph-visualization.toml`: Defaults for this TUI repository plus Lotus and Medley import profiles.
- `tests/test_call_graph_tree.py`: Unit tests against a small fixture package.
- `tests/test_call_graph_runner.py`: Regression tests for named profiles, fallback defaults, target-local overrides, and root selection.
- `tests/test_variable_lineage.py`: Unit tests for scoped IDs, LEGB, edges, summaries, stats, and HTML/JSON output.
- `tests/fixtures/call_graph_sample/`: Minimal package with known call edges, a cycle, and cohesive vs unrelated branches.
- `tests/fixtures/variable_lineage_sample/`: Fixture covering assignment lineage, mutations, unique/ambiguous calls, returns, and scope rules.

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
- 2026-09-06: Added inclusive-threshold candidate-feature grouping over qualifying parent→child and sibling relations, with deterministic JSON/HTML/SVG exposure and stable member-derived IDs.
- 2026-09-07: Added an AST variable-lineage pass that builds scoped Name/Attribute graphs and function summaries, computes function/read/mutation/derived stats, and surfaces them on the call-graph HTML review page with a JSON sidecar for later import resource detection.
- 2026-09-07: Made the variable-lineage stats table horizontally pannable with a focusable labeled scroll region and readable minimum-width node/name columns.
- 2026-09-10: Added manual Lotus and Medley project profiles with configurable roots, recursive Python discovery, common exclusions, and target-local parameter overrides.
- 2026-09-10: Preserved the caller's path spelling when resolving the current project so macOS symlink normalization does not break working-directory comparisons.
