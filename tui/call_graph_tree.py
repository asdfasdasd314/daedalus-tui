"""Static call-graph analysis and top-down HTML tree rendering via pyan3."""

from __future__ import annotations

import html
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

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
_FONT_SIZE = 14


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


def _layout_subtree(node: TreeNode, depth: int, next_x: list[float]) -> _LayoutNode:
    """Assign horizontal positions using leaf-order spacing (tidy top-down tree)."""
    if not node.children:
        x = next_x[0]
        next_x[0] += 1.0
        return _LayoutNode(node=node, x=x, y=float(depth), children=[])

    children = [_layout_subtree(child, depth + 1, next_x) for child in node.children]
    x = (children[0].x + children[-1].x) / 2.0
    return _LayoutNode(node=node, x=x, y=float(depth), children=children)


def _to_pixel_layout(layout: _LayoutNode, x_offset: float) -> _LayoutNode:
    return _LayoutNode(
        node=layout.node,
        x=layout.x * _SIBLING_GAP + x_offset,
        y=layout.y * _LEVEL_GAP,
        children=[_to_pixel_layout(child, x_offset) for child in layout.children],
    )


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
        next_x = [0.0]
        layout = _layout_subtree(tree, 0, next_x)
        if next_x[0] <= 1.0:
            span = _node_label_width(tree.name)
        else:
            span = (next_x[0] - 1.0) * _SIBLING_GAP + _MIN_NODE_WIDTH
        layouts.append(_to_pixel_layout(layout, x_offset))
        x_offset += span + _ROOT_GAP
    return layouts


def _layout_bounds(layouts: list[_LayoutNode]) -> tuple[float, float]:
    min_x = float("inf")
    max_x = float("-inf")
    max_y = 0.0

    def visit(node: _LayoutNode) -> None:
        nonlocal min_x, max_x, max_y
        half = _node_label_width(node.node.name) / 2.0
        min_x = min(min_x, node.x - half)
        max_x = max(max_x, node.x + half)
        max_y = max(max_y, node.y + _NODE_HEIGHT)
        for child in node.children:
            visit(child)

    for layout in layouts:
        visit(layout)

    if not layouts:
        return 0.0, 0.0
    return max_x - min_x, max_y


def _render_layout_edges(layout: _LayoutNode, parts: list[str]) -> None:
    parent_bottom_y = layout.y + _NODE_HEIGHT
    parent_x = layout.x
    for child in layout.children:
        child_top_y = child.y
        mid_y = (parent_bottom_y + child_top_y) / 2.0
        parts.append(
            f'<path class="edge" d="M {parent_x:.1f},{parent_bottom_y:.1f} '
            f'V {mid_y:.1f} H {child.x:.1f} V {child_top_y:.1f}"/>'
        )
        _render_layout_edges(child, parts)


def _render_layout_nodes(layout: _LayoutNode, parts: list[str]) -> None:
    label = html.escape(layout.node.name)
    width = _node_label_width(layout.node.name)
    height = _NODE_HEIGHT
    x = layout.x - width / 2.0
    y = layout.y
    class_names = ["node"]
    if layout.node.is_cycle:
        class_names.append("cycle")
    parts.append(
        f'<g class="{" ".join(class_names)}" transform="translate({x:.1f},{y:.1f})">'
        f'<rect width="{width:.1f}" height="{height:.1f}" rx="6" ry="6"/>'
        f'<text x="{width / 2:.1f}" y="{height / 2:.1f}" '
        f'text-anchor="middle" dominant-baseline="central">{label}</text>'
        f"</g>"
    )
    for child in layout.children:
        _render_layout_nodes(child, parts)


def render_tree_svg(trees: list[TreeNode]) -> str:
    """Render tree nodes as a top-down SVG diagram with connector lines."""
    layouts = _layout_trees(trees)
    if not layouts:
        return ""

    margin = 24.0
    min_x = min(
        layout.x - _node_label_width(layout.node.name) / 2.0 for layout in layouts
    )
    shifted = [
        _translate_layout(layout, margin - min_x, margin) for layout in layouts
    ]

    parts: list[str] = []
    for layout in shifted:
        _render_layout_edges(layout, parts)
    for layout in shifted:
        _render_layout_nodes(layout, parts)

    content_width, content_height = _layout_bounds(shifted)
    svg_width = content_width + margin * 2
    svg_height = content_height + margin * 2
    body = "\n  ".join(parts)
    return (
        f'<svg class="call-tree" xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {svg_width:.1f} {svg_height:.1f}" '
        f'width="{svg_width:.1f}" height="{svg_height:.1f}" role="img" '
        f'aria-label="Call graph tree diagram">\n  {body}\n</svg>'
    )


def render_html(
    trees: list[TreeNode],
    project_name: str,
    *,
    generated_at: datetime | None = None,
    empty_message: str | None = None,
) -> str:
    """Render a self-contained HTML page for the call trees."""
    timestamp = (generated_at or datetime.now(timezone.utc)).strftime("%Y-%m-%d %H:%M:%S UTC")
    title = html.escape(f"Call graph — {project_name}")

    if empty_message:
        body = f"<p class=\"empty\">{html.escape(empty_message)}</p>"
    elif trees:
        body = f'<div class="diagram">{render_tree_svg(trees)}</div>'
    else:
        body = '<p class="empty">No call graph roots were found.</p>'

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
    .node rect {{
      fill: rgba(127, 127, 127, 0.12);
      stroke: #888;
      stroke-width: 1;
    }}
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
  </style>
</head>
<body>
  <h1>{title}</h1>
  <p class="meta">Generated {html.escape(timestamp)}</p>
  {body}
</body>
</html>
"""


def render_call_graph_tree(project_root: Path, config: CallGraphConfig) -> Path:
    """Analyze the project at *project_root* and write the HTML call tree."""
    project_root = project_root.resolve()
    file_paths = discover_source_files(project_root, config.source_globs, config.exclude)
    edges, all_nodes = extract_uses_edges(file_paths, project_root, config.pyan_depth)
    roots = select_roots(edges, all_nodes, config.entry_points)

    if not file_paths:
        trees: list[TreeNode] = []
        message = "No Python source files matched the configured source_globs."
    elif not roots:
        trees = []
        message = "No call graph roots were found for the configured entry_points."
    else:
        trees = [build_tree(root, edges, config.max_tree_depth) for root in roots]
        message = None

    html_output = render_html(trees, project_root.name, empty_message=message)
    output_path = (project_root / config.output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_output, encoding="utf-8")
    return output_path
