"""Immutable, deny-by-default policy for disposable agent runs."""
from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Sequence


_IMAGE_DIGEST = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9._/:+-]*@sha256:[0-9a-f]{64}$"
)


@dataclass(frozen=True)
class ContainmentPolicy:
    """Resource limits; security boundaries are deliberately not configurable."""

    memory_mb: int = 128
    cpus: float = 0.5
    pids_limit: int = 64
    timeout_seconds: int = 30
    output_limit_bytes: int = 262_144
    tmpfs_mb: int = 16

    def __post_init__(self) -> None:
        bounds = (
            ("memory_mb", self.memory_mb, 64, 1024),
            ("pids_limit", self.pids_limit, 16, 256),
            ("timeout_seconds", self.timeout_seconds, 1, 300),
            ("output_limit_bytes", self.output_limit_bytes, 1024, 4_194_304),
            ("tmpfs_mb", self.tmpfs_mb, 1, 64),
        )
        for name, value, minimum, maximum in bounds:
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(f"{name} must be an integer")
            if not minimum <= value <= maximum:
                raise ValueError(f"{name} must be between {minimum} and {maximum}")
        if isinstance(self.cpus, bool) or not isinstance(self.cpus, (int, float)):
            raise ValueError("cpus must be numeric")
        if not 0.1 <= float(self.cpus) <= 2.0:
            raise ValueError("cpus must be between 0.1 and 2.0")


@dataclass(frozen=True)
class AgentRunSpec:
    """A pinned, prebuilt image plus an argv vector; no shell or host mounts."""

    image: str
    command: Sequence[str]
    policy: ContainmentPolicy = field(default_factory=ContainmentPolicy)

    def __post_init__(self) -> None:
        if not isinstance(self.image, str) or not _IMAGE_DIGEST.fullmatch(self.image):
            raise ValueError("image must be pinned by a full sha256 digest")
        if isinstance(self.command, (str, bytes)) or not self.command:
            raise ValueError("command must be a non-empty argument sequence")
        if len(self.command) > 128:
            raise ValueError("command contains too many arguments")
        total = 0
        for item in self.command:
            if not isinstance(item, str) or not item or "\x00" in item:
                raise ValueError("command arguments must be non-empty strings without NUL")
            total += len(item.encode("utf-8"))
        if total > 16_384:
            raise ValueError("command arguments exceed the 16 KiB limit")
        object.__setattr__(self, "command", tuple(self.command))


@dataclass(frozen=True)
class RunResult:
    status: str
    exit_code: int | None
    output: str
    duration_ms: int
    output_truncated: bool = False
