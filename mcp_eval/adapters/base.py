from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class AdapterResponse:
    final_answer: str
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    trace: list[dict[str, Any]] = field(default_factory=list)
    estimated_cost_usd: float = 0.0
    total_latency_ms: int = 0


class ModelAdapter(ABC):
    name: str

    @abstractmethod
    def run_task(self, *, prompt: str, tool_specs: list[dict[str, Any]], context: dict[str, Any]) -> AdapterResponse:
        raise NotImplementedError
