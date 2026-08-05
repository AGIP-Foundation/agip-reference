"""Immutable models for deterministic analysis execution."""

from dataclasses import dataclass

from agip.features import Feature, Observation
from agip.graphology import RuleOutcome


@dataclass(frozen=True, slots=True)
class AnalysisContext:
    """Validated input context for one analysis execution."""

    observations: tuple[Observation, ...]

    def __post_init__(self) -> None:
        if not self.observations:
            raise ValueError("observations must not be empty")


@dataclass(frozen=True, slots=True)
class RuleTrace:
    """Trace entry describing one evaluated graphology rule."""

    rule_id: str
    matched: bool
    priority: int
    knowledge_refs: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class AnalysisResult:
    """Structured, reproducible output of an analysis execution."""

    features: tuple[Feature, ...]
    inferences: tuple[RuleOutcome, ...]
    trace: tuple[RuleTrace, ...]
