"""The publish contract, as code.

Everything the homepage publishes passes through this module before it is
written. It is deliberately pure — no clock, no filesystem, no CPI — so the one
component whose mistake is a leak is also the one component that is trivial to
test. The clock is passed in; the caller reads it.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from datetime import datetime, timedelta
from typing import Any

DEFAULT_EMBARGO_DAYS = 7


def _aware(moment: datetime) -> datetime:
    if moment.tzinfo is None or moment.tzinfo.utcoffset(moment) is None:
        raise ValueError(f"{moment!r} is not timezone-aware")
    return moment


def cutoff(now: datetime, days: int = DEFAULT_EMBARGO_DAYS) -> datetime:
    """The newest instant that may be published: nothing after ``now - days``.

    The window is what keeps the public feed off the present, so that no page can
    become a live signal of where someone is or what they are doing right now.
    """
    if days < 0:
        raise ValueError("embargo days must be >= 0")
    return _aware(now) - timedelta(days=days)


def apply_embargo[T](
    rows: Iterable[T],
    *,
    time_of: Callable[[T], datetime],
    now: datetime,
    days: int = DEFAULT_EMBARGO_DAYS,
) -> list[T]:
    """Drop rows whose event time is newer than the cutoff.

    The boundary is inclusive on the older side: a row exactly on the cutoff is
    kept, so "7 days" means "through seven days ago".
    """
    gate = cutoff(now, days)
    return [row for row in rows if _aware(time_of(row)) <= gate]


def select(row: Mapping[str, Any], allowed: Iterable[str]) -> dict[str, Any]:
    """Default-deny projection: emit exactly ``allowed``.

    A projected field that is absent upstream is an error, not a silent omission:
    a renamed column must stop the build, not quietly drop something a page still
    refers to.
    """
    keys = tuple(allowed)
    missing = [key for key in keys if key not in row]
    if missing:
        raise KeyError(f"row is missing projected field(s): {', '.join(missing)}")
    return {key: row[key] for key in keys}


def load_denylist(text: str) -> frozenset[str]:
    """Parse a denylist file: one name per line, ``#`` comments and blanks ignored."""
    names = set()
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            names.add(line)
    return frozenset(names)


def drop_denylisted[T](
    rows: Iterable[T],
    *,
    value_of: Callable[[T], str],
    deny: frozenset[str],
) -> list[T]:
    """Keep rows whose value is not on the denylist, matched exactly (as in CPI)."""
    return [row for row in rows if value_of(row) not in deny]


def find_forbidden(payload: Any, forbidden: Iterable[str]) -> list[str]:
    """Every path in a JSON-ish payload whose string contains a forbidden term.

    The safety net for a projection mistake: run it on the assembled payload right
    before writing, and a leak becomes a failed build rather than a published one.
    """
    terms = [term.casefold() for term in forbidden]

    def walk(node: Any, path: tuple[str, ...]) -> list[str]:
        if isinstance(node, str):
            low = node.casefold()
            if any(term in low for term in terms):
                return [".".join(path) if path else "<root>"]
            return []
        if isinstance(node, Mapping):
            hits: list[str] = []
            for key, value in node.items():
                hits += walk(value, (*path, str(key)))
            return hits
        if isinstance(node, (list, tuple)):
            hits = []
            for index, value in enumerate(node):
                hits += walk(value, (*path, str(index)))
            return hits
        return []

    return walk(payload, ())
