import json

import pytest

from sentinel.experiments import compare_policies, to_jsonl
from sentinel.engine import POLICIES


def test_comparison_runs_all_policies_for_each_seed():
    result = compare_policies([3, 9], max_nodes=16, max_steps=8)
    assert [(run["seed"], run["policy"]) for run in result["runs"]] == [
        (seed, policy) for seed in (3, 9) for policy in POLICIES
    ]
    assert set(result["summary"]) == set(POLICIES)
    assert result["seed_count"] == 2


def test_comparison_is_reproducible_except_runtime_metric():
    first = compare_policies([5], max_nodes=12, max_steps=6)
    second = compare_policies([5], max_nodes=12, max_steps=6)
    for a, b in zip(first["runs"], second["runs"]):
        assert a["events"] == b["events"]
        assert {k: v for k, v in a["metrics"].items() if k != "elapsed_ms"} == {
            k: v for k, v in b["metrics"].items() if k != "elapsed_ms"
        }


def test_empty_seed_list_rejected():
    with pytest.raises(ValueError):
        compare_policies([])


def test_jsonl_contains_events_runs_and_experiment_summary():
    result = compare_policies([2], max_nodes=8, max_steps=4)
    records = [json.loads(line) for line in to_jsonl(result).splitlines()]
    assert any(row["record_type"] == "event" for row in records)
    assert len([row for row in records if row["record_type"] == "run_summary"]) == len(POLICIES)
    assert records[-1]["record_type"] == "experiment_summary"
    assert "paired_difference_vs_static_decoy" in records[-1]
