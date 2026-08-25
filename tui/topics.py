"""Topic file discovery, loading, and prompt embedding."""

from __future__ import annotations

from pathlib import Path

TOPIC_DIR = "topic_files"
TOPIC_START = "BEGIN_DAEDALUS_TOPIC"
TOPIC_END = "END_DAEDALUS_TOPIC"
# Select value for no topic; empty string can collide with Textual Select.BLANK.
TOPIC_NONE_VALUE = "__none__"

REQUIRED_HEADINGS = ("## Topic Goal", "## Topic Status", "## State Log")


def list_topic_slugs(project_root: Path) -> list[str]:
    """Return sorted topic filename stems from ``topic_files/*.md``."""
    directory = project_root / TOPIC_DIR
    if not directory.is_dir():
        return []
    slugs: list[str] = []
    try:
        entries = directory.iterdir()
    except OSError:
        return []
    for path in entries:
        if path.is_file() and path.suffix == ".md" and path.stem:
            slugs.append(path.stem)
    return sorted(slugs)


def topic_path(project_root: Path, slug: str) -> Path:
    """Resolve ``topic_files/{slug}.md`` under the project checkout."""
    return project_root / TOPIC_DIR / f"{slug}.md"


def load_topic_text(project_root: Path, slug: str) -> str | None:
    """Load topic markdown for ``slug``, or ``None`` when missing/unreadable."""
    cleaned = slug.strip()
    if not cleaned or cleaned == TOPIC_NONE_VALUE:
        return None
    path = topic_path(project_root, cleaned)
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None


def topic_select_options(project_root: Path) -> list[tuple[str, str]]:
    """Build Select options: ``(None)`` plus each discovered topic slug."""
    options: list[tuple[str, str]] = [("(None)", TOPIC_NONE_VALUE)]
    for slug in list_topic_slugs(project_root):
        options.append((slug, slug))
    return options


def validate_topic_markdown(text: str) -> list[str]:
    """Return missing required headings; empty list means structurally complete."""
    missing: list[str] = []
    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            missing.append(heading.removeprefix("## ").strip())
    return missing


def build_topic_instructions(mode: str) -> str:
    """Mode-specific rules for using an embedded topic file."""
    shared = (
        "When a topic is tagged, treat the embedded topic markdown as the shared "
        "umbrella context for this task.\n"
        "- **State Log** is the shared recurrent memory across related tasks: "
        "append one concise, generalized, topic-scoped summary per completed "
        "coding contribution (similar to a feature State Log entry, but shorter "
        "and umbrella-focused).\n"
        "- **Topic Goal** is immutable unless the user explicitly asks to change it.\n"
        "- **Topic Status** stays minimal: use only `open` or `complete`. Put "
        "tallies or detailed progress in the State Log if needed.\n"
        "Write updates into the worktree topic file "
        f"`{TOPIC_DIR}/{{slug}}.md` when allowed for this mode."
    )
    if mode in {"ask", "plan"}:
        return (
            f"{shared}\n"
            "This mode is read-only for topic files: do not modify Topic Goal, "
            "Topic Status, or the State Log."
        )
    if mode == "coding":
        return (
            f"{shared}\n"
            "After completing this coding task, append one State Log entry "
            "summarizing the topic-level outcome. You may set Topic Status to "
            "`open` or `complete` when the umbrella outcome changes."
        )
    # repair / integrating (resolver)
    return (
        f"{shared}\n"
        "Re-use the tagged topic for context. Adjust Topic Status or append a "
        "State Log entry only when the repair or resolution materially changes "
        "the topic-level outcome; prefer a single concise coding-completion "
        "style entry rather than one entry per repair attempt."
    )


def embed_topic(topic_text: str, mode: str) -> str:
    """Wrap topic markdown and instructions for inline prompt injection."""
    instructions = build_topic_instructions(mode)
    return (
        f"{TOPIC_START}\n"
        "The following topic is tagged on this task and has already been supplied "
        "inline. Apply it directly; do not open the topic file merely to read it "
        "again. Write allowed updates into the worktree topic file.\n"
        "--- TOPIC CONTENT START ---\n"
        f"{topic_text.rstrip()}\n"
        "--- TOPIC CONTENT END ---\n"
        "--- TOPIC INSTRUCTIONS ---\n"
        f"{instructions}\n"
        f"{TOPIC_END}\n"
    )
