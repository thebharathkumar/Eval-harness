# mcp-eval

`mcp-eval` is an open-source evaluation harness for measuring MCP tool-calling performance of LLMs.

## What exists in this scaffold

- YAML-on-disk task format (JSON-compatible YAML) with schema validation hooks.
- Deterministic synthetic Postgres mock server.
- Adapter interface with provider stubs and a mock adapter.
- Runner + grader + JSONL results writer.
- CLI entrypoint for end-to-end runs.

## Quickstart

```bash
uv sync
uv run mcp-eval run --model mock --tasks tasks/core
```

This executes the sample tasks and writes a timestamped JSONL file under `runs/`.

## Project layout

- `mcp_eval/schemas.py`: core models for tasks and outcomes.
- `mcp_eval/task_loader.py`: YAML task loading.
- `mcp_eval/mock_servers/postgres.py`: deterministic synthetic Postgres server.
- `mcp_eval/adapters/`: model adapter interface and implementations.
- `mcp_eval/runner.py`: task execution orchestration.
- `mcp_eval/grader.py`: deterministic grading logic.
- `mcp_eval/results.py`: JSONL results writer (Polars-ready input).
- `tasks/core/*.yaml`: first benchmark tasks.

## Next milestones

1. Wire real provider adapters (Anthropic/OpenAI/Google) with true MCP tool loops.
2. Expand failure taxonomy and primary/secondary failure attribution.
3. Add additional synthetic MCP servers (CRM/filesystem/ticketing).
4. Add leaderboard generation pipeline from parquet artifacts.
