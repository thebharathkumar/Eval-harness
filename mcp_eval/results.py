from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from mcp_eval.schemas import TaskOutcome


def write_results(outcomes: list[TaskOutcome], out_dir: str) -> Path:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    path = out / f"run_{ts}.jsonl"
    with path.open("w", encoding="utf-8") as f:
        for outcome in outcomes:
            f.write(json.dumps(outcome.model_dump()) + "\n")
    return path
