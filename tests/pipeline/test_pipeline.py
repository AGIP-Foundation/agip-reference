"""Integration tests for the deterministic analysis pipeline."""

import pytest

from agip.features import Observation
from agip.graphology import (
    ComparisonOperator,
    GraphologyRule,
    RuleCondition,
    RuleOutcome,
)
from agip.pipeline import AnalysisContext, AnalysisPipeline


def _rule(
    rule_id: str,
    feature: str,
    expected: str,
    trait: str,
    priority: int,
) -> GraphologyRule:
    return GraphologyRule(
        rule_id=rule_id,
        conditions=(RuleCondition(feature, ComparisonOperator.EQUALS, expected),),
        outcome=RuleOutcome(
            trait=trait,
            score=0.6,
            confidence=0.8,
            explanation=f"{feature} supports {trait}.",
        ),
        priority=priority,
        knowledge_refs=(f"kb.{feature}.{expected}",),
    )


def test_pipeline_runs_end_to_end_with_stable_trace() -> None:
    pipeline = AnalysisPipeline(
        (
            _rule("graphology.energy.001", "pressure", "strong", "energy", 5),
            _rule(
                "graphology.self_control.001",
                "pressure",
                "regular",
                "self_control",
                10,
            ),
        )
    )

    result = pipeline.analyze((Observation("Pressure", " Regular "),))

    assert tuple(feature.name for feature in result.features) == ("pressure",)
    assert tuple(outcome.trait for outcome in result.inferences) == ("self_control",)
    assert tuple(entry.rule_id for entry in result.trace) == (
        "graphology.self_control.001",
        "graphology.energy.001",
    )
    assert tuple(entry.matched for entry in result.trace) == (True, False)
    assert result.trace[0].knowledge_refs == ("kb.pressure.regular",)


def test_pipeline_is_deterministic_for_rule_input_order() -> None:
    first = _rule("rule.b", "slant", "right", "sociability", 1)
    second = _rule("rule.a", "slant", "right", "openness", 1)
    observations = (Observation("slant", "right"),)

    first_result = AnalysisPipeline((first, second)).analyze(observations)
    second_result = AnalysisPipeline((second, first)).analyze(observations)

    assert first_result == second_result
    assert tuple(entry.rule_id for entry in first_result.trace) == ("rule.a", "rule.b")


def test_pipeline_rejects_duplicate_rule_identifiers() -> None:
    rule = _rule("rule.duplicate", "pressure", "regular", "control", 1)

    with pytest.raises(ValueError, match="rule identifiers must be unique"):
        AnalysisPipeline((rule, rule))


def test_analysis_context_requires_observations() -> None:
    with pytest.raises(ValueError, match="observations must not be empty"):
        AnalysisContext(())
