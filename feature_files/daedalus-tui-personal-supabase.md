# Daedalus TUI Personal Shared Supabase

## Summary
Opt-in registration that scaffolds a dedicated Postgres schema for a Daedalus-managed
target project inside one operator-owned shared Supabase database. Registration is
file-only (`supabase/` config + `CREATE SCHEMA` migration, `.env.example`, coding and
architecture profile guidance, and a `.daedalus` marker); orchestration continues to
own remote `supabase db push` after verification.

## Key Points
- **Shared database, per-project schema**: Schema identity is always the validated
  project slug. Apps share auth on the single Supabase project; agents must never
  default to `public`.
- **File-only register**: Writes durable project files only. Does not call the Supabase
  Management API or `supabase db push` at register time.
- **New Project opt-in**: One choice in the New Project backend selector; when selected,
  registration runs after template materialization and before the initial
  `git add`/`git commit`.
- **Existing-project action**: The task-bar Register Backend dialog runs the same helper
  against the selected project root (schema = project slug) when Supabase is chosen, and
  the control disables once the project is registered for a backend.
- **One backend per project**: The `.daedalus` marker records either a Supabase schema or
  a Firebase project id, so the TUI can tell which backend a project targets.
- **Agent teaching**: Idempotently appends a Personal Supabase Schema section to
  `.agents/profiles/coding.md` and `architecture.md` (no Cursor skill file).
- **Env placeholders**: Only the target project's `.env.example` gets shared URL/key
  placeholders plus `SUPABASE_SCHEMA=<slug>` and a Data API allow-list reminder.
- **Idempotency / conflicts**: Same-schema re-register is a no-op success; conflicting
  markers or foreign `supabase/migrations` content fail without mutating the tree.
- **Manual API exposure**: Operators must allow-list the schema in Supabase Dashboard
  Data API / PostgREST settings after the migration is applied remotely.
- **Orchestration boundary**: Existing `supabase_db_push_enabled` verify→push path is
  unchanged; this feature only materializes migrations when opted in.

## Relevant Files
- `tui/personal_supabase.py`: Registration helper, marker I/O, env/profile/migration scaffolding.
- `tui/project_initializer.py`: Optional `registerPersonalSupabase` flag wired pre-commit.
- `tui/app.py`: New Project backend selector and task-bar Register Backend dialog.
- `feature_files/daedalus-tui-firebase.md`: The sibling backend registration feature.
- `parameter_files/daedalus-tui-personal-supabase.toml`: Snippet version, env key names, migration filename.
- `tests/test_personal_supabase.py`, `tests/test_app.py`, `tests/test_project_initializer.py`: Coverage.

## Dev Mode
HACKING

## State Log
- 2026-09-15: Moved the New Project checkbox and task-bar button behind the shared backend selector that now also offers Firebase.
- 2026-09-13: Added file-only personal Supabase schema registration with New Project checkbox, task-bar button, profile guidance, and target `.env.example` placeholders.
