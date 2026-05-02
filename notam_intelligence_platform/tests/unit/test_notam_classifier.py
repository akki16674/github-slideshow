"""Unit tests for NOTAM classification rules."""

from app.services.notam_classifier import classify_notam


def test_classify_runway() -> None:
    assert classify_notam("RWY 09 CLSD") == "Runway"


def test_classify_taxiway() -> None:
    assert classify_notam("TWY B CLSD") == "Taxiway"


def test_classify_nav_aid() -> None:
    assert classify_notam("ILS U/S") == "Nav Aid"


def test_classify_airspace() -> None:
    assert classify_notam("TFR ACTIVE") == "Airspace"


def test_classify_other() -> None:
    assert classify_notam("BIRD ACTIVITY") == "Other"
