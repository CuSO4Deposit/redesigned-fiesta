from datetime import UTC, datetime, timedelta

import pytest

from pipeline.sanitize import (
    apply_embargo,
    cutoff,
    drop_denylisted,
    find_forbidden,
    load_denylist,
    select,
)

NOW = datetime(2026, 9, 25, 12, 0, tzinfo=UTC)


def test_cutoff_is_seven_days_back():
    assert cutoff(NOW) == NOW - timedelta(days=7)


def test_cutoff_rejects_a_naive_clock():
    with pytest.raises(ValueError):
        cutoff(datetime(2026, 9, 25, 12, 0))


def test_cutoff_rejects_negative_days():
    with pytest.raises(ValueError):
        cutoff(NOW, -1)


def test_embargo_keeps_old_and_the_boundary_drops_the_new():
    rows = [
        {"at": NOW - timedelta(days=8)},
        {"at": NOW - timedelta(days=7)},
        {"at": NOW - timedelta(days=6)},
    ]
    kept = apply_embargo(rows, time_of=lambda row: row["at"], now=NOW)
    assert kept == [
        {"at": NOW - timedelta(days=8)},
        {"at": NOW - timedelta(days=7)},
    ]


def test_select_returns_exactly_the_allowed_fields():
    assert select({"a": 1, "b": 2}, ["a"]) == {"a": 1}


def test_select_fails_when_a_projected_field_is_absent():
    with pytest.raises(KeyError):
        select({"a": 1}, ["a", "b"])


def test_load_denylist_ignores_comments_and_blanks():
    text = "# a comment\n\nfoo  # trailing\nbar\n"
    assert load_denylist(text) == frozenset({"foo", "bar"})


def test_drop_denylisted_matches_exactly_not_by_substring():
    rows = [{"n": "foo"}, {"n": "foobar"}, {"n": "bar"}]
    kept = drop_denylisted(rows, value_of=lambda row: row["n"], deny=frozenset({"foo"}))
    assert kept == [{"n": "foobar"}, {"n": "bar"}]


def test_find_forbidden_walks_nested_payloads():
    payload = {"a": [{"b": "see secret.example"}]}
    assert find_forbidden(payload, ["secret.example"]) == ["a.0.b"]


def test_find_forbidden_is_case_insensitive_and_clean_when_absent():
    assert find_forbidden({"x": "Sekret"}, ["sekret"]) == ["x"]
    assert find_forbidden({"x": "fine"}, ["sekret"]) == []
