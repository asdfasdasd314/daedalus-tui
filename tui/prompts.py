"""Prompt wrappers used by task and resolver agents."""

from collections.abc import Sequence


def build_task_prompt(
    prompt: str,
    mode: str = "coding",
    resume_notes: Sequence[str] = (),
    resumed: bool = False,
) -> str:
    if mode == "ask":
        instructions = (
            "Answer the user's question using the repository as read-only context. "
            "Do not modify files or create generated artifacts."
        )
    elif mode == "plan":
        instructions = (
            "Inspect the repository and produce a clear implementation plan. "
            "Do not modify files or create generated artifacts."
        )
    elif mode == "coding":
        instructions = "Make the requested file changes and leave them in the worktree."
    else:
        raise ValueError(f"Unsupported task mode: {mode}")
    task_prompt = (
        f"TASK_MODE: {mode}\n\n"
        f"{prompt}\n\n"
        f"{instructions} Work only in this Git worktree. "
        "Do not run git add, git commit, git merge, git push, or switch branches. "
        "Do not run graphify, `graphify update`, or any graph refresh. "
        "The orchestration layer owns all file staging, commits, merges, graph refreshes, and cleanup."
    )
    if not resumed:
        return task_prompt

    continuation = (
        "This is a resumption of work already started in this existing worktree. "
        "Do not restart the task or discard work that is already present. "
        "First inspect the current state with git status and git diff, then continue "
        "from the existing implementation and make only the updates still needed."
    )
    cleaned_notes = [note.strip() for note in resume_notes if note.strip()]
    if cleaned_notes:
        continuation += "\n\nAdditional notes from the user:\n" + "\n\n".join(cleaned_notes)
    return f"{task_prompt}\n\n{continuation}"


def build_repair_prompt(original: str, failure: str, attempt: int, limit: int) -> str:
    return (
        "TASK_MODE: coding\n\n"
        "Repair the failing verification suite in this existing isolated Git worktree. "
        "Preserve the original task intent and make the smallest compatible fix. "
        "Do not run git add, git commit, git merge, git push, or switch branches. "
        "Do not run graphify, `graphify update`, or any graph refresh. "
        "Leave file changes in the worktree for the orchestration layer to stage, commit, and refresh.\n\n"
        f"Original task:\n{original}\n\n"
        f"Repair attempt: {attempt}/{limit}\n\n"
        f"Verification failure:\n{failure}"
    )


def build_resolver_prompt(original: str, failure: str, attempt: int, limit: int) -> str:
    return (
        "TASK_MODE: integrating\n\n"
        "Resolve the current integration failure in this existing Git worktree. "
        "Preserve the task intent, resolve conflicts or repair the failing checks, and run relevant checks. "
        "Do not run git add, git commit, git merge, git push, or switch branches. "
        "Do not run graphify, `graphify update`, or any graph refresh. "
        "Leave all resolutions in the worktree for the orchestration layer to stage, commit, and refresh.\n\n"
        f"Task goal:\n{original}\n\n"
        f"Resolver attempt: {attempt}/{limit}\n\n"
        f"Failure details:\n{failure}"
    )
