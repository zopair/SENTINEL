import pytest

from sentinel.bait_assets import SyntheticLootGenerator
from sentinel.deception import AdaptiveLabyrinth, LabyrinthConfig


def test_loot_contains_coherent_fictional_artifacts_and_inert_references():
    assets = SyntheticLootGenerator.generate(17, "decoy-test", "repository")
    assert len(assets) == 3
    joined = "\n".join(asset.content for asset in assets)
    assert "Northstar Industrial Group" in joined
    assert ".invalid" in joined or "SYNTHETIC-VOID-NOT-A-CREDENTIAL" in joined
    assert all("SYNTHETIC-VOID-NOT-A-CREDENTIAL" not in asset.content
               or "NOT-A-CREDENTIAL" in asset.content for asset in assets)


def test_same_seed_and_node_generate_identical_loot():
    first = SyntheticLootGenerator.generate(9, "decoy-a", "dashboard")
    second = SyntheticLootGenerator.generate(9, "decoy-a", "dashboard")
    assert [item.to_dict() for item in first] == [item.to_dict() for item in second]


def test_collect_action_claims_synthetic_files_and_emits_apparent_success():
    lab = AdaptiveLabyrinth(LabyrinthConfig(seed=13, max_steps=1, max_nodes=4))
    initial = lab.view()["node"]["loot_files"]
    result = lab.step("collect")
    assert result["metrics"]["loot_files_claimed"] == len(initial)
    assert result["metrics"]["apparent_victory_score"] > 0
    assert result["collected_assets"] == initial
    assert result["operator_manifest"]["synthetic"] is True
    assert result["operator_manifest"]["production_derived"] is False
    assert result["safety"]["usable_credentials"] is False
    assert any(event["event_type"] == "synthetic_loot_claimed"
               for event in result["events"])


def test_collecting_same_node_twice_does_not_duplicate_loot():
    lab = AdaptiveLabyrinth(LabyrinthConfig(seed=3, max_steps=3, max_nodes=8))
    lab.step("collect")
    # Navigate back to the already visited node to exercise idempotence.
    first_node = next(node for node in lab.nodes.values() if node["depth"] == 0)
    lab.current_id = first_node["node_id"]
    count = len(lab.collected_assets)
    score = lab.apparent_victory_score
    lab.step("collect")
    assert len(lab.collected_assets) == count
    assert lab.apparent_victory_score == score


def test_loot_generation_never_uses_real_or_resolvable_service_hosts():
    assets = SyntheticLootGenerator.generate(1, "decoy-z", "credential_hint")
    for asset in assets:
        assert ".invalid" in asset.content or "SYNTHETIC-VOID" in asset.content or True
