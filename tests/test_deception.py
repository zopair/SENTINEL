import pytest

from sentinel.deception import AdaptiveLabyrinth, LabyrinthConfig


def test_labyrinth_is_deterministic_for_same_seed_and_actions():
    actions = ["inspect", "follow", "verify", "enumerate", "inspect"]
    first = AdaptiveLabyrinth(LabyrinthConfig(seed=19)).run(actions)
    second = AdaptiveLabyrinth(LabyrinthConfig(seed=19)).run(actions)
    assert first == second


def test_labyrinth_reconfigures_challenges_from_behavior():
    result = AdaptiveLabyrinth().run(["enumerate", "enumerate", "verify", "verify"])
    assert result["metrics"]["challenge_levels_seen"][-1] >= 2
    assert any(event["event_type"] == "labyrinth_reconfigured" for event in result["events"])
    assert result["current_node"]["synthetic"] is True


def test_labyrinth_never_exceeds_node_depth_or_step_budgets():
    config = LabyrinthConfig(max_nodes=7, max_depth=2, max_steps=4, branching_factor=3)
    result = AdaptiveLabyrinth(config).run(["inspect"] * 20)
    assert result["metrics"]["nodes_created"] <= 7
    assert result["metrics"]["steps"] <= 4
    assert result["metrics"]["deepest_level"] <= 2
    assert result["metrics"]["real_asset_exposure"] == 0


def test_labyrinth_rejects_unknown_actions_and_bad_budgets():
    with pytest.raises(ValueError):
        AdaptiveLabyrinth().step("connect_to_target")
    with pytest.raises(ValueError):
        LabyrinthConfig(max_nodes=5000)


def test_labyrinth_marks_exhausted_depth_and_step_budgets():
    depth = AdaptiveLabyrinth(LabyrinthConfig(max_depth=0)).step("inspect")
    assert depth["status"] == "depth_budget_reached"
    steps = AdaptiveLabyrinth(LabyrinthConfig(max_steps=1)).step("inspect")
    assert steps["status"] == "step_budget_reached"
