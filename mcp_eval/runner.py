from __future__ import annotations

from mcp_eval.adapters.base import ModelAdapter
from mcp_eval.grader import grade
from mcp_eval.schemas import TaskOutcome, TaskSpec, ToolCallRecord


class Runner:
    def __init__(self, adapter: ModelAdapter) -> None:
        self.adapter = adapter

    def run_task(self, task: TaskSpec, tool_specs: list[dict], context: dict) -> TaskOutcome:
        resp = self.adapter.run_task(prompt=task.user_prompt, tool_specs=tool_specs, context=context)
        records = [ToolCallRecord(**x) for x in resp.tool_calls]
        outcome = TaskOutcome(
            task_id=task.id,
            model=self.adapter.name,
            success=False,
            turns=max(1, len(records) + 1),
            total_latency_ms=resp.total_latency_ms,
            estimated_cost_usd=resp.estimated_cost_usd,
            tool_calls=records,
            final_answer=resp.final_answer,
            raw_trace=resp.trace,
        )
        return grade(task, outcome)
