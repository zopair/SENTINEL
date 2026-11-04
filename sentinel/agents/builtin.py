"""Allowlisted deterministic agent strategies."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sentinel.engine import DeceptionEngine, EngineConfig


@dataclass(frozen=True)
class BuiltinPolicyAgent:
    name: str
    policy: str

    def run(self, config: EngineConfig) -> dict[str, Any]:
        return DeceptionEngine(config).run(policy=self.policy)


BUILTIN_AGENTS = {
    "baseline": BuiltinPolicyAgent("baseline", "baseline"),
    "adaptive": BuiltinPolicyAgent("adaptive", "adaptive"),
}
