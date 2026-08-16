import unittest

from tui.prompts import build_repair_prompt, build_resolver_prompt, build_task_prompt


class PromptTests(unittest.TestCase):
    def test_task_prompt_assigns_git_ownership_to_orchestrator(self):
        prompt = build_task_prompt("Build the feature")
        self.assertIn("leave them in the worktree", prompt)
        self.assertIn("orchestration layer owns all file staging, commits, merges, graph refreshes, and cleanup", prompt)
        self.assertIn("Do not run git add, git commit, git merge, git push, or switch branches", prompt)
        self.assertIn("Do not run graphify", prompt)

    def test_repair_and_resolver_prompts_forbid_agent_git_operations(self):
        for prompt in (
            build_repair_prompt("Original", "Failure", 1, 3),
            build_resolver_prompt("Original", "Failure", 1, 3),
        ):
            self.assertIn("Do not run git add, git commit, git merge, git push, or switch branches", prompt)
            self.assertIn("orchestration layer", prompt)
            self.assertIn("Do not run graphify", prompt)

    def test_ask_and_plan_modes_are_read_only(self):
        ask = build_task_prompt("Explain this", "ask")
        plan = build_task_prompt("Design this", "plan")
        self.assertIn("TASK_MODE: ask", ask)
        self.assertIn("read-only context", ask)
        self.assertIn("TASK_MODE: plan", plan)
        self.assertIn("implementation plan", plan)
        self.assertIn("Do not modify files", ask)
        self.assertIn("Do not modify files", plan)

    def test_resumed_prompt_explains_existing_work_and_omits_empty_notes_section(self):
        without_notes = build_task_prompt("Continue", resumed=True)
        with_notes = build_task_prompt(
            "Continue",
            resume_notes=("The API already exists in app/api/client.py.",),
            resumed=True,
        )

        self.assertIn("resumption of work already started", without_notes)
        self.assertIn("git status and git diff", without_notes)
        self.assertNotIn("Additional notes from the user", without_notes)
        self.assertIn("Additional notes from the user", with_notes)
        self.assertIn("The API already exists in app/api/client.py.", with_notes)


if __name__ == "__main__":
    unittest.main()
