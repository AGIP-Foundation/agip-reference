"""Tests for executable graphology rule models."""

import pytest

from agip.graphology import (
    ComparisonOperator,
    GraphologyRule,
    RuleCondition,
    RuleOutcome,
)


def test_rule_returns_explainable_outcome_when_all_conditions_match() -> None:
    outcome = RuleOutcome(
        trait="self_control",
        score=0.7,
        confidence=0.8,
        explanation="Regular pressure and stable baseline support this inference.",
    )
    rule = GraphologyRule(
        rule_id="graphology.self_control.001",
        conditions=(
            RuleCondition("pressure", ComparisonOperator.EQUALS, "regular"),
            RuleCondition("baseline_stability", ComparisonOperator.GREATER_THAN_OR_EQUAL, 0.7),
        ),
        outcome=outcome,
        priority=10,
        knowledge_refs=("kb.pressure.regular", "kb.baseline.stable"),
    )

    result = rule.evaluate({"baseline_stability": 0.8, "pressure": "regular"})

    assert result == outcome
    assert result.explanation
    assert rule.knowledge_refs == ("kb.pressure.regular", "kb.baseline.stable")


def test_rule_returns_none_when_a_condition_does_not_match() -> None:
    rule = GraphologyRule(
        rule_id="graphology.energy.001",
        conditions=(RuleCondition("pressure", ComparisonOperator.EQUALS, "strong"),),
        outcome=RuleOutcome("energy", 0.6, 0.7, "Strong pressure may support vitality."),
    )

    assert rule.evaluate({"pressure": "light"}) is None
    assert rule.evaluate({}) is None


@pytest.mark.parametrize(
    ("operator", "expected", "actual", "matches"),
    [
        (ComparisonOperator.GREATER_THAN, 0.5, 0.6, True),
        (ComparisonOperator.GREATER_THAN_OR_EQUAL, 0.5, 0.5, True),
        (ComparisonOperator.LESS_THAN, 0.5, 0.4, True),
        (ComparisonOperator.LESS_THAN_OR_EQUAL, 0.5, 0.5, True),
        (ComparisonOperator.NOT_EQUALS, "left", "right", True),
    ],
)
def test_condition_operators(
    operator: ComparisonOperator,
    expected: str | float,
    actual: str | float,
    matches: bool,
) -> None:
    condition = RuleCondition("feature", operator, expected)

    assert condition.matches({"feature": actual}) is matches


def test_numeric_comparison_rejects_non_numeric_values() -> None:
    condition = RuleCondition("slant", ComparisonOperator.GREATER_THAN, 0.5)

    assert condition.matches({"slant": "right"}) is False
    assert condition.matches({"slant": True}) is False


def test_invalid_models_are_rejected_explicitly() -> None:
    with pytest.raises(ValueError, match="feature must not be empty"):
        RuleCondition(" ", ComparisonOperator.EQUALS, "value")
    with pytest.raises(ValueError, match="score must be between"):
        RuleOutcome("trait", 1.1, 0.5, "Explanation")
    with pytest.raises(ValueError, match="confidence must be between"):
        RuleOutcome("trait", 0.5, -0.1, "Explanation")
    with pytest.raises(ValueError, match="conditions must not be empty"):
        GraphologyRule(
            rule_id="rule",
            conditions=(),
            outcome=RuleOutcome("trait", 0.5, 0.5, "Explanation"),
        )
    with pytest.raises(ValueError, match="knowledge references must be unique"):
        GraphologyRule(
            rule_id="rule",
            conditions=(RuleCondition("feature", ComparisonOperator.EQUALS, "value"),),
            outcome=RuleOutcome("trait", 0.5, 0.5, "Explanation"),
            knowledge_refs=("kb.one", "kb.one"),
        )
