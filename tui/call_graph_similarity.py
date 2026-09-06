"""Semantic similarity scores for call-graph parent/child and sibling edges."""

from __future__ import annotations

import ast
import hashlib
import json
import math
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

_DOT_SPLIT = re.compile(r"\.+")
_UNDERSCORE_SPLIT = re.compile(r"_+")
_WORD_SPLIT = re.compile(r"[^a-z0-9_]+")
_EMBEDDING_BACKEND = "sklearn-tfidf"


@dataclass(frozen=True)
class SymbolContext:
    fqn: str
    short_name: str
    callers: tuple[str, ...]
    callees: tuple[str, ...]
    siblings: tuple[str, ...]
    doc: str


@dataclass(frozen=True)
class ScoredRelation:
    kind: str  # "parent_child" | "sibling"
    a: str
    b: str
    score: float
    shared_callers: tuple[str, ...] = ()


@dataclass(frozen=True)
class CandidateFeatureGroup:
    """A deterministic connected component of qualifying similarity relations."""

    feature_id: str
    members: tuple[str, ...]
    qualifying_relations: tuple[ScoredRelation, ...]
    relation_kinds: tuple[str, ...]
    score_stats: dict[str, Any]

    @property
    def id(self) -> str:
        """Return the stable identifier using the concise ``id`` spelling."""
        return self.feature_id

    @property
    def relations(self) -> tuple[ScoredRelation, ...]:
        """Compatibility alias for callers that refer to group relations directly."""
        return self.qualifying_relations


@dataclass
class SimilarityResult:
    relations: list[ScoredRelation]
    descriptors: dict[str, str] = field(default_factory=dict)
    mean_sibling_score: dict[str, float] = field(default_factory=dict)
    summary: dict[str, Any] = field(default_factory=dict)
    embedding_backend: str = _EMBEDDING_BACKEND
    feature_similarity_threshold: float = 0.55
    feature_grouping_mode: str = "undirected_qualifying_relations"
    candidate_features: list[CandidateFeatureGroup] = field(default_factory=list)


def short_name(fqn: str) -> str:
    return fqn.rsplit(".", 1)[-1]


def invert_edges(edges: dict[str, list[str]]) -> dict[str, list[str]]:
    callers: dict[str, set[str]] = defaultdict(set)
    for caller, callees in edges.items():
        for callee in callees:
            callers[callee].add(caller)
    return {name: sorted(parents) for name, parents in callers.items()}


def sibling_map(edges: dict[str, list[str]]) -> dict[str, set[str]]:
    """Symbols that share at least one common caller (excluding self)."""
    siblings: dict[str, set[str]] = defaultdict(set)
    for callees in edges.values():
        unique = sorted(set(callees))
        for name in unique:
            for peer in unique:
                if peer != name:
                    siblings[name].add(peer)
    return siblings


def shared_callers_for_pair(
    a: str,
    b: str,
    callers_of: dict[str, list[str]],
) -> tuple[str, ...]:
    return tuple(sorted(set(callers_of.get(a, [])) & set(callers_of.get(b, []))))


def _module_path_candidates(fqn: str, project_root: Path) -> list[Path]:
    """Best-effort map from FQN prefixes to Python module paths."""
    parts = fqn.split(".")
    candidates: list[Path] = []
    for length in range(len(parts) - 1, 0, -1):
        module_parts = parts[:length]
        file_path = project_root.joinpath(*module_parts).with_suffix(".py")
        package_init = project_root.joinpath(*module_parts, "__init__.py")
        if file_path.is_file():
            candidates.append(file_path)
        if package_init.is_file():
            candidates.append(package_init)
    return candidates


def _leading_comments(source_lines: list[str], lineno: int) -> str:
    """Collect contiguous `#` comments immediately above *lineno* (1-based)."""
    if lineno <= 1:
        return ""
    collected: list[str] = []
    index = lineno - 2
    while index >= 0:
        line = source_lines[index].rstrip()
        stripped = line.lstrip()
        if not stripped:
            if collected:
                break
            index -= 1
            continue
        if stripped.startswith("#"):
            collected.append(stripped[1:].strip())
            index -= 1
            continue
        break
    collected.reverse()
    return " ".join(collected)


def _doc_for_definition(node: ast.AST, source_lines: list[str]) -> str:
    docstring = ast.get_docstring(node) or ""
    lineno = getattr(node, "lineno", None)
    comments = _leading_comments(source_lines, lineno) if lineno else ""
    parts = [part for part in (docstring.strip(), comments.strip()) if part]
    return " ".join(parts)


def extract_docs_for_symbols(
    symbols: Iterable[str],
    project_root: Path,
    file_paths: list[Path] | None = None,
) -> dict[str, str]:
    """Extract docstring + leading comments for symbols when source is available."""
    project_root = project_root.resolve()
    docs: dict[str, str] = {}
    known_files = {path.resolve() for path in (file_paths or [])}

    # Cache parsed modules by path.
    parsed: dict[Path, tuple[ast.AST, list[str]]] = {}

    def load(path: Path) -> tuple[ast.AST, list[str]] | None:
        path = path.resolve()
        if path in parsed:
            return parsed[path]
        if known_files and path not in known_files and not path.is_file():
            return None
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            return None
        try:
            tree = ast.parse(text, filename=str(path))
        except SyntaxError:
            return None
        lines = text.splitlines()
        parsed[path] = (tree, lines)
        return parsed[path]

    for fqn in symbols:
        if fqn in docs:
            continue
        name = short_name(fqn)
        for candidate in _module_path_candidates(fqn, project_root):
            loaded = load(candidate)
            if loaded is None:
                continue
            tree, lines = loaded
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if node.name == name:
                        docs[fqn] = _doc_for_definition(node, lines)
                        break
            if fqn in docs:
                break
        docs.setdefault(fqn, "")
    return docs


def build_symbol_contexts(
    edges: dict[str, list[str]],
    all_nodes: set[str],
    project_root: Path,
    file_paths: list[Path] | None = None,
) -> dict[str, SymbolContext]:
    """Build per-symbol semantic context from uses-edges and source docs."""
    callers_of = invert_edges(edges)
    siblings_of = sibling_map(edges)
    symbols = set(all_nodes) | set(edges.keys()) | {c for cs in edges.values() for c in cs}
    docs = extract_docs_for_symbols(symbols, project_root, file_paths=file_paths)

    contexts: dict[str, SymbolContext] = {}
    for fqn in sorted(symbols):
        contexts[fqn] = SymbolContext(
            fqn=fqn,
            short_name=short_name(fqn),
            callers=tuple(callers_of.get(fqn, [])),
            callees=tuple(edges.get(fqn, [])),
            siblings=tuple(sorted(siblings_of.get(fqn, set()))),
            doc=docs.get(fqn, ""),
        )
    return contexts


def _format_name_list(names: Iterable[str], limit: int) -> str:
    items = list(names)
    if not items:
        return ""
    if len(items) > limit:
        shown = items[:limit]
        remaining = len(items) - limit
        return ", ".join(shown) + f", … (+{remaining} more)"
    return ", ".join(items)


def format_descriptor(
    context: SymbolContext,
    *,
    max_neighbors: int,
    omit: frozenset[str] | set[str] | None = None,
) -> str:
    """Format a stable descriptor using terminal names for graph peers."""
    omit = set(omit or ())
    callers = [name for name in context.callers if name not in omit]
    callees = [name for name in context.callees if name not in omit]
    siblings = [name for name in context.siblings if name not in omit]

    sections = [f"Symbol {context.short_name}."]
    callee_text = _format_name_list(
        (short_name(name) for name in callees),
        max_neighbors,
    )
    if callee_text:
        sections.append(f"Calls: {callee_text}.")
    caller_text = _format_name_list(
        (short_name(name) for name in callers),
        max_neighbors,
    )
    if caller_text:
        sections.append(f"Called by: {caller_text}.")
    sibling_text = _format_name_list(
        (short_name(name) for name in siblings),
        max_neighbors,
    )
    if sibling_text:
        sections.append(f"Siblings: {sibling_text}.")
    if context.doc.strip():
        sections.append(f"Docs: {context.doc.strip()}")
    return " ".join(sections)


def tokenize_descriptor(text: str) -> list[str]:
    """Lowercase and split identifiers on `.` / `_` while keeping word tokens."""
    tokens: list[str] = []
    for raw in text.split():
        lowered = raw.lower().strip(".,;:()[]{}\"'")
        if not lowered:
            continue
        # Keep the readable full token when it has alphanumeric content.
        if any(ch.isalnum() for ch in lowered):
            tokens.append(lowered)
        # Split FQNs on dots first so create_order survives from pkg.create_order,
        # then split remaining identifiers on underscores into fragments.
        for dotted in _DOT_SPLIT.split(lowered):
            if not dotted:
                continue
            if dotted != lowered:
                tokens.append(dotted)
            for underscored in _UNDERSCORE_SPLIT.split(dotted):
                if not underscored:
                    continue
                if underscored != dotted:
                    tokens.append(underscored)
                for fragment in _WORD_SPLIT.split(underscored):
                    if fragment and fragment != underscored:
                        tokens.append(fragment)
    return tokens


def _descriptor_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class DescriptorEmbedder:
    """Fit TF-IDF over symbol descriptors and score cosine similarity."""

    def __init__(self) -> None:
        self._vectorizer = TfidfVectorizer(
            analyzer=tokenize_descriptor,
            lowercase=False,
        )
        self._matrix = None
        self._index: dict[str, int] = {}
        self._cache: dict[str, Any] = {}
        self._fitted = False

    def fit(self, descriptors: dict[str, str]) -> None:
        ordered = sorted(descriptors.items())
        if not ordered:
            self._fitted = False
            return
        keys = [key for key, _ in ordered]
        texts = [text if text.strip() else key for _, text in ordered]
        self._matrix = self._vectorizer.fit_transform(texts)
        self._index = {key: i for i, key in enumerate(keys)}
        self._cache = {
            key: _descriptor_hash(text) for key, text in zip(keys, texts, strict=True)
        }
        self._fitted = True

    def cosine(self, a: str, b: str, descriptor_a: str, descriptor_b: str) -> float:
        if not self._fitted or self._matrix is None:
            return 0.0
        # Prefer matrix rows when descriptors match the fitted set.
        if (
            a in self._index
            and b in self._index
            and self._cache.get(a) == _descriptor_hash(descriptor_a)
            and self._cache.get(b) == _descriptor_hash(descriptor_b)
        ):
            score = float(
                cosine_similarity(self._matrix[self._index[a]], self._matrix[self._index[b]])[0, 0]
            )
        else:
            pair = self._vectorizer.transform([descriptor_a, descriptor_b])
            score = float(cosine_similarity(pair[0], pair[1])[0, 0])
        if math.isnan(score):
            return 0.0
        return max(0.0, min(1.0, score))


def _percentile(sorted_scores: list[float], pct: float) -> float | None:
    if not sorted_scores:
        return None
    if len(sorted_scores) == 1:
        return sorted_scores[0]
    rank = (len(sorted_scores) - 1) * (pct / 100.0)
    low = math.floor(rank)
    high = math.ceil(rank)
    if low == high:
        return sorted_scores[low]
    weight = rank - low
    return sorted_scores[low] * (1.0 - weight) + sorted_scores[high] * weight


def summarize_scores(relations: list[ScoredRelation]) -> dict[str, Any]:
    scores = sorted(relation.score for relation in relations)
    by_kind: dict[str, list[float]] = defaultdict(list)
    for relation in relations:
        by_kind[relation.kind].append(relation.score)

    def kind_summary(values: list[float]) -> dict[str, Any]:
        ordered = sorted(values)
        return {
            "count": len(ordered),
            "min": ordered[0] if ordered else None,
            "max": ordered[-1] if ordered else None,
            "mean": (sum(ordered) / len(ordered)) if ordered else None,
            "p25": _percentile(ordered, 25),
            "p50": _percentile(ordered, 50),
            "p75": _percentile(ordered, 75),
            "p90": _percentile(ordered, 90),
        }

    buckets = [0] * 10
    for score in scores:
        index = min(9, int(score * 10))
        buckets[index] += 1

    return {
        "count": len(scores),
        "min": scores[0] if scores else None,
        "max": scores[-1] if scores else None,
        "mean": (sum(scores) / len(scores)) if scores else None,
        "p25": _percentile(scores, 25),
        "p50": _percentile(scores, 50),
        "p75": _percentile(scores, 75),
        "p90": _percentile(scores, 90),
        "histogram_buckets": buckets,
        "by_kind": {kind: kind_summary(values) for kind, values in sorted(by_kind.items())},
    }


def candidate_feature_id(members: Iterable[str]) -> str:
    """Return a stable ID derived solely from a group's sorted member symbols."""
    ordered = tuple(sorted(set(members)))
    digest = hashlib.sha256("\0".join(ordered).encode("utf-8")).hexdigest()
    return f"feature-{digest[:16]}"


def group_candidate_features(
    relations: Iterable[ScoredRelation],
    *,
    threshold: float = 0.55,
) -> list[CandidateFeatureGroup]:
    """Group symbols connected by inclusive-threshold relations.

    Parent/child direction remains part of each relation, but connectivity is
    intentionally undirected so qualifying chains form one candidate feature.
    """
    ordered_relations = sorted(
        relations,
        key=lambda relation: (relation.kind, relation.a, relation.b, relation.score),
    )
    qualifying = [
        relation for relation in ordered_relations if relation.score >= threshold
    ]
    if not qualifying:
        return []

    parent: dict[str, str] = {}

    def find(symbol: str) -> str:
        root = parent.setdefault(symbol, symbol)
        while parent[root] != root:
            parent[root] = parent[parent[root]]
            root = parent[root]
        while parent[symbol] != symbol:
            next_symbol = parent[symbol]
            parent[symbol] = root
            symbol = next_symbol
        return root

    def union(left: str, right: str) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root == right_root:
            return
        # Lexicographic root choice makes the intermediate forest deterministic.
        if left_root < right_root:
            parent[right_root] = left_root
        else:
            parent[left_root] = right_root

    for relation in qualifying:
        union(relation.a, relation.b)

    members_by_root: dict[str, set[str]] = defaultdict(set)
    for symbol in parent:
        members_by_root[find(symbol)].add(symbol)

    groups: list[CandidateFeatureGroup] = []
    for members in members_by_root.values():
        ordered_members = tuple(sorted(members))
        if len(ordered_members) < 2:
            continue
        member_set = set(ordered_members)
        group_relations = tuple(
            relation
            for relation in qualifying
            if relation.a in member_set and relation.b in member_set
        )
        groups.append(
            CandidateFeatureGroup(
                feature_id=candidate_feature_id(ordered_members),
                members=ordered_members,
                qualifying_relations=group_relations,
                relation_kinds=tuple(sorted({r.kind for r in group_relations})),
                score_stats=summarize_scores(list(group_relations)),
            )
        )

    return sorted(groups, key=lambda group: group.members)


def score_relationships(
    contexts: dict[str, SymbolContext],
    edges: dict[str, list[str]],
    *,
    max_neighbors_in_descriptor: int = 20,
    max_sibling_pairs_per_parent: int = 50,
    feature_similarity_threshold: float = 0.55,
) -> SimilarityResult:
    """Score every unique parent→child edge and capped sibling pairs."""
    base_descriptors = {
        fqn: format_descriptor(ctx, max_neighbors=max_neighbors_in_descriptor)
        for fqn, ctx in contexts.items()
    }
    embedder = DescriptorEmbedder()
    embedder.fit(base_descriptors)

    callers_of = invert_edges(edges)
    relations: list[ScoredRelation] = []
    seen_parent_child: set[tuple[str, str]] = set()
    seen_siblings: set[tuple[str, str]] = set()

    for caller, callees in edges.items():
        unique_callees = sorted(set(callees))
        for callee in unique_callees:
            pair = (caller, callee)
            if pair in seen_parent_child:
                continue
            seen_parent_child.add(pair)
            ctx_a = contexts.get(caller)
            ctx_b = contexts.get(callee)
            if ctx_a is None or ctx_b is None:
                continue
            desc_a = format_descriptor(
                ctx_a,
                max_neighbors=max_neighbors_in_descriptor,
                omit=frozenset({callee}),
            )
            desc_b = format_descriptor(
                ctx_b,
                max_neighbors=max_neighbors_in_descriptor,
                omit=frozenset({caller}),
            )
            score = embedder.cosine(caller, callee, desc_a, desc_b)
            relations.append(
                ScoredRelation(kind="parent_child", a=caller, b=callee, score=score)
            )

        # Sibling pairs under this shared caller.
        pair_budget = max_sibling_pairs_per_parent
        for i, left in enumerate(unique_callees):
            for right in unique_callees[i + 1 :]:
                if pair_budget <= 0:
                    break
                key = (left, right) if left < right else (right, left)
                if key in seen_siblings:
                    continue
                seen_siblings.add(key)
                pair_budget -= 1
                ctx_a = contexts.get(left)
                ctx_b = contexts.get(right)
                if ctx_a is None or ctx_b is None:
                    continue
                desc_a = format_descriptor(
                    ctx_a,
                    max_neighbors=max_neighbors_in_descriptor,
                    omit=frozenset({right}),
                )
                desc_b = format_descriptor(
                    ctx_b,
                    max_neighbors=max_neighbors_in_descriptor,
                    omit=frozenset({left}),
                )
                score = embedder.cosine(left, right, desc_a, desc_b)
                shared = shared_callers_for_pair(left, right, callers_of)
                relations.append(
                    ScoredRelation(
                        kind="sibling",
                        a=key[0],
                        b=key[1],
                        score=score,
                        shared_callers=shared,
                    )
                )
            if pair_budget <= 0:
                break

    sibling_scores: dict[str, list[float]] = defaultdict(list)
    for relation in relations:
        if relation.kind != "sibling":
            continue
        sibling_scores[relation.a].append(relation.score)
        sibling_scores[relation.b].append(relation.score)

    mean_sibling = {
        name: sum(values) / len(values)
        for name, values in sibling_scores.items()
        if values
    }

    relations.sort(key=lambda relation: (relation.kind, relation.a, relation.b))

    return SimilarityResult(
        relations=relations,
        descriptors=base_descriptors,
        mean_sibling_score=mean_sibling,
        summary=summarize_scores(relations),
        embedding_backend=_EMBEDDING_BACKEND,
        feature_similarity_threshold=feature_similarity_threshold,
        candidate_features=group_candidate_features(
            relations,
            threshold=feature_similarity_threshold,
        ),
    )


def parent_child_score_map(relations: list[ScoredRelation]) -> dict[tuple[str, str], float]:
    return {
        (relation.a, relation.b): relation.score
        for relation in relations
        if relation.kind == "parent_child"
    }


def write_similarity_json(path: Path, result: SimilarityResult) -> None:
    def relation_payload(relation: ScoredRelation) -> dict[str, Any]:
        return {
            "kind": relation.kind,
            "a": relation.a,
            "b": relation.b,
            "score": relation.score,
            "shared_callers": list(relation.shared_callers),
        }

    payload = {
        "embedding_backend": result.embedding_backend,
        "summary": result.summary,
        "descriptors": result.descriptors,
        "mean_sibling_score": result.mean_sibling_score,
        "feature_similarity_threshold": result.feature_similarity_threshold,
        "feature_grouping_mode": result.feature_grouping_mode,
        "candidate_features": [
            {
                "feature_id": group.feature_id,
                "members": list(group.members),
                "relations": [
                    relation_payload(relation)
                    for relation in group.qualifying_relations
                ],
                "relation_kinds": list(group.relation_kinds),
                "score_stats": group.score_stats,
            }
            for group in result.candidate_features
        ],
        "relations": [relation_payload(relation) for relation in result.relations],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def score_band(score: float, low: float, high: float) -> str:
    if score >= high:
        return "high"
    if score <= low:
        return "low"
    return "mid"


def similarity_json_path(html_output_path: Path) -> Path:
    return html_output_path.with_name("edge-similarities.json")
