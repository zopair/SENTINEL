"""Repeatable multi-policy experiments and paired uncertainty estimates."""
from __future__ import annotations

import json
import random
from math import sqrt
from statistics import mean, pstdev
from typing import Any, Iterable

from sentinel.engine import DeceptionEngine, EngineConfig, POLICIES

METRIC_KEYS = (
    "nodes_created", "nodes_visited", "steps", "deepest_visited_level",
    "interaction_rate", "step_budget_utilization",
)
PERMUTATIONS = 10_000
MAX_EXPERIMENT_SEEDS = 1_000
MAX_EXPERIMENT_RECORDS = 100_000


def _interval(values: list[float]) -> dict[str, float]:
    """Normal-approximation 95% CI; explicitly labelled, not a t interval."""
    if not values:
        return {"mean": 0.0, "ci95_low": 0.0, "ci95_high": 0.0, "sd": 0.0}
    avg = mean(values)
    margin = 1.96 * (pstdev(values) / sqrt(len(values))) if len(values) > 1 else 0.0
    return {"mean": round(avg, 4), "ci95_low": round(avg - margin, 4),
            "ci95_high": round(avg + margin, 4), "sd": round(pstdev(values), 4)}


def _paired_sign_flip_test(
    differences: list[float], *, permutations: int = PERMUTATIONS, seed: int = 20261104
) -> float:
    """Two-sided Monte Carlo paired randomization test for a mean difference.

    This is an exploratory test under exchangeable sign assignments, not proof of
    practical importance. The +1 correction prevents a zero Monte Carlo p-value.
    """
    if not differences:
        return 1.0
    observed = abs(mean(differences))
    if observed == 0 or len(differences) == 1:
        return 1.0
    rng = random.Random(seed)  # nosec B311 - deterministic experiment resampling only
    extreme = 0
    for _ in range(permutations):
        permuted = abs(mean(value if rng.getrandbits(1) else -value for value in differences))
        if permuted >= observed - 1e-12:
            extreme += 1
    return (extreme + 1) / (permutations + 1)


def _holm_adjust(raw: dict[tuple[str, str], float]) -> dict[tuple[str, str], float]:
    """Holm step-down family-wise adjustment across all reported paired tests."""
    ordered = sorted(raw.items(), key=lambda item: item[1])
    count = len(ordered)
    adjusted: dict[tuple[str, str], float] = {}
    running = 0.0
    for rank, (key, p_value) in enumerate(ordered):
        running = max(running, min(1.0, (count - rank) * p_value))
        adjusted[key] = round(running, 6)
    return adjusted


def compare_policies(
    seeds: Iterable[int] = tuple(range(30)),
    *, max_nodes: int = 64, max_depth: int = 8,
    max_steps: int = 20, branching_factor: int = 3,
) -> dict[str, Any]:
    """Compare six policies on identical pre-generated graphs and budgets."""
    seed_list = []
    for seed in seeds:
        if len(seed_list) >= MAX_EXPERIMENT_SEEDS:
            raise ValueError(f"seed count exceeds the safety limit of {MAX_EXPERIMENT_SEEDS}")
        if isinstance(seed, bool) or not isinstance(seed, int) or not -(2**63) <= seed <= 2**63 - 1:
            raise ValueError("every seed must be a signed 64-bit integer")
        seed_list.append(seed)
    if not seed_list:
        raise ValueError("at least one seed is required")
    if len(set(seed_list)) != len(seed_list):
        raise ValueError("seed values must be unique for paired comparisons")
    EngineConfig(seed=0, max_nodes=max_nodes, max_depth=max_depth,
                 max_steps=max_steps, branching_factor=branching_factor).validate()
    estimated_records = len(seed_list) * len(POLICIES) * (4 * max_nodes + 2) + 1
    if estimated_records > MAX_EXPERIMENT_RECORDS:
        raise ValueError(
            f"estimated JSONL records ({estimated_records}) exceed the safety limit "
            f"of {MAX_EXPERIMENT_RECORDS}; reduce seeds or max_nodes"
        )
    runs = []
    for seed in seed_list:
        config = EngineConfig(seed=seed, max_nodes=max_nodes, max_depth=max_depth,
                              max_steps=max_steps, branching_factor=branching_factor)
        for policy in POLICIES:
            result = DeceptionEngine(config).run(policy=policy)
            runs.append({"seed": seed, "policy": policy,
                         "metrics": result["metrics"], "events": result["events"]})

    summary = {
        policy: {
            key: _interval([float(r["metrics"][key]) for r in runs if r["policy"] == policy])
            for key in METRIC_KEYS
        } for policy in POLICIES
    }
    paired = {}
    raw_p_values: dict[tuple[str, str], float] = {}
    for policy_index, policy in enumerate(POLICIES):
        if policy == "static_decoy":
            continue
        paired[policy] = {}
        for metric_index, metric in enumerate(METRIC_KEYS):
            values = {r["seed"]: float(r["metrics"][metric])
                      for r in runs if r["policy"] == policy}
            baseline = {r["seed"]: float(r["metrics"][metric])
                        for r in runs if r["policy"] == "static_decoy"}
            differences = [values[s] - baseline[s] for s in seed_list]
            paired[policy][metric] = _interval(differences)
            raw_p_values[(policy, metric)] = _paired_sign_flip_test(
                differences, seed=20261104 + policy_index * 101 + metric_index
            )

    adjusted = _holm_adjust(raw_p_values)
    paired_tests = {
        policy: {
            metric: {
                "method": "paired_sign_flip_permutation_monte_carlo",
                "permutations": PERMUTATIONS,
                "p_value": round(raw_p_values[(policy, metric)], 6),
                "p_value_holm": adjusted[(policy, metric)],
            }
            for metric in METRIC_KEYS
        }
        for policy in paired
    }

    return {
        "schema_version": "2.0",
        "experiment": "six_policy_matched_seed_comparison",
        "seeds": seed_list,
        "seed_count": len(seed_list),
        "recommended_minimum_seeds": 30,
        "statistical_method": (
            "paired per-seed differences; descriptive normal-approximation 95% CI; "
            "two-sided paired sign-flip Monte Carlo test with 10000 permutations; "
            "Holm correction across reported policy/metric tests; exploratory only"
        ),
        "runs": runs,
        "summary": summary,
        "paired_difference_vs_static_decoy": paired,
        "paired_tests_vs_static_decoy": paired_tests,
        "limitations": [
            "All policies run on the exact same pre-generated graph for each seed/configuration.",
            "Adaptive is a hand-designed deterministic heuristic, not a learning agent.",
            "Scripted profiles and policy heuristics may share design assumptions; held-out strategies are needed.",
            "Normal-approximation intervals are descriptive and may be unreliable for small samples or non-normal outcomes.",
            "Permutation p-values depend on exchangeability assumptions and Monte Carlo sampling; they do not measure practical effect size.",
            "Holm adjustment covers the reported paired policy/metric tests, not analyses selected after inspecting results.",
            "No real attacker, production network, or real asset is exercised.",
        ],
    }


def to_jsonl(result: dict[str, Any]) -> str:
    """Serialize v1 legacy or v2 research telemetry without changing old fixtures."""
    version = result["schema_version"]
    lines = []
    for run in result["runs"]:
        for event in run["events"]:
            lines.append(json.dumps({
                "schema_version": version, "record_type": "event",
                "seed": run["seed"], "policy": run["policy"], **event,
            }, sort_keys=True))
        lines.append(json.dumps({
            "schema_version": version, "record_type": "run_summary",
            "seed": run["seed"], "policy": run["policy"], "metrics": run["metrics"],
        }, sort_keys=True))
    summary = {
        "schema_version": version, "record_type": "experiment_summary",
        "experiment": result["experiment"], "seeds": result["seeds"],
        "summary": result["summary"],
    }
    if version == "2.0":
        summary["paired_difference_vs_static_decoy"] = result["paired_difference_vs_static_decoy"]
        summary["paired_tests_vs_static_decoy"] = result["paired_tests_vs_static_decoy"]
        summary["limitations"] = result["limitations"]
    lines.append(json.dumps(summary, sort_keys=True))
    return "\n".join(lines) + "\n"
