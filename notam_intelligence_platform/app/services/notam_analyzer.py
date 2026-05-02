"""NOTAM analysis service."""

from __future__ import annotations

from app.models.notam import NotamAnalysis, NotamRecord
from app.services.notam_classifier import classify_notam
from app.services.notam_impact_scorer import score_notam_impact


def analyze_notam(record: NotamRecord, departure: str, arrival: str) -> NotamAnalysis:
    """Analyze normalized NOTAM text and produce impact metadata."""
    combined_text = f"{record.raw_text} {record.expanded_text}"
    impact = score_notam_impact(record.expanded_text, departure=departure, arrival=arrival)
    category = classify_notam(combined_text)
    return NotamAnalysis(
        departure=departure,
        arrival=arrival,
        raw_text=record.raw_text,
        expanded_text=record.expanded_text,
        impact_score=impact.score,
        severity=impact.severity,
        category=category,
    )
