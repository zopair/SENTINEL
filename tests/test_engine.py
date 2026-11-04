import pytest

from sentinel.engine import DeceptionEngine, EngineConfig, POLICIES


def test_seed_is_deterministic():
    config = EngineConfig(seed=42, max_nodes=20, max_steps=10)
    first, second = DeceptionEngine(config).run(), DeceptionEngine(config).run()
    assert first["events"] == second["events"]
    assert first["metrics"]["nodes_created"] == second["metrics"]["nodes_created"]


@pytest.mark.parametrize("policy", POLICIES)
def test_every_policy_is_deterministic_and_bounded(policy):
    config = EngineConfig(seed=42, max_nodes=20, max_depth=4, max_steps=9)
    first = DeceptionEngine(config).run(policy=policy)
    second = DeceptionEngine(config).run(policy=policy)
    assert first["events"] == second["events"]
    assert first["metrics"]["nodes_created"] <= config.max_nodes
    assert first["metrics"]["steps"] <= config.max_steps
    assert all(event["depth"] <= config.max_depth for event in first["events"])
    assert first["metrics"]["real_asset_exposure"] == 0


def test_baseline_remains_bfs_alias():
    config = EngineConfig(seed=4, max_nodes=20, max_steps=8)
    assert DeceptionEngine(config).run("baseline")["events"] == DeceptionEngine(config).run("bfs")["events"]


def test_invalid_config_rejected():
    with pytest.raises(ValueError):
        EngineConfig(max_nodes=0).validate()


def test_unknown_policy_rejected():
    with pytest.raises(ValueError):
        DeceptionEngine().run(policy="unknown")
