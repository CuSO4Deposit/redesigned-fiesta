"""What every page carries: the date the published data runs through.

Not `now - embargo_days`: that is when the window opened, not when the data ends. With
a source that stopped months ago it would round a March number up to September. The
site is only as current as its stalest source, so this is the earliest source date, and
only falls back to the cutoff when there is no data at all.
"""

from __future__ import annotations

from datetime import UTC, datetime

from ..sanitize import cutoff


def build(
    now: datetime,
    embargo_days: int,
    through_dates: list[str],
) -> dict[str, object]:
    dates = sorted(date for date in through_dates if date)
    through = dates[0] if dates else cutoff(now, embargo_days).date().isoformat()
    return {
        "through": through,
        "embargo_days": embargo_days,
        "built_at": now.astimezone(UTC).isoformat(timespec="seconds"),
    }
