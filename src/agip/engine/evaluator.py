"""Rule evaluator implementation."""

from agip.engine.models import InferenceResult, Observations
from agip.engine.registry import RuleRegistry


class Evaluator:
    """Evaluate registered rules without domain-specific knowledge."""

    def __init__(self, registry: RuleRegistry) -> None:
        self._registry = registry

    def evaluate(self, observations: Observations) -> InferenceResult:
        """Return all successful rule matches in registration order."""

        matches = tuple(
            match
            for rule in self._registry
            if (match := rule.evaluate(observations)) is not None
        )
        return InferenceResult(matches=matches)
