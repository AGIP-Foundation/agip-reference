"""Deterministic in-memory knowledge base."""

from collections.abc import Iterable

from .models import KnowledgeEntry


class KnowledgeBase:
    """Register and query immutable knowledge entries by stable identifiers."""

    def __init__(self, entries: Iterable[KnowledgeEntry] = ()) -> None:
        self._entries: dict[str, KnowledgeEntry] = {}
        for entry in entries:
            self.add(entry)

    def add(self, entry: KnowledgeEntry) -> None:
        """Register one entry, rejecting duplicate identifiers."""
        if entry.id in self._entries:
            raise ValueError(f"duplicate knowledge entry id: {entry.id}")
        self._entries[entry.id] = entry

    def get(self, entry_id: str) -> KnowledgeEntry:
        """Return one entry by identifier."""
        try:
            return self._entries[entry_id]
        except KeyError as exc:
            raise KeyError(f"unknown knowledge entry id: {entry_id}") from exc

    def all(self) -> tuple[KnowledgeEntry, ...]:
        """Return all entries ordered by identifier."""
        return tuple(self._entries[key] for key in sorted(self._entries))

    def find_by_tag(self, tag: str) -> tuple[KnowledgeEntry, ...]:
        """Return entries containing a tag, ordered by identifier."""
        return tuple(entry for entry in self.all() if tag in entry.tags)

    def __len__(self) -> int:
        return len(self._entries)
