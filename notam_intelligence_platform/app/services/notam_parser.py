"""NOTAM parsing service."""

from __future__ import annotations

from app.models.notam import NotamRecord
from app.schemas.notam_schema import validate_notam_text
from app.services.notam_abbreviation_expander import expand_notam_abbreviations


def parse_notam(notam_text: str) -> NotamRecord:
    """Validate and normalize a NOTAM into a structured record."""
    raw = validate_notam_text(notam_text)
    expanded = expand_notam_abbreviations(raw)
    return NotamRecord(raw_text=raw, expanded_text=expanded)
