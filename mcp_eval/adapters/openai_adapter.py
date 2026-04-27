from __future__ import annotations

from mcp_eval.adapters.base import AdapterResponse, ModelAdapter


class OpenAIAdapter(ModelAdapter):
    name = "openai"

    def __init__(self, model: str) -> None:
        self.model = model

    def run_task(self, *, prompt: str, tool_specs: list[dict[str, object]], context: dict[str, object]) -> AdapterResponse:
        raise NotImplementedError(
            "OpenAI adapter wiring is intentionally deferred. Use model=mock for the initial end-to-end run."
        )
