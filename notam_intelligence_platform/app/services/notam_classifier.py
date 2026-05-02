"""NOTAM category classification utilities."""

from __future__ import annotations


def classify_notam(text: str) -> str:
    """Classify NOTAM text into a high-level operational category."""
    text = (text or "").upper()

    if "RWY" in text or "RUNWAY" in text:
        return "Runway"
    if "TWY" in text or "TAXIWAY" in text:
        return "Taxiway"
    if "ILS" in text or "VOR" in text:
        return "Nav Aid"
    if "TFR" in text or "RESTRICTED" in text:
        return "Airspace"
    return "Other"
