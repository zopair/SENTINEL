import json

import pytest

from sentinel.adapters.jsonl import parse_jsonl
from sentinel.engine import EngineConfig, MAX_DEPTH_LIMIT, MAX_NODES_LIMIT, MAX_STEPS_LIMIT
from sentinel.experiments import _paired_sign_flip_test, compare_policies, to_jsonl


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("max_nodes", MAX_NODES_LIMIT + 1),
        ("max_depth", MAX_DEPTH_LIMIT + 1),
        ("max_steps", MAX_STEPS_LIMIT + 1),
        ("branching_factor", 9),
    ],
)
def test_engine_rejects_configurations_above_hard_resource_ceilings(field, value):
    with pytest.raises(ValueError):
        EngineConfig(**{field: value}).validate()


def test_engine_rejects_non_integer_seed():
    with pytest.raises(ValueError):
        EngineConfig(seed=True).validate()


def test_paired_permutation_test_is_deterministic_and_bounded():
    differences = [1.0, 2.0, 1.0, 3.0, 2.0, 1.0]
    first = _paired_sign_flip_test(differences, permutations=500, seed=91)
    second = _paired_sign_flip_test(differences, permutations=500, seed=91)
    assert first == second
    assert 0 < first <= 1


def test_jsonl_v2_contains_validated_paired_test_metadata():
    result = compare_policies([3, 9, 17], max_nodes=12, max_steps=6)
    lines = to_jsonl(result).splitlines()
    records = parse_jsonl(lines)
    summary = json.loads(lines[-1])
    assert records[-1].record_type == "experiment_summary"
    assert set(summary["paired_tests_vs_static_decoy"]) == {
        "random_walk", "greedy", "bfs", "dfs", "adaptive"
    }
    assert summary["paired_tests_vs_static_decoy"]["adaptive"]["steps"]["p_value_holm"] <= 1


def test_engine_rejects_seed_outside_signed_64_bit_range():
    with pytest.raises(ValueError):
        EngineConfig(seed=2**63).validate()

@pytest.mark.parametrize("field", ["max_nodes", "max_depth", "max_steps", "branching_factor", "seed"])
def test_engine_rejects_boolean_numeric_configuration(field):
    with pytest.raises(ValueError):
        EngineConfig(**{field: True}).validate()


@pytest.mark.parametrize("field", ["max_nodes", "max_depth", "max_steps", "branching_factor"])
def test_engine_rejects_fractional_configuration(field):
    with pytest.raises(ValueError):
        EngineConfig(**{field: 2.5}).validate()

def test_comparison_rejects_duplicate_seeds():
    with pytest.raises(ValueError, match="unique"):
        compare_policies([4, 4], max_nodes=8, max_steps=4)


def test_comparison_rejects_estimated_telemetry_overflow():
    with pytest.raises(ValueError, match="estimated JSONL records"):
        compare_policies([1, 2, 3], max_nodes=4096, max_steps=20)
