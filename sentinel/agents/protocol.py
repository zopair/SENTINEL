"""Narrow protocol for trusted, built-in synthetic agent strategies.

Third-party code is deliberately not importable through this interface. Future
external agents must run out-of-process inside a separately verified sandbox.
"""
from __future__ import annotations

from typing import Any, Protocol

from sentinel.engine import EngineConfig


class AgentAdapter(Protocol):
    name: str

    def run(self, config: EngineConfig) -> dict[str, Any]:
        """Return one bounded synthetic exploration result."""
