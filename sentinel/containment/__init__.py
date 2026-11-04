"""Fail-closed runtime containment primitives."""

from sentinel.containment.policy import AgentRunSpec, ContainmentPolicy, RunResult
from sentinel.containment.podman import PodmanRunner

__all__ = ["AgentRunSpec", "ContainmentPolicy", "PodmanRunner", "RunResult"]
