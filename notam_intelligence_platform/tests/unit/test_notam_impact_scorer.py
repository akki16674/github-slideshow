"""Unit tests for rule-based NOTAM impact scoring."""

from app.services.notam_impact_scorer import is_relevant, score_notam_impact


def test_is_relevant_matches_departure_or_arrival() -> None:
    assert is_relevant("NOTAM FOR KJFK", "KJFK", "KLAX") is True
    assert is_relevant("NOTAM FOR KLAX", "KJFK", "KLAX") is True
    assert is_relevant("NOTAM FOR KORD", "KJFK", "KLAX") is False


def test_runway_closure_is_high_impact() -> None:
    result = score_notam_impact("RWY 09/27 CLSD DUE WIP", departure="KJFK", arrival="KLAX")
    assert result.score >= 45
    assert result.severity in {"MEDIUM", "HIGH", "CRITICAL"}


def test_expanded_runway_closure_is_high_impact() -> None:
    result = score_notam_impact(
        "Runway 09/27 Closed due work in progress", departure="KJFK", arrival="KLAX"
    )
    assert result.score >= 45


def test_route_match_increases_score() -> None:
    baseline = score_notam_impact("RWY CLSD", departure="", arrival="")
    route_specific = score_notam_impact("KJFK RWY CLSD", departure="KJFK", arrival="KLAX")
    assert route_specific.score >= baseline.score + 30


def test_combined_major_outages_are_critical() -> None:
    result = score_notam_impact(
        "AIRPORT CLOSED. ILS U/S. TFR ACTIVE", departure="KJFK", arrival="KLAX"
    )
    assert result.score == 100
    assert result.severity == "CRITICAL"


def test_minor_notice_is_low() -> None:
    result = score_notam_impact("BIRD ACTIVITY IN VICINITY", departure="KJFK", arrival="KLAX")
    assert result.score == 0
    assert result.severity == "LOW"


def test_relevance_filter() -> None:
    assert is_relevant("RWY CLSD AT VOBL", "VOBL", "VABB") is True
    assert is_relevant("RWY CLSD AT XXXX", "VOBL", "VABB") is False
