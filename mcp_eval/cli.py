from __future__ import annotations

import argparse
from pathlib import Path

from mcp_eval.adapters.anthropic_adapter import AnthropicAdapter
from mcp_eval.adapters.google_adapter import GoogleAdapter
from mcp_eval.adapters.mock import MockModelAdapter
from mcp_eval.adapters.openai_adapter import OpenAIAdapter
from mcp_eval.mock_servers.postgres import SyntheticPostgresServer
from mcp_eval.results import write_results
from mcp_eval.runner import Runner
from mcp_eval.schemas import TaskSpec
from mcp_eval.task_loader import load_tasks


def _build_adapter(model: str):
    if model == "mock":
        return MockModelAdapter()
    if model.startswith("openai:"):
        return OpenAIAdapter(model=model)
    if model.startswith("anthropic:"):
        return AnthropicAdapter(model=model)
    if model.startswith("google:"):
        return GoogleAdapter(model=model)
    raise ValueError(f"Unknown model '{model}'.")


def _build_context(task: TaskSpec) -> tuple[list[dict], dict]:
    if task.server != "synthetic_postgres":
        raise ValueError(f"Unsupported server '{task.server}'")
    pg = SyntheticPostgresServer(seed=task.seed)
    oracle = pg.oracle_recent_and_inactive(signup_days=7, inactive_days=7)
    return pg.tool_specs(), {"oracle": oracle}


def run(model: str, tasks: str, out_dir: str) -> None:
    task_specs = load_tasks(Path(tasks))
    adapter = _build_adapter(model)
    runner = Runner(adapter)

    outcomes = []
    for task in task_specs:
        tool_specs, context = _build_context(task)
        outcomes.append(runner.run_task(task, tool_specs=tool_specs, context=context))

    out_path = write_results(outcomes, out_dir=out_dir)
    success_rate = sum(1 for o in outcomes if o.success) / max(1, len(outcomes))

    print(f"Completed {len(outcomes)} task(s).")
    print(f"Success rate: {success_rate:.2%}")
    print(f"Results: {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="mcp-eval CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    run_parser = sub.add_parser("run", help="Run tasks")
    run_parser.add_argument("--model", default="mock")
    run_parser.add_argument("--tasks", default="tasks/core")
    run_parser.add_argument("--out-dir", default="runs")

    args = parser.parse_args()
    if args.command == "run":
        run(model=args.model, tasks=args.tasks, out_dir=args.out_dir)


if __name__ == "__main__":
    main()
