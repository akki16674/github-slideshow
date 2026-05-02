"""Rule-based scoring for operational impact of NOTAM messages."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NotamImpactResult:
    """Structured result for NOTAM impact scoring."""

    score: int
    severity: str


def _has_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term in text for term in terms)


def is_relevant(text: str, departure: str, arrival: str) -> bool:
    """Return True when NOTAM text mentions departure or arrival aerodrome."""
    normalized_text = (text or "").upper()
    dep = (departure or "").strip().upper()
    arr = (arrival or "").strip().upper()
    return (dep and dep in normalized_text) or (arr and arr in normalized_text)


def score_notam_impact(notam_text: str, departure: str, arrival: str) -> NotamImpactResult:
    """Score NOTAM impact using rule-based aviation logic and route context."""
    text = (notam_text or "").upper()
    dep = (departure or "").strip().upper()
    arr = (arrival or "").strip().upper()
    score = 0

    runway_present = _has_any(text, ("RWY", "RUNWAY"))
    closed_present = _has_any(text, ("CLSD", "CLOSED"))

    if runway_present and closed_present:
        score += 45
    if _has_any(text, ("AD CLSD", "AERODROME CLOSED", "AIRPORT CLOSED")):
        score += 50

    if _has_any(text, ("ILS", "VOR", "NDB", "GNSS")) and _has_any(
        text, ("U/S", "UNSERVICEABLE", "OUT OF SERVICE")
    ):
        score += 25

    if _has_any(text, ("LIGHT", "LIGHTS", "LGTS", "PAPI", "VASIS")) and _has_any(
        text, ("U/S", "UNSERVICEABLE", "OUT", "OUT OF SERVICE")
    ):
        score += 20

    if _has_any(text, ("TWY", "TAXIWAY")) and closed_present:
        score += 15
    if "APRON" in text and closed_present:
        score += 10

    if _has_any(text, ("EMERGENCY", "SAR", "MIL OPS", "INTERCEPT")):
        score += 20

    if _has_any(text, ("TFR", "PROHIBITED", "RESTRICTED AREA ACTIVATED")):
        score += 30

    # Route-aware amplification if NOTAM explicitly references departure/arrival aerodromes.
    if is_relevant(text, dep, arr):
        if dep and dep in text:
            score += 30
        if arr and arr in text:
            score += 25

    score = max(0, min(score, 100))

    if score >= 80:
        severity = "CRITICAL"
    elif score >= 60:
        severity = "HIGH"
    elif score >= 30:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return NotamImpactResult(score=score, severity=severity)
