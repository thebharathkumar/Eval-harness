from __future__ import annotations

from mcp_eval.schemas import TaskOutcome, TaskSpec


def grade(task: TaskSpec, outcome: TaskOutcome) -> TaskOutcome:
    expected = str(task.grading.expected_output.get("final_answer", "")).strip()
    actual = outcome.final_answer.strip()

    if actual != expected:
        outcome.success = False
        outcome.failure_code = "F13_WRONG_FINAL_ANSWER"
        return outcome

    used_tools = [c.tool_name for c in outcome.tool_calls]
    must_include = task.grading.tool_constraints.must_include
    if any(t not in used_tools for t in must_include):
        outcome.success = False
        outcome.failure_code = "F2_WRONG_TOOL_SELECTION"
        return outcome

    if len(used_tools) < task.grading.tool_constraints.min_tool_calls:
        outcome.success = False
        outcome.failure_code = "F7_PREMATURE_FINALIZATION"
        return outcome

    outcome.success = True
    outcome.failure_code = None
    return outcome
