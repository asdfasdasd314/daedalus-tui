import unittest
from pathlib import Path

from tui.call_graph_tree import (
    CallGraphConfig,
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

    def test_render_html_contains_expected_fqns_and_list_nesting(self):
        trees = [build_tree("call_graph_sample.a.alpha", {"call_graph_sample.a.alpha": ["call_graph_sample.b.beta"]}, 4)]
        output = render_html(trees, "sample")
        self.assertIn("call_graph_sample.a.alpha", output)
        self.assertIn("call_graph_sample.b.beta", output)
        self.assertIn('<ul class="tree roots">', output)
        self.assertIn('<ul class="tree">', output)

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

    def test_render_call_graph_tree_writes_html_for_fixture(self):
        config = CallGraphConfig(
            source_globs=["call_graph_sample/**/*.py"],
            exclude=["**/cycle_*.py"],
            entry_points=["call_graph_sample.a.alpha"],
            output_path="call-graph-out/test-call-tree.html",
            max_tree_depth=8,
            pyan_depth=2,
        )
        output = render_call_graph_tree(SAMPLE_PROJECT_ROOT, config)
        self.assertTrue(output.is_file())
        content = output.read_text(encoding="utf-8")
        self.assertIn("call_graph_sample.a.alpha", content)
        self.assertIn("call_graph_sample.c.gamma", content)
        output.unlink()
        output.parent.rmdir()


if __name__ == "__main__":
    unittest.main()
