from mcp_eval.task_loader import load_tasks


def test_load_tasks() -> None:
    tasks = load_tasks("tasks/core")
    assert len(tasks) == 3
    assert tasks[0].id.startswith("t")
