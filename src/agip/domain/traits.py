"""Trait models inferred by the rule engine."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Trait:
    """A domain trait that can be inferred from observations."""

    code: str
    name: str
    description: str = ""

    def __post_init__(self) -> None:
        if not self.code.strip():
            raise ValueError("trait code must not be empty")
        if not self.name.strip():
            raise ValueError("trait name must not be empty")
