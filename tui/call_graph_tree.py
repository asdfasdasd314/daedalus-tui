"""Static call-graph analysis and top-down HTML tree rendering via pyan3."""

from __future__ import annotations

import html
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

from tui.call_graph_similarity import (
    SimilarityResult,
    build_symbol_contexts,
    parent_child_score_map,
    score_band,
    score_relationships,
    similarity_json_path,
    write_similarity_json,
)

if TYPE_CHECKING:
    from pyan.analyzer import CallGraphVisitor


@dataclass(frozen=True)
class CallGraphConfig:
    source_globs: list[str]
    exclude: list[str]
    entry_points: list[str]
    output_path: str
    max_tree_depth: int
    pyan_depth: int
    similarity_enabled: bool = True
    embedding_backend: str = "sklearn-tfidf"
    max_neighbors_in_descriptor: int = 20
    max_sibling_pairs_per_parent: int = 50
    similarity_display_low: float = 0.25
    similarity_display_high: float = 0.55
    similarity_tint_siblings: bool = False
    write_similarity_json: bool = True


@dataclass
class TreeNode:
    name: str
    children: list[TreeNode]
    is_cycle: bool = False


@dataclass
class _LayoutNode:
    node: TreeNode
    x: float
    y: float
    children: list[_LayoutNode]


# Layout and SVG rendering constants (pixels).
_CHAR_WIDTH = 8.4
_H_PADDING = 16
_V_PADDING = 10
_NODE_HEIGHT = 32
_MIN_NODE_WIDTH = 80
_SIBLING_GAP = 40
_LEVEL_GAP = 72
_ROOT_GAP = 64
_SVG_MARGIN = 48
_FONT_SIZE = 14
_EDGE_LABEL_FONT = 11


def discover_source_files(
    project_root: Path,
    source_globs: list[str],
    exclude: list[str],
) -> list[Path]:
    """Collect Python source files matching *source_globs* and not *exclude*."""
    project_root = project_root.resolve()
    discovered: set[Path] = set()

    for pattern in source_globs:
        for path in project_root.glob(pattern):
            if path.is_file() and path.suffix == ".py":
                discovered.add(path.resolve())

    kept: list[Path] = []
    for path in sorted(discovered):
        relative = path.relative_to(project_root).as_posix()
        if any(Path(relative).match(pattern) for pattern in exclude):
            continue
        kept.append(path)
    return kept


def _collect_node_names(visitor: Any) -> set[str]:
    names: set[str] = set()
    for node_list in visitor.nodes.values():
        for node in node_list:
            if node.namespace is not None:
                names.add(node.get_name())
    return names


def _collapse_inner_safe(visitor: Any) -> None:
    """Run pyan's collapse_inner while skipping anonymous nodes pyan cannot parent-resolve."""
    from pyan.anutils import ANON_SCOPE_NAMES

    anon_nodes = [
        node
        for name in list(visitor.nodes)
        if name.partition(".")[0] in ANON_SCOPE_NAMES
        for node in visitor.nodes[name]
    ]
    anon_nodes.sort(key=lambda node: node.get_name().count("."), reverse=True)

    for node in anon_nodes:
        if node.namespace is None:
            node.defined = False
            continue
        parent = visitor.get_parent_node(node)
        if node in visitor.uses_edges:
            for callee in visitor.uses_edges[node]:
                if callee is parent:
                    continue
                visitor.logger.info(
                    "Collapsing inner from %s to %s, uses %s",
                    node,
                    parent,
                    callee,
                )
                visitor.add_uses_edge(parent, callee)
        node.defined = False


class _SafeCallGraphVisitor:
    """CallGraphVisitor with a collapse_inner guard for namespace-less anonymous nodes."""

    @classmethod
    def create(
        cls,
        file_paths: list[str],
        *,
        project_root: Path,
    ) -> CallGraphVisitor:
        from pyan.analyzer import CallGraphVisitor
        from pyan.postprocessor import (
            contract_nonexistents,
            cull_subsumed,
            expand_unknowns,
            resolve_imports,
        )

        class Visitor(CallGraphVisitor):
            def postprocess(self) -> None:
                resolve_imports(self)
                contract_nonexistents(self)
                expand_unknowns(self)
                _collapse_inner_safe(self)
                if self.cull_subsumed_edges:
                    cull_subsumed(self)

        return Visitor(file_paths, root=str(project_root))


def extract_uses_edges(
    file_paths: list[Path],
    project_root: Path,
    pyan_depth: int,
) -> tuple[dict[str, list[str]], set[str]]:
    """Run pyan analysis and return caller→callees edges plus all node names."""
    if not file_paths:
        return {}, set()

    project_root = project_root.resolve()
    visitor = _SafeCallGraphVisitor.create(
        [str(path) for path in file_paths],
        project_root=project_root,
    )
    visitor.filter_by_depth(pyan_depth)

    edges: dict[str, list[str]] = {}
    for from_node, to_nodes in visitor.uses_edges.items():
        if from_node.namespace is None:
            continue
        caller = from_node.get_name()
        callees = sorted(
            to_node.get_name()
            for to_node in to_nodes
            if to_node.namespace is not None
        )
        if callees:
            edges[caller] = callees

    return edges, _collect_node_names(visitor)


def select_roots(
    edges: dict[str, list[str]],
    all_nodes: set[str],
    entry_points: list[str],
) -> list[str]:
    """Choose tree roots from configured entry points or orphan graph nodes."""
    if entry_points:
        roots = [name for name in entry_points if name in all_nodes or name in edges]
        if roots:
            return roots

    incoming: set[str] = set()
    for callees in edges.values():
        incoming.update(callees)

    candidates = (set(edges.keys()) | all_nodes) - incoming
    return sorted(candidates)


def build_tree(
    root: str,
    edges: dict[str, list[str]],
    max_tree_depth: int,
) -> TreeNode:
    """Build a call tree from *root* with cycle and depth limits."""

    def visit(name: str, visited: frozenset[str], depth: int) -> TreeNode:
        if name in visited:
            return TreeNode(name=f"{name} … (cycle)", children=[], is_cycle=True)
        if depth + 1 >= max_tree_depth:
            return TreeNode(name=name, children=[])

        next_visited = visited | {name}
        children = [
            visit(callee, next_visited, depth + 1)
            for callee in edges.get(name, [])
        ]
        return TreeNode(name=name, children=children)

    return visit(root, frozenset(), 0)


def _node_label_width(name: str) -> float:
    return max(len(name) * _CHAR_WIDTH + _H_PADDING * 2, _MIN_NODE_WIDTH)


def _subtree_bounds(layout: _LayoutNode) -> tuple[float, float]:
    """Return the left and right x extents of a laid-out subtree."""
    half = _node_label_width(layout.node.name) / 2.0
    left = layout.x - half
    right = layout.x + half
    for child in layout.children:
        child_left, child_right = _subtree_bounds(child)
        left = min(left, child_left)
        right = max(right, child_right)
    return left, right


def _layout_subtree(node: TreeNode, depth: int) -> _LayoutNode:
    """Assign horizontal positions using subtree widths so labels never overlap."""
    y = float(depth) * _LEVEL_GAP
    if not node.children:
        width = _node_label_width(node.name)
        return _LayoutNode(node=node, x=width / 2.0, y=y, children=[])

    children = [_layout_subtree(child, depth + 1) for child in node.children]
    positioned: list[_LayoutNode] = []
    x_cursor = 0.0
    for child in children:
        child_left, _ = _subtree_bounds(child)
        positioned_child = _translate_layout(child, x_cursor - child_left, 0)
        positioned.append(positioned_child)
        _, child_right = _subtree_bounds(positioned_child)
        x_cursor = child_right + _SIBLING_GAP

    parent_x = (positioned[0].x + positioned[-1].x) / 2.0
    return _LayoutNode(node=node, x=parent_x, y=y, children=positioned)


def _translate_layout(layout: _LayoutNode, dx: float, dy: float = 0.0) -> _LayoutNode:
    return _LayoutNode(
        node=layout.node,
        x=layout.x + dx,
        y=layout.y + dy,
        children=[_translate_layout(child, dx, dy) for child in layout.children],
    )


def _layout_trees(trees: list[TreeNode]) -> list[_LayoutNode]:
    """Lay out each root tree separately, offsetting siblings horizontally."""
    layouts: list[_LayoutNode] = []
    x_offset = 0.0
    for tree in trees:
        layout = _layout_subtree(tree, 0)
        left, right = _subtree_bounds(layout)
        layout = _translate_layout(layout, x_offset - left, 0)
        _, right = _subtree_bounds(layout)
        layouts.append(layout)
        x_offset = right + _ROOT_GAP
    return layouts


def _layout_extent_y(layout: _LayoutNode) -> float:
    max_y = layout.y + _NODE_HEIGHT
    for child in layout.children:
        max_y = max(max_y, _layout_extent_y(child))
    return max_y


def _layouts_bounds(layouts: list[_LayoutNode]) -> tuple[float, float, float, float]:
    if not layouts:
        return 0.0, 0.0, 0.0, 0.0

    min_x = float("inf")
    max_x = float("-inf")
    min_y = float("inf")
    max_y = float("-inf")
    for layout in layouts:
        left, right = _subtree_bounds(layout)
        min_x = min(min_x, left)
        max_x = max(max_x, right)
        min_y = min(min_y, layout.y)
        max_y = max(max_y, _layout_extent_y(layout))
    return min_x, max_x, min_y, max_y


def _canonical_tree_name(name: str) -> str:
    if " … (cycle)" in name:
        return name.split(" … (cycle)", 1)[0]
    return name


def _render_layout_edges(
    layout: _LayoutNode,
    parts: list[str],
    *,
    edge_scores: dict[tuple[str, str], float] | None = None,
    display_low: float = 0.25,
    display_high: float = 0.55,
) -> None:
    parent_bottom_y = layout.y + _NODE_HEIGHT
    parent_x = layout.x
    parent_name = _canonical_tree_name(layout.node.name)
    for child in layout.children:
        child_top_y = child.y
        mid_y = (parent_bottom_y + child_top_y) / 2.0
        child_name = _canonical_tree_name(child.node.name)
        score = None if edge_scores is None else edge_scores.get((parent_name, child_name))
        band = score_band(score, display_low, display_high) if score is not None else "mid"
        class_names = ["edge", f"edge-{band}"] if score is not None else ["edge"]
        parts.append(
            f'<path class="{" ".join(class_names)}" d="M {parent_x:.1f},{parent_bottom_y:.1f} '
            f'V {mid_y:.1f} H {child.x:.1f} V {child_top_y:.1f}"/>'
        )
        if score is not None:
            label_x = (parent_x + child.x) / 2.0
            label = f"{score:.2f}"
            parts.append(
                f'<text class="edge-score edge-score-{band}" '
                f'x="{label_x:.1f}" y="{mid_y - 4:.1f}" '
                f'text-anchor="middle">{html.escape(label)}</text>'
            )
        _render_layout_edges(
            child,
            parts,
            edge_scores=edge_scores,
            display_low=display_low,
            display_high=display_high,
        )


def _render_layout_nodes(
    layout: _LayoutNode,
    parts: list[str],
    *,
    mean_sibling_score: dict[str, float] | None = None,
    tint_siblings: bool = False,
    display_low: float = 0.25,
    display_high: float = 0.55,
) -> None:
    label = html.escape(layout.node.name)
    width = _node_label_width(layout.node.name)
    height = _NODE_HEIGHT
    x = layout.x - width / 2.0
    y = layout.y
    class_names = ["node"]
    if layout.node.is_cycle:
        class_names.append("cycle")
    if tint_siblings and mean_sibling_score is not None:
        canonical = _canonical_tree_name(layout.node.name)
        mean = mean_sibling_score.get(canonical)
        if mean is not None:
            class_names.append(f"sib-{score_band(mean, display_low, display_high)}")
    parts.append(
        f'<g class="{" ".join(class_names)}" transform="translate({x:.1f},{y:.1f})">'
        f'<rect width="{width:.1f}" height="{height:.1f}" rx="6" ry="6"/>'
        f'<text x="{width / 2:.1f}" y="{height / 2:.1f}" '
        f'text-anchor="middle" dominant-baseline="central">{label}</text>'
        f"</g>"
    )
    for child in layout.children:
        _render_layout_nodes(
            child,
            parts,
            mean_sibling_score=mean_sibling_score,
            tint_siblings=tint_siblings,
            display_low=display_low,
            display_high=display_high,
        )


def render_tree_svg(
    trees: list[TreeNode],
    *,
    edge_scores: dict[tuple[str, str], float] | None = None,
    mean_sibling_score: dict[str, float] | None = None,
    tint_siblings: bool = False,
    display_low: float = 0.25,
    display_high: float = 0.55,
) -> str:
    """Render tree nodes as a top-down SVG diagram with connector lines."""
    layouts = _layout_trees(trees)
    if not layouts:
        return ""

    margin = _SVG_MARGIN
    min_x, max_x, min_y, max_y = _layouts_bounds(layouts)
    shifted = [
        _translate_layout(layout, margin - min_x, margin - min_y) for layout in layouts
    ]

    parts: list[str] = []
    for layout in shifted:
        _render_layout_edges(
            layout,
            parts,
            edge_scores=edge_scores,
            display_low=display_low,
            display_high=display_high,
        )
    for layout in shifted:
        _render_layout_nodes(
            layout,
            parts,
            mean_sibling_score=mean_sibling_score,
            tint_siblings=tint_siblings,
            display_low=display_low,
            display_high=display_high,
        )

    content_width = max_x - min_x
    content_height = max_y - min_y
    svg_width = content_width + margin * 2
    svg_height = content_height + margin * 2
    body = "\n  ".join(parts)
    return (
        f'<svg class="call-tree" xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {svg_width:.1f} {svg_height:.1f}" '
        f'width="{svg_width:.1f}" height="{svg_height:.1f}" role="img" '
        f'aria-label="Call graph tree diagram">\n  {body}\n</svg>'
    )


def _histogram_bars(buckets: list[int]) -> str:
    if not buckets:
        return "<p class=\"empty\">No similarity scores.</p>"
    max_count = max(buckets) or 1
    cells: list[str] = []
    for index, count in enumerate(buckets):
        height = max(2, int(round(40 * count / max_count))) if count else 2
        low = index / 10.0
        high = (index + 1) / 10.0
        label = f"{low:.1f}-{high:.1f}"
        cells.append(
            "<div class=\"hist-bar\">"
            f'<div class="hist-fill" style="height:{height}px" title="{count}"></div>'
            f'<span class="hist-label">{label}</span>'
            f'<span class="hist-count">{count}</span>'
            "</div>"
        )
    return '<div class="histogram">' + "".join(cells) + "</div>"


def _render_similarity_panel(
    result: SimilarityResult,
    *,
    display_low: float,
    display_high: float,
) -> str:
    summary = result.summary
    sibling_rows = [
        relation for relation in result.relations if relation.kind == "sibling"
    ]
    sibling_rows.sort(key=lambda item: (-item.score, item.a, item.b))

    table_rows: list[str] = []
    for relation in sibling_rows:
        shared = ", ".join(relation.shared_callers) if relation.shared_callers else "—"
        band = score_band(relation.score, display_low, display_high)
        table_rows.append(
            "<tr>"
            f"<td>{html.escape(relation.a)}</td>"
            f"<td>{html.escape(relation.b)}</td>"
            f"<td>{html.escape(shared)}</td>"
            f'<td class="score score-{band}" data-score="{relation.score:.6f}">'
            f"{relation.score:.3f}</td>"
            "</tr>"
        )
    if not table_rows:
        table_body = '<tr><td colspan="4" class="empty">No sibling pairs scored.</td></tr>'
    else:
        table_body = "\n".join(table_rows)

    mean = summary.get("mean")
    p50 = summary.get("p50")
    p75 = summary.get("p75")
    p90 = summary.get("p90")
    counts_high = sum(
        1 for relation in result.relations if relation.score >= display_high
    )
    counts_low = sum(
        1 for relation in result.relations if relation.score <= display_low
    )

    def fmt(value: Any) -> str:
        if value is None:
            return "—"
        return f"{float(value):.3f}"

    return f"""
  <section class="similarity" aria-label="Edge semantic similarity">
    <h2>Edge semantic similarity</h2>
    <p class="meta">
      Backend {html.escape(result.embedding_backend)};
      cosine of TF-IDF descriptors (name, callers, callees, siblings, docs).
      Display bands: low ≤ {display_low:.2f}, high ≥ {display_high:.2f}.
    </p>
    <div class="legend">
      <span class="swatch low">low</span>
      <span class="swatch mid">mid</span>
      <span class="swatch high">high</span>
      <span>Parent→child scores label SVG edges; siblings are listed below.</span>
    </div>
    <div class="stats">
      <div>relations: {summary.get("count", 0)}</div>
      <div>mean: {fmt(mean)}</div>
      <div>p50: {fmt(p50)}</div>
      <div>p75: {fmt(p75)}</div>
      <div>p90: {fmt(p90)}</div>
      <div>≥ high: {counts_high}</div>
      <div>≤ low: {counts_low}</div>
    </div>
    {_histogram_bars(list(summary.get("histogram_buckets") or []))}
    <h3>Sibling pairs</h3>
    <table class="sibling-table" id="sibling-table">
      <thead>
        <tr>
          <th data-col="0">a</th>
          <th data-col="1">b</th>
          <th data-col="2">shared caller(s)</th>
          <th data-col="3" data-default-sort="desc">score</th>
        </tr>
      </thead>
      <tbody>
        {table_body}
      </tbody>
    </table>
  </section>
  <script>
    (function () {{
      const table = document.getElementById("sibling-table");
      if (!table) return;
      const tbody = table.tBodies[0];
      const headers = table.tHead.rows[0].cells;
      let sortCol = 3;
      let sortAsc = false;
      function cellValue(row, col) {{
        const cell = row.cells[col];
        if (col === 3) {{
          return parseFloat(cell.getAttribute("data-score") || cell.textContent) || 0;
        }}
        return (cell.textContent || "").trim().toLowerCase();
      }}
      function sortBy(col) {{
        if (sortCol === col) {{
          sortAsc = !sortAsc;
        }} else {{
          sortCol = col;
          sortAsc = col !== 3;
        }}
        const rows = Array.from(tbody.rows);
        rows.sort((a, b) => {{
          const va = cellValue(a, col);
          const vb = cellValue(b, col);
          if (va < vb) return sortAsc ? -1 : 1;
          if (va > vb) return sortAsc ? 1 : -1;
          return 0;
        }});
        rows.forEach((row) => tbody.appendChild(row));
      }}
      Array.from(headers).forEach((th) => {{
        th.style.cursor = "pointer";
        th.addEventListener("click", () => sortBy(Number(th.getAttribute("data-col"))));
      }});
    }})();
  </script>
"""


def render_html(
    trees: list[TreeNode],
    project_name: str,
    *,
    generated_at: datetime | None = None,
    empty_message: str | None = None,
    similarity: SimilarityResult | None = None,
    display_low: float = 0.25,
    display_high: float = 0.55,
    tint_siblings: bool = False,
) -> str:
    """Render a self-contained HTML page for the call trees."""
    timestamp = (generated_at or datetime.now(timezone.utc)).strftime("%Y-%m-%d %H:%M:%S UTC")
    title = html.escape(f"Call graph — {project_name}")

    edge_scores = None
    mean_sibling = None
    if similarity is not None:
        edge_scores = parent_child_score_map(similarity.relations)
        mean_sibling = similarity.mean_sibling_score

    if empty_message:
        body = f"<p class=\"empty\">{html.escape(empty_message)}</p>"
    elif trees:
        svg = render_tree_svg(
            trees,
            edge_scores=edge_scores,
            mean_sibling_score=mean_sibling,
            tint_siblings=tint_siblings,
            display_low=display_low,
            display_high=display_high,
        )
        body = f'<div class="diagram">{svg}</div>'
    else:
        body = '<p class="empty">No call graph roots were found.</p>'

    similarity_panel = ""
    if similarity is not None:
        similarity_panel = _render_similarity_panel(
            similarity,
            display_low=display_low,
            display_high=display_high,
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    :root {{
      color-scheme: light dark;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      line-height: 1.4;
    }}
    body {{
      margin: 1.5rem;
    }}
    h1 {{
      font-size: 1.25rem;
      margin: 0 0 0.25rem;
    }}
    h2 {{
      font-size: 1.05rem;
      margin: 1.5rem 0 0.5rem;
    }}
    h3 {{
      font-size: 0.95rem;
      margin: 1rem 0 0.5rem;
    }}
    .meta {{
      color: #666;
      margin: 0 0 1.5rem;
      font-size: 0.9rem;
    }}
    .diagram {{
      overflow: auto;
      max-height: calc(100vh - 6rem);
      border: 1px solid rgba(127, 127, 127, 0.25);
      border-radius: 6px;
      background: Canvas;
    }}
    svg.call-tree {{
      display: block;
    }}
    .edge {{
      fill: none;
      stroke: #999;
      stroke-width: 1.5;
    }}
    .edge-low {{
      stroke: #c45c26;
    }}
    .edge-mid {{
      stroke: #888;
    }}
    .edge-high {{
      stroke: #2a7a4b;
    }}
    .edge-score {{
      font-size: {_EDGE_LABEL_FONT}px;
      fill: CanvasText;
    }}
    .edge-score-low {{ fill: #c45c26; }}
    .edge-score-mid {{ fill: #666; }}
    .edge-score-high {{ fill: #2a7a4b; }}
    .node rect {{
      fill: rgba(127, 127, 127, 0.12);
      stroke: #888;
      stroke-width: 1;
    }}
    .node.sib-low rect {{ stroke: #c45c26; stroke-width: 2; }}
    .node.sib-mid rect {{ stroke: #888; stroke-width: 2; }}
    .node.sib-high rect {{ stroke: #2a7a4b; stroke-width: 2; }}
    .node text {{
      font: inherit;
      font-size: {_FONT_SIZE}px;
      fill: CanvasText;
    }}
    .node.cycle rect {{
      stroke-dasharray: 4 3;
      opacity: 0.9;
    }}
    .node.cycle text {{
      font-style: italic;
      opacity: 0.85;
    }}
    .empty {{
      color: #666;
    }}
    .similarity {{
      margin-top: 1.5rem;
      max-width: 960px;
    }}
    .legend {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem;
      align-items: center;
      margin: 0 0 1rem;
      font-size: 0.85rem;
    }}
    .swatch {{
      padding: 0.1rem 0.45rem;
      border-radius: 4px;
      border: 1px solid rgba(127,127,127,0.35);
    }}
    .swatch.low {{ color: #c45c26; }}
    .swatch.mid {{ color: #666; }}
    .swatch.high {{ color: #2a7a4b; }}
    .stats {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem 1.25rem;
      margin: 0 0 1rem;
      font-size: 0.85rem;
    }}
    .histogram {{
      display: flex;
      gap: 0.35rem;
      align-items: flex-end;
      margin: 0 0 1rem;
      min-height: 70px;
    }}
    .hist-bar {{
      display: flex;
      flex-direction: column;
      align-items: center;
      width: 3.2rem;
      font-size: 0.65rem;
    }}
    .hist-fill {{
      width: 100%;
      background: rgba(42, 122, 75, 0.55);
      border-radius: 2px 2px 0 0;
    }}
    .hist-label, .hist-count {{
      color: #666;
    }}
    .sibling-table {{
      border-collapse: collapse;
      width: 100%;
      font-size: 0.85rem;
    }}
    .sibling-table th, .sibling-table td {{
      border: 1px solid rgba(127,127,127,0.25);
      padding: 0.35rem 0.5rem;
      text-align: left;
      vertical-align: top;
    }}
    .sibling-table th {{
      background: rgba(127,127,127,0.08);
    }}
    .score-low {{ color: #c45c26; }}
    .score-mid {{ color: inherit; }}
    .score-high {{ color: #2a7a4b; font-weight: 600; }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  <p class="meta">Generated {html.escape(timestamp)}</p>
  {body}
  {similarity_panel}
</body>
</html>
"""


def render_call_graph_tree(project_root: Path, config: CallGraphConfig) -> Path:
    """Analyze the project at *project_root* and write the HTML call tree."""
    project_root = project_root.resolve()
    file_paths = discover_source_files(project_root, config.source_globs, config.exclude)
    edges, all_nodes = extract_uses_edges(file_paths, project_root, config.pyan_depth)
    roots = select_roots(edges, all_nodes, config.entry_points)

    similarity: SimilarityResult | None = None
    if config.similarity_enabled and edges:
        contexts = build_symbol_contexts(
            edges,
            all_nodes,
            project_root,
            file_paths=file_paths,
        )
        similarity = score_relationships(
            contexts,
            edges,
            max_neighbors_in_descriptor=config.max_neighbors_in_descriptor,
            max_sibling_pairs_per_parent=config.max_sibling_pairs_per_parent,
        )

    if not file_paths:
        trees: list[TreeNode] = []
        message = "No Python source files matched the configured source_globs."
    elif not roots:
        trees = []
        message = "No call graph roots were found for the configured entry_points."
    else:
        trees = [build_tree(root, edges, config.max_tree_depth) for root in roots]
        message = None

    html_output = render_html(
        trees,
        project_root.name,
        empty_message=message,
        similarity=similarity,
        display_low=config.similarity_display_low,
        display_high=config.similarity_display_high,
        tint_siblings=config.similarity_tint_siblings,
    )
    output_path = (project_root / config.output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_output, encoding="utf-8")

    if similarity is not None and config.write_similarity_json:
        write_similarity_json(similarity_json_path(output_path), similarity)

    return output_path
