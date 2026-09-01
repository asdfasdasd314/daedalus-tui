"""Static call-graph analysis and top-down HTML tree rendering via pyan3."""

from __future__ import annotations

import html
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

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


def _collect_node_names(visitor: CallGraphVisitor) -> set[str]:
    names: set[str] = set()
    for node_list in visitor.nodes.values():
        for node in node_list:
            if node.namespace is not None:
                names.add(node.get_name())
    return names


def extract_uses_edges(
    file_paths: list[Path],
    project_root: Path,
    pyan_depth: int,
) -> tuple[dict[str, list[str]], set[str]]:
    """Run pyan analysis and return caller→callees edges plus all node names."""
    if not file_paths:
        return {}, set()

    project_root = project_root.resolve()
    visitor = CallGraphVisitor(
        [str(path) for path in file_paths],
        root=str(project_root),
    )
    visitor.process()
    visitor.filter_by_depth(pyan_depth)

    edges: dict[str, list[str]] = {}
    for from_node, to_nodes in visitor.uses_edges.items():
        caller = from_node.get_name()
        callees = sorted({to_node.get_name() for to_node in to_nodes})
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
        if depth >= max_tree_depth:
            return TreeNode(name=name, children=[])

        next_visited = visited | {name}
        children = [
            visit(callee, next_visited, depth + 1)
            for callee in edges.get(name, [])
        ]
        return TreeNode(name=name, children=children)

    return visit(root, frozenset(), 0)


def render_tree_list(trees: list[TreeNode]) -> str:
    """Render tree nodes as nested HTML lists."""
    parts: list[str] = []
    for tree in trees:
        parts.append(_render_tree_node(tree))
    return "\n".join(parts)


def _render_tree_node(node: TreeNode) -> str:
    class_names = ["name"]
    if node.is_cycle:
        class_names.append("cycle")
    label = html.escape(node.name)
    if not node.children:
        return f'<li><span class="{" ".join(class_names)}">{label}</span></li>'

    child_html = "\n".join(_render_tree_node(child) for child in node.children)
    return (
        f'<li><span class="{" ".join(class_names)}">{label}</span>'
        f'<ul class="tree">\n{child_html}\n</ul></li>'
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
        body = f'<ul class="tree roots">\n{render_tree_list(trees)}\n</ul>'
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
      max-width: 120rem;
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
    ul.tree {{
      list-style: none;
      margin: 0;
      padding-left: 1.25rem;
      border-left: 1px solid #bbb;
    }}
    ul.tree.roots {{
      border-left: none;
      padding-left: 0;
    }}
    li {{
      margin: 0.2rem 0;
      position: relative;
    }}
    li::before {{
      content: "";
      position: absolute;
      left: -1.25rem;
      top: 0.75rem;
      width: 0.85rem;
      border-top: 1px solid #bbb;
    }}
    ul.tree.roots > li::before {{
      display: none;
    }}
    .name {{
      display: inline-block;
      padding: 0.1rem 0.35rem;
      border-radius: 0.2rem;
      background: rgba(127, 127, 127, 0.12);
    }}
    .name.cycle {{
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
