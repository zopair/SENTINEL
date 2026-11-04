"""Strict, bounded, read-only JSONL telemetry ingestion.

Treat all imported telemetry as untrusted data. This module never executes
commands, loads plugins, opens sockets, or writes files.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import math
from typing import Any, Iterable

SCHEMA_VERSION = "1.0"
MAX_LINE_BYTES = 65_536
MAX_RECORDS = 100_000
MAX_INPUT_LINES = 100_000
MAX_TEXT_CHARS = 2_048
POLICIES = {"baseline", "adaptive"}

EVENT_FIELDS = {
    "schema_version", "record_type", "seed", "policy", "sequence",
    "event_type", "node_id", "depth", "detail",
}
SUMMARY_FIELDS = {"schema_version", "record_type", "seed", "policy", "metrics"}
EXPERIMENT_FIELDS = {
    "schema_version", "record_type", "experiment", "seeds", "summary"
}
METRIC_FIELDS = {
    "nodes_created", "nodes_visited", "events", "steps",
    "deepest_visited_level", "interaction_rate",
    "step_budget_utilization", "elapsed_ms", "real_asset_exposure",
}
EXPERIMENT_METRIC_FIELDS = {
    "nodes_created", "nodes_visited", "steps",
    "deepest_visited_level", "interaction_rate",
    "step_budget_utilization",
}
COUNT_METRICS = {
    "nodes_created", "nodes_visited", "events", "steps",
    "deepest_visited_level", "real_asset_exposure",
}


@dataclass(frozen=True)
class TelemetryRecord:
    """Validated record envelope; payload remains an untrusted observation."""
    record_type: str
    payload: dict[str, Any]


def _require_int(value: Any, field: str, *, minimum: int = 0) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{field} must be an integer")
    if value < minimum or value > (2**63 - 1):
        raise ValueError(f"{field} is outside the supported integer range")


def _require_text(value: Any, field: str, *, maximum: int = MAX_TEXT_CHARS) -> None:
    if not isinstance(value, str) or len(value) > maximum:
        raise ValueError(f"{field} must be a string <= {maximum} chars")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError(f"{field} must contain valid Unicode scalar values") from exc


def _validate_metrics(metrics: Any, prefix: str) -> None:
    if not isinstance(metrics, dict) or set(metrics) != METRIC_FIELDS:
        raise ValueError(prefix + "metrics fields do not match schema")
    for field, value in metrics.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(prefix + f"metrics.{field} must be numeric")
        if isinstance(value, int) and value > (2**63 - 1):
            raise ValueError(prefix + f"metrics.{field} exceeds the supported integer range")
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError(prefix + f"metrics.{field} must be finite")
        if value < 0:
            raise ValueError(prefix + f"metrics.{field} must be non-negative")
        if field in COUNT_METRICS and not isinstance(value, int):
            raise ValueError(prefix + f"metrics.{field} must be an integer")
    if metrics["interaction_rate"] > 1:
        raise ValueError(prefix + "interaction_rate must be <= 1")
    if metrics["step_budget_utilization"] > 1:
        raise ValueError(prefix + "step_budget_utilization must be <= 1")
    if metrics["real_asset_exposure"] != 0:
        raise ValueError(prefix + "real_asset_exposure must remain zero")


def _validate_experiment_metrics(metrics: Any, prefix: str) -> None:
    if not isinstance(metrics, dict) or set(metrics) != EXPERIMENT_METRIC_FIELDS:
        raise ValueError(prefix + "experiment summary metrics fields do not match schema")
    for field, value in metrics.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(prefix + f"summary.{field} must be numeric")
        if isinstance(value, int) and value > (2**63 - 1):
            raise ValueError(prefix + f"summary.{field} exceeds the supported integer range")
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError(prefix + f"summary.{field} must be finite")
        if value < 0:
            raise ValueError(prefix + f"summary.{field} must be non-negative")
    if metrics["interaction_rate"] > 1 or metrics["step_budget_utilization"] > 1:
        raise ValueError(prefix + "summary ratios must be <= 1")


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
        if not isinstance(record["policy"], str) or record["policy"] not in POLICIES:
            raise ValueError(prefix + "invalid policy")
        for field in ("node_id", "event_type", "detail"):
            _require_text(record[field], field)
    elif kind == "run_summary":
        _require_int(record["seed"], "seed", minimum=-(2**63))
        if not isinstance(record["policy"], str) or record["policy"] not in POLICIES:
            raise ValueError(prefix + "invalid policy")
        _validate_metrics(record["metrics"], prefix)
    else:
        _require_text(record["experiment"], "experiment", maximum=128)
        seeds = record["seeds"]
        if not isinstance(seeds, list) or len(seeds) > MAX_RECORDS:
            raise ValueError(prefix + "seeds must be a bounded array")
        for seed in seeds:
            _require_int(seed, "seed", minimum=-(2**63))
        summary = record["summary"]
        if not isinstance(summary, dict) or set(summary) != POLICIES:
            raise ValueError(prefix + "summary must contain baseline and adaptive")
        for metrics in summary.values():
            _validate_experiment_metrics(metrics, prefix)
    return TelemetryRecord(kind, record)


def _reject_non_json_constant(value: str) -> None:
    raise ValueError(f"non-standard JSON constant: {value}")


def parse_jsonl(lines: Iterable[str]) -> list[TelemetryRecord]:
    """Parse bounded JSONL records; reject malformed or unknown schemas.

    Both non-empty records and total physical input lines are bounded so a
    stream of blank lines cannot bypass the parser's work limit.
    """
    parsed: list[TelemetryRecord] = []
    for line_number, line in enumerate(lines, start=1):
        if line_number > MAX_INPUT_LINES:
            raise ValueError("input line count exceeds safety limit")
        if not isinstance(line, str):
            raise ValueError(f"line {line_number}: input must be text")
        try:
            line_size = len(line.encode("utf-8"))
        except UnicodeEncodeError as exc:
            raise ValueError(f"line {line_number}: input is not valid UTF-8 text") from exc
        if line_size > MAX_LINE_BYTES:
            raise ValueError(f"line {line_number}: record exceeds byte limit")
        if not line.strip():
            continue
        if len(parsed) >= MAX_RECORDS:
            raise ValueError("record count exceeds safety limit")
        try:
            value = json.loads(line, parse_constant=_reject_non_json_constant)
        except (json.JSONDecodeError, ValueError) as exc:
            raise ValueError(f"line {line_number}: invalid JSON") from exc
        parsed.append(_validate(value, line_number))
    return parsed
