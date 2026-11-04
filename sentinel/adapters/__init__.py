"""Read-only adapters for SENTINEL telemetry."""

from sentinel.adapters.jsonl import TelemetryRecord, parse_jsonl

__all__ = ["TelemetryRecord", "parse_jsonl"]
