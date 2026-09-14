"""File-only personal shared-Supabase schema registration for target projects."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import tomllib

from .project_config import DAEDALUS_CONFIG_FILENAME

TUI_ROOT = Path(__file__).resolve().parents[1]
PARAMETER_PATH = TUI_ROOT / "parameter_files" / "daedalus-tui-personal-supabase.toml"
PROFILE_RELATIVE_PATHS = (
    Path(".agents") / "profiles" / "coding.md",
    Path(".agents") / "profiles" / "architecture.md",
)
SECTION_TABLE = "personal_supabase"


def _validate_schema_name(schema: object, maximum_length: int) -> str:
    # Imported lazily to avoid a circular import with project_initializer.
    from .project_initializer import validate_project_name

    return validate_project_name(schema, maximum_length)


@dataclass(frozen=True)
class PersonalSupabaseStatus:
    """Registration marker loaded from a target project's ``.daedalus`` file."""

    registered: bool
    schema: str | None = None


@dataclass(frozen=True)
class RegistrationResult:
    """Outcome of scaffolding personal-Supabase files into a project tree."""

    status: str
    schema: str
    message: str
    project_root: Path
    already_registered: bool = False


def load_personal_supabase_settings() -> dict:
    """Load tunables for schema registration from the paired parameter file."""
    with PARAMETER_PATH.open("rb") as source:
        return tomllib.load(source)


def schema_from_project_root(project_root: Path, maximum_length: int | None = None) -> str:
    """Derive and validate the Postgres schema name from the project directory slug."""
    settings = load_personal_supabase_settings()
    limit = int(maximum_length if maximum_length is not None else settings["maximum_schema_name_length"])
    return _validate_schema_name(project_root.resolve().name, limit)


def load_personal_supabase_status(project_root: Path) -> PersonalSupabaseStatus:
    """Return the ``[personal_supabase]`` marker, or an unregistered default."""
    path = project_root / DAEDALUS_CONFIG_FILENAME
    if not path.is_file():
        return PersonalSupabaseStatus(registered=False)
    try:
        with path.open("rb") as source:
            values = tomllib.load(source)
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise ValueError(f"Could not read project configuration {path}: {error}") from error

    table = values.get(SECTION_TABLE, {})
    if table in (None, {}):
        return PersonalSupabaseStatus(registered=False)
    if not isinstance(table, dict):
        raise ValueError(f"{path} {SECTION_TABLE} must be a table.")

    registered = table.get("registered", False)
    if not isinstance(registered, bool):
        raise ValueError(f"{path} {SECTION_TABLE}.registered must be a boolean.")
    schema = table.get("schema")
    if schema is not None and (not isinstance(schema, str) or not schema.strip()):
        raise ValueError(f"{path} {SECTION_TABLE}.schema must be a non-empty string when set.")
    return PersonalSupabaseStatus(registered=registered, schema=schema.strip() if isinstance(schema, str) else None)


def is_personal_supabase_registered(project_root: Path, schema: str | None = None) -> bool:
    """True when the project is marked registered for ``schema`` (or any schema if omitted)."""
    try:
        status = load_personal_supabase_status(project_root)
    except ValueError:
        return False
    if not status.registered:
        return False
    if schema is None:
        return True
    return status.schema == schema


def register_personal_supabase(
    project_root: Path,
    schema: str | None = None,
) -> RegistrationResult:
    """Scaffold supabase files, env placeholders, profiles, and a ``.daedalus`` marker.

    Remote apply is intentionally out of scope; orchestration owns ``supabase db push``.
    """
    root = project_root.expanduser().resolve()
    settings = load_personal_supabase_settings()
    if schema is None:
        try:
            schema_name = schema_from_project_root(root)
        except ValueError as error:
            return RegistrationResult(
                status="failed",
                schema="",
                message=str(error),
                project_root=root,
            )
    else:
        try:
            schema_name = _validate_schema_name(
                schema,
                int(settings["maximum_schema_name_length"]),
            )
        except ValueError as error:
            return RegistrationResult(
                status="failed",
                schema=str(schema),
                message=str(error),
                project_root=root,
            )

    try:
        status = load_personal_supabase_status(root)
    except ValueError as error:
        return RegistrationResult(
            status="failed",
            schema=schema_name,
            message=str(error),
            project_root=root,
        )

    if status.registered and status.schema == schema_name:
        return RegistrationResult(
            status="success",
            schema=schema_name,
            message=f"Schema {schema_name!r} is already registered.",
            project_root=root,
            already_registered=True,
        )
    if status.registered and status.schema and status.schema != schema_name:
        return RegistrationResult(
            status="failed",
            schema=schema_name,
            message=(
                f"Project is already registered for schema {status.schema!r}; "
                f"refusing to register {schema_name!r}."
            ),
            project_root=root,
        )

    conflict = _supabase_layout_conflict(root, schema_name, settings)
    if conflict:
        return RegistrationResult(
            status="failed",
            schema=schema_name,
            message=conflict,
            project_root=root,
        )

    try:
        _ensure_supabase_scaffold(root, schema_name, settings)
        _ensure_env_example(root, schema_name, settings)
        _ensure_profile_guidance(root, schema_name, settings)
        _write_registration_marker(root, schema_name)
    except (OSError, ValueError) as error:
        return RegistrationResult(
            status="failed",
            schema=schema_name,
            message=str(error),
            project_root=root,
        )

    return RegistrationResult(
        status="success",
        schema=schema_name,
        message=f"Registered personal Supabase schema {schema_name!r}.",
        project_root=root,
    )


def profile_guidance_section(schema: str, settings: dict | None = None) -> str:
    """Return the markdown section appended to coding/architecture profiles."""
    values = settings or load_personal_supabase_settings()
    heading = str(values["profile_section_heading"])
    env_key = str(values["env_schema_key"])
    return (
        f"{heading}\n\n"
        f"This project uses a dedicated Postgres schema `{schema}` on the operator's "
        "shared personal Supabase database. Do **not** use the default `public` schema "
        "for application tables or migrations.\n\n"
        f"- Read the schema name from `{env_key}` in `.env` (expected value: `{schema}`).\n"
        f"- Qualify SQL, migrations, RLS policies, and client/API configuration for `{schema}`.\n"
        "- Never assume PostgREST or Supabase clients default to `public` for this app.\n"
        "- Auth is shared across apps on this Supabase project; reuse the existing auth setup.\n"
        "- Agents must not run `supabase db push`; orchestration owns remote migration apply "
        "after verification when `supabase/migrations/` changes.\n"
        "- After the first remote apply, the operator must allow-list this schema in the "
        "Supabase Dashboard Data API / PostgREST exposed-schemas settings.\n"
    )


def _supabase_layout_conflict(root: Path, schema: str, settings: dict) -> str | None:
    supabase = root / "supabase"
    if not supabase.exists():
        return None
    if not supabase.is_dir():
        return "A file named supabase exists; refusing to scaffold a directory."

    migrations = supabase / "migrations"
    if migrations.exists() and not migrations.is_dir():
        return "supabase/migrations exists but is not a directory."

    expected_name = str(settings["migration_filename"])
    if migrations.is_dir():
        foreign = []
        for path in sorted(migrations.glob("*.sql")):
            text = path.read_text(encoding="utf-8")
            owns_schema = _migration_creates_schema(text, schema)
            if path.name == expected_name and owns_schema:
                continue
            if owns_schema and path.name != expected_name:
                # Alternate filename still claiming this schema is acceptable.
                continue
            foreign.append(path.name)
        if foreign:
            return (
                "Existing supabase/migrations content is incompatible with personal "
                f"schema registration ({', '.join(foreign)})."
            )
    return None


def _migration_creates_schema(text: str, schema: str) -> bool:
    pattern = re.compile(
        rf'CREATE\s+SCHEMA\s+IF\s+NOT\s+EXISTS\s+"{re.escape(schema)}"\s*;',
        re.IGNORECASE,
    )
    return bool(pattern.search(text))


def _ensure_supabase_scaffold(root: Path, schema: str, settings: dict) -> None:
    supabase = root / "supabase"
    migrations = supabase / "migrations"
    migrations.mkdir(parents=True, exist_ok=True)

    config_path = supabase / "config.toml"
    if not config_path.exists():
        placeholder = str(settings["config_project_id_placeholder"])
        config_path.write_text(
            (
                "# Scaffolded by Daedalus personal Supabase registration.\n"
                "# Replace project_id with your shared Supabase project ref after linking.\n"
                "# Registration writes files only; orchestration runs `supabase db push`.\n"
                f'project_id = "{placeholder}"\n'
                "\n"
                "[api]\n"
                "# Exposed schemas for a shared project are allow-listed in the Supabase\n"
                "# Dashboard (Data API / PostgREST). Manually add this project's schema\n"
                "# after the CREATE SCHEMA migration is applied remotely.\n"
            ),
            encoding="utf-8",
        )

    migration_path = migrations / str(settings["migration_filename"])
    if not migration_path.exists():
        migration_path.write_text(
            (
                f"-- Personal shared Supabase schema for this Daedalus project.\n"
                f"-- Operators must allow-list \"{schema}\" in Supabase Data API settings.\n"
                f'CREATE SCHEMA IF NOT EXISTS "{schema}";\n'
                "\n"
                f'GRANT USAGE ON SCHEMA "{schema}" TO anon, authenticated, service_role;\n'
                f'GRANT ALL ON SCHEMA "{schema}" TO postgres, service_role;\n'
                f'ALTER DEFAULT PRIVILEGES IN SCHEMA "{schema}" '
                "GRANT ALL ON TABLES TO postgres, service_role;\n"
                f'ALTER DEFAULT PRIVILEGES IN SCHEMA "{schema}" '
                "GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO anon, authenticated;\n"
            ),
            encoding="utf-8",
        )
    elif not _migration_creates_schema(migration_path.read_text(encoding="utf-8"), schema):
        raise ValueError(
            f"{migration_path.name} exists but does not create schema {schema!r}."
        )


def _ensure_env_example(root: Path, schema: str, settings: dict) -> None:
    path = root / ".env.example"
    block = _env_example_block(schema, settings)
    if not path.exists():
        path.write_text(block, encoding="utf-8")
        return

    existing = path.read_text(encoding="utf-8")
    schema_key = str(settings["env_schema_key"])
    match = re.search(rf"(?m)^{re.escape(schema_key)}=(.*)$", existing)
    if match:
        current = match.group(1).strip()
        if current and current != schema:
            raise ValueError(
                f".env.example already sets {schema_key}={current!r}; "
                f"refusing to overwrite with {schema!r}."
            )
        if current == schema and "allow-list" in existing.lower():
            return
        # Keep other keys; refresh the schema line / ensure guidance when missing.
        updated = re.sub(
            rf"(?m)^{re.escape(schema_key)}=.*$",
            f"{schema_key}={schema}",
            existing,
            count=1,
        )
        if "allow-list" not in updated.lower():
            updated = updated.rstrip() + "\n\n" + _allow_list_comment(schema) + "\n"
        path.write_text(updated if updated.endswith("\n") else updated + "\n", encoding="utf-8")
        return

    path.write_text(existing.rstrip() + "\n\n" + block, encoding="utf-8")


def _env_example_block(schema: str, settings: dict) -> str:
    return (
        "# Shared personal Supabase project (fill in from the operator dashboard).\n"
        "# Never commit real keys; copy this file to .env locally.\n"
        f"{settings['env_url_key']}=\n"
        f"{settings['env_anon_key']}=\n"
        f"{settings['env_service_role_key']}=\n"
        "# Optional direct database URL for CLI workflows:\n"
        f"{settings['env_db_url_key']}=\n"
        "\n"
        "# Project-specific Postgres schema on the shared database (never use public).\n"
        f"{settings['env_schema_key']}={schema}\n"
        "\n"
        f"{_allow_list_comment(schema)}\n"
    )


def _allow_list_comment(schema: str) -> str:
    return (
        f"# After migrations apply, allow-list schema \"{schema}\" in Supabase Dashboard → "
        "Project Settings → Data API (PostgREST exposed schemas)."
    )


def _ensure_profile_guidance(root: Path, schema: str, settings: dict) -> None:
    section = profile_guidance_section(schema, settings)
    heading = str(settings["profile_section_heading"])
    for relative in PROFILE_RELATIVE_PATHS:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            if heading in text:
                if schema not in text.split(heading, 1)[1]:
                    raise ValueError(
                        f"{relative} already has a Personal Supabase Schema section "
                        f"that does not reference {schema!r}."
                    )
                continue
            path.write_text(text.rstrip() + "\n\n" + section, encoding="utf-8")
        else:
            path.write_text(section, encoding="utf-8")


def _write_registration_marker(root: Path, schema: str) -> None:
    path = root / DAEDALUS_CONFIG_FILENAME
    section = (
        f"[{SECTION_TABLE}]\n"
        "registered = true\n"
        f'schema = "{schema}"\n'
    )
    if not path.exists():
        path.write_text(section, encoding="utf-8")
        return

    text = path.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"(?ms)^\[{re.escape(SECTION_TABLE)}\]\n.*?(?=^\[|\Z)",
    )
    if pattern.search(text):
        updated = pattern.sub(section + "\n", text, count=1)
    else:
        updated = text.rstrip() + "\n\n" + section
    path.write_text(updated if updated.endswith("\n") else updated + "\n", encoding="utf-8")
