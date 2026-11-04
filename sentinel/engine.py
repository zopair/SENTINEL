"""Safe in-memory procedural deception graph; no sockets, shell, or host-file access."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import random
import time
from typing import Any


POLICIES = ("static_decoy", "random_walk", "greedy", "bfs", "dfs", "adaptive")
POLICY_ALIASES = {"baseline": "bfs"}

# Hard ceilings protect callers that construct EngineConfig from untrusted input.
MAX_NODES_LIMIT = 4096
MAX_DEPTH_LIMIT = 64
MAX_STEPS_LIMIT = 4096
MAX_BRANCHING_LIMIT = 8


@dataclass(frozen=True)
class EngineConfig:
    seed: int = 7
    max_nodes: int = 64
    max_depth: int = 8
    max_steps: int = 20
    branching_factor: int = 3

    def validate(self) -> None:
        for field, value in (
            ("seed", self.seed), ("max_nodes", self.max_nodes),
            ("max_depth", self.max_depth), ("max_steps", self.max_steps),
            ("branching_factor", self.branching_factor),
        ):
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(f"{field} must be an integer")
        if not -(2**63) <= self.seed <= 2**63 - 1:
            raise ValueError("seed must be a signed 64-bit integer")
        if not 1 <= self.max_nodes <= MAX_NODES_LIMIT:
            raise ValueError(f"max_nodes must be between 1 and {MAX_NODES_LIMIT}")
        if not 0 <= self.max_depth <= MAX_DEPTH_LIMIT:
            raise ValueError(f"max_depth must be between 0 and {MAX_DEPTH_LIMIT}")
        if not 0 <= self.max_steps <= MAX_STEPS_LIMIT:
            raise ValueError(f"max_steps must be between 0 and {MAX_STEPS_LIMIT}")
        if not 1 <= self.branching_factor <= MAX_BRANCHING_LIMIT:
            raise ValueError(f"branching_factor must be between 1 and {MAX_BRANCHING_LIMIT}")
        if isinstance(self.seed, bool) or not isinstance(self.seed, int) or not -(2**63) <= self.seed <= 2**63 - 1:
            raise ValueError("seed must be a signed 64-bit integer")


@dataclass
class Node:
    node_id: str
    kind: str
    title: str
    depth: int
    parent_id: str | None
    decoy: bool = True


@dataclass
class Event:
    sequence: int
    event_type: str
    node_id: str
    depth: int
    detail: str


class DeceptionEngine:
    """Explore one pre-generated synthetic graph with bounded, reproducible policies.

    Every policy receives the exact same graph for a given seed/configuration.
    Adaptive is a transparent heuristic, not a learning model or attacker model.
    """
    KINDS = ("service", "document", "repository", "dashboard", "credential_hint")
    ADAPTIVE_PRIORITY = {
        "credential_hint": 5, "repository": 4, "dashboard": 3,
        "service": 2, "document": 1,
    }

    def __init__(self, config: EngineConfig | None = None) -> None:
        self.config = config or EngineConfig()
        self.config.validate()
        self.nodes: dict[str, Node] = {}
        self.children: dict[str, list[Node]] = {}
        self.events: list[Event] = []
        root = self._create_node(None, 0)
        queue = [root]
        while queue and len(self.nodes) < self.config.max_nodes:
            parent = queue.pop(0)
            if parent.depth >= self.config.max_depth:
                continue
            for _ in range(min(self.config.branching_factor,
                               self.config.max_nodes - len(self.nodes))):
                child = self._create_node(parent.node_id, parent.depth + 1)
                self.children[parent.node_id].append(child)
                queue.append(child)

    def _create_node(self, parent_id: str | None, depth: int) -> Node:
        ordinal = len(self.nodes)
        digest = hashlib.sha256(
            f"{self.config.seed}:{ordinal}:{parent_id}:{depth}".encode()
        ).hexdigest()[:12]
        kind = self.KINDS[int(digest, 16) % len(self.KINDS)]
        node = Node(
            node_id=f"decoy-{digest}", kind=kind,
            title=f"Synthetic {kind.replace('_', ' ').title()} {ordinal + 1}",
            depth=depth, parent_id=parent_id,
        )
        self.nodes[node.node_id] = node
        self.children[node.node_id] = []
        return node

    def _record(self, event_type: str, node: Node, detail: str) -> None:
        self.events.append(Event(len(self.events) + 1, event_type, node.node_id, node.depth, detail))

    def run(self, policy: str = "baseline") -> dict[str, Any]:
        """Run one policy; baseline remains a backwards-compatible BFS alias."""
        requested_policy = policy
        policy = POLICY_ALIASES.get(policy, policy)
        if policy not in POLICIES:
            raise ValueError(f"policy must be one of: {', '.join(POLICIES)}")

        started = time.monotonic()
        # Deterministic PRNG is intentional for reproducible experiments, never for secrets.
        rng = random.Random(self.config.seed ^ 0x5E17)  # nosec B311
        root = next(iter(self.nodes.values()))
        frontier = [root]
        visited: set[str] = set()
        steps = 0

        while frontier and steps < self.config.max_steps:
            if policy == "static_decoy":
                index = min(range(len(frontier)), key=lambda i: frontier[i].node_id)
                current = frontier.pop(index)
            elif policy == "bfs":
                current = frontier.pop(0)
            elif policy == "dfs":
                current = frontier.pop()
            elif policy == "random_walk":
                current = frontier.pop(rng.randrange(len(frontier)))
            elif policy == "greedy":
                index = max(range(len(frontier)),
                            key=lambda i: self.ADAPTIVE_PRIORITY[frontier[i].kind])
                current = frontier.pop(index)
            else:
                index = max(
                    range(len(frontier)),
                    key=lambda i: self.ADAPTIVE_PRIORITY[frontier[i].kind] * 10 + frontier[i].depth,
                )
                current = frontier.pop(index)

            if current.node_id in visited:
                continue
            visited.add(current.node_id)
            steps += 1
            self._record("decoy_discovered", current, f"Visited synthetic {current.kind}")

            if current.depth >= self.config.max_depth:
                self._record("depth_budget_reached", current, "Maximum depth reached")
                continue

            for child in self.children[current.node_id]:
                self._record("decoy_generated", child, "Pre-generated in the shared static graph")
                frontier.append(child)
            if not self.children[current.node_id] and len(self.nodes) >= self.config.max_nodes:
                self._record("node_budget_reached", current, "Maximum node count reached")

        if frontier and steps >= self.config.max_steps:
            self._record("step_budget_reached", frontier[0], "Maximum step count reached")

        deepest = max((self.nodes[node_id].depth for node_id in visited), default=0)
        return {
            "policy": requested_policy, "config": asdict(self.config),
            "metrics": {
                "nodes_created": len(self.nodes), "nodes_visited": len(visited),
                "events": len(self.events), "steps": steps,
                "deepest_visited_level": deepest,
                "interaction_rate": round(len(visited) / max(1, len(self.nodes)), 4),
                "step_budget_utilization": round(steps / max(1, self.config.max_steps), 4),
                "elapsed_ms": round((time.monotonic() - started) * 1000, 3),
                "real_asset_exposure": 0,
            },
            "events": [asdict(event) for event in self.events],
        }
