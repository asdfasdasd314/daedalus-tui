"""Topic file discovery, creation, loading, and prompt embedding."""

from __future__ import annotations

from pathlib import Path
import re
import tomllib

TOPIC_DIR = "topic_files"
TOPIC_START = "BEGIN_DAEDALUS_TOPIC"
TOPIC_END = "END_DAEDALUS_TOPIC"
# Select value for no topic; empty string can collide with Textual Select.BLANK.
TOPIC_NONE_VALUE = "__none__"
PARAMETER_PATH = Path(__file__).resolve().parents[1] / "parameter_files" / "daedalus-tui-topics.toml"

REQUIRED_HEADINGS = ("## Topic Goal", "## Topic Status", "## State Log")
TOPIC_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 -]*$")


def load_topic_settings() -> dict:
    """Load tunable limits for topic creation from the paired parameter file."""
    with PARAMETER_PATH.open("rb") as source:
        return tomllib.load(source)


def validate_topic_name(topic_name: object, maximum_length: int) -> str:
    """Return a display name suitable for an H1 and a filesystem slug."""
    if not isinstance(topic_name, str):
        raise ValueError("Topic name must be a string.")
    normalized = " ".join(topic_name.strip().split())
    if not normalized:
        raise ValueError("Topic name is required.")
    if len(normalized) > maximum_length:
        raise ValueError(f"Topic name must be at most {maximum_length} characters.")
    if not TOPIC_NAME_PATTERN.fullmatch(normalized):
        raise ValueError("Use letters, numbers, spaces, and hyphens only for the topic name.")
    return normalized


def topic_slug_from_name(topic_name: str, maximum_length: int) -> str:
    """Convert a validated topic name to the filename stem used by the TUI."""
    slug = re.sub(r"[^a-z0-9]+", "-", topic_name.lower()).strip("-")
    if not slug:
        raise ValueError("Topic name must contain at least one letter or number.")
    if len(slug) > maximum_length:
        raise ValueError(f"Topic name produces a slug longer than {maximum_length} characters.")
    return slug


def build_topic_template(topic_name: str, topic_goal: str) -> str:
    """Build the initial markdown shape that the population agent will complete."""
    return (
        f"# {topic_name}\n\n"
        "## Topic Goal\n"
        f"{topic_goal.strip()}\n\n"
        "## Topic Status\n"
        "open\n\n"
        "## State Log\n"
        "- Topic initialized; the population agent should record the starting context and next steps.\n"
    )


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
