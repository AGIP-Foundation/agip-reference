"""Public extraction contract for feature providers."""

from collections.abc import Iterable
from typing import Protocol

from agip.features.models import Feature, Observation


class FeatureExtractor(Protocol):
    """Contract implemented by components that produce normalized features."""

    def extract(self, observations: Iterable[Observation]) -> tuple[Feature, ...]:
        """Return normalized features for the supplied observations."""
        ...
