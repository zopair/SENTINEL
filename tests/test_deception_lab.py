import pytest

from sentinel.deception_lab import evaluate_profiles


def test_profile_evaluation_is_deterministic():
    first = evaluate_profiles([11, 22], max_steps=8)
    second = evaluate_profiles([11, 22], max_steps=8)
    assert first == second


def test_all_profiles_obey_the_same_resource_budgets():
    result = evaluate_profiles([7], max_nodes=10, max_depth=3, max_steps=5)
    assert len(result["runs"]) == 5
    for run in result["runs"]:
        metrics = run["metrics"]
        assert metrics["nodes_created"] <= 10
        assert metrics["steps"] <= 5
        assert metrics["deepest_level"] <= 3
        assert metrics["real_asset_exposure"] == 0


def test_profile_evaluation_requires_at_least_one_seed():
    with pytest.raises(ValueError):
        evaluate_profiles([])
