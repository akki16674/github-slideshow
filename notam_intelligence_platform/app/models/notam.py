"""Data models for NOTAM entities."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NotamRecord:
    """Raw and normalized NOTAM text."""

    raw_text: str
    expanded_text: str


@dataclass(frozen=True)
class NotamAnalysis:
    """Structured analysis output for a processed NOTAM."""

    departure: str
    arrival: str
    raw_text: str
    expanded_text: str
    impact_score: int
    severity: str
    category: str
