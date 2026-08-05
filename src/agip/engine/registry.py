"""Registry for inference rules."""

from collections.abc import Iterable, Iterator

from agip.engine.rule import Rule


class RuleRegistry:
    """Store rules in deterministic registration order."""

    def __init__(self, rules: Iterable[Rule] = ()) -> None:
        self._rules: dict[str, Rule] = {}
        for rule in rules:
            self.register(rule)

    def register(self, rule: Rule) -> None:
        """Register a rule and reject duplicate identifiers."""

        if not rule.rule_id.strip():
            raise ValueError("rule_id must not be empty")
        if rule.rule_id in self._rules:
            raise ValueError(f"duplicate rule_id: {rule.rule_id}")
        self._rules[rule.rule_id] = rule

    def __iter__(self) -> Iterator[Rule]:
        return iter(self._rules.values())

    def __len__(self) -> int:
        return len(self._rules)
