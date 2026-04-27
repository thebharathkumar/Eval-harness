from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Difficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


@dataclass
class ToolCallRecord:
    tool_name: str
    arguments: dict[str, Any] = field(default_factory=dict)
    ok: bool = True
    error_code: str | None = None
    latency_ms: int | None = None


@dataclass
class ExpectedToolConstraint:
    must_include: list[str] = field(default_factory=list)
    must_not_include: list[str] = field(default_factory=list)
    min_tool_calls: int = 1
    max_tool_calls: int = 20


@dataclass
class GradingSpec:
    method: str
    expected_output: dict[str, Any]
    tool_constraints: ExpectedToolConstraint


@dataclass
class TaskSpec:
    id: str
    title: str
    description: str
    category: str
    difficulty: Difficulty
    min_turns: int
    max_turns: int
    seed: int
    server: str
    tools: list[str]
    user_prompt: str
    grading: GradingSpec

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "TaskSpec":
        tc = ExpectedToolConstraint(**raw["grading"].get("tool_constraints", {}))
        grading = GradingSpec(
            method=raw["grading"].get("method", "programmatic"),
            expected_output=raw["grading"]["expected_output"],
            tool_constraints=tc,
        )
        return cls(
            id=raw["id"],
            title=raw["title"],
            description=raw["description"],
            category=raw["category"],
            difficulty=Difficulty(raw.get("difficulty", "medium")),
            min_turns=raw.get("min_turns", 3),
            max_turns=raw.get("max_turns", 12),
            seed=raw.get("seed", 42),
            server=raw["server"],
            tools=raw["tools"],
            user_prompt=raw["user_prompt"],
            grading=grading,
        )


@dataclass
class RunnerConfig:
    model: str
    tasks_path: str
    out_dir: str = "runs"
    max_parallel_tasks: int = 1


@dataclass
class TaskOutcome:
    task_id: str
    model: str
    success: bool
    turns: int
    total_latency_ms: int
    estimated_cost_usd: float
    tool_calls: list[ToolCallRecord]
    final_answer: str
    raw_trace: list[dict[str, Any]]
    failure_code: str | None = None


    def model_dump(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "model": self.model,
            "success": self.success,
            "failure_code": self.failure_code,
            "turns": self.turns,
            "total_latency_ms": self.total_latency_ms,
            "estimated_cost_usd": self.estimated_cost_usd,
            "tool_calls": [c.__dict__ for c in self.tool_calls],
            "final_answer": self.final_answer,
            "raw_trace": self.raw_trace,
        }
