"""Tests for the deterministic knowledge base."""

import pytest

from agip.knowledge import EvidenceRef, KnowledgeBase, KnowledgeEntry


def test_registers_and_returns_entries_in_stable_order() -> None:
    later = KnowledgeEntry(id="zeta", statement="Later entry")
    earlier = KnowledgeEntry(id="alpha", statement="Earlier entry")

    knowledge = KnowledgeBase([later, earlier])

    assert knowledge.all() == (earlier, later)
    assert knowledge.get("alpha") is earlier
    assert len(knowledge) == 2


def test_rejects_duplicate_identifiers() -> None:
    entry = KnowledgeEntry(id="pressure.high", statement="High pressure")
    knowledge = KnowledgeBase([entry])

    with pytest.raises(ValueError, match="duplicate knowledge entry id"):
        knowledge.add(entry)


def test_filters_entries_by_tag_deterministically() -> None:
    first = KnowledgeEntry(id="a", statement="A", tags=("pressure",))
    second = KnowledgeEntry(id="b", statement="B", tags=("pressure", "rhythm"))
    unrelated = KnowledgeEntry(id="c", statement="C", tags=("size",))

    knowledge = KnowledgeBase([unrelated, second, first])

    assert knowledge.find_by_tag("pressure") == (first, second)


def test_models_reject_invalid_values() -> None:
    with pytest.raises(ValueError, match="source must not be empty"):
        EvidenceRef(source=" ", locator="page:1")

    with pytest.raises(ValueError, match="statement must not be empty"):
        KnowledgeEntry(id="entry", statement=" ")


def test_unknown_identifier_is_explicit() -> None:
    with pytest.raises(KeyError, match="unknown knowledge entry id"):
        KnowledgeBase().get("missing")
