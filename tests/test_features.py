"""Tests for the feature extraction MVP."""

import pytest

from agip.features import Normalizer, Observation


def test_normalizer_is_deterministic() -> None:
    normalizer = Normalizer()
    observations = [
        Observation("  Writing-Size ", " LARGE ", 0.8),
        Observation("Pressure", 7, 0.9),
    ]

    result = normalizer.normalize(observations)

    assert [feature.name for feature in result] == ["pressure", "writing_size"]
    assert result[0].value == 7
    assert result[1].value == "large"
    assert result[1].confidence == 0.8


def test_normalizer_rejects_duplicate_canonical_names() -> None:
    normalizer = Normalizer()

    with pytest.raises(ValueError, match="duplicate normalized feature name"):
        normalizer.normalize(
            [Observation("Writing Size", "large"), Observation("writing-size", "small")]
        )


@pytest.mark.parametrize("confidence", [-0.01, 1.01])
def test_observation_rejects_invalid_confidence(confidence: float) -> None:
    with pytest.raises(ValueError, match="confidence"):
        Observation("pressure", 5, confidence)


def test_observation_rejects_blank_name_and_value() -> None:
    with pytest.raises(ValueError, match="name"):
        Observation("   ", 5)

    with pytest.raises(ValueError, match="string values"):
        Observation("pressure", "   ")
