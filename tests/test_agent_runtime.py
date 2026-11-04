import pytest

from sentinel.agent_lab import benchmark
from sentinel.agents import AgentRuntime
from sentinel.engine import EngineConfig


def test_runtime_allows_only_registered_builtin_agents():
    runtime = AgentRuntime()
    result = runtime.run("baseline", EngineConfig(seed=7, max_steps=3))
    assert result["metrics"]["real_asset_exposure"] == 0
    with pytest.raises(ValueError, match="not allowlisted"):
        runtime.run("untrusted-plugin", EngineConfig())


def test_runtime_matrix_uses_identical_seeded_budgets():
    rows = AgentRuntime().run_matrix([3, 9], max_nodes=16, max_steps=8)
    assert [(row["seed"], row["policy"]) for row in rows] == [
        (3, "baseline"), (3, "adaptive"),
        (9, "baseline"), (9, "adaptive"),
    ]
    assert all(row["metrics"]["steps"] <= 8 for row in rows)


def test_synthetic_benchmark_scores_and_hard_gates():
    result = benchmark([3, 9], max_nodes=16, max_steps=8)
    assert result["overall_score"] == 100
    assert all(agent["passed"] for agent in result["agents"].values())
