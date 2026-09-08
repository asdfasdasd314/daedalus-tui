"""AST variable-lineage pass for call-graph import evidence.

Collects scoped Name/Attribute usage into a graph plus function summaries,
then aggregates per-variable statistics (function span, reads, mutations,
transitive derivatives). No semantic resource classification in this pass.
"""

from __future__ import annotations

import ast
import html
import json
from collections import defaultdict, deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


# ---------------------------------------------------------------------------
# Graph model
# ---------------------------------------------------------------------------

NODE_FUNCTION = "Function"
NODE_VARIABLE = "Variable"
NODE_ATTRIBUTE = "Attribute"
NODE_RETURN = "ReturnValue"

EDGE_ASSIGNED_FROM = "ASSIGNED_FROM"
EDGE_PASSED_TO = "PASSED_TO"
EDGE_RETURNED_TO = "RETURNED_TO"
EDGE_DERIVED_FROM = "DERIVED_FROM"
EDGE_READS = "READS"
EDGE_WRITES = "WRITES"
EDGE_MUTATES = "MUTATES"
EDGE_CALLS = "CALLS"

_DERIVATION_EDGE_KINDS = frozenset(
    {EDGE_DERIVED_FROM, EDGE_ASSIGNED_FROM, EDGE_PASSED_TO}
)


@dataclass
class GraphNode:
    id: str
    kind: str
    name: str
    scope: str
    module: str
    lineno: int | None = None
    col_offset: int | None = None
    file: str | None = None


@dataclass
class GraphEdge:
    source: str
    target: str
    kind: str
    lineno: int | None = None
    col_offset: int | None = None
    function_id: str | None = None
    file: str | None = None


@dataclass
class FunctionSummary:
    function_id: str
    name: str
    qualname: str
    module: str
    file: str | None
    lineno: int | None
    parameters: list[str] = field(default_factory=list)
    definitions: list[str] = field(default_factory=list)
    reads: list[str] = field(default_factory=list)
    writes: list[str] = field(default_factory=list)
    assignments: list[dict[str, Any]] = field(default_factory=list)
    calls: list[dict[str, Any]] = field(default_factory=list)
    returns: list[str] = field(default_factory=list)
    mutations: list[str] = field(default_factory=list)
    derivations: list[dict[str, str]] = field(default_factory=list)


@dataclass
class VariableStats:
    node_id: str
    kind: str
    name: str
    scope: str
    function_count: int
    read_count: int
    mutation_count: int
    derived_count: int
    write_count: int = 0
    enclosing_functions: tuple[str, ...] = ()
    derivatives: tuple[str, ...] = ()


@dataclass
class VariableLineageResult:
    nodes: dict[str, GraphNode] = field(default_factory=dict)
    edges: list[GraphEdge] = field(default_factory=list)
    summaries: dict[str, FunctionSummary] = field(default_factory=dict)
    stats: list[VariableStats] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)


@dataclass
class _FunctionInfo:
    function_id: str
    simple_name: str
    qualname: str
    module: str
    param_names: list[str]
    param_node_ids: list[str]
    file: str | None
    lineno: int | None


@dataclass
class _ScopeFrame:
    kind: str  # module | class | function
    name: str
    qualname: str  # empty for module; Class or outer.inner for others
    bindings: dict[str, str] = field(default_factory=dict)
    globals_decl: set[str] = field(default_factory=set)
    nonlocals_decl: set[str] = field(default_factory=set)
    function_id: str | None = None
    summary: FunctionSummary | None = None


@dataclass
class _PendingCall:
    caller_function_id: str | None
    callee_name: str
    positional_args: list[str | None]  # resolved arg node ids
    keyword_args: dict[str, str | None]  # param name -> arg node id
    lineno: int | None
    col_offset: int | None
    file: str | None
    assign_target_id: str | None = None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def module_fqn_from_path(file_path: Path, project_root: Path) -> str:
    """Map a project-relative Python path to a dotted module FQN."""
    relative = file_path.resolve().relative_to(project_root.resolve())
    parts = list(relative.with_suffix("").parts)
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def _scope_prefix(module: str, qualname: str) -> str:
    if qualname:
        return f"{module}.{qualname}"
    return module


def make_scoped_id(module: str, qualname: str, name: str) -> str:
    return f"{_scope_prefix(module, qualname)}::{name}"


def return_node_id(function_id: str) -> str:
    return f"{function_id}::return"


def _attr_dotted(node: ast.AST) -> str | None:
    """Return dotted attribute path for Attribute/Name chains, else None."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _attr_dotted(node.value)
        if base is None:
            return None
        return f"{base}.{node.attr}"
    return None


def _truncate_list(items: Iterable[str], limit: int = 8) -> str:
    ordered = list(items)
    if not ordered:
        return "—"
    if len(ordered) <= limit:
        return ", ".join(ordered)
    shown = ordered[:limit]
    remaining = len(ordered) - limit
    return ", ".join(shown) + f" (+{remaining} more)"


# ---------------------------------------------------------------------------
# Visitor
# ---------------------------------------------------------------------------


class VariableLineageVisitor(ast.NodeVisitor):
    """Collect scoped variable/attribute lineage for one module."""

    def __init__(
        self,
        *,
        module: str,
        file_rel: str,
        function_index: dict[str, list[_FunctionInfo]],
        nodes: dict[str, GraphNode],
        edges: list[GraphEdge],
        summaries: dict[str, FunctionSummary],
        pending_calls: list[_PendingCall],
    ) -> None:
        self.module = module
        self.file_rel = file_rel
        self.function_index = function_index
        self.nodes = nodes
        self.edges = edges
        self.summaries = summaries
        self.pending_calls = pending_calls
        self.scopes: list[_ScopeFrame] = []
        self._edge_keys: set[tuple[Any, ...]] = set()

    # -- scope helpers -----------------------------------------------------

    def _push_scope(
        self,
        kind: str,
        name: str,
        qualname: str,
        *,
        function_id: str | None = None,
        summary: FunctionSummary | None = None,
    ) -> _ScopeFrame:
        frame = _ScopeFrame(
            kind=kind,
            name=name,
            qualname=qualname,
            function_id=function_id,
            summary=summary,
        )
        self.scopes.append(frame)
        return frame

    def _pop_scope(self) -> None:
        self.scopes.pop()

    def _current(self) -> _ScopeFrame:
        return self.scopes[-1]

    def _current_function_frame(self) -> _ScopeFrame | None:
        for frame in reversed(self.scopes):
            if frame.kind == "function":
                return frame
        return None

    def _current_qualname_for_binding(self) -> str:
        """Qualname used for Store binding identity in the current scope."""
        frame = self._current()
        if frame.kind == "module":
            return ""
        return frame.qualname

    def _ensure_node(
        self,
        node_id: str,
        *,
        kind: str,
        name: str,
        scope: str,
        lineno: int | None = None,
        col_offset: int | None = None,
    ) -> GraphNode:
        existing = self.nodes.get(node_id)
        if existing is not None:
            if existing.lineno is None and lineno is not None:
                existing.lineno = lineno
                existing.col_offset = col_offset
            return existing
        graph_node = GraphNode(
            id=node_id,
            kind=kind,
            name=name,
            scope=scope,
            module=self.module,
            lineno=lineno,
            col_offset=col_offset,
            file=self.file_rel,
        )
        self.nodes[node_id] = graph_node
        return graph_node

    def _add_edge(
        self,
        source: str,
        target: str,
        kind: str,
        *,
        lineno: int | None = None,
        col_offset: int | None = None,
        function_id: str | None = None,
    ) -> None:
        if not source or not target:
            return
        resolved_function = function_id or (
            self._current_function_frame().function_id
            if self._current_function_frame()
            else None
        )
        # Deduplicate identical usage edges at the same source location.
        if kind in {EDGE_READS, EDGE_WRITES, EDGE_MUTATES}:
            key = (source, target, kind, lineno, resolved_function)
            if key in self._edge_keys:
                return
            self._edge_keys.add(key)
        self.edges.append(
            GraphEdge(
                source=source,
                target=target,
                kind=kind,
                lineno=lineno,
                col_offset=col_offset,
                function_id=resolved_function,
                file=self.file_rel,
            )
        )

    def _record_usage_on_summary(
        self,
        node_id: str,
        *,
        as_read: bool = False,
        as_write: bool = False,
        as_def: bool = False,
        as_mutation: bool = False,
    ) -> None:
        frame = self._current_function_frame()
        if frame is None or frame.summary is None:
            return
        summary = frame.summary
        if as_read and node_id not in summary.reads:
            summary.reads.append(node_id)
        if as_write and node_id not in summary.writes:
            summary.writes.append(node_id)
        if as_def and node_id not in summary.definitions:
            summary.definitions.append(node_id)
        if as_mutation and node_id not in summary.mutations:
            summary.mutations.append(node_id)

    # -- binding resolution ------------------------------------------------

    def _resolve_nonlocal_target(self, name: str) -> str | None:
        """Find nearest enclosing function (not class/module) binding for nonlocal."""
        # Skip current function frame; search outward function frames only.
        seen_current = False
        for frame in reversed(self.scopes):
            if frame.kind != "function":
                continue
            if not seen_current:
                seen_current = True
                continue
            if name in frame.bindings:
                return frame.bindings[name]
            # Binding may not exist yet; still target that scope's identity.
            return make_scoped_id(self.module, frame.qualname, name)
        return None

    def _store_target_id(self, name: str) -> tuple[str, str]:
        """Return (node_id, scope_qualname) for a Store of *name*."""
        frame = self._current()
        if frame.kind == "function":
            if name in frame.globals_decl:
                node_id = make_scoped_id(self.module, "", name)
                return node_id, ""
            if name in frame.nonlocals_decl:
                resolved = self._resolve_nonlocal_target(name)
                if resolved is not None:
                    # scope qualname is between module and ::name
                    scope = resolved.rsplit("::", 1)[0]
                    if scope.startswith(self.module + "."):
                        qual = scope[len(self.module) + 1 :]
                    elif scope == self.module:
                        qual = ""
                    else:
                        qual = scope
                    return resolved, qual
            node_id = make_scoped_id(self.module, frame.qualname, name)
            return node_id, frame.qualname
        if frame.kind == "class":
            node_id = make_scoped_id(self.module, frame.qualname, name)
            return node_id, frame.qualname
        node_id = make_scoped_id(self.module, "", name)
        return node_id, ""

    def _load_target_id(self, name: str) -> tuple[str, str]:
        """LEGB-style Load resolution: enclosing function, then module.

        Class scopes are skipped when looking up free names from methods.
        """
        frame = self._current()
        if frame.kind == "function":
            if name in frame.globals_decl:
                return make_scoped_id(self.module, "", name), ""
            if name in frame.nonlocals_decl:
                resolved = self._resolve_nonlocal_target(name)
                if resolved is not None:
                    scope = resolved.rsplit("::", 1)[0]
                    if scope.startswith(self.module + "."):
                        qual = scope[len(self.module) + 1 :]
                    elif scope == self.module:
                        qual = ""
                    else:
                        qual = scope
                    return resolved, qual
            if name in frame.bindings:
                return frame.bindings[name], frame.qualname

            # Walk enclosing function scopes, then module. Skip class frames.
            for outer in reversed(self.scopes[:-1]):
                if outer.kind == "class":
                    continue
                if outer.kind == "function" and name in outer.bindings:
                    return outer.bindings[name], outer.qualname
                if outer.kind == "module" and name in outer.bindings:
                    return outer.bindings[name], ""
            # No enclosing Store: current-scope read-only node.
            node_id = make_scoped_id(self.module, frame.qualname, name)
            return node_id, frame.qualname

        if frame.kind == "class":
            if name in frame.bindings:
                return frame.bindings[name], frame.qualname
            # Class body: look at module only (not enclosing class chain for free names).
            for outer in reversed(self.scopes[:-1]):
                if outer.kind == "module" and name in outer.bindings:
                    return outer.bindings[name], ""
            return make_scoped_id(self.module, frame.qualname, name), frame.qualname

        # Module scope
        if name in frame.bindings:
            return frame.bindings[name], ""
        return make_scoped_id(self.module, "", name), ""

    def _bind_store(self, name: str, node_id: str) -> None:
        frame = self._current()
        if frame.kind == "function":
            if name in frame.globals_decl:
                # Binding lives on module frame.
                for outer in self.scopes:
                    if outer.kind == "module":
                        outer.bindings[name] = node_id
                        return
                return
            if name in frame.nonlocals_decl:
                # Binding lives on enclosing function; do not rebind locally.
                for outer in reversed(self.scopes[:-1]):
                    if outer.kind == "function":
                        outer.bindings.setdefault(name, node_id)
                        return
                return
        frame.bindings[name] = node_id

    # -- visitors ----------------------------------------------------------

    def visit_Module(self, node: ast.Module) -> None:
        self._push_scope("module", self.module, "")
        self.generic_visit(node)
        self._pop_scope()

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        parent = self._current()
        if parent.kind == "module":
            qualname = node.name
        elif parent.kind == "class":
            qualname = f"{parent.qualname}.{node.name}"
        else:
            # Nested class inside function
            qualname = f"{parent.qualname}.{node.name}" if parent.qualname else node.name
        self._push_scope("class", node.name, qualname)
        # Visit body only; skip decorators/bases for lineage simplicity.
        for child in node.body:
            self.visit(child)
        self._pop_scope()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._visit_function(node)

    def _visit_function(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> None:
        parent = self._current()
        if parent.kind == "module":
            qualname = node.name
        else:
            qualname = f"{parent.qualname}.{node.name}" if parent.qualname else node.name
        function_id = f"{self.module}.{qualname}"
        summary = FunctionSummary(
            function_id=function_id,
            name=node.name,
            qualname=qualname,
            module=self.module,
            file=self.file_rel,
            lineno=node.lineno,
        )
        self.summaries[function_id] = summary
        self._ensure_node(
            function_id,
            kind=NODE_FUNCTION,
            name=node.name,
            scope=_scope_prefix(self.module, parent.qualname if parent.kind != "module" else ""),
            lineno=node.lineno,
            col_offset=node.col_offset,
        )

        frame = self._push_scope(
            "function",
            node.name,
            qualname,
            function_id=function_id,
            summary=summary,
        )

        param_names: list[str] = []
        param_node_ids: list[str] = []
        args = node.args
        for arg in list(args.posonlyargs) + list(args.args) + list(args.kwonlyargs):
            param_names.append(arg.arg)
            node_id = make_scoped_id(self.module, qualname, arg.arg)
            self._ensure_node(
                node_id,
                kind=NODE_VARIABLE,
                name=arg.arg,
                scope=_scope_prefix(self.module, qualname),
                lineno=getattr(arg, "lineno", node.lineno),
                col_offset=getattr(arg, "col_offset", node.col_offset),
            )
            frame.bindings[arg.arg] = node_id
            param_node_ids.append(node_id)
            summary.parameters.append(node_id)
            if node_id not in summary.definitions:
                summary.definitions.append(node_id)
            self._add_edge(
                function_id,
                node_id,
                EDGE_WRITES,
                lineno=getattr(arg, "lineno", node.lineno),
                col_offset=getattr(arg, "col_offset", node.col_offset),
                function_id=function_id,
            )

        if args.vararg is not None:
            name = args.vararg.arg
            param_names.append(name)
            node_id = make_scoped_id(self.module, qualname, name)
            self._ensure_node(
                node_id,
                kind=NODE_VARIABLE,
                name=name,
                scope=_scope_prefix(self.module, qualname),
                lineno=getattr(args.vararg, "lineno", node.lineno),
                col_offset=getattr(args.vararg, "col_offset", node.col_offset),
            )
            frame.bindings[name] = node_id
            param_node_ids.append(node_id)
            summary.parameters.append(node_id)
            if node_id not in summary.definitions:
                summary.definitions.append(node_id)

        if args.kwarg is not None:
            name = args.kwarg.arg
            param_names.append(name)
            node_id = make_scoped_id(self.module, qualname, name)
            self._ensure_node(
                node_id,
                kind=NODE_VARIABLE,
                name=name,
                scope=_scope_prefix(self.module, qualname),
                lineno=getattr(args.kwarg, "lineno", node.lineno),
                col_offset=getattr(args.kwarg, "col_offset", node.col_offset),
            )
            frame.bindings[name] = node_id
            param_node_ids.append(node_id)
            summary.parameters.append(node_id)
            if node_id not in summary.definitions:
                summary.definitions.append(node_id)

        info = _FunctionInfo(
            function_id=function_id,
            simple_name=node.name,
            qualname=qualname,
            module=self.module,
            param_names=param_names,
            param_node_ids=param_node_ids,
            file=self.file_rel,
            lineno=node.lineno,
        )
        self.function_index.setdefault(node.name, []).append(info)
        self.function_index.setdefault(function_id, []).append(info)

        for child in node.body:
            self.visit(child)
        self._pop_scope()

    def visit_Global(self, node: ast.Global) -> None:
        frame = self._current()
        if frame.kind == "function":
            frame.globals_decl.update(node.names)

    def visit_Nonlocal(self, node: ast.Nonlocal) -> None:
        frame = self._current()
        if frame.kind == "function":
            frame.nonlocals_decl.update(node.names)

    def visit_Assign(self, node: ast.Assign) -> None:
        sources = self._collect_rhs_sources(node.value)
        call_assign_target: str | None = None
        for target in node.targets:
            target_ids = self._handle_store_target(target, is_mutation=False)
            for target_id in target_ids:
                self._record_assignment(target_id, sources, node)
                if isinstance(node.value, ast.Call) and call_assign_target is None:
                    call_assign_target = target_id
        # Visit Call specially to attach RETURNED_TO via pending call.
        if isinstance(node.value, ast.Call):
            self._visit_call(node.value, assign_target_id=call_assign_target)
        else:
            # Still walk value for nested constructs, but skip re-processing Names
            # already collected as RHS sources — visit for nested defs/calls.
            self._visit_value_for_nested(node.value)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        sources: list[str] = []
        if node.value is not None:
            sources = self._collect_rhs_sources(node.value)
        target_ids = self._handle_store_target(node.target, is_mutation=False)
        for target_id in target_ids:
            self._record_assignment(target_id, sources, node)
        if node.value is not None:
            if isinstance(node.value, ast.Call) and target_ids:
                self._visit_call(node.value, assign_target_id=target_ids[0])
            else:
                self._visit_value_for_nested(node.value)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        # Target is mutated; RHS sources also derive into the target.
        # AugAssign also reads the target before writing.
        sources = self._collect_rhs_sources(node.value)
        target_ids = self._handle_store_target(node.target, is_mutation=True)
        for target_id in target_ids:
            func = self._current_function_frame()
            self._add_edge(
                func.function_id if func else _scope_prefix(self.module, ""),
                target_id,
                EDGE_READS,
                lineno=node.lineno,
                col_offset=node.col_offset,
            )
            self._record_usage_on_summary(target_id, as_read=True)
            self._record_assignment(target_id, sources, node)
            self._add_edge(
                func.function_id if func else _scope_prefix(self.module, ""),
                target_id,
                EDGE_MUTATES,
                lineno=node.lineno,
                col_offset=node.col_offset,
                function_id=func.function_id if func else None,
            )
            self._record_usage_on_summary(target_id, as_mutation=True, as_write=True)
        self._visit_value_for_nested(node.value)

    def _visit_value_for_nested(self, node: ast.AST) -> None:
        """Visit nested function/class/call constructs inside expressions."""
        if isinstance(node, ast.Call):
            self._visit_call(node, assign_target_id=None)
            return
        for child in ast.iter_child_nodes(node):
            if isinstance(
                child,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                    ast.ClassDef,
                    ast.Lambda,
                    ast.ListComp,
                    ast.SetComp,
                    ast.DictComp,
                    ast.GeneratorExp,
                ),
            ):
                self.visit(child)
            elif isinstance(child, ast.Call):
                self._visit_call(child, assign_target_id=None)
            else:
                self._visit_value_for_nested(child)

    def _collect_rhs_sources(self, value: ast.AST) -> list[str]:
        sources: list[str] = []
        seen: set[str] = set()

        def walk(node: ast.AST) -> None:
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                node_id, scope_qual = self._load_target_id(node.id)
                self._ensure_node(
                    node_id,
                    kind=NODE_VARIABLE,
                    name=node.id,
                    scope=_scope_prefix(self.module, scope_qual),
                    lineno=node.lineno,
                    col_offset=node.col_offset,
                )
                if node_id not in seen:
                    seen.add(node_id)
                    sources.append(node_id)
                self._add_edge(
                    (
                        self._current_function_frame().function_id
                        if self._current_function_frame()
                        else _scope_prefix(self.module, "")
                    ),
                    node_id,
                    EDGE_READS,
                    lineno=node.lineno,
                    col_offset=node.col_offset,
                )
                self._record_usage_on_summary(node_id, as_read=True)
                return
            if isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Load):
                dotted = _attr_dotted(node)
                if dotted is not None:
                    qual = self._current_qualname_for_binding()
                    # Attribute loads bind to the current function/module/class scope.
                    func = self._current_function_frame()
                    if func is not None:
                        qual = func.qualname
                    node_id = make_scoped_id(self.module, qual, dotted)
                    self._ensure_node(
                        node_id,
                        kind=NODE_ATTRIBUTE,
                        name=dotted,
                        scope=_scope_prefix(self.module, qual),
                        lineno=node.lineno,
                        col_offset=node.col_offset,
                    )
                    if node_id not in seen:
                        seen.add(node_id)
                        sources.append(node_id)
                    self._add_edge(
                        (
                            self._current_function_frame().function_id
                            if self._current_function_frame()
                            else _scope_prefix(self.module, "")
                        ),
                        node_id,
                        EDGE_READS,
                        lineno=node.lineno,
                        col_offset=node.col_offset,
                    )
                    self._record_usage_on_summary(node_id, as_read=True)
                    # Also record base Name load for LEGB (portfolio in portfolio.capital).
                    self._record_attribute_base_reads(node)
                    return
            for child in ast.iter_child_nodes(node):
                # Do not descend into nested function/class bodies for RHS sources.
                if isinstance(
                    child,
                    (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda),
                ):
                    continue
                walk(child)

        walk(value)
        return sources

    def _record_base_name_read(self, node: ast.AST) -> None:
        """Record Load on the root Name of an attribute/value chain."""
        current: ast.AST = node
        while isinstance(current, ast.Attribute):
            current = current.value
        if not isinstance(current, ast.Name):
            return
        node_id, scope_qual = self._load_target_id(current.id)
        self._ensure_node(
            node_id,
            kind=NODE_VARIABLE,
            name=current.id,
            scope=_scope_prefix(self.module, scope_qual),
            lineno=current.lineno,
            col_offset=current.col_offset,
        )
        self._add_edge(
            (
                self._current_function_frame().function_id
                if self._current_function_frame()
                else _scope_prefix(self.module, "")
            ),
            node_id,
            EDGE_READS,
            lineno=current.lineno,
            col_offset=current.col_offset,
        )
        self._record_usage_on_summary(node_id, as_read=True)

    def _record_attribute_base_reads(self, node: ast.Attribute) -> None:
        """Record Load on the root Name of an attribute chain."""
        self._record_base_name_read(node.value)

    def _handle_store_target(
        self, target: ast.AST, *, is_mutation: bool
    ) -> list[str]:
        ids: list[str] = []
        if isinstance(target, ast.Name):
            node_id, scope_qual = self._store_target_id(target.id)
            self._ensure_node(
                node_id,
                kind=NODE_VARIABLE,
                name=target.id,
                scope=_scope_prefix(self.module, scope_qual),
                lineno=target.lineno,
                col_offset=target.col_offset,
            )
            self._bind_store(target.id, node_id)
            func = self._current_function_frame()
            self._add_edge(
                func.function_id if func else _scope_prefix(self.module, ""),
                node_id,
                EDGE_WRITES,
                lineno=target.lineno,
                col_offset=target.col_offset,
            )
            self._record_usage_on_summary(
                node_id, as_write=True, as_def=not is_mutation
            )
            ids.append(node_id)
        elif isinstance(target, ast.Attribute):
            dotted = _attr_dotted(target)
            if dotted is not None:
                func = self._current_function_frame()
                qual = func.qualname if func is not None else self._current_qualname_for_binding()
                node_id = make_scoped_id(self.module, qual, dotted)
                self._ensure_node(
                    node_id,
                    kind=NODE_ATTRIBUTE,
                    name=dotted,
                    scope=_scope_prefix(self.module, qual),
                    lineno=target.lineno,
                    col_offset=target.col_offset,
                )
                self._add_edge(
                    func.function_id if func else _scope_prefix(self.module, ""),
                    node_id,
                    EDGE_WRITES,
                    lineno=target.lineno,
                    col_offset=target.col_offset,
                )
                self._record_usage_on_summary(
                    node_id, as_write=True, as_def=not is_mutation
                )
                # Base name is loaded for attribute write (portfolio in portfolio.x = ...).
                self._record_base_name_read(target.value)
                ids.append(node_id)
        elif isinstance(target, (ast.Tuple, ast.List)):
            for elt in target.elts:
                ids.extend(self._handle_store_target(elt, is_mutation=is_mutation))
        elif isinstance(target, ast.Starred):
            ids.extend(self._handle_store_target(target.value, is_mutation=is_mutation))
        elif isinstance(target, ast.Subscript):
            # Treat subscript store as mutation of the base Name/Attribute if resolvable.
            base = target.value
            dotted = _attr_dotted(base)
            if dotted is not None:
                func = self._current_function_frame()
                if isinstance(base, ast.Name):
                    node_id, scope_qual = self._store_target_id(base.id)
                    # Subscript assignment mutates existing object; prefer load binding.
                    node_id, scope_qual = self._load_target_id(base.id)
                    self._ensure_node(
                        node_id,
                        kind=NODE_VARIABLE,
                        name=base.id,
                        scope=_scope_prefix(self.module, scope_qual),
                        lineno=target.lineno,
                        col_offset=target.col_offset,
                    )
                else:
                    qual = (
                        func.qualname
                        if func is not None
                        else self._current_qualname_for_binding()
                    )
                    node_id = make_scoped_id(self.module, qual, dotted)
                    self._ensure_node(
                        node_id,
                        kind=NODE_ATTRIBUTE,
                        name=dotted,
                        scope=_scope_prefix(self.module, qual),
                        lineno=target.lineno,
                        col_offset=target.col_offset,
                    )
                if not is_mutation:
                    func = self._current_function_frame()
                    self._add_edge(
                        func.function_id if func else _scope_prefix(self.module, ""),
                        node_id,
                        EDGE_MUTATES,
                        lineno=target.lineno,
                        col_offset=target.col_offset,
                    )
                    self._record_usage_on_summary(node_id, as_mutation=True, as_write=True)
                ids.append(node_id)
            # Still walk slice for nested reads.
            self._collect_rhs_sources(target.slice)
        return ids

    def _record_assignment(
        self,
        target_id: str,
        sources: list[str],
        node: ast.AST,
    ) -> None:
        frame = self._current_function_frame()
        summary = frame.summary if frame else None
        lineno = getattr(node, "lineno", None)
        col = getattr(node, "col_offset", None)
        for source_id in sources:
            self._add_edge(
                source_id,
                target_id,
                EDGE_DERIVED_FROM,
                lineno=lineno,
                col_offset=col,
            )
            self._add_edge(
                source_id,
                target_id,
                EDGE_ASSIGNED_FROM,
                lineno=lineno,
                col_offset=col,
            )
            if summary is not None:
                summary.derivations.append({"from": source_id, "to": target_id})
        if summary is not None:
            summary.assignments.append(
                {
                    "target": target_id,
                    "sources": list(sources),
                    "lineno": lineno,
                }
            )

    def visit_Call(self, node: ast.Call) -> None:
        self._visit_call(node, assign_target_id=None)

    def _visit_call(self, node: ast.Call, *, assign_target_id: str | None) -> None:
        callee_name = self._callee_simple_name(node.func)
        func_frame = self._current_function_frame()
        caller_id = func_frame.function_id if func_frame else None

        positional: list[str | None] = []
        for arg in node.args:
            if isinstance(arg, ast.Starred):
                positional.append(None)
                self._collect_rhs_sources(arg.value)
                continue
            sources = self._collect_rhs_sources(arg)
            positional.append(sources[0] if len(sources) == 1 else (sources[0] if sources else None))
            # If expression has multiple sources, still pass primary if single Name/Attr;
            # for multi-source exprs, use None for param mapping but sources were read.

        keywords: dict[str, str | None] = {}
        for kw in node.keywords:
            if kw.arg is None:
                self._collect_rhs_sources(kw.value)
                continue
            sources = self._collect_rhs_sources(kw.value)
            keywords[kw.arg] = sources[0] if sources else None

        # Record reads on func expression bases (obj.method).
        if isinstance(node.func, ast.Attribute):
            self._collect_rhs_sources(node.func.value)
        elif isinstance(node.func, ast.Name):
            # Calling a name is a read of that name when it is a variable.
            node_id, scope_qual = self._load_target_id(node.func.id)
            # Only create read if it looks like a bound variable (has store) or free.
            self._ensure_node(
                node_id,
                kind=NODE_VARIABLE,
                name=node.func.id,
                scope=_scope_prefix(self.module, scope_qual),
                lineno=node.func.lineno,
                col_offset=node.func.col_offset,
            )

        call_record = {
            "callee": callee_name or "<unknown>",
            "lineno": node.lineno,
            "positional": list(positional),
            "keywords": dict(keywords),
        }
        if func_frame and func_frame.summary is not None:
            func_frame.summary.calls.append(call_record)

        self.pending_calls.append(
            _PendingCall(
                caller_function_id=caller_id,
                callee_name=callee_name or "",
                positional_args=positional,
                keyword_args=keywords,
                lineno=node.lineno,
                col_offset=node.col_offset,
                file=self.file_rel,
                assign_target_id=assign_target_id,
            )
        )

        # Nested calls inside args already handled via _collect_rhs_sources reads;
        # still visit nested Call nodes inside args for pending call records.
        for arg in node.args:
            if isinstance(arg, ast.Starred):
                self._visit_nested_calls(arg.value)
            else:
                self._visit_nested_calls(arg)
        for kw in node.keywords:
            self._visit_nested_calls(kw.value)

    def _visit_nested_calls(self, node: ast.AST) -> None:
        for child in ast.walk(node):
            if child is node:
                continue
            if isinstance(child, ast.Call):
                # Avoid double-processing top-level; only deeper calls.
                pass
        # Re-walk with visitor for Call nodes that weren't the root.
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.Call):
                self._visit_call(child, assign_target_id=None)
            elif isinstance(
                child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
            ):
                self.visit(child)
            else:
                self._visit_nested_calls(child)

    def _callee_simple_name(self, func: ast.AST) -> str | None:
        if isinstance(func, ast.Name):
            return func.id
        if isinstance(func, ast.Attribute):
            return func.attr
        return None

    def visit_Return(self, node: ast.Return) -> None:
        frame = self._current_function_frame()
        if frame is None or frame.function_id is None:
            return
        ret_id = return_node_id(frame.function_id)
        self._ensure_node(
            ret_id,
            kind=NODE_RETURN,
            name="return",
            scope=frame.function_id,
            lineno=node.lineno,
            col_offset=node.col_offset,
        )
        if frame.summary is not None and ret_id not in frame.summary.returns:
            frame.summary.returns.append(ret_id)
        if node.value is not None:
            sources = self._collect_rhs_sources(node.value)
            for source_id in sources:
                self._add_edge(
                    source_id,
                    ret_id,
                    EDGE_DERIVED_FROM,
                    lineno=node.lineno,
                    col_offset=node.col_offset,
                )
                self._add_edge(
                    source_id,
                    ret_id,
                    EDGE_ASSIGNED_FROM,
                    lineno=node.lineno,
                    col_offset=node.col_offset,
                )
            if isinstance(node.value, ast.Call):
                self._visit_call(node.value, assign_target_id=None)
            else:
                self._visit_value_for_nested(node.value)

    def visit_Name(self, node: ast.Name) -> None:
        # Standalone Name visits (not handled via Assign/Call collectors).
        if isinstance(node.ctx, ast.Load):
            node_id, scope_qual = self._load_target_id(node.id)
            self._ensure_node(
                node_id,
                kind=NODE_VARIABLE,
                name=node.id,
                scope=_scope_prefix(self.module, scope_qual),
                lineno=node.lineno,
                col_offset=node.col_offset,
            )
            self._add_edge(
                (
                    self._current_function_frame().function_id
                    if self._current_function_frame()
                    else _scope_prefix(self.module, "")
                ),
                node_id,
                EDGE_READS,
                lineno=node.lineno,
                col_offset=node.col_offset,
            )
            self._record_usage_on_summary(node_id, as_read=True)
        elif isinstance(node.ctx, ast.Store):
            # Bare stores outside Assign are rare; still bind.
            node_id, scope_qual = self._store_target_id(node.id)
            self._ensure_node(
                node_id,
                kind=NODE_VARIABLE,
                name=node.id,
                scope=_scope_prefix(self.module, scope_qual),
                lineno=node.lineno,
                col_offset=node.col_offset,
            )
            self._bind_store(node.id, node_id)
            self._record_usage_on_summary(node_id, as_write=True, as_def=True)
        elif isinstance(node.ctx, ast.Del):
            node_id, scope_qual = self._load_target_id(node.id)
            self._ensure_node(
                node_id,
                kind=NODE_VARIABLE,
                name=node.id,
                scope=_scope_prefix(self.module, scope_qual),
                lineno=node.lineno,
                col_offset=node.col_offset,
            )
            self._record_usage_on_summary(node_id, as_write=True)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        dotted = _attr_dotted(node)
        if dotted is None:
            self.generic_visit(node)
            return
        func = self._current_function_frame()
        qual = func.qualname if func is not None else self._current_qualname_for_binding()
        node_id = make_scoped_id(self.module, qual, dotted)
        kind = NODE_ATTRIBUTE
        if isinstance(node.ctx, ast.Load):
            self._ensure_node(
                node_id,
                kind=kind,
                name=dotted,
                scope=_scope_prefix(self.module, qual),
                lineno=node.lineno,
                col_offset=node.col_offset,
            )
            self._add_edge(
                func.function_id if func else _scope_prefix(self.module, ""),
                node_id,
                EDGE_READS,
                lineno=node.lineno,
                col_offset=node.col_offset,
            )
            self._record_usage_on_summary(node_id, as_read=True)
            self._record_attribute_base_reads(node)
        elif isinstance(node.ctx, (ast.Store, ast.Del)):
            self._ensure_node(
                node_id,
                kind=kind,
                name=dotted,
                scope=_scope_prefix(self.module, qual),
                lineno=node.lineno,
                col_offset=node.col_offset,
            )
            self._add_edge(
                func.function_id if func else _scope_prefix(self.module, ""),
                node_id,
                EDGE_WRITES,
                lineno=node.lineno,
                col_offset=node.col_offset,
            )
            self._record_usage_on_summary(node_id, as_write=True)

    # Lambdas / comprehensions: attribute names to enclosing function/module.
    def visit_Lambda(self, node: ast.Lambda) -> None:
        # Parameters bind in enclosing scope for v1 stability.
        frame = self._current()
        for arg in list(node.args.posonlyargs) + list(node.args.args) + list(
            node.args.kwonlyargs
        ):
            qual = (
                frame.qualname
                if frame.kind != "module"
                else (self._current_function_frame().qualname if self._current_function_frame() else "")
            )
            if frame.kind == "function":
                qual = frame.qualname
            elif self._current_function_frame() is not None:
                qual = self._current_function_frame().qualname  # type: ignore[union-attr]
            else:
                qual = ""
            node_id = make_scoped_id(self.module, qual, arg.arg)
            self._ensure_node(
                node_id,
                kind=NODE_VARIABLE,
                name=arg.arg,
                scope=_scope_prefix(self.module, qual),
                lineno=getattr(arg, "lineno", None),
                col_offset=getattr(arg, "col_offset", None),
            )
            frame.bindings[arg.arg] = node_id
        self.visit(node.body)

    def _visit_comprehension(self, generators: list[ast.comprehension], visit_elt) -> None:
        frame = self._current()
        for gen in generators:
            # Target names bind in enclosing scope (v1).
            self._handle_store_target(gen.target, is_mutation=False)
            self._collect_rhs_sources(gen.iter)
            for if_clause in gen.ifs:
                self._collect_rhs_sources(if_clause)
        visit_elt()


# ---------------------------------------------------------------------------
# Call resolution & stats
# ---------------------------------------------------------------------------


def _unique_callee(
    callee_name: str, function_index: dict[str, list[_FunctionInfo]]
) -> _FunctionInfo | None:
    if not callee_name:
        return None
    matches = function_index.get(callee_name, [])
    # Deduplicate by function_id (indexed under both simple and FQN).
    by_id = {info.function_id: info for info in matches}
    unique = list(by_id.values())
    if len(unique) == 1:
        return unique[0]
    return None


def resolve_pending_calls(
    pending: list[_PendingCall],
    function_index: dict[str, list[_FunctionInfo]],
    nodes: dict[str, GraphNode],
    edges: list[GraphEdge],
    summaries: dict[str, FunctionSummary],
) -> None:
    for call in pending:
        callee = _unique_callee(call.callee_name, function_index)
        if call.caller_function_id and callee is not None:
            edges.append(
                GraphEdge(
                    source=call.caller_function_id,
                    target=callee.function_id,
                    kind=EDGE_CALLS,
                    lineno=call.lineno,
                    col_offset=call.col_offset,
                    function_id=call.caller_function_id,
                    file=call.file,
                )
            )

        if callee is None:
            continue

        # Positional mapping (skip *args slots marked None without matching).
        for index, arg_id in enumerate(call.positional_args):
            if arg_id is None:
                continue
            if index >= len(callee.param_node_ids):
                break
            # Skip mapping onto *vararg / **kwarg loosely: map only plain params
            # that have a corresponding positional slot in param_names without stars.
            param_id = callee.param_node_ids[index]
            edges.append(
                GraphEdge(
                    source=arg_id,
                    target=param_id,
                    kind=EDGE_PASSED_TO,
                    lineno=call.lineno,
                    col_offset=call.col_offset,
                    function_id=call.caller_function_id,
                    file=call.file,
                )
            )
            if call.caller_function_id and call.caller_function_id in summaries:
                summaries[call.caller_function_id].derivations.append(
                    {"from": arg_id, "to": param_id}
                )

        # Keyword mapping by parameter name.
        name_to_param = {
            name: node_id
            for name, node_id in zip(callee.param_names, callee.param_node_ids, strict=False)
        }
        for kw_name, arg_id in call.keyword_args.items():
            if arg_id is None:
                continue
            param_id = name_to_param.get(kw_name)
            if param_id is None:
                continue
            edges.append(
                GraphEdge(
                    source=arg_id,
                    target=param_id,
                    kind=EDGE_PASSED_TO,
                    lineno=call.lineno,
                    col_offset=call.col_offset,
                    function_id=call.caller_function_id,
                    file=call.file,
                )
            )

        if call.assign_target_id is not None:
            ret_id = return_node_id(callee.function_id)
            if ret_id not in nodes:
                nodes[ret_id] = GraphNode(
                    id=ret_id,
                    kind=NODE_RETURN,
                    name="return",
                    scope=callee.function_id,
                    module=callee.module,
                    lineno=callee.lineno,
                    file=callee.file,
                )
            edges.append(
                GraphEdge(
                    source=ret_id,
                    target=call.assign_target_id,
                    kind=EDGE_RETURNED_TO,
                    lineno=call.lineno,
                    col_offset=call.col_offset,
                    function_id=call.caller_function_id,
                    file=call.file,
                )
            )


def _transitive_derivatives(
    node_id: str, adjacency: dict[str, set[str]]
) -> set[str]:
    seen: set[str] = set()
    queue: deque[str] = deque(adjacency.get(node_id, ()))
    while queue:
        current = queue.popleft()
        if current in seen or current == node_id:
            continue
        seen.add(current)
        queue.extend(adjacency.get(current, ()))
    return seen


def compute_variable_stats(
    nodes: dict[str, GraphNode],
    edges: list[GraphEdge],
    summaries: dict[str, FunctionSummary],
) -> list[VariableStats]:
    read_counts: dict[str, int] = defaultdict(int)
    write_counts: dict[str, int] = defaultdict(int)
    mutation_counts: dict[str, int] = defaultdict(int)
    functions_by_node: dict[str, set[str]] = defaultdict(set)
    derivation_adj: dict[str, set[str]] = defaultdict(set)

    for edge in edges:
        if edge.kind == EDGE_READS:
            read_counts[edge.target] += 1
            if edge.function_id:
                functions_by_node[edge.target].add(edge.function_id)
        elif edge.kind == EDGE_WRITES:
            write_counts[edge.target] += 1
            if edge.function_id:
                functions_by_node[edge.target].add(edge.function_id)
        elif edge.kind == EDGE_MUTATES:
            mutation_counts[edge.target] += 1
            if edge.function_id:
                functions_by_node[edge.target].add(edge.function_id)
        elif edge.kind in _DERIVATION_EDGE_KINDS:
            derivation_adj[edge.source].add(edge.target)
            if edge.function_id:
                functions_by_node[edge.source].add(edge.function_id)
                functions_by_node[edge.target].add(edge.function_id)

    # Parameters / definitions from summaries also count as function presence.
    for summary in summaries.values():
        for node_id in summary.parameters:
            functions_by_node[node_id].add(summary.function_id)
        for node_id in summary.definitions:
            functions_by_node[node_id].add(summary.function_id)
        for node_id in summary.reads:
            functions_by_node[node_id].add(summary.function_id)
        for node_id in summary.mutations:
            functions_by_node[node_id].add(summary.function_id)
        for call in summary.calls:
            for arg_id in call.get("positional") or []:
                if arg_id:
                    functions_by_node[arg_id].add(summary.function_id)
            for arg_id in (call.get("keywords") or {}).values():
                if arg_id:
                    functions_by_node[arg_id].add(summary.function_id)

    stats: list[VariableStats] = []
    for node in nodes.values():
        if node.kind not in {NODE_VARIABLE, NODE_ATTRIBUTE}:
            continue
        derivatives = _transitive_derivatives(node.id, derivation_adj)
        enclosing = tuple(sorted(functions_by_node.get(node.id, ())))
        stats.append(
            VariableStats(
                node_id=node.id,
                kind=node.kind,
                name=node.name,
                scope=node.scope,
                function_count=len(enclosing),
                read_count=read_counts.get(node.id, 0),
                mutation_count=mutation_counts.get(node.id, 0),
                derived_count=len(derivatives),
                write_count=write_counts.get(node.id, 0),
                enclosing_functions=enclosing,
                derivatives=tuple(sorted(derivatives)),
            )
        )

    stats.sort(
        key=lambda item: (
            -item.function_count,
            -item.derived_count,
            -item.mutation_count,
            -item.read_count,
            item.node_id,
        )
    )
    return stats


def analyze_sources(
    file_paths: list[Path],
    project_root: Path,
) -> VariableLineageResult:
    """Analyze Python sources and return lineage graph, summaries, and stats."""
    project_root = project_root.resolve()
    nodes: dict[str, GraphNode] = {}
    edges: list[GraphEdge] = []
    summaries: dict[str, FunctionSummary] = {}
    function_index: dict[str, list[_FunctionInfo]] = {}
    pending_calls: list[_PendingCall] = []

    for path in sorted(file_paths, key=lambda p: p.as_posix()):
        path = path.resolve()
        try:
            relative = path.relative_to(project_root).as_posix()
        except ValueError:
            relative = path.as_posix()
        try:
            source = path.read_text(encoding="utf-8")
        except OSError:
            continue
        try:
            tree = ast.parse(source, filename=str(path))
        except SyntaxError:
            continue
        module = module_fqn_from_path(path, project_root)
        visitor = VariableLineageVisitor(
            module=module,
            file_rel=relative,
            function_index=function_index,
            nodes=nodes,
            edges=edges,
            summaries=summaries,
            pending_calls=pending_calls,
        )
        visitor.visit(tree)

    resolve_pending_calls(pending_calls, function_index, nodes, edges, summaries)
    stats = compute_variable_stats(nodes, edges, summaries)

    var_attr_count = sum(
        1 for node in nodes.values() if node.kind in {NODE_VARIABLE, NODE_ATTRIBUTE}
    )
    summary = {
        "file_count": len(file_paths),
        "function_count": sum(
            1 for node in nodes.values() if node.kind == NODE_FUNCTION
        ),
        "variable_count": sum(
            1 for node in nodes.values() if node.kind == NODE_VARIABLE
        ),
        "attribute_count": sum(
            1 for node in nodes.values() if node.kind == NODE_ATTRIBUTE
        ),
        "edge_count": len(edges),
        "stats_count": len(stats),
        "node_count": len(nodes),
        "var_attr_count": var_attr_count,
    }
    return VariableLineageResult(
        nodes=nodes,
        edges=edges,
        summaries=summaries,
        stats=stats,
        summary=summary,
    )


def variable_lineage_json_path(html_output_path: Path) -> Path:
    return html_output_path.with_name("variable-lineage.json")


def write_variable_lineage_json(path: Path, result: VariableLineageResult) -> None:
    payload = {
        "summary": result.summary,
        "nodes": [
            {
                "id": node.id,
                "kind": node.kind,
                "name": node.name,
                "scope": node.scope,
                "module": node.module,
                "lineno": node.lineno,
                "col_offset": node.col_offset,
                "file": node.file,
            }
            for node in sorted(result.nodes.values(), key=lambda item: item.id)
        ],
        "edges": [
            {
                "source": edge.source,
                "target": edge.target,
                "kind": edge.kind,
                "lineno": edge.lineno,
                "col_offset": edge.col_offset,
                "function_id": edge.function_id,
                "file": edge.file,
            }
            for edge in result.edges
        ],
        "summaries": {
            key: {
                "function_id": summary.function_id,
                "name": summary.name,
                "qualname": summary.qualname,
                "module": summary.module,
                "file": summary.file,
                "lineno": summary.lineno,
                "parameters": summary.parameters,
                "definitions": summary.definitions,
                "reads": summary.reads,
                "writes": summary.writes,
                "assignments": summary.assignments,
                "calls": summary.calls,
                "returns": summary.returns,
                "mutations": summary.mutations,
                "derivations": summary.derivations,
            }
            for key, summary in sorted(result.summaries.items())
        },
        "stats": [
            {
                "node_id": item.node_id,
                "kind": item.kind,
                "name": item.name,
                "scope": item.scope,
                "function_count": item.function_count,
                "read_count": item.read_count,
                "mutation_count": item.mutation_count,
                "derived_count": item.derived_count,
                "write_count": item.write_count,
                "enclosing_functions": list(item.enclosing_functions),
                "derivatives": list(item.derivatives),
            }
            for item in result.stats
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def render_variable_lineage_panel(
    result: VariableLineageResult,
    *,
    row_limit: int = 200,
) -> str:
    """Render the HTML section for variable lineage statistics."""
    rows = result.stats[: max(0, row_limit)]
    table_rows: list[str] = []
    for item in rows:
        table_rows.append(
            "<tr>"
            f"<td><code>{html.escape(item.node_id)}</code></td>"
            f"<td>{html.escape(item.kind)}</td>"
            f"<td>{item.function_count}</td>"
            f"<td>{item.read_count}</td>"
            f"<td>{item.mutation_count}</td>"
            f"<td>{item.derived_count}</td>"
            f"<td>{html.escape(_truncate_list(item.derivatives))}</td>"
            f"<td>{html.escape(_truncate_list(item.enclosing_functions))}</td>"
            "</tr>"
        )
    if not table_rows:
        table_body = (
            '<tr><td colspan="8" class="empty">No variables or attributes found.</td></tr>'
        )
    else:
        table_body = "\n".join(table_rows)

    summary = result.summary
    truncated_note = ""
    if len(result.stats) > row_limit:
        truncated_note = (
            f" Showing {row_limit} of {len(result.stats)} rows"
            " (full stats in variable-lineage.json)."
        )

    return f"""
  <section class="variable-lineage" aria-label="Variable lineage">
    <h2>Variable lineage</h2>
    <p class="meta">
      AST-scoped Name/Attribute usage for later resource/key-point detection.
      Sorted by function_count, derived_count, mutation_count, read_count.
      {html.escape(truncated_note.strip())}
    </p>
    <div class="stats">
      <div>variables: {summary.get("variable_count", 0)}</div>
      <div>attributes: {summary.get("attribute_count", 0)}</div>
      <div>functions: {summary.get("function_count", 0)}</div>
      <div>edges: {summary.get("edge_count", 0)}</div>
      <div>stats rows: {len(result.stats)}</div>
    </div>
    <table class="lineage-table" id="lineage-table">
      <thead>
        <tr>
          <th>node</th>
          <th>kind</th>
          <th>functions</th>
          <th>reads</th>
          <th>mutations</th>
          <th>derived</th>
          <th>derivatives</th>
          <th>enclosing functions</th>
        </tr>
      </thead>
      <tbody>
        {table_body}
      </tbody>
    </table>
  </section>
"""
