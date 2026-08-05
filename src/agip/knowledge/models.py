"""Domain models for the AGIP knowledge base."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EvidenceRef:
    """Reference to evidence supporting a knowledge entry."""

    source: str
    locator: str

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise ValueError("source must not be empty")
        if not self.locator.strip():
            raise ValueError("locator must not be empty")


@dataclass(frozen=True, slots=True)
class KnowledgeEntry:
    """Immutable unit of domain knowledge."""

    id: str
    statement: str
    tags: tuple[str, ...] = ()
    evidence: tuple[EvidenceRef, ...] = ()

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("id must not be empty")
        if not self.statement.strip():
            raise ValueError("statement must not be empty")
        if any(not tag.strip() for tag in self.tags):
            raise ValueError("tags must not contain empty values")
