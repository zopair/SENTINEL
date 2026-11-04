"""Fail-closed registry for built-in synthetic agents only."""
from __future__ import annotations

from typing import Any, Iterable

from sentinel.agents.builtin import BUILTIN_AGENTS
from sentinel.engine import EngineConfig


class AgentRuntime:
    """Dispatch allowlisted strategies; never imports or executes plugin code."""

    def run(self, agent_name: str, config: EngineConfig) -> dict[str, Any]:
        agent = BUILTIN_AGENTS.get(agent_name)
        if agent is None:
            raise ValueError(f"agent is not allowlisted: {agent_name}")
        return agent.run(config)

    def run_matrix(
        self,
        seeds: Iterable[int],
        *,
        max_nodes: int = 64,
        max_depth: int = 8,
        max_steps: int = 20,
        branching_factor: int = 3,
    ) -> list[dict[str, Any]]:
        seed_list = list(seeds)
        if not seed_list:
            raise ValueError("at least one seed is required")
        results = []
        for seed in seed_list:
            for agent_name in ("baseline", "adaptive"):
                config = EngineConfig(
                    seed=seed,
                    max_nodes=max_nodes,
                    max_depth=max_depth,
                    max_steps=max_steps,
                    branching_factor=branching_factor,
                )
                results.append({
                    "seed": seed,
                    "policy": agent_name,
                    **self.run(agent_name, config),
                })
        return results
