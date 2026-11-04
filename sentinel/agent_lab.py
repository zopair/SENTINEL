"""Run a reproducible synthetic agent benchmark and emit a transparent score."""
from __future__ import annotations

import argparse
import json
import sys
from statistics import mean
from typing import Any

from sentinel.adapters import parse_jsonl
from sentinel.agents import AgentRuntime
from sentinel.experiments import METRIC_KEYS, to_jsonl


def _stable(result: dict[str, Any]) -> tuple[Any, ...]:
    metrics = {key: value for key, value in result["metrics"].items() if key != "elapsed_ms"}
    return result["events"], metrics


def benchmark(
    seeds: list[int],
    *,
    max_nodes: int = 64,
    max_depth: int = 8,
    max_steps: int = 20,
) -> dict[str, Any]:
    if not seeds:
        raise ValueError("at least one seed is required")
    runtime = AgentRuntime()
    runs = runtime.run_matrix(
        seeds, max_nodes=max_nodes, max_depth=max_depth, max_steps=max_steps
    )
    repeated = runtime.run_matrix(
        seeds, max_nodes=max_nodes, max_depth=max_depth, max_steps=max_steps
    )
    stable_by_key = {
        (row["seed"], row["policy"]): _stable(row)
        for row in repeated
    }

    policies: dict[str, dict[str, Any]] = {}
    for name in ("baseline", "adaptive"):
        selected = [row for row in runs if row["policy"] == name]
        repeatable = all(
            _stable(row) == stable_by_key[(row["seed"], name)]
            for row in selected
        )
        budget_ok = all(
            row["metrics"]["nodes_created"] <= max_nodes
            and row["metrics"]["steps"] <= max_steps
            and row["metrics"]["deepest_visited_level"] <= max_depth
            for row in selected
        )
        zero_exposure = all(
            row["metrics"]["real_asset_exposure"] == 0
            and all(event["node_id"].startswith("decoy-") for event in row["events"])
            for row in selected
        )
        summary = {
            key: round(mean(row["metrics"][key] for row in selected), 4)
            for key in METRIC_KEYS
        }
        other = "adaptive" if name == "baseline" else "baseline"
        experiment = {
            "schema_version": "1.0",
            "experiment": "agent_runtime_benchmark",
            "seeds": seeds,
            "runs": [
                {
                    "seed": row["seed"],
                    "policy": name,
                    "metrics": row["metrics"],
                    "events": row["events"],
                }
                for row in selected
            ],
            "summary": {name: summary, other: summary},
        }
        parsed = parse_jsonl(to_jsonl(experiment).splitlines())
        expected_records = sum(len(row["events"]) + 1 for row in selected) + 1
        telemetry_ok = (
            len(parsed) == expected_records
            and parsed[-1].record_type == "experiment_summary"
        )
        progress = min(
            1.0,
            mean(row["metrics"]["steps"] for row in selected) / max(1, max_steps),
        )
        checks = {
            "budget_compliance": 25 if budget_ok else 0,
            "zero_real_asset_exposure": 25 if zero_exposure else 0,
            "telemetry_integrity": 20 if telemetry_ok else 0,
            "deterministic_replay": 15 if repeatable else 0,
            "bounded_task_progress": round(15 * progress, 2),
        }
        score = round(sum(checks.values()), 2)
        policies[name] = {
            "score": score,
            "passed": score >= 90 and budget_ok and zero_exposure and telemetry_ok,
            "checks": checks,
            "averages": summary,
        }

    return {
        "benchmark": "SENTINEL synthetic agent runtime v1",
        "seeds": seeds,
        "limits": {
            "max_nodes": max_nodes,
            "max_depth": max_depth,
            "max_steps": max_steps,
        },
        "score_definition": {
            "budget_compliance": 25,
            "zero_real_asset_exposure": 25,
            "telemetry_integrity": 20,
            "deterministic_replay": 15,
            "bounded_task_progress": 15,
        },
        "agents": policies,
        "overall_score": round(mean(item["score"] for item in policies.values()), 2),
        "limitations": [
            "This score measures this synthetic benchmark contract, not real-world attacker skill.",
            "The two agents are deterministic built-in policies, not third-party autonomous agents.",
            "The benchmark does not test kernel exploits, container escapes, side channels, or production targets.",
            "Containment is evaluated separately by the Linux Podman preflight and runtime probe.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the synthetic SENTINEL agent benchmark")
    parser.add_argument("--seeds", type=int, nargs="+", default=[7, 17, 27, 37, 47, 57, 67, 77, 87, 97])
    parser.add_argument("--max-nodes", type=int, default=64)
    parser.add_argument("--max-depth", type=int, default=8)
    parser.add_argument("--max-steps", type=int, default=20)
    args = parser.parse_args()
    result = benchmark(
        args.seeds,
        max_nodes=args.max_nodes,
        max_depth=args.max_depth,
        max_steps=args.max_steps,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if not all(agent["passed"] for agent in result["agents"].values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
