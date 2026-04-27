from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any


@dataclass
class SyntheticPostgresServer:
    seed: int

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)
        self._now = datetime(2026, 4, 27, tzinfo=timezone.utc)
        self._users = self._generate_users()

    def tool_specs(self) -> list[dict[str, Any]]:
        return [
            {
                "name": "list_recent_signups",
                "description": "Return users created in the last N days",
                "input_schema": {"type": "object", "properties": {"days": {"type": "integer", "minimum": 1}}},
            },
            {
                "name": "list_inactive_users",
                "description": "Return users who have not logged in since N days",
                "input_schema": {"type": "object", "properties": {"days": {"type": "integer", "minimum": 1}}},
            },
            {
                "name": "intersect_user_ids",
                "description": "Return intersection of two user-id lists",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "left_ids": {"type": "array", "items": {"type": "integer"}},
                        "right_ids": {"type": "array", "items": {"type": "integer"}},
                    },
                },
            },
        ]

    def oracle_recent_and_inactive(self, *, signup_days: int, inactive_days: int) -> dict[str, Any]:
        recent = self.list_recent_signups(days=signup_days)["user_ids"]
        inactive = self.list_inactive_users(days=inactive_days)["user_ids"]
        both = self.intersect_user_ids(left_ids=recent, right_ids=inactive)["user_ids"]
        return {
            "tool_calls": [
                {"tool_name": "list_recent_signups", "arguments": {"days": signup_days}, "ok": True},
                {"tool_name": "list_inactive_users", "arguments": {"days": inactive_days}, "ok": True},
                {
                    "tool_name": "intersect_user_ids",
                    "arguments": {"left_ids": recent, "right_ids": inactive},
                    "ok": True,
                },
            ],
            "final_answer": ",".join(str(x) for x in both),
            "expected_ids": both,
        }

    def list_recent_signups(self, *, days: int) -> dict[str, Any]:
        cutoff = self._now - timedelta(days=days)
        rows = [u for u in self._users if u["created_at"] >= cutoff]
        return {"user_ids": sorted(r["id"] for r in rows)}

    def list_inactive_users(self, *, days: int) -> dict[str, Any]:
        cutoff = self._now - timedelta(days=days)
        rows = [u for u in self._users if u["last_login_at"] <= cutoff]
        return {"user_ids": sorted(r["id"] for r in rows)}

    def intersect_user_ids(self, *, left_ids: list[int], right_ids: list[int]) -> dict[str, Any]:
        return {"user_ids": sorted(set(left_ids).intersection(right_ids))}

    def _generate_users(self) -> list[dict[str, Any]]:
        users: list[dict[str, Any]] = []
        for user_id in range(1, 51):
            created_days_ago = self._rng.randint(0, 60)
            last_login_days_ago = self._rng.randint(0, 60)
            users.append(
                {
                    "id": user_id,
                    "created_at": self._now - timedelta(days=created_days_ago),
                    "last_login_at": self._now - timedelta(days=last_login_days_ago),
                }
            )
        return users
