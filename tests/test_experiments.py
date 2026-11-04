import json

import pytest

from sentinel.experiments import compare_policies, to_jsonl


def test_comparison_runs_both_policies_for_each_seed():
    result = compare_policies([3, 9], max_nodes=16, max_steps=8)
    assert [(run["seed"], run["policy"]) for run in result["runs"]] == [
        (3, "baseline"), (3, "adaptive"), (9, "baseline"), (9, "adaptive")
    ]
    assert set(result["summary"]) == {"baseline", "adaptive"}


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


def test_jsonl_contains_event_and_summary_records():
    result = compare_policies([2], max_nodes=8, max_steps=4)
    records = [json.loads(line) for line in to_jsonl(result).splitlines()]
    assert any(row["record_type"] == "event" for row in records)
    assert any(row["record_type"] == "run_summary" for row in records)
    assert records[-1]["record_type"] == "experiment_summary"
