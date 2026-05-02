"""Unit tests for NOTAM parser."""

import pytest

from app.services.notam_parser import parse_notam


def test_parse_notam_expands_abbreviations() -> None:
    record = parse_notam("RWY CLSD")
    assert record.raw_text == "RWY CLSD"
    assert record.expanded_text == "Runway Closed"


def test_parse_notam_rejects_empty_text() -> None:
    with pytest.raises(ValueError):
        parse_notam("   ")
