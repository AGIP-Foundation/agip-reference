"""Domain models for normalized feature extraction."""

from dataclasses import dataclass

type ScalarValue = str | int | float | bool


@dataclass(frozen=True, slots=True)
class Observation:
    """Raw named observation supplied to the feature layer."""

    name: str
    value: ScalarValue
    confidence: float = 1.0

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("name must not be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
        if isinstance(self.value, str) and not self.value.strip():
            raise ValueError("string values must not be empty")


@dataclass(frozen=True, slots=True)
class Feature:
    """Normalized feature ready to be consumed by inference rules."""

    name: str
    value: ScalarValue
    confidence: float
