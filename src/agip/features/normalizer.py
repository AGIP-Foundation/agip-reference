"""Deterministic normalization of raw observations."""

import re
from collections.abc import Iterable

from agip.features.models import Feature, Observation, ScalarValue

_SEPARATOR_PATTERN = re.compile(r"[\s-]+")


class Normalizer:
    """Convert observations into a stable, validated feature sequence."""

    def normalize(self, observations: Iterable[Observation]) -> tuple[Feature, ...]:
        """Normalize and sort observations by canonical feature name."""

        features: dict[str, Feature] = {}
        for observation in observations:
            name = self._normalize_name(observation.name)
            if name in features:
                raise ValueError(f"duplicate normalized feature name: {name}")
            features[name] = Feature(
                name=name,
                value=self._normalize_value(observation.value),
                confidence=observation.confidence,
            )
        return tuple(features[name] for name in sorted(features))

    @staticmethod
    def _normalize_name(name: str) -> str:
        normalized = _SEPARATOR_PATTERN.sub("_", name.strip().casefold())
        if not normalized:
            raise ValueError("normalized name must not be empty")
        return normalized

    @staticmethod
    def _normalize_value(value: ScalarValue) -> ScalarValue:
        if isinstance(value, str):
            return value.strip().casefold()
        return value
