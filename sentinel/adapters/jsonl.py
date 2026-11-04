"""Strict, read-only JSONL telemetry ingestion.

Input is treated as untrusted data. This module never executes commands,
loads plugins, opens sockets, or writes files.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Iterable

SCHEMA_VERSION = "1.0"
MAX_LINE_BYTES = 65_536
MAX_RECORDS = 100_000
EVENT_FIELDS = {
    "schema_version", "record_type", "seed", "policy", "sequence",
    "event_type", "node_id", "depth", "detail",
}
SUMMARY_FIELDS = {"schema_version", "record_type", "seed", "policy", "metrics"}
EXPERIMENT_FIELDS = {
    "schema_version", "record_type", "experiment", "seeds", "summary"
}


@dataclass(frozen=True)
class TelemetryRecord:
    """Validated envelope; payload values remain untrusted observations."""
    record_type: str
    payload: dict[str, Any]


def _require_int(value: Any, field: str, *, minimum: int = 0) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{field} must be an integer >= {minimum}")


def _validate(record: Any, line_number: int) -> TelemetryRecord:
    prefix = f"line {line_number}: "
    if not isinstance(record, dict):
        raise ValueError(prefix + "record must be a JSON object")
    if record.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(prefix + "unsupported or missing schema_version")
    kind = record.get("record_type")
    if not isinstance(kind, str):
        raise ValueError(prefix + "record_type must be a string")
    expected = {
        "event": EVENT_FIELDS,
        "run_summary": SUMMARY_FIELDS,
        "experiment_summary": EXPERIMENT_FIELDS,
    }.get(kind)
    if expected is None:
        raise ValueError(prefix + "unsupported record_type")
    if set(record) != expected:
        raise ValueError(prefix + "record fields do not match the schema")

    if kind == "event":
        _require_int(record["seed"], "seed", minimum=-(2**63))
        _require_int(record["sequence"], "sequence", minimum=1)
        _require_int(record["depth"], "depth")
        if not isinstance(record["policy"], str) or record["policy"] not in {"baseline", "adaptive"}:
            raise ValueError(prefix + "invalid policy")
        for field in ("node_id", "event_type", "detail"):
            if not isinstance(record[field], str) or len(record[field]) > 2048:
                raise ValueError(prefix + f"{field} must be a string <= 2048 chars")
    elif kind == "run_summary":
        _require_int(record["seed"], "seed", minimum=-(2**63))
        if record["policy"] not in {"baseline", "adaptive"}:
            raise ValueError(prefix + "invalid policy")
        if not isinstance(record["metrics"], dict):
            raise ValueError(prefix + "metrics must be an object")
    else:
        if not isinstance(record["experiment"], str) or len(record["experiment"]) > 128:
            raise ValueError(prefix + "invalid experiment label")
        if not isinstance(record["seeds"], list) or len(record["seeds"]) > MAX_RECORDS:
            raise ValueError(prefix + "seeds must be a bounded array")
        for seed in record["seeds"]:
            _require_int(seed, "seed", minimum=-(2**63))
        if not isinstance(record["summary"], dict):
            raise ValueError(prefix + "summary must be an object")
    return TelemetryRecord(kind, record)


def parse_jsonl(lines: Iterable[str]) -> list[TelemetryRecord]:
    """Parse bounded JSONL records; reject malformed or unknown schemas."""
    parsed: list[TelemetryRecord] = []
    for line_number, line in enumerate(lines, start=1):
        if len(parsed) >= MAX_RECORDS:
            raise ValueError("record count exceeds safety limit")
        if not isinstance(line, str):
            raise ValueError(f"line {line_number}: input must be text")
        if len(line.encode("utf-8")) > MAX_LINE_BYTES:
            raise ValueError(f"line {line_number}: record exceeds byte limit")
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"line {line_number}: invalid JSON") from exc
        parsed.append(_validate(value, line_number))
    return parsed
