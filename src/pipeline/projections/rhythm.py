"""Arcaea's public numbers, as of the embargo cutoff.

Y-Offline's `potential_trend` replays the best pool in record order, so the point at
each play reflects only the plays up to it — the series is causal. That is what makes
the embargo cheap here: drop the points newer than the cutoff and keep the last, and
you have the headline as it stood seven days ago, with no change to Y-Offline and no
second copy of the v7 top-ten double weight.

`through` is the date of that last kept play, not the cutoff date, so a page says when
the data actually ends rather than when the window opened.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from ..config import Config
from ..sanitize import apply_embargo


def _tz(config: Config):
    return ZoneInfo(config.local_tz) if config.local_tz else UTC


def build(config: Config, now: datetime) -> dict[str, object] | None:
    """The Arcaea projection, or None when no catalogue / database is configured."""
    if not (config.yoffline_db and config.yoffline_user and config.arcaea_charts):
        return None

    from y_offline.arcaea.utils import ArcaeaChartRepository, ArcaeaManager

    manager = ArcaeaManager(
        chart_repo=ArcaeaChartRepository(
            arcsong_path=Path(config.arcaea_charts).expanduser()
        ),
        userdb_path=Path(config.yoffline_db).expanduser(),
    )

    points = manager.potential_trend(config.yoffline_user, only_changes=False)
    kept = apply_embargo(
        points,
        time_of=lambda point: datetime.fromtimestamp(point.at, tz=UTC),
        now=now,
        days=config.embargo_days,
    )
    if not kept:
        return None
    last = kept[-1]

    return {
        "through": datetime.fromtimestamp(last.at, tz=_tz(config)).date().isoformat(),
        "arcaea": {
            "potential": round(last.potential, 4),
            "b50_average": round(last.b50_average, 4),
            "b50_size": last.b50_size,
            "best_capacity": manager.best_capacity,
        },
    }
