"""Rule contract for the generic inference engine."""

from typing import Protocol

from agip.engine.models import Observations, RuleMatch


class Rule(Protocol):
    """A deterministic rule that may produce an explainable match."""

    @property
    def rule_id(self) -> str:
        """Return the stable identifier for this rule."""

    def evaluate(self, observations: Observations) -> RuleMatch | None:
        """Evaluate observations and return a match when the rule applies."""
