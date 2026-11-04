import json

import pytest
from hypothesis import given, strategies as st

from sentinel.adapters import parse_jsonl


def event_record(**overrides):
    record = {
        "schema_version": "1.0",
        "record_type": "event",
        "seed": 7,
        "policy": "baseline",
        "sequence": 1,
        "event_type": "decoy_discovered",
        "node_id": "decoy-example",
        "depth": 0,
        "detail": "Synthetic service",
    }
    record.update(overrides)
    return json.dumps(record)


def valid_metrics():
    return {
        "nodes_created": 1,
        "nodes_visited": 1,
        "events": 1,
        "steps": 1,
        "deepest_visited_level": 0,
        "interaction_rate": 1.0,
        "step_budget_utilization": 0.05,
        "elapsed_ms": 0.1,
        "real_asset_exposure": 0,
    }


def summary_record(**overrides):
    record = {
        "schema_version": "1.0",
        "record_type": "run_summary",
        "seed": 7,
        "policy": "baseline",
        "metrics": valid_metrics(),
    }
    record.update(overrides)
    return json.dumps(record)


def experiment_record(**overrides):
    record = {
        "schema_version": "1.0",
        "record_type": "experiment_summary",
        "experiment": "baseline_vs_adaptive",
        "seeds": [7, 17],
        "summary": {
            "baseline": valid_metrics(),
            "adaptive": valid_metrics(),
        },
    }
    record.update(overrides)
    return json.dumps(record)


def test_accepts_valid_event_and_ignores_blank_lines():
    result = parse_jsonl(["\n", event_record() + "\n"])
    assert len(result) == 1
    assert result[0].record_type == "event"


def test_accepts_all_supported_record_types():
    result = parse_jsonl([
        event_record(),
        summary_record(),
        experiment_record(),
    ])
    assert [row.record_type for row in result] == [
        "event", "run_summary", "experiment_summary"
    ]


@pytest.mark.parametrize("record", [
    event_record(schema_version="99"),
    event_record(command="rm -rf /"),
    event_record(policy="execute"),
    event_record(sequence=True),
    event_record(seed=2**63),
    event_record(node_id=17),
])
def test_rejects_invalid_event_envelopes(record):
    with pytest.raises(ValueError):
        parse_jsonl([record])


def test_rejects_invalid_nested_metrics_and_real_asset_exposure():
    metrics = valid_metrics()
    metrics["nodes_visited"] = True
    with pytest.raises(ValueError, match="numeric"):
        parse_jsonl([summary_record(metrics=metrics)])

    metrics = valid_metrics()
    metrics["real_asset_exposure"] = 1
    with pytest.raises(ValueError, match="must remain zero"):
        parse_jsonl([summary_record(metrics=metrics)])


def test_rejects_non_finite_json_constants():
    with pytest.raises(ValueError, match="invalid JSON"):
        parse_jsonl([summary_record().replace('"elapsed_ms": 0.1', '"elapsed_ms": NaN')])


def test_rejects_malformed_json_and_oversized_line():
    with pytest.raises(ValueError, match="invalid JSON"):
        parse_jsonl(["{broken"])
    with pytest.raises(ValueError, match="byte limit"):
        parse_jsonl([" " * 65_537])


def test_rejects_non_text_and_invalid_unicode():
    with pytest.raises(ValueError, match="input must be text"):
        parse_jsonl([123])
    with pytest.raises(ValueError, match="valid UTF-8"):
        parse_jsonl(["\ud800"])


def test_rejects_unknown_record_type_and_bad_experiment_summary():
    with pytest.raises(ValueError, match="record_type"):
        parse_jsonl([json.dumps({"schema_version": "1.0", "record_type": "command"})])
    invalid = json.loads(experiment_record())
    invalid["summary"].pop("adaptive")
    with pytest.raises(ValueError, match="baseline and adaptive"):
        parse_jsonl([json.dumps(invalid)])


def test_rejects_more_than_record_limit(monkeypatch):
    import sentinel.adapters.jsonl as adapter

    monkeypatch.setattr(adapter, "MAX_RECORDS", 1)
    with pytest.raises(ValueError, match="record count"):
        parse_jsonl([event_record(), event_record(sequence=2)])


def test_rejects_too_many_blank_input_lines(monkeypatch):
    import sentinel.adapters.jsonl as adapter

    monkeypatch.setattr(adapter, "MAX_INPUT_LINES", 2)
    with pytest.raises(ValueError, match="input line count"):
        parse_jsonl(["\n", "\n", "\n"])


@given(st.integers(min_value=-(2**63), max_value=2**63 - 1))
def test_accepts_signed_64_bit_event_seeds(seed):
    assert parse_jsonl([event_record(seed=seed)])[0].payload["seed"] == seed


@given(st.text(max_size=2048))
def test_accepts_bounded_unicode_detail(detail):
    assert parse_jsonl([event_record(detail=detail)])[0].payload["detail"] == detail
