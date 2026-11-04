import pytest

from sentinel.engine import DeceptionEngine, EngineConfig


def test_seed_is_deterministic():
    config = EngineConfig(seed=42, max_nodes=20, max_steps=10)
    first, second = DeceptionEngine(config).run(), DeceptionEngine(config).run()
    assert first["events"] == second["events"]
    assert first["metrics"]["nodes_created"] == second["metrics"]["nodes_created"]


def test_node_budget_is_never_exceeded():
    result = DeceptionEngine(EngineConfig(max_nodes=5, max_steps=100)).run()
    assert result["metrics"]["nodes_created"] <= 5


def test_step_budget_is_never_exceeded():
    result = DeceptionEngine(EngineConfig(max_nodes=100, max_steps=3)).run()
    assert result["metrics"]["steps"] <= 3


def test_depth_budget_is_never_exceeded():
    result = DeceptionEngine(EngineConfig(max_nodes=100, max_depth=1, max_steps=100)).run()
    assert all(event["depth"] <= 1 for event in result["events"])


def test_invalid_config_rejected():
    with pytest.raises(ValueError):
        EngineConfig(max_nodes=0).validate()


def test_core_reports_zero_real_asset_exposure():
    result = DeceptionEngine().run()
    assert result["metrics"]["real_asset_exposure"] == 0


def test_unknown_policy_rejected():
    with pytest.raises(ValueError):
        DeceptionEngine().run(policy="unknown")


def test_adaptive_policy_obeys_all_budgets():
    config = EngineConfig(seed=11, max_nodes=12, max_depth=3, max_steps=7)
    result = DeceptionEngine(config).run(policy="adaptive")
    assert result["metrics"]["nodes_created"] <= config.max_nodes
    assert result["metrics"]["steps"] <= config.max_steps
    assert all(event["depth"] <= config.max_depth for event in result["events"])
