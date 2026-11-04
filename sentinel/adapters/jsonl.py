"""Strict, bounded, read-only JSONL telemetry ingestion.

Treat imported telemetry as untrusted data. Never execute commands or load plugins.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import math
from typing import Any, Iterable

SCHEMA_VERSION = "1.0"
SCHEMA_V2 = "2.0"
MAX_LINE_BYTES = 65_536
MAX_RECORDS = 100_000
MAX_INPUT_LINES = 100_000
MAX_TEXT_CHARS = 2_048
LEGACY_POLICIES = {"baseline", "adaptive"}
POLICIES_V2 = {"static_decoy", "random_walk", "greedy", "bfs", "dfs", "adaptive"}

EVENT_FIELDS = {"schema_version", "record_type", "seed", "policy", "sequence",
                "event_type", "node_id", "depth", "detail"}
SUMMARY_FIELDS = {"schema_version", "record_type", "seed", "policy", "metrics"}
EXPERIMENT_FIELDS_V1 = {"schema_version", "record_type", "experiment", "seeds", "summary"}
EXPERIMENT_FIELDS_V2 = EXPERIMENT_FIELDS_V1 | {
    "paired_difference_vs_static_decoy", "paired_tests_vs_static_decoy", "limitations"
}
METRIC_FIELDS = {"nodes_created", "nodes_visited", "events", "steps",
                 "deepest_visited_level", "interaction_rate",
                 "step_budget_utilization", "elapsed_ms", "real_asset_exposure"}
EXPERIMENT_METRIC_FIELDS = {"nodes_created", "nodes_visited", "steps",
                            "deepest_visited_level", "interaction_rate",
                            "step_budget_utilization"}
COUNT_METRICS = {"nodes_created", "nodes_visited", "events", "steps",
                 "deepest_visited_level", "real_asset_exposure"}


@dataclass(frozen=True)
class TelemetryRecord:
    record_type: str
    payload: dict[str, Any]


def _require_int(value: Any, field: str, *, minimum: int = 0) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{field} must be an integer")
    if value < minimum or value > 2**63 - 1:
        raise ValueError(f"{field} is outside the supported integer range")


def _require_text(value: Any, field: str, *, maximum: int = MAX_TEXT_CHARS) -> None:
    if not isinstance(value, str) or len(value) > maximum:
        raise ValueError(f"{field} must be a string <= {maximum} chars")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError(f"{field} must contain valid Unicode scalar values") from exc


def _number(value: Any, field: str, *, nonnegative: bool = True) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field} must be numeric")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{field} must be finite")
    if nonnegative and value < 0:
        raise ValueError(f"{field} must be non-negative")


def _validate_metrics(metrics: Any, prefix: str) -> None:
    if not isinstance(metrics, dict) or set(metrics) != METRIC_FIELDS:
        raise ValueError(prefix + "metrics fields do not match schema")
    for field, value in metrics.items():
        _number(value, f"metrics.{field}")
        if isinstance(value, int) and value > 2**63 - 1:
            raise ValueError(prefix + f"metrics.{field} exceeds integer range")
        if field in COUNT_METRICS and not isinstance(value, int):
            raise ValueError(prefix + f"metrics.{field} must be an integer")
    if metrics["interaction_rate"] > 1 or metrics["step_budget_utilization"] > 1:
        raise ValueError(prefix + "metrics ratios must be <= 1")
    if metrics["real_asset_exposure"] != 0:
        raise ValueError(prefix + "real_asset_exposure must remain zero")


def _validate_legacy_summary(summary: Any, prefix: str) -> None:
    if not isinstance(summary, dict) or set(summary) != LEGACY_POLICIES:
        raise ValueError(prefix + "summary must contain baseline and adaptive")
    for metrics in summary.values():
        if not isinstance(metrics, dict) or set(metrics) != EXPERIMENT_METRIC_FIELDS:
            raise ValueError(prefix + "experiment summary metrics fields do not match schema")
        for field, value in metrics.items():
            _number(value, f"summary.{field}")
        if metrics["interaction_rate"] > 1 or metrics["step_budget_utilization"] > 1:
            raise ValueError(prefix + "summary ratios must be <= 1")


def _validate_v2_intervals(summary: Any, prefix: str, policies: set[str]) -> None:
    if not isinstance(summary, dict) or set(summary) != policies:
        raise ValueError(prefix + "summary policy set does not match schema")
    for policy_metrics in summary.values():
        if not isinstance(policy_metrics, dict) or set(policy_metrics) != EXPERIMENT_METRIC_FIELDS:
            raise ValueError(prefix + "summary metric set does not match schema")
        for metric, interval in policy_metrics.items():
            if not isinstance(interval, dict) or set(interval) != {"mean", "ci95_low", "ci95_high", "sd"}:
                raise ValueError(prefix + "invalid confidence interval fields")
            for field, value in interval.items():
                _number(value, f"{metric}.{field}", nonnegative=(field in {"mean", "sd"}))
            if interval["ci95_low"] > interval["ci95_high"] or interval["sd"] < 0:
                raise ValueError(prefix + "invalid confidence interval bounds")


def _validate(record: Any, line_number: int) -> TelemetryRecord:
    prefix = f"line {line_number}: "
    if not isinstance(record, dict):
        raise ValueError(prefix + "record must be a JSON object")
    version = record.get("schema_version")
    if version not in {SCHEMA_VERSION, SCHEMA_V2}:
        raise ValueError(prefix + "unsupported or missing schema_version")
    policies = LEGACY_POLICIES if version == SCHEMA_VERSION else POLICIES_V2
    kind = record.get("record_type")
    expected = {"event": EVENT_FIELDS, "run_summary": SUMMARY_FIELDS}.get(kind)
    if kind == "experiment_summary":
        expected = EXPERIMENT_FIELDS_V1 if version == SCHEMA_VERSION else EXPERIMENT_FIELDS_V2
    if expected is None:
        raise ValueError(prefix + "unsupported record_type")
    if set(record) != expected:
        raise ValueError(prefix + "record fields do not match the schema")

    if kind == "event":
        _require_int(record["seed"], "seed", minimum=-(2**63))
        _require_int(record["sequence"], "sequence", minimum=1)
        _require_int(record["depth"], "depth")
        if not isinstance(record["policy"], str) or record["policy"] not in policies:
            raise ValueError(prefix + "invalid policy")
        for field in ("node_id", "event_type", "detail"):
            _require_text(record[field], field)
    elif kind == "run_summary":
        _require_int(record["seed"], "seed", minimum=-(2**63))
        if not isinstance(record["policy"], str) or record["policy"] not in policies:
            raise ValueError(prefix + "invalid policy")
        _validate_metrics(record["metrics"], prefix)
    else:
        _require_text(record["experiment"], "experiment", maximum=128)
        seeds = record["seeds"]
        if not isinstance(seeds, list) or len(seeds) > MAX_RECORDS:
            raise ValueError(prefix + "seeds must be a bounded array")
        for seed in seeds:
            _require_int(seed, "seed", minimum=-(2**63))
        if version == SCHEMA_VERSION:
            _validate_legacy_summary(record["summary"], prefix)
        else:
            _validate_v2_intervals(record["summary"], prefix, policies)
            paired = record["paired_difference_vs_static_decoy"]
            expected_paired = policies - {"static_decoy"}
            if not isinstance(paired, dict) or set(paired) != expected_paired:
                raise ValueError(prefix + "paired comparison policy set does not match")
            for metrics in paired.values():
                if not isinstance(metrics, dict) or set(metrics) != EXPERIMENT_METRIC_FIELDS:
                    raise ValueError(prefix + "paired metric set does not match")
                for interval in metrics.values():
                    if not isinstance(interval, dict) or set(interval) != {"mean", "ci95_low", "ci95_high", "sd"}:
                        raise ValueError(prefix + "invalid paired interval fields")
                    for field, value in interval.items():
                        _number(value, f"paired.{field}", nonnegative=(field == "sd"))
            tests = record["paired_tests_vs_static_decoy"]
            if not isinstance(tests, dict) or set(tests) != expected_paired:
                raise ValueError(prefix + "paired test policy set does not match")
            for metrics in tests.values():
                if not isinstance(metrics, dict) or set(metrics) != EXPERIMENT_METRIC_FIELDS:
                    raise ValueError(prefix + "paired test metric set does not match")
                for test in metrics.values():
                    if not isinstance(test, dict) or set(test) != {"method", "permutations", "p_value", "p_value_holm"}:
                        raise ValueError(prefix + "invalid paired test fields")
                    if test["method"] != "paired_sign_flip_permutation_monte_carlo":
                        raise ValueError(prefix + "unsupported paired test method")
                    _require_int(test["permutations"], "permutations", minimum=1)
                    for field in ("p_value", "p_value_holm"):
                        _number(test[field], field)
                        if not 0 <= test[field] <= 1:
                            raise ValueError(prefix + "p-values must be between 0 and 1")
            limitations = record["limitations"]
            if not isinstance(limitations, list) or any(not isinstance(x, str) for x in limitations):
                raise ValueError(prefix + "limitations must be an array of strings")
    return TelemetryRecord(kind, record)


def _reject_non_json_constant(value: str) -> None:
    raise ValueError(f"non-standard JSON constant: {value}")


def parse_jsonl(lines: Iterable[str]) -> list[TelemetryRecord]:
    """Parse bounded JSONL records; reject malformed or unknown schemas."""
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
