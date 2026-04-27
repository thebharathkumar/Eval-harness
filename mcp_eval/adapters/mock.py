from __future__ import annotations

from mcp_eval.adapters.base import AdapterResponse, ModelAdapter


class MockModelAdapter(ModelAdapter):
    name = "mock"

    def run_task(self, *, prompt: str, tool_specs: list[dict[str, object]], context: dict[str, object]) -> AdapterResponse:
        oracle = context["oracle"]
        return AdapterResponse(
            final_answer=str(oracle["final_answer"]),
            tool_calls=list(oracle["tool_calls"]),
            trace=[{"role": "user", "content": prompt}, {"role": "assistant", "content": oracle["final_answer"]}],
            estimated_cost_usd=0.0,
            total_latency_ms=3,
        )
