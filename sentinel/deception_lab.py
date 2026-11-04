"""Reproducible scripted strategies for evaluating the synthetic labyrinth."""
from __future__ import annotations

from statistics import mean
from typing import Any

from sentinel.deception import AdaptiveLabyrinth, LabyrinthConfig


PROFILE_ACTIONS = {
    "broad_survey": ("enumerate",) * 12,
    "deep_path": ("follow",) * 12,
    "validation": ("verify",) * 12,
    "detail_inspection": ("inspect",) * 12,
    "mixed_explorer": (
        "inspect", "enumerate", "follow", "verify", "wait", "enumerate",
        "inspect", "follow", "verify", "wait", "enumerate", "inspect",
    ),
}


def evaluate_profiles(
    seeds: list[int] | tuple[int, ...] = (7, 17, 27),
    *,
    max_nodes: int = 64,
    max_depth: int = 8,
    max_steps: int = 12,
    branching_factor: int = 3,
) -> dict[str, Any]:
    """Run deterministic action scripts under identical synthetic budgets."""
    if not seeds:
        raise ValueError("at least one seed is required")
    runs = []
    for seed in seeds:
        for name, actions in PROFILE_ACTIONS.items():
            config = LabyrinthConfig(
                seed=seed, max_nodes=max_nodes, max_depth=max_depth,
                max_steps=max_steps, branching_factor=branching_factor,
            )
            result = AdaptiveLabyrinth(config).run(actions[:max_steps])
            runs.append({
                "seed": seed,
                "profile": name,
                "metrics": result["metrics"],
                "behavior": result["behavior"],
                "status": result["status"],
            })

    summary = {}
    for name in PROFILE_ACTIONS:
        selected = [row["metrics"] for row in runs if row["profile"] == name]
        summary[name] = {
            "avg_nodes_created": round(mean(row["nodes_created"] for row in selected), 3),
            "avg_steps": round(mean(row["steps"] for row in selected), 3),
            "avg_deepest_level": round(mean(row["deepest_level"] for row in selected), 3),
        }

    return {
        "schema_version": "1.0",
        "experiment": "synthetic_labyrinth_profile_evaluation",
        "seeds": list(seeds),
        "limits": {
            "max_nodes": max_nodes, "max_depth": max_depth,
            "max_steps": max_steps, "branching_factor": branching_factor,
        },
        "runs": runs,
        "summary": summary,
        "limitations": [
            "Profiles are deterministic action scripts, not real or third-party autonomous agents.",
            "Results measure synthetic labyrinth behavior only and do not establish real attacker effectiveness.",
            "No production systems, external hosts, or real assets are contacted.",
        ],
    }
