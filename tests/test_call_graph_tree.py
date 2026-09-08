import json
import unittest
from pathlib import Path

from tui.call_graph_similarity import (
    ScoredRelation,
    SimilarityResult,
    SymbolContext,
    build_symbol_contexts,
    format_descriptor,
    group_candidate_features,
    score_relationships,
    tokenize_descriptor,
    write_similarity_json,
)
from tui.call_graph_tree import (
    CallGraphConfig,
    _layout_trees,
    _subtree_bounds,
    build_tree,
    discover_source_files,
    extract_uses_edges,
    render_call_graph_tree,
    render_html,
    select_roots,
)


FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures"
SAMPLE_ROOT = FIXTURE_ROOT / "call_graph_sample"
SAMPLE_PROJECT_ROOT = FIXTURE_ROOT


class CallGraphTreeTests(unittest.TestCase):
    def test_discover_source_files_respects_exclude_globs(self):
        files = discover_source_files(
            SAMPLE_PROJECT_ROOT,
            source_globs=["call_graph_sample/**/*.py"],
            exclude=["**/cycle_*.py"],
        )
        relative = {path.relative_to(SAMPLE_PROJECT_ROOT).as_posix() for path in files}
        self.assertIn("call_graph_sample/a.py", relative)
        self.assertIn("call_graph_sample/b.py", relative)
        self.assertIn("call_graph_sample/orders.py", relative)
        self.assertIn("call_graph_sample/ui.py", relative)
        self.assertNotIn("call_graph_sample/cycle_a.py", relative)
        self.assertNotIn("call_graph_sample/cycle_b.py", relative)

    def test_extract_uses_edges_contains_expected_pairs(self):
        files = discover_source_files(
            SAMPLE_PROJECT_ROOT,
            source_globs=["call_graph_sample/**/*.py"],
            exclude=["**/cycle_*.py"],
        )
        edges, _ = extract_uses_edges(files, SAMPLE_PROJECT_ROOT, pyan_depth=2)

        self.assertIn("call_graph_sample.a.alpha", edges)
        self.assertIn("call_graph_sample.b.beta", edges["call_graph_sample.a.alpha"])
        self.assertIn("call_graph_sample.c.gamma", edges["call_graph_sample.b.beta"])
        self.assertIn(
            "call_graph_sample.orders.create_order",
            edges["call_graph_sample.a.alpha"],
        )
        self.assertIn(
            "call_graph_sample.ui.manage_ui",
            edges["call_graph_sample.a.alpha"],
        )
        self.assertIn(
            "call_graph_sample.orders.submit_order",
            edges["call_graph_sample.orders.create_order"],
        )
        self.assertIn(
            "call_graph_sample.ui.create_task",
            edges["call_graph_sample.ui.manage_ui"],
        )

    def test_build_tree_marks_cycles_and_respects_max_depth(self):
        edges = {
            "root": ["child"],
            "child": ["root"],
            "leaf": [],
        }
        tree = build_tree("root", edges, max_tree_depth=4)
        self.assertEqual(tree.name, "root")
        self.assertEqual(tree.children[0].name, "child")
        self.assertTrue(tree.children[0].children[0].is_cycle)
        self.assertIn("(cycle)", tree.children[0].children[0].name)

        shallow = build_tree("root", edges, max_tree_depth=1)
        self.assertEqual(shallow.name, "root")
        self.assertEqual(shallow.children, [])

    def test_select_roots_prefers_entry_points(self):
        edges = {"a.fn": ["b.fn"]}
        all_nodes = {"a.fn", "b.fn"}
        roots = select_roots(edges, all_nodes, ["a.fn"])
        self.assertEqual(roots, ["a.fn"])

    def test_select_roots_falls_back_to_orphan_nodes(self):
        edges = {"a.fn": ["b.fn"], "orphan.fn": ["b.fn"]}
        all_nodes = {"a.fn", "b.fn", "orphan.fn"}
        roots = select_roots(edges, all_nodes, [])
        self.assertEqual(roots, ["a.fn", "orphan.fn"])

    def test_render_html_contains_expected_fqns_and_svg_tree(self):
        trees = [
            build_tree(
                "call_graph_sample.a.alpha",
                {"call_graph_sample.a.alpha": ["call_graph_sample.b.beta"]},
                4,
            )
        ]
        output = render_html(trees, "sample")
        self.assertIn("call_graph_sample.a.alpha", output)
        self.assertIn("call_graph_sample.b.beta", output)
        self.assertIn('<svg class="call-tree"', output)
        self.assertIn('class="edge"', output)
        self.assertIn('class="node"', output)
        self.assertNotIn('width="100%"', output)
        self.assertIn("overflow: auto", output)

    def test_layout_keeps_wide_sibling_labels_from_overlapping(self):
        trees = [
            build_tree(
                "root",
                {
                    "root": [
                        "package.module_a.very_long_function_name_one",
                        "package.module_b.very_long_function_name_two",
                    ],
                },
                4,
            )
        ]
        layouts = _layout_trees(trees)
        leaves: list[tuple[float, float]] = []

        def collect_leaves(layout):
            if not layout.children:
                leaves.append(_subtree_bounds(layout))
            for child in layout.children:
                collect_leaves(child)

        for layout in layouts:
            collect_leaves(layout)

        self.assertEqual(len(leaves), 2)
        leaves.sort(key=lambda bounds: bounds[0])
        self.assertGreaterEqual(leaves[1][0], leaves[0][1])

    def test_extract_uses_edges_handles_lambda_scopes_without_namespace(self):
        files = discover_source_files(
            SAMPLE_PROJECT_ROOT,
            source_globs=["call_graph_sample/**/*.py"],
            exclude=["**/cycle_*.py"],
        )
        edges, nodes = extract_uses_edges(files, SAMPLE_PROJECT_ROOT, pyan_depth=2)

        self.assertIn("call_graph_sample.lambda_edge.make_runner", nodes)
        self.assertIn(
            "call_graph_sample.c.gamma",
            edges.get("call_graph_sample.lambda_edge.make_runner", []),
        )

    def test_tokenize_descriptor_splits_identifiers(self):
        tokens = tokenize_descriptor("Symbol pkg.create_order calls save_order.")
        self.assertIn("create_order", tokens)
        self.assertIn("create", tokens)
        self.assertIn("order", tokens)
        self.assertIn("save", tokens)

    def test_format_descriptor_peer_stripping_and_docs(self):
        context = SymbolContext(
            fqn="pkg.create_order",
            short_name="create_order",
            callers=("pkg.alpha",),
            callees=("pkg.submit_order", "pkg.save_order"),
            siblings=("pkg.manage_ui",),
            doc="Create a customer order.",
        )
        full = format_descriptor(context, max_neighbors=20)
        self.assertIn("create_order", full)
        self.assertIn("Calls: submit_order, save_order", full)
        self.assertIn("Docs: Create a customer order.", full)

        stripped = format_descriptor(
            context,
            max_neighbors=20,
            omit={"pkg.submit_order", "pkg.manage_ui"},
        )
        self.assertNotIn("submit_order", stripped)
        self.assertNotIn("manage_ui", stripped)
        self.assertIn("save_order", stripped)

    def test_format_descriptor_uses_only_terminal_symbol_names(self):
        context = SymbolContext(
            fqn="tui.agent_runner.call",
            short_name="call",
            callers=("tui.agent_runner",),
            callees=("tui.agent_runner.run",),
            siblings=("other.agent_runner",),
            doc="",
        )

        descriptor = format_descriptor(context, max_neighbors=20)

        self.assertIn("Symbol call.", descriptor)
        self.assertIn("Calls: run.", descriptor)
        self.assertIn("Called by: agent_runner.", descriptor)
        self.assertIn("Siblings: agent_runner.", descriptor)
        self.assertNotIn("tui.agent_runner.call", descriptor)
        self.assertNotIn("tui.agent_runner.run", descriptor)
        self.assertNotIn("other.agent_runner", descriptor)

    def test_score_relationships_bounds_and_kinds(self):
        edges = {
            "pkg.create_order": ["pkg.submit_order", "pkg.save_order"],
            "pkg.manage_ui": ["pkg.create_task", "pkg.render_panel"],
        }
        contexts = {
            "pkg.create_order": SymbolContext(
                fqn="pkg.create_order",
                short_name="create_order",
                callers=(),
                callees=("pkg.submit_order", "pkg.save_order"),
                siblings=(),
                doc="Create a customer order.",
            ),
            "pkg.submit_order": SymbolContext(
                fqn="pkg.submit_order",
                short_name="submit_order",
                callers=("pkg.create_order",),
                callees=(),
                siblings=("pkg.save_order",),
                doc="Submit order payment.",
            ),
            "pkg.save_order": SymbolContext(
                fqn="pkg.save_order",
                short_name="save_order",
                callers=("pkg.create_order",),
                callees=(),
                siblings=("pkg.submit_order",),
                doc="Save order records.",
            ),
            "pkg.manage_ui": SymbolContext(
                fqn="pkg.manage_ui",
                short_name="manage_ui",
                callers=(),
                callees=("pkg.create_task", "pkg.render_panel"),
                siblings=(),
                doc="Manage the application shell.",
            ),
            "pkg.create_task": SymbolContext(
                fqn="pkg.create_task",
                short_name="create_task",
                callers=("pkg.manage_ui",),
                callees=(),
                siblings=("pkg.render_panel",),
                doc="Create a UI task widget.",
            ),
            "pkg.render_panel": SymbolContext(
                fqn="pkg.render_panel",
                short_name="render_panel",
                callers=("pkg.manage_ui",),
                callees=(),
                siblings=("pkg.create_task",),
                doc="Render a decorative display panel.",
            ),
        }
        result = score_relationships(contexts, edges)
        self.assertTrue(result.relations)
        for relation in result.relations:
            self.assertGreaterEqual(relation.score, 0.0)
            self.assertLessEqual(relation.score, 1.0)
            self.assertIn(relation.kind, {"parent_child", "sibling"})

        by_key = {(r.kind, r.a, r.b): r.score for r in result.relations}
        order_sibling = by_key[("sibling", "pkg.save_order", "pkg.submit_order")]
        ui_parent = by_key[("parent_child", "pkg.manage_ui", "pkg.create_task")]
        order_parent = by_key[("parent_child", "pkg.create_order", "pkg.submit_order")]
        self.assertGreater(order_sibling, 0.0)
        self.assertGreater(order_parent, ui_parent)

    def test_candidate_features_join_fully_qualifying_parent_child_chain(self):
        relations = [
            ScoredRelation("parent_child", "root", "child", 0.55),
            ScoredRelation("parent_child", "child", "grandchild", 0.80),
        ]

        groups = group_candidate_features(relations, threshold=0.55)

        self.assertEqual(
            [group.members for group in groups],
            [("child", "grandchild", "root")],
        )
        self.assertEqual(groups[0].relation_kinds, ("parent_child",))
        self.assertEqual(groups[0].score_stats["count"], 2)

    def test_candidate_features_split_at_below_threshold_edge(self):
        relations = [
            ScoredRelation("parent_child", "a", "b", 0.90),
            ScoredRelation("parent_child", "b", "c", 0.54),
            ScoredRelation("parent_child", "c", "d", 0.90),
        ]

        groups = group_candidate_features(relations, threshold=0.55)

        self.assertEqual(
            [group.members for group in groups],
            [("a", "b"), ("c", "d")],
        )
        self.assertTrue(all(len(group.qualifying_relations) == 1 for group in groups))

    def test_candidate_features_are_empty_when_no_relation_qualifies(self):
        relation = ScoredRelation("parent_child", "a", "b", 0.54)

        self.assertEqual(group_candidate_features([relation], threshold=0.55), [])

    def test_candidate_features_include_qualifying_sibling_pair(self):
        relations = [
            ScoredRelation("parent_child", "root", "left", 0.80),
            ScoredRelation(
                "sibling",
                "left",
                "right",
                0.55,
                shared_callers=("root",),
            ),
        ]

        groups = group_candidate_features(relations, threshold=0.55)

        self.assertEqual(groups[0].members, ("left", "right", "root"))
        self.assertEqual(groups[0].relation_kinds, ("parent_child", "sibling"))
        self.assertEqual(
            [(relation.kind, relation.a, relation.b) for relation in groups[0].relations],
            [("parent_child", "root", "left"), ("sibling", "left", "right")],
        )

    def test_candidate_features_are_deterministic_and_exclude_singletons(self):
        relations = [
            ScoredRelation("parent_child", "z", "z", 1.0),
            ScoredRelation("parent_child", "d", "e", 0.90),
            ScoredRelation("parent_child", "a", "b", 0.90),
        ]

        groups = group_candidate_features(reversed(relations), threshold=0.55)
        repeated = group_candidate_features(relations, threshold=0.55)

        self.assertEqual(
            [group.members for group in groups],
            [("a", "b"), ("d", "e")],
        )
        self.assertEqual(
            [group.feature_id for group in groups],
            [group.feature_id for group in repeated],
        )
        self.assertNotIn("z", {member for group in groups for member in group.members})

    def test_similarity_json_serializes_candidate_features_and_threshold(self):
        relation = ScoredRelation("parent_child", "root", "child", 0.75)
        group = group_candidate_features([relation], threshold=0.55)[0]
        result = SimilarityResult(
            relations=[relation],
            descriptors={"root": "Symbol root.", "child": "Symbol child."},
            mean_sibling_score={},
            summary={"count": 1},
            feature_similarity_threshold=0.55,
            candidate_features=[group],
        )

        with self.subTest("serialization"):
            output_path = SAMPLE_PROJECT_ROOT / "edge-similarities-test.json"
            write_similarity_json(output_path, result)
            try:
                payload = json.loads(output_path.read_text(encoding="utf-8"))
            finally:
                output_path.unlink()

        self.assertEqual(payload["feature_similarity_threshold"], 0.55)
        self.assertEqual(
            payload["feature_grouping_mode"],
            "undirected_qualifying_relations",
        )
        self.assertEqual(payload["descriptors"]["root"], "Symbol root.")
        self.assertEqual(
            payload["candidate_features"][0]["feature_id"],
            group.feature_id,
        )
        self.assertEqual(payload["candidate_features"][0]["members"], ["child", "root"])
        self.assertEqual(payload["candidate_features"][0]["relations"][0]["score"], 0.75)

    def test_candidate_feature_widget_and_svg_annotations(self):
        relation = ScoredRelation("parent_child", "root", "child", 0.75)
        group = group_candidate_features([relation], threshold=0.55)[0]
        result = SimilarityResult(
            relations=[relation],
            summary={"count": 1},
            feature_similarity_threshold=0.55,
            candidate_features=[group],
        )
        tree = build_tree("root", {"root": ["child"]}, 4)

        output = render_html([tree], "sample", similarity=result)

        self.assertIn('aria-label="Candidate features"', output)
        self.assertIn("Candidate features", output)
        self.assertIn(group.feature_id, output)
        self.assertIn("Threshold: 0.55", output)
        self.assertIn(f'data-feature-id="{group.feature_id}"', output)

    def test_similarity_disabled_html_has_no_candidate_feature_widget(self):
        tree = build_tree("root", {"root": ["child"]}, 4)

        output = render_html([tree], "sample", similarity=None)

        self.assertNotIn("Candidate features", output)
        self.assertNotIn("data-feature-id", output)

    def test_build_symbol_contexts_extracts_fixture_docs(self):
        files = discover_source_files(
            SAMPLE_PROJECT_ROOT,
            source_globs=["call_graph_sample/**/*.py"],
            exclude=["**/cycle_*.py"],
        )
        edges, nodes = extract_uses_edges(files, SAMPLE_PROJECT_ROOT, pyan_depth=2)
        contexts = build_symbol_contexts(
            edges,
            nodes,
            SAMPLE_PROJECT_ROOT,
            file_paths=files,
        )
        order_ctx = contexts["call_graph_sample.orders.create_order"]
        self.assertIn("customer order", order_ctx.doc.lower())
        self.assertIn("call_graph_sample.orders.submit_order", order_ctx.callees)
        submit_ctx = contexts["call_graph_sample.orders.submit_order"]
        self.assertIn(
            "call_graph_sample.orders.save_order",
            submit_ctx.siblings,
        )

    def test_render_call_graph_tree_writes_html_scores_and_json(self):
        config = CallGraphConfig(
            source_globs=["call_graph_sample/**/*.py"],
            exclude=["**/cycle_*.py"],
            entry_points=["call_graph_sample.a.alpha"],
            output_path="call-graph-out/test-call-tree.html",
            max_tree_depth=8,
            pyan_depth=2,
            similarity_enabled=True,
            write_similarity_json=True,
            similarity_tint_siblings=True,
            variable_lineage_enabled=True,
            write_variable_lineage_json=True,
        )
        output = render_call_graph_tree(SAMPLE_PROJECT_ROOT, config)
        self.assertTrue(output.is_file())
        content = output.read_text(encoding="utf-8")
        self.assertIn("call_graph_sample.a.alpha", content)
        self.assertIn("call_graph_sample.c.gamma", content)
        self.assertIn("call_graph_sample.orders.create_order", content)
        self.assertIn("Edge semantic similarity", content)
        self.assertIn("sklearn-tfidf", content)
        self.assertIn("sibling-table", content)
        self.assertIn("edge-score", content)
        self.assertIn("histogram", content)
        self.assertRegex(content, r'class="edge edge-(low|mid|high)"')
        self.assertIn("Variable lineage", content)
        self.assertIn("lineage-table", content)
        self.assertIn("lineage-table-scroll", content)
        self.assertIn('aria-label="Variable lineage table"', content)
        self.assertIn("overflow-x: auto", content)

        json_path = output.with_name("edge-similarities.json")
        self.assertTrue(json_path.is_file())
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        self.assertEqual(payload["embedding_backend"], "sklearn-tfidf")
        self.assertIn("summary", payload)
        self.assertIn("relations", payload)
        self.assertTrue(payload["relations"])
        kinds = {item["kind"] for item in payload["relations"]}
        self.assertIn("parent_child", kinds)
        self.assertIn("sibling", kinds)

        lineage_json = output.with_name("variable-lineage.json")
        self.assertTrue(lineage_json.is_file())

        output.unlink()
        json_path.unlink()
        lineage_json.unlink()
        output.parent.rmdir()

    def test_render_html_includes_variable_lineage_when_provided(self):
        from tui.variable_lineage import analyze_sources

        lineage_root = FIXTURE_ROOT / "variable_lineage_sample"
        lineage = analyze_sources(sorted(lineage_root.glob("*.py")), FIXTURE_ROOT)
        tree = build_tree("root", {"root": ["child"]}, 4)
        output = render_html([tree], "sample", variable_lineage=lineage)
        self.assertIn("Variable lineage", output)
        self.assertIn("lineage-table", output)
        self.assertIn('aria-label="Variable lineage"', output)


if __name__ == "__main__":
    unittest.main()
