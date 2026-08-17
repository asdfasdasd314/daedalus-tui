"""Structured plan review data exchanged between the agent and the TUI."""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any


PLAN_START = "BEGIN_DAEDALUS_PLAN"
PLAN_END = "END_DAEDALUS_PLAN"


@dataclass(frozen=True)
class PlanOption:
    option_id: str
    label: str


@dataclass(frozen=True)
class PlanQuestion:
    question_id: str
    text: str
    options: tuple[PlanOption, ...]
    required: bool = True


@dataclass(frozen=True)
class PlanResult:
    plan: str
    questions: tuple[PlanQuestion, ...]
    no_more_questions: bool
    valid: bool = True
    error: str | None = None


def parse_plan_response(response: str) -> PlanResult:
    """Extract the agent's plan payload without exposing protocol text in the UI."""
    payload_text = _payload_text(response)
    if payload_text is None:
        return PlanResult(response.strip(), (), False, valid=False, error="Plan response was not in the required format.")
    try:
        payload = json.loads(payload_text)
    except json.JSONDecodeError as error:
        return PlanResult(
            response.strip(),
            (),
            False,
            valid=False,
            error=f"Plan response was not valid JSON: {error.msg}.",
        )
    if not isinstance(payload, dict):
        return PlanResult(response.strip(), (), False, valid=False, error="Plan payload must be a JSON object.")

    plan = payload.get("plan")
    raw_questions = payload.get("questions", [])
    no_more_questions = payload.get("no_more_questions")
    if not isinstance(plan, str) or not plan.strip():
        return PlanResult(response.strip(), (), False, valid=False, error="Plan payload is missing a plan.")
    if not isinstance(raw_questions, list) or not isinstance(no_more_questions, bool):
        return PlanResult(
            plan.strip(),
            (),
            False,
            valid=False,
            error="Plan payload must include questions and no_more_questions.",
        )

    questions: list[PlanQuestion] = []
    try:
        for raw_question in raw_questions:
            questions.append(_parse_question(raw_question))
    except ValueError as error:
        return PlanResult(plan.strip(), (), False, valid=False, error=str(error))
    return PlanResult(plan.strip(), tuple(questions), no_more_questions)


def build_plan_followup_prompt(
    original_prompt: str,
    plan: str,
    questions: tuple[PlanQuestion, ...],
    answers: dict[str, str],
) -> str:
    answer_lines = []
    question_by_id = {question.question_id: question for question in questions}
    for question_id, answer_id in answers.items():
        question = question_by_id.get(question_id)
        if question is None:
            continue
        option = next((option for option in question.options if option.option_id == answer_id), None)
        answer_lines.append(f"- {question.text}: {option.label if option else answer_id}")
    answers_text = "\n".join(answer_lines) or "(No answers were supplied.)"
    return (
        "Re-evaluate the plan using the user's answers below. Preserve the original request and "
        "return the exact structured plan format from your planning instructions. Ask another "
        "multiple-choice question if any decision is still required. Set no_more_questions to "
        "true only when you have no remaining questions that could change the implementation. "
        "Do not modify files.\n\n"
        f"Original request:\n{original_prompt}\n\n"
        f"Current plan:\n{plan}\n\n"
        f"User answers:\n{answers_text}"
    )


def build_implementation_prompt(
    original_prompt: str,
    plan: str,
    answers: dict[str, str],
) -> str:
    answer_text = "\n".join(f"- {question_id}: {answer}" for question_id, answer in answers.items())
    return (
        f"Original user request:\n{original_prompt}\n\n"
        f"Approved implementation plan:\n{plan}\n\n"
        "Decisions confirmed during plan review:\n"
        f"{answer_text or '- No additional decisions were required.'}\n\n"
        "Implement the approved plan in this worktree. Do not reopen plan review unless a blocking "
        "technical problem makes the plan impossible; in that case explain the problem clearly."
    )


def _payload_text(response: str) -> str | None:
    start = response.find(PLAN_START)
    if start >= 0:
        start += len(PLAN_START)
        end = response.find(PLAN_END, start)
        return response[start:end if end >= 0 else len(response)].strip()
    fenced_start = response.find("```")
    if fenced_start >= 0:
        content_start = response.find("\n", fenced_start)
        fenced_end = response.find("```", content_start + 1) if content_start >= 0 else -1
        if content_start >= 0 and fenced_end >= 0:
            return response[content_start + 1 : fenced_end].strip()
    object_start = response.find("{")
    object_end = response.rfind("}")
    if object_start >= 0 and object_end > object_start:
        return response[object_start : object_end + 1].strip()
    return None


def _parse_question(raw_question: Any) -> PlanQuestion:
    if not isinstance(raw_question, dict):
        raise ValueError("Each plan question must be an object.")
    question_id = raw_question.get("id")
    text = raw_question.get("question")
    raw_options = raw_question.get("options")
    if not isinstance(question_id, str) or not question_id.strip():
        raise ValueError("Each plan question needs an id.")
    if not isinstance(text, str) or not text.strip():
        raise ValueError(f"Plan question {question_id!r} needs question text.")
    if not isinstance(raw_options, list) or len(raw_options) < 2:
        raise ValueError(f"Plan question {question_id!r} needs at least two options.")
    options = []
    for raw_option in raw_options:
        if not isinstance(raw_option, dict):
            raise ValueError(f"Plan question {question_id!r} has an invalid option.")
        option_id = raw_option.get("id")
        label = raw_option.get("label")
        if not isinstance(option_id, str) or not option_id.strip() or not isinstance(label, str) or not label.strip():
            raise ValueError(f"Plan question {question_id!r} has an invalid option.")
        options.append(PlanOption(option_id.strip(), label.strip()))
    required = raw_question.get("required", True)
    if not isinstance(required, bool):
        raise ValueError(f"Plan question {question_id!r} has an invalid required value.")
    return PlanQuestion(question_id.strip(), text.strip(), tuple(options), required)
