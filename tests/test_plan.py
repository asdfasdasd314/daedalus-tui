import unittest

from tui.plan import (
    PLAN_END,
    PLAN_START,
    PlanOption,
    PlanQuestion,
    build_implementation_prompt,
    build_plan_followup_prompt,
    parse_plan_response,
)


class PlanTests(unittest.TestCase):
    def test_parser_extracts_only_plan_and_multiple_choice_questions(self):
        response = (
            "BEGIN_DAEDALUS_PLAN\n"
            '{"plan":"1. Add the API.\\n2. Test it.","questions":[{"id":"q1",'
            '"question":"Which store?","required":true,"options":['
            '{"id":"a","label":"SQLite"},{"id":"b","label":"JSON"}]}],'
            '"no_more_questions":false}\n'
            "END_DAEDALUS_PLAN"
        )

        result = parse_plan_response(response)

        self.assertTrue(result.valid)
        self.assertEqual(result.plan, "1. Add the API.\n2. Test it.")
        self.assertEqual(result.questions[0].text, "Which store?")
        self.assertEqual(result.questions[0].options[1], PlanOption("b", "JSON"))
        self.assertFalse(result.no_more_questions)

    def test_parser_requires_explicit_confirmation(self):
        result = parse_plan_response('{"plan":"Do it.","questions":[],"no_more_questions":false}')
        self.assertFalse(result.no_more_questions)
        self.assertFalse(parse_plan_response("plain markdown plan").valid)

    def test_parser_rejects_ambiguous_question_and_option_ids(self):
        duplicate_questions = (
            '{"plan":"Do it.","questions":[{"id":"q1","question":"First?","options":['
            '{"id":"a","label":"A"},{"id":"b","label":"B"}]},{"id":"q1",'
            '"question":"Second?","options":[{"id":"a","label":"A"},{"id":"b","label":"B"}]}],'
            '"no_more_questions":false}'
        )
        duplicate_options = (
            '{"plan":"Do it.","questions":[{"id":"q1","question":"Choose?","options":['
            '{"id":"a","label":"First"},{"id":"a","label":"Second"}]}],'
            '"no_more_questions":false}'
        )
        contradictory_confirmation = (
            '{"plan":"Do it.","questions":[{"id":"q1","question":"Choose?","options":['
            '{"id":"a","label":"First"},{"id":"b","label":"Second"}]}],'
            '"no_more_questions":true}'
        )

        self.assertFalse(parse_plan_response(duplicate_questions).valid)
        self.assertFalse(parse_plan_response(duplicate_options).valid)
        self.assertFalse(parse_plan_response(contradictory_confirmation).valid)

    def test_followup_and_implementation_prompts_include_review_context(self):
        question = PlanQuestion("q1", "Which store?", (PlanOption("a", "SQLite"), PlanOption("b", "JSON")))
        followup = build_plan_followup_prompt("Build it", "Use a store.", (question,), {"q1": "b"})
        implementation = build_implementation_prompt("Build it", "Use a store.", {"q1": "b"})

        self.assertIn("JSON", followup)
        self.assertIn("Approved implementation plan", implementation)
        self.assertIn("q1: b", implementation)


if __name__ == "__main__":
    unittest.main()
