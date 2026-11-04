import pytest

from sentinel.behavior import BehaviorAnalyzer


def test_empty_history_is_exploratory():
    result = BehaviorAnalyzer.analyze({})
    assert result.strategy == "exploratory"
    assert result.challenge == "cross_reference"


@pytest.mark.parametrize(
    ("counts", "strategy", "challenge"),
    [
        ({"enumerate": 4}, "broad_discovery", "synthetic_inventory"),
        ({"verify": 3}, "validation_oriented", "consistency_check"),
        ({"follow": 3}, "path_seeking", "decoy_route"),
        ({"inspect": 3}, "detail_inspection", "symbol_sequence"),
        ({"wait": 3}, "timing_observation", "temporal_pattern"),
    ],
)
def test_profiles_recommend_bounded_challenges(counts, strategy, challenge):
    result = BehaviorAnalyzer.analyze(counts)
    assert result.strategy == strategy
    assert result.challenge == challenge
    assert 1 <= result.difficulty <= 5


def test_ties_are_deterministic():
    result = BehaviorAnalyzer.analyze({"verify": 2, "enumerate": 2})
    assert result.dominant_action == "enumerate"


@pytest.mark.parametrize("counts", [{"inspect": -1}, {"inspect": True}, {"unknown": 1}])
def test_invalid_telemetry_is_rejected(counts):
    with pytest.raises(ValueError):
        BehaviorAnalyzer.analyze(counts)
