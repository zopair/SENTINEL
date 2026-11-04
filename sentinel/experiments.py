"""Repeatable policy comparisons and JSON Lines telemetry export."""
from __future__ import annotations

from dataclasses import asdict
import json
from statistics import mean
from typing import Any, Iterable

from sentinel.engine import DeceptionEngine, EngineConfig


METRIC_KEYS = (
    "nodes_created",
    "nodes_visited",
    "steps",
    "deepest_visited_level",
    "interaction_rate",
    "step_budget_utilization",
)


def compare_policies(
    seeds: Iterable[int] = (7, 17, 27),
    *,
    max_nodes: int = 64,
    max_depth: int = 8,
    max_steps: int = 20,
    branching_factor: int = 3,
) -> dict[str, Any]:
    """Run both policies with identical per-seed budgets and synthetic inputs."""
    seed_list = list(seeds)
    if not seed_list:
        raise ValueError("at least one seed is required")

    runs: list[dict[str, Any]] = []
    for seed in seed_list:
        config = EngineConfig(
            seed=seed,
            max_nodes=max_nodes,
            max_depth=max_depth,
            max_steps=max_steps,
            branching_factor=branching_factor,
        )
        for policy in ("baseline", "adaptive"):
            result = DeceptionEngine(config).run(policy=policy)
            runs.append({
                "seed": seed,
                "policy": policy,
                "metrics": result["metrics"],
                "events": result["events"],
            })

    summary: dict[str, dict[str, float]] = {}
    for policy in ("baseline", "adaptive"):
        selected = [run["metrics"] for run in runs if run["policy"] == policy]
        summary[policy] = {
            key: round(mean(metric[key] for metric in selected), 4)
            for key in METRIC_KEYS
        }

    return {
        "schema_version": "1.0",
        "experiment": "baseline_vs_adaptive",
        "seeds": seed_list,
        "runs": runs,
        "summary": summary,
        "notes": [
            "Adaptive is a deterministic synthetic priority heuristic, not a real attacker model.",
            "Elapsed time is reported per run but excluded from policy comparison due to runtime noise.",
            "real_asset_exposure is a core invariant for this in-memory prototype, not an external audit result.",
        ],
    }


def to_jsonl(result: dict[str, Any]) -> str:
    """Serialize run events and summaries as newline-delimited JSON records."""
    lines: list[str] = []
    for run in result["runs"]:
        for event in run["events"]:
            lines.append(json.dumps({
                "schema_version": result["schema_version"],
                "record_type": "event",
                "seed": run["seed"],
                "policy": run["policy"],
                **event,
            }, sort_keys=True))
        lines.append(json.dumps({
            "schema_version": result["schema_version"],
            "record_type": "run_summary",
            "seed": run["seed"],
            "policy": run["policy"],
            "metrics": run["metrics"],
        }, sort_keys=True))
    lines.append(json.dumps({
        "schema_version": result["schema_version"],
        "record_type": "experiment_summary",
        "experiment": result["experiment"],
        "seeds": result["seeds"],
        "summary": result["summary"],
    }, sort_keys=True))
    return "\n".join(lines) + "\n"
