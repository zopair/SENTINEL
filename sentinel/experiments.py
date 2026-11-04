"""Repeatable multi-policy experiments and paired uncertainty estimates."""
from __future__ import annotations

import json
from math import sqrt
from statistics import mean, pstdev
from typing import Any, Iterable

from sentinel.engine import DeceptionEngine, EngineConfig, POLICIES

METRIC_KEYS = (
    "nodes_created", "nodes_visited", "steps", "deepest_visited_level",
    "interaction_rate", "step_budget_utilization",
)


def _interval(values: list[float]) -> dict[str, float]:
    """Normal-approximation 95% CI; explicitly labelled, not a t interval."""
    if not values:
        return {"mean": 0.0, "ci95_low": 0.0, "ci95_high": 0.0, "sd": 0.0}
    avg = mean(values)
    margin = 1.96 * (pstdev(values) / sqrt(len(values))) if len(values) > 1 else 0.0
    return {
        "mean": round(avg, 4), "ci95_low": round(avg - margin, 4),
        "ci95_high": round(avg + margin, 4), "sd": round(pstdev(values), 4),
    }


def compare_policies(
    seeds: Iterable[int] = tuple(range(30)),
    *, max_nodes: int = 64, max_depth: int = 8,
    max_steps: int = 20, branching_factor: int = 3,
) -> dict[str, Any]:
    """Compare six policies with matched seeds, graph inputs, and resource budgets."""
    seed_list = list(seeds)
    if not seed_list:
        raise ValueError("at least one seed is required")
    runs: list[dict[str, Any]] = []
    for seed in seed_list:
        config = EngineConfig(seed=seed, max_nodes=max_nodes, max_depth=max_depth,
                              max_steps=max_steps, branching_factor=branching_factor)
        for policy in POLICIES:
            result = DeceptionEngine(config).run(policy=policy)
            runs.append({"seed": seed, "policy": policy,
                         "metrics": result["metrics"], "events": result["events"]})

    summary = {}
    for policy in POLICIES:
        selected = [r["metrics"] for r in runs if r["policy"] == policy]
        summary[policy] = {key: _interval([float(m[key]) for m in selected])
                           for key in METRIC_KEYS}

    paired = {}
    reference = "static_decoy"
    for policy in POLICIES:
        if policy == reference:
            continue
        paired[policy] = {}
        for metric in METRIC_KEYS:
            by_seed = {
                r["seed"]: float(r["metrics"][metric])
                for r in runs if r["policy"] == policy
            }
            ref_by_seed = {
                r["seed"]: float(r["metrics"][metric])
                for r in runs if r["policy"] == reference
            }
            differences = [by_seed[s] - ref_by_seed[s] for s in seed_list]
            paired[policy][metric] = _interval(differences)

    return {
        "schema_version": "2.0",
        "experiment": "six_policy_matched_seed_comparison",
        "seeds": seed_list,
        "seed_count": len(seed_list),
        "recommended_minimum_seeds": 30,
        "statistical_method": "paired per-seed differences; normal-approximation 95% CI (1.96); descriptive, not a significance claim",
        "runs": runs, "summary": summary,
        "paired_difference_vs_static_decoy": paired,
        "limitations": [
            "All policies are algorithmic baselines operating in the same synthetic, lazily generated graph.",
            "Adaptive is a hand-designed deterministic heuristic, not a learning agent.",
            "Scripted profiles and policy heuristics may share design assumptions; held-out external strategies are needed.",
            "A 95% normal-approximation interval is descriptive and may be unreliable for small samples or non-normal outcomes.",
            "No real attacker, production network, or real asset is exercised."
        ],
    }


def to_jsonl(result: dict[str, Any]) -> str:
    """Serialize run events and summaries as newline-delimited JSON records."""
    lines: list[str] = []
    for run in result["runs"]:
        for event in run["events"]:
            lines.append(json.dumps({
                "schema_version": result["schema_version"], "record_type": "event",
                "seed": run["seed"], "policy": run["policy"], **event,
            }, sort_keys=True))
        lines.append(json.dumps({
            "schema_version": result["schema_version"], "record_type": "run_summary",
            "seed": run["seed"], "policy": run["policy"], "metrics": run["metrics"],
        }, sort_keys=True))
    lines.append(json.dumps({
        "schema_version": result["schema_version"], "record_type": "experiment_summary",
        "experiment": result["experiment"], "seeds": result["seeds"],
        "summary": result["summary"], "paired_difference_vs_static_decoy":
            result["paired_difference_vs_static_decoy"],
        "limitations": result["limitations"],
    }, sort_keys=True))
    return "\n".join(lines) + "\n"
