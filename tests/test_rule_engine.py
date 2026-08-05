from dataclasses import dataclass

import pytest

from agip.domain import Trait
from agip.engine import Evaluator, Observations, RuleMatch, RuleRegistry


@dataclass(frozen=True, slots=True)
class MinimumValueRule:
    rule_id: str
    observation: str
    minimum: float
    trait: Trait

    def evaluate(self, observations: Observations) -> RuleMatch | None:
        value = observations.get(self.observation)
        if not isinstance(value, int | float) or value < self.minimum:
            return None
        return RuleMatch(
            rule_id=self.rule_id,
            trait=self.trait,
            confidence=0.8,
            observations=(self.observation,),
            explanation=f"{self.observation} met the minimum threshold",
        )


def test_evaluator_returns_explainable_matches_in_registration_order() -> None:
    focus = Trait(code="focus", name="Focus")
    energy = Trait(code="energy", name="Energy")
    registry = RuleRegistry(
        (
            MinimumValueRule("R-001", "spacing", 5.0, focus),
            MinimumValueRule("R-002", "pressure", 7.0, energy),
        )
    )

    result = Evaluator(registry).evaluate({"spacing": 6.0, "pressure": 8.0})

    assert [match.rule_id for match in result.matches] == ["R-001", "R-002"]
    assert result.traits == (focus, energy)
    assert result.matches[0].observations == ("spacing",)
    assert result.matches[0].explanation


def test_evaluator_ignores_rules_that_do_not_match() -> None:
    trait = Trait(code="focus", name="Focus")
    registry = RuleRegistry((MinimumValueRule("R-001", "spacing", 5.0, trait),))

    result = Evaluator(registry).evaluate({"spacing": 2.0})

    assert result.matches == ()


def test_registry_rejects_duplicate_rule_ids() -> None:
    trait = Trait(code="focus", name="Focus")
    rule = MinimumValueRule("R-001", "spacing", 5.0, trait)
    registry = RuleRegistry((rule,))

    with pytest.raises(ValueError, match="duplicate rule_id"):
        registry.register(rule)


def test_rule_match_rejects_invalid_confidence() -> None:
    with pytest.raises(ValueError, match="confidence"):
        RuleMatch(
            rule_id="R-001",
            trait=Trait(code="focus", name="Focus"),
            confidence=1.1,
            observations=("spacing",),
            explanation="invalid confidence",
        )
