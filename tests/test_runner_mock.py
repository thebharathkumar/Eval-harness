from mcp_eval.adapters.mock import MockModelAdapter
from mcp_eval.mock_servers.postgres import SyntheticPostgresServer
from mcp_eval.runner import Runner
from mcp_eval.task_loader import load_task


def test_runner_end_to_end_mock() -> None:
    task = load_task("tasks/core/t001_recent_inactive_easy.yaml")
    pg = SyntheticPostgresServer(seed=task.seed)
    context = {"oracle": pg.oracle_recent_and_inactive(signup_days=7, inactive_days=7)}

    outcome = Runner(MockModelAdapter()).run_task(task, tool_specs=pg.tool_specs(), context=context)

    assert outcome.success is True
    assert outcome.failure_code is None
    assert outcome.final_answer == "2,8,13,20,31,33,41"
