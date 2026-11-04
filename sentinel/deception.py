"""Adaptive, synthetic-only labyrinth sessions with explicit resource budgets."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
from typing import Any, Iterable


@dataclass(frozen=True)
class LabyrinthConfig:
    seed: int = 7
    max_nodes: int = 64
    max_depth: int = 8
    max_steps: int = 20
    branching_factor: int = 3

    def __post_init__(self) -> None:
        if self.max_nodes < 1 or self.max_nodes > 4096:
            raise ValueError("max_nodes must be between 1 and 4096")
        if self.max_depth < 0 or self.max_depth > 32:
            raise ValueError("max_depth must be between 0 and 32")
        if self.max_steps < 0 or self.max_steps > 512:
            raise ValueError("max_steps must be between 0 and 512")
        if not 1 <= self.branching_factor <= 8:
            raise ValueError("branching_factor must be between 1 and 8")


class AdaptiveLabyrinth:
    """A deterministic simulation; it has no network, host, or production connectors.

    Each accepted synthetic action changes the next decoy's challenge profile.
    The graph is generated only within fixed node, depth, and step budgets.
    """

    ACTIONS = frozenset({"inspect", "follow", "enumerate", "verify", "wait"})
    KINDS = ("service", "document", "repository", "dashboard", "credential_hint")
    CHALLENGES = {
        "inspect": "symbol_sequence",
        "follow": "decoy_route",
        "enumerate": "synthetic_inventory",
        "verify": "consistency_check",
        "wait": "timing_observation",
    }

    def __init__(self, config: LabyrinthConfig | None = None) -> None:
        self.config = config or LabyrinthConfig()
        self.nodes: dict[str, dict[str, Any]] = {}
        self.events: list[dict[str, Any]] = []
        self.action_counts = {action: 0 for action in self.ACTIONS}
        self.steps = 0
        self.status = "active"
        self.current_id = self._make_node(None, 0, "inspect", 1)

    def _digest(self, value: str) -> str:
        return hashlib.sha256(f"{self.config.seed}:{value}".encode()).hexdigest()

    def _make_node(
        self, parent_id: str | None, depth: int, action: str, challenge_level: int
    ) -> str:
        ordinal = len(self.nodes)
        digest = self._digest(f"{ordinal}:{parent_id}:{depth}:{action}:{challenge_level}")
        node_id = "decoy-" + digest[:12]
        kind = self.KINDS[int(digest[12:20], 16) % len(self.KINDS)]
        self.nodes[node_id] = {
            "node_id": node_id,
            "kind": kind,
            "depth": depth,
            "parent_id": parent_id,
            "challenge": self.CHALLENGES[action],
            "challenge_level": challenge_level,
            "synthetic": True,
        }
        return node_id

    def _record(self, event_type: str, **fields: Any) -> None:
        self.events.append({
            "sequence": len(self.events) + 1,
            "event_type": event_type,
            **fields,
        })

    def view(self) -> dict[str, Any]:
        node = dict(self.nodes[self.current_id])
        return {"status": self.status, "node": node, "steps_remaining": max(
            0, self.config.max_steps - self.steps
        )}

    def step(self, action: str) -> dict[str, Any]:
        if action not in self.ACTIONS:
            raise ValueError("action must be one of the supported synthetic actions")
        if self.status != "active":
            return self.result()
        if self.steps >= self.config.max_steps:
            self.status = "step_budget_reached"
            return self.result()

        current = self.nodes[self.current_id]
        self.steps += 1
        self.action_counts[action] += 1
        challenge_level = min(5, 1 + self.action_counts[action] // 2
                              + (1 if action in {"enumerate", "verify"} else 0))
        self._record(
            "synthetic_interaction",
            node_id=self.current_id,
            action=action,
            challenge=current["challenge"],
            challenge_level=current["challenge_level"],
        )

        if current["depth"] >= self.config.max_depth:
            self.status = "depth_budget_reached"
            self._record("depth_budget_reached", node_id=self.current_id)
            return self.result()

        remaining = self.config.max_nodes - len(self.nodes)
        count = min(self.config.branching_factor, remaining)
        if count <= 0:
            self.status = "node_budget_reached"
            self._record("node_budget_reached", node_id=self.current_id)
            return self.result()

        children = [
            self._make_node(self.current_id, current["depth"] + 1, action, challenge_level)
            for _ in range(count)
        ]
        selector = int(self._digest(
            f"route:{self.current_id}:{action}:{self.steps}:{challenge_level}"
        )[:8], 16)
        self.current_id = children[selector % len(children)]
        self._record(
            "labyrinth_reconfigured",
            parent_id=current["node_id"],
            selected_node_id=self.current_id,
            branches_created=count,
            challenge_level=challenge_level,
        )
        if self.steps >= self.config.max_steps:
            self.status = "step_budget_reached"
        elif len(self.nodes) >= self.config.max_nodes:
            # Existing nodes remain navigable; the next action will stop at the node budget.
            pass
        return self.result()

    def run(self, actions: Iterable[str]) -> dict[str, Any]:
        for action in actions:
            if self.status != "active":
                break
            self.step(action)
        return self.result()

    def result(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "experiment": "adaptive_synthetic_labyrinth",
            "status": self.status,
            "config": asdict(self.config),
            "current_node": dict(self.nodes[self.current_id]),
            "metrics": {
                "nodes_created": len(self.nodes),
                "steps": self.steps,
                "deepest_level": max(node["depth"] for node in self.nodes.values()),
                "challenge_levels_seen": sorted({
                    node["challenge_level"] for node in self.nodes.values()
                }),
                "real_asset_exposure": 0,
            },
            "action_counts": dict(self.action_counts),
            "events": list(self.events),
            "safety": {
                "synthetic_only": True,
                "network_access": False,
                "host_access": False,
                "production_connectors": False,
                "resource_budgets_enforced": True,
            },
        }
