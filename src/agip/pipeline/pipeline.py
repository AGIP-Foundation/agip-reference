"""Deterministic orchestration of normalized observations and graphology rules."""

from collections.abc import Iterable

from agip.features import Normalizer, Observation, ScalarValue
from agip.graphology import GraphologyRule, RuleOutcome
from agip.pipeline.models import AnalysisContext, AnalysisResult, RuleTrace


class AnalysisPipeline:
    """Normalize observations, evaluate rules, and preserve an execution trace."""

    def __init__(
        self,
        rules: Iterable[GraphologyRule],
        normalizer: Normalizer | None = None,
    ) -> None:
        ordered_rules = tuple(sorted(rules, key=lambda rule: (-rule.priority, rule.rule_id)))
        rule_ids = tuple(rule.rule_id for rule in ordered_rules)
        if len(set(rule_ids)) != len(rule_ids):
            raise ValueError("rule identifiers must be unique")
        self._rules = ordered_rules
        self._normalizer = normalizer or Normalizer()

    def run(self, context: AnalysisContext) -> AnalysisResult:
        """Execute the complete MVP flow and return a stable result."""
        features = self._normalizer.normalize(context.observations)
        feature_map: dict[str, ScalarValue] = {
            feature.name: feature.value for feature in features
        }
        inferences: list[RuleOutcome] = []
        trace: list[RuleTrace] = []

        for rule in self._rules:
            outcome = rule.evaluate(feature_map)
            matched = outcome is not None
            if outcome is not None:
                inferences.append(outcome)
            trace.append(
                RuleTrace(
                    rule_id=rule.rule_id,
                    matched=matched,
                    priority=rule.priority,
                    knowledge_refs=rule.knowledge_refs,
                )
            )

        return AnalysisResult(
            features=features,
            inferences=tuple(inferences),
            trace=tuple(trace),
        )

    def analyze(self, observations: Iterable[Observation]) -> AnalysisResult:
        """Convenience wrapper that builds an analysis context."""
        return self.run(AnalysisContext(tuple(observations)))
