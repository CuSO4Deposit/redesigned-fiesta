from datetime import UTC, datetime

from pipeline.projections.meta import build

NOW = datetime(2026, 9, 26, tzinfo=UTC)


def test_through_is_the_oldest_source_date_not_the_window():
    out = build(NOW, 7, ["2026-03-01", "2026-09-19"])
    assert out["through"] == "2026-03-01"


def test_through_falls_back_to_the_cutoff_when_there_is_no_data():
    out = build(NOW, 7, [])
    assert out["through"] == "2026-09-19"
