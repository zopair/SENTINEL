"""Deterministic behavior profiles for synthetic labyrinth telemetry."""
from dataclasses import asdict, dataclass
from typing import Mapping


@dataclass(frozen=True)
class BehaviorAssessment:
    strategy: str
    dominant_action: str
    confidence: float
    challenge: str
    difficulty: int

    def to_dict(self):
        return asdict(self)


class BehaviorAnalyzer:
    ACTIONS = ("enumerate", "verify", "follow", "inspect", "collect", "wait")
    PROFILES = {
        "enumerate": ("broad_discovery", "synthetic_inventory"),
        "verify": ("validation_oriented", "consistency_check"),
        "follow": ("path_seeking", "decoy_route"),
        "inspect": ("detail_inspection", "symbol_sequence"),
        "collect": ("asset_seeking", "archive_bundle"),
        "wait": ("timing_observation", "temporal_pattern"),
    }

    @classmethod
    def analyze(cls, counts: Mapping[str, int]) -> BehaviorAssessment:
        if any(key not in cls.ACTIONS for key in counts):
            raise ValueError("unknown behavior action")
        values = {}
        for action in cls.ACTIONS:
            value = counts.get(action, 0)
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError("counts must be non-negative integers")
            values[action] = value
        total = sum(values.values())
        if total == 0:
            return BehaviorAssessment("exploratory", "none", 0.0, "cross_reference", 1)
        dominant = max(cls.ACTIONS, key=lambda action: values[action])
        strategy, challenge = cls.PROFILES[dominant]
        return BehaviorAssessment(
            strategy, dominant, round(values[dominant] / total, 3),
            challenge, min(5, 1 + values[dominant] // 2),
        )
