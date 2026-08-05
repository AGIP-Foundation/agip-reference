"""Core data models used by the inference engine."""

from dataclasses import dataclass

from agip.domain import Trait

type ObservationValue = str | int | float | bool
type Observations = dict[str, ObservationValue]


@dataclass(frozen=True, slots=True)
class RuleMatch:
    """A successful, explainable rule evaluation."""

    rule_id: str
    trait: Trait
    confidence: float
    observations: tuple[str, ...]
    explanation: str

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
        if not self.rule_id.strip():
            raise ValueError("rule_id must not be empty")
        if not self.explanation.strip():
            raise ValueError("explanation must not be empty")


@dataclass(frozen=True, slots=True)
class InferenceResult:
    """Deterministic collection of rule matches produced by an evaluation."""

    matches: tuple[RuleMatch, ...]

    @property
    def traits(self) -> tuple[Trait, ...]:
        """Return inferred traits in rule evaluation order."""

        return tuple(match.trait for match in self.matches)
