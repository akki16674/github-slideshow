"""Unit tests for NOTAM abbreviation expansion."""

from app.services.notam_abbreviation_expander import expand_notam_abbreviations


def test_expand_known_abbreviations() -> None:
    text = "RWY 27 CLSD, TWY B WIP"
    assert (
        expand_notam_abbreviations(text)
        == "Runway 27 Closed, Taxiway B Work in Progress"
    )


def test_case_insensitive_expansion() -> None:
    text = "rwy 09 clsd"
    assert expand_notam_abbreviations(text) == "Runway 09 Closed"


def test_custom_abbreviation_override() -> None:
    text = "PPR required for APRON access"
    assert (
        expand_notam_abbreviations(text, {"PPR": "Permission Needed"})
        == "Permission Needed required for Apron access"
    )
