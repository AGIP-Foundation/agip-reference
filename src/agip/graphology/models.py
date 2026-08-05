"""Typed domain models for executable graphology rules."""

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum

type ScalarValue = str | int | float | bool


class ComparisonOperator(StrEnum):
    """Supported deterministic comparison operators."""

    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    GREATER_THAN = "greater_than"
    GREATER_THAN_OR_EQUAL = "greater_than_or_equal"
    LESS_THAN = "less_than"
    LESS_THAN_OR_EQUAL = "less_than_or_equal"


@dataclass(frozen=True, slots=True)
class RuleCondition:
    """Single condition evaluated against a normalized feature map."""

    feature: str
    operator: ComparisonOperator
    expected: ScalarValue

    def __post_init__(self) -> None:
        if not self.feature.strip():
            raise ValueError("feature must not be empty")

    def matches(self, features: Mapping[str, ScalarValue]) -> bool:
        """Return whether this condition matches the supplied features."""
        if self.feature not in features:
            return False
        actual = features[self.feature]
        if self.operator is ComparisonOperator.EQUALS:
            return actual == self.expected
        if self.operator is ComparisonOperator.NOT_EQUALS:
            return actual != self.expected
        if not isinstance(actual, (int, float)) or isinstance(actual, bool):
            return False
        if not isinstance(self.expected, (int, float)) or isinstance(
            self.expected, bool
        ):
            return False
        if self.operator is ComparisonOperator.GREATER_THAN:
            return actual > self.expected
        if self.operator is ComparisonOperator.GREATER_THAN_OR_EQUAL:
            return actual >= self.expected
        if self.operator is ComparisonOperator.LESS_THAN:
            return actual < self.expected
        return actual <= self.expected


@dataclass(frozen=True, slots=True)
class RuleOutcome:
    """Inference emitted by a matched graphology rule."""

    trait: str
    score: float
    confidence: float
    explanation: str

    def __post_init__(self) -> None:
        if not self.trait.strip():
            raise ValueError("trait must not be empty")
        if not -1.0 <= self.score <= 1.0:
            raise ValueError("score must be between -1.0 and 1.0")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
        if not self.explanation.strip():
            raise ValueError("explanation must not be empty")


@dataclass(frozen=True, slots=True)
class GraphologyRule:
    """Immutable, explainable graphology rule."""

    rule_id: str
    conditions: tuple[RuleCondition, ...]
    outcome: RuleOutcome
    priority: int = 0
    knowledge_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.rule_id.strip():
            raise ValueError("rule_id must not be empty")
        if not self.conditions:
            raise ValueError("conditions must not be empty")
        if any(not reference.strip() for reference in self.knowledge_refs):
            raise ValueError("knowledge references must not be empty")
        if len(set(self.knowledge_refs)) != len(self.knowledge_refs):
            raise ValueError("knowledge references must be unique")

    def evaluate(self, features: Mapping[str, ScalarValue]) -> RuleOutcome | None:
        """Return the outcome when all conditions match."""
        if all(condition.matches(features) for condition in self.conditions):
            return self.outcome
        return None
