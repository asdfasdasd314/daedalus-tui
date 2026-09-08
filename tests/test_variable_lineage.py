"""Unit tests for AST variable-lineage analysis."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tui.call_graph_tree import CallGraphConfig, build_tree, render_call_graph_tree, render_html
from tui.variable_lineage import (
    EDGE_ASSIGNED_FROM,
    EDGE_DERIVED_FROM,
    EDGE_MUTATES,
    EDGE_PASSED_TO,
    EDGE_READS,
    EDGE_RETURNED_TO,
    NODE_ATTRIBUTE,
    NODE_VARIABLE,
    analyze_sources,
    make_scoped_id,
    write_variable_lineage_json,
)


FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures"
SAMPLE_ROOT = FIXTURE_ROOT / "variable_lineage_sample"
SAMPLE_PROJECT_ROOT = FIXTURE_ROOT


def _sample_files() -> list[Path]:
    return sorted(SAMPLE_ROOT.glob("*.py"))


class VariableLineageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = analyze_sources(_sample_files(), SAMPLE_PROJECT_ROOT)

    def _edges(self, kind: str) -> set[tuple[str, str]]:
        return {
            (edge.source, edge.target)
            for edge in self.result.edges
            if edge.kind == kind
        }

    def test_scoped_ids_differ_across_functions(self) -> None:
        self.assertIn(
            "variable_lineage_sample.trading.execute_trade::capital",
            self.result.nodes,
        )
        self.assertIn(
            "variable_lineage_sample.trading::capital",
            self.result.nodes,
        )
        self.assertNotEqual(
            "variable_lineage_sample.trading.execute_trade::capital",
            "variable_lineage_sample.trading::capital",
        )

    def test_assignment_lineage_and_derivations(self) -> None:
        derived = self._edges(EDGE_DERIVED_FROM)
        assigned = self._edges(EDGE_ASSIGNED_FROM)
        self.assertIn(
            (
                "variable_lineage_sample.trading.execute_trade::capital",
                "variable_lineage_sample.trading.execute_trade::risk",
            ),
            derived,
        )
        self.assertIn(
            (
                "variable_lineage_sample.trading.execute_trade::risk",
                "variable_lineage_sample.trading.execute_trade::size",
            ),
            derived,
        )
        self.assertIn(
            (
                "variable_lineage_sample.trading.execute_trade::capital",
                "variable_lineage_sample.trading.execute_trade::risk",
            ),
            assigned,
        )

    def test_augassign_mutates_local(self) -> None:
        mutations = self._edges(EDGE_MUTATES)
        self.assertIn(
            (
                "variable_lineage_sample.trading.execute_trade",
                "variable_lineage_sample.trading.execute_trade::amount",
            ),
            mutations,
        )

    def test_attribute_mutate_creates_attribute_node(self) -> None:
        attr_id = "variable_lineage_sample.trading.Portfolio.apply_cost::self.capital"
        self.assertIn(attr_id, self.result.nodes)
        self.assertEqual(self.result.nodes[attr_id].kind, NODE_ATTRIBUTE)
        mutations = self._edges(EDGE_MUTATES)
        self.assertIn(
            ("variable_lineage_sample.trading.Portfolio.apply_cost", attr_id),
            mutations,
        )

    def test_unique_call_param_mapping_and_return(self) -> None:
        passed = self._edges(EDGE_PASSED_TO)
        self.assertIn(
            (
                "variable_lineage_sample.trading::capital",
                "variable_lineage_sample.trading.calculate::x",
            ),
            passed,
        )
        returned = self._edges(EDGE_RETURNED_TO)
        self.assertIn(
            (
                "variable_lineage_sample.trading.calculate::return",
                "variable_lineage_sample.trading.run_pipeline::sized",
            ),
            returned,
        )

    def test_ambiguous_callee_skips_passed_to(self) -> None:
        passed = self._edges(EDGE_PASSED_TO)
        for source, target in passed:
            self.assertNotIn("ambiguous_a.helper::", target)
            self.assertNotIn("ambiguous_b.helper::", target)
        # Calls are still recorded on summaries.
        local_summary = self.result.summaries[
            "variable_lineage_sample.ambiguous_a.run_local"
        ]
        self.assertTrue(
            any(call.get("callee") == "helper" for call in local_summary.calls)
        )

    def test_module_resource_legb_across_functions(self) -> None:
        bankroll = "variable_lineage_sample.module_resource::bankroll"
        self.assertIn(bankroll, self.result.nodes)
        reads = {
            edge.function_id
            for edge in self.result.edges
            if edge.kind == EDGE_READS and edge.target == bankroll
        }
        self.assertIn("variable_lineage_sample.module_resource.allocate", reads)
        self.assertIn("variable_lineage_sample.module_resource.report", reads)
        stats_by_id = {item.node_id: item for item in self.result.stats}
        self.assertGreaterEqual(stats_by_id[bankroll].function_count, 2)

    def test_nested_and_nonlocal_global_mutations(self) -> None:
        total_id = "variable_lineage_sample.scopes.outer::total"
        shared_id = "variable_lineage_sample.scopes::shared"
        mutations = self._edges(EDGE_MUTATES)
        self.assertIn(
            ("variable_lineage_sample.scopes.outer.inner", total_id),
            mutations,
        )
        self.assertIn(
            ("variable_lineage_sample.scopes.bump_shared", shared_id),
            mutations,
        )
        # Free read of shared from inner resolves to module binding.
        reads = self._edges(EDGE_READS)
        self.assertIn(
            ("variable_lineage_sample.scopes.outer.inner", shared_id),
            reads,
        )

    def test_function_summary_shape(self) -> None:
        summary = self.result.summaries[
            "variable_lineage_sample.trading.execute_trade"
        ]
        self.assertEqual(
            summary.parameters,
            [
                "variable_lineage_sample.trading.execute_trade::capital",
                "variable_lineage_sample.trading.execute_trade::price",
            ],
        )
        self.assertIn(
            "variable_lineage_sample.trading.execute_trade::risk",
            summary.definitions,
        )
        self.assertTrue(summary.derivations)
        self.assertIn(
            "variable_lineage_sample.trading.execute_trade::amount",
            summary.mutations,
        )

    def test_stats_sort_and_derived_count_includes_passed_to(self) -> None:
        stats = self.result.stats
        self.assertTrue(stats)
        for earlier, later in zip(stats, stats[1:]):
            self.assertGreaterEqual(
                (
                    earlier.function_count,
                    earlier.derived_count,
                    earlier.mutation_count,
                    earlier.read_count,
                ),
                (
                    later.function_count,
                    later.derived_count,
                    later.mutation_count,
                    later.read_count,
                ),
            )
        capital = "variable_lineage_sample.trading::capital"
        stats_by_id = {item.node_id: item for item in stats}
        self.assertIn(capital, stats_by_id)
        # Module capital derives risk_budget and is PASSED_TO calculate::x / execute_trade::capital.
        self.assertGreaterEqual(stats_by_id[capital].derived_count, 2)
        self.assertEqual(stats_by_id[capital].kind, NODE_VARIABLE)

    def test_make_scoped_id_helper(self) -> None:
        self.assertEqual(
            make_scoped_id("pkg.mod", "Class.method", "x"),
            "pkg.mod.Class.method::x",
        )
        self.assertEqual(make_scoped_id("pkg.mod", "", "x"), "pkg.mod::x")

    def test_json_sidecar_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "variable-lineage.json"
            write_variable_lineage_json(path, self.result)
            payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertIn("stats", payload)
        self.assertIn("edges", payload)
        self.assertIn("summaries", payload)
        self.assertEqual(payload["summary"]["stats_count"], len(self.result.stats))

    def test_html_panel_renders_variable_lineage_section(self) -> None:
        tree = build_tree("root", {"root": ["child"]}, 4)
        output = render_html(
            [tree],
            "sample",
            variable_lineage=self.result,
            variable_stats_row_limit=50,
        )
        self.assertIn('aria-label="Variable lineage"', output)
        self.assertIn(
            'class="lineage-table-scroll" role="region"',
            output,
        )
        self.assertIn('aria-label="Variable lineage table"', output)
        self.assertIn('tabindex="0"', output)
        self.assertIn("Variable lineage", output)
        self.assertIn("lineage-table", output)
        self.assertIn("overflow-x: auto", output)
        self.assertIn("overflow-y: visible", output)
        self.assertIn("width: max-content", output)
        self.assertIn("min-width: 24rem", output)
        self.assertIn("min-width: 20rem", output)
        self.assertIn("white-space: nowrap", output)
        self.assertIn("word-break: normal", output)
        self.assertIn("variable_lineage_sample.trading::capital", output)
        self.assertIn(
            "variable_lineage_sample.trading.Portfolio.apply_cost::self.capital",
            output,
        )

    def test_render_call_graph_tree_writes_lineage_json(self) -> None:
        config = CallGraphConfig(
            source_globs=["variable_lineage_sample/**/*.py"],
            exclude=[],
            entry_points=[],
            output_path="call-graph-out/lineage-test-call-tree.html",
            max_tree_depth=4,
            pyan_depth=2,
            similarity_enabled=False,
            write_similarity_json=False,
            variable_lineage_enabled=True,
            write_variable_lineage_json=True,
        )
        output = render_call_graph_tree(SAMPLE_PROJECT_ROOT, config)
        try:
            content = output.read_text(encoding="utf-8")
            self.assertIn("Variable lineage", content)
            json_path = output.with_name("variable-lineage.json")
            self.assertTrue(json_path.is_file())
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertTrue(payload["stats"])
        finally:
            for path in (output, output.with_name("variable-lineage.json")):
                if path.is_file():
                    path.unlink()
            if output.parent.is_dir() and not any(output.parent.iterdir()):
                output.parent.rmdir()


if __name__ == "__main__":
    unittest.main()
