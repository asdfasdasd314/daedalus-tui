import unittest

from tui.prompts import build_repair_prompt, build_resolver_prompt, build_task_prompt


class PromptTests(unittest.TestCase):
    def test_task_prompt_assigns_git_ownership_to_orchestrator(self):
        prompt = build_task_prompt("Build the feature")
        self.assertIn("leave them in the worktree", prompt)
        self.assertIn("orchestration layer owns all file staging, commits, merges, graph refreshes, and cleanup", prompt)
        self.assertIn("Do not run git add, git commit, git merge, git push, or switch branches", prompt)
        self.assertIn("Do not run graphify", prompt)

    def test_task_prompt_embeds_profile_after_user_prompt_and_before_constraints(self):
        profile = "CODING_PROFILE_SENTINEL\nUse the repository's feature files."

        prompt = build_task_prompt("Build the feature", profile_text=profile)

        self.assertIn(profile, prompt)
        self.assertIn("BEGIN_DAEDALUS_PROFILE", prompt)
        self.assertIn("Apply it directly; do not open the profile file merely to read it again", prompt)
        self.assertLess(prompt.index(profile), prompt.index("Make the requested file changes"))
        self.assertLess(prompt.index("Make the requested file changes"), prompt.index("Do not run graphify"))

    def test_plan_repair_and_resolver_prompts_embed_distinct_profiles(self):
        prompts = (
            build_task_prompt("Plan the feature", "plan", profile_text="PLANNING_PROFILE_SENTINEL"),
            build_repair_prompt("Original", "Failure", 1, 3, profile_text="REPAIR_PROFILE_SENTINEL"),
            build_resolver_prompt("Original", "Failure", 1, 3, profile_text="RESOLVER_PROFILE_SENTINEL"),
        )

        for prompt, profile in zip(
            prompts,
            ("PLANNING_PROFILE_SENTINEL", "REPAIR_PROFILE_SENTINEL", "RESOLVER_PROFILE_SENTINEL"),
        ):
            self.assertIn(profile, prompt)
            self.assertLess(prompt.index(profile), prompt.index("Do not run git add"))

    def test_missing_profile_preserves_prompt_without_a_file_pointer(self):
        prompt = build_task_prompt("Build the feature", profile_text=None)

        self.assertNotIn("BEGIN_DAEDALUS_PROFILE", prompt)
        self.assertNotIn(".agents/profiles", prompt)

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
        self.assertIn("BEGIN_DAEDALUS_PLAN", plan)
        self.assertIn("no_more_questions", plan)
        self.assertIn('(Recommended)', plan)
        self.assertIn("exactly one option as the recommended default", plan)
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

    def test_topic_embeds_for_coding_plan_ask_repair_and_resolver(self):
        topic = (
            "# Sample Topic\n\n## Topic Goal\nWhy\n\n## Topic Status\nopen\n\n"
            "## State Log\n- 2026-08-24: Started.\n"
        )
        coding = build_task_prompt("Build", "coding", topic_text=topic)
        plan = build_task_prompt("Design", "plan", topic_text=topic)
        ask = build_task_prompt("Explain", "ask", topic_text=topic)
        repair = build_repair_prompt("Original", "Failure", 1, 3, topic_text=topic)
        resolver = build_resolver_prompt("Original", "Failure", 1, 3, topic_text=topic)

        for prompt in (coding, plan, ask, repair, resolver):
            self.assertIn("BEGIN_DAEDALUS_TOPIC", prompt)
            self.assertIn("Sample Topic", prompt)
            self.assertIn("TOPIC INSTRUCTIONS", prompt)

        self.assertIn("append one State Log entry", coding)
        self.assertIn("read-only for topic files", plan)
        self.assertIn("read-only for topic files", ask)
        self.assertIn("repair or resolution materially changes", repair)
        self.assertIn("repair or resolution materially changes", resolver)

    def test_untagged_prompts_omit_topic_blocks(self):
        for prompt in (
            build_task_prompt("Build"),
            build_task_prompt("Design", "plan"),
            build_task_prompt("Explain", "ask"),
            build_repair_prompt("Original", "Failure", 1, 3),
            build_resolver_prompt("Original", "Failure", 1, 3),
        ):
            self.assertNotIn("BEGIN_DAEDALUS_TOPIC", prompt)
            self.assertNotIn("topic_files", prompt)


if __name__ == "__main__":
    unittest.main()
