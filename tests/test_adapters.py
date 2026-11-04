import json

import pytest

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


def test_accepts_valid_event_and_ignores_blank_lines():
    result = parse_jsonl(["\n", event_record() + "\n"])
    assert len(result) == 1
    assert result[0].record_type == "event"


def test_rejects_unknown_schema_version():
    with pytest.raises(ValueError, match="schema_version"):
        parse_jsonl([event_record(schema_version="99")])


def test_rejects_extra_fields():
    with pytest.raises(ValueError, match="fields"):
        parse_jsonl([event_record(command="rm -rf /")])


def test_rejects_invalid_policy():
    with pytest.raises(ValueError, match="policy"):
        parse_jsonl([event_record(policy="execute")])


def test_rejects_boolean_sequence():
    with pytest.raises(ValueError, match="sequence"):
        parse_jsonl([event_record(sequence=True)])


def test_rejects_malformed_json():
    with pytest.raises(ValueError, match="invalid JSON"):
        parse_jsonl(["{broken"])


def test_rejects_oversized_line():
    with pytest.raises(ValueError, match="byte limit"):
        parse_jsonl([" " * 65_537])
