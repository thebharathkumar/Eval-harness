from __future__ import annotations

import json
from pathlib import Path

from mcp_eval.schemas import TaskSpec


def load_task(path: str | Path) -> TaskSpec:
    raw = json.loads(Path(path).read_text())
    return TaskSpec.from_dict(raw)


def load_tasks(path: str | Path) -> list[TaskSpec]:
    root = Path(path)
    files = [root] if root.is_file() else sorted(root.glob("*.yaml"))
    return [load_task(f) for f in files]
