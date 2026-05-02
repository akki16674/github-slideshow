"""Unit tests for end-to-end NOTAM processing pipeline."""

from app.main import process_notam


def test_pipeline_returns_analysis_with_severity() -> None:
    result = process_notam("RWY 09 CLSD. TFR ACTIVE", departure="KJFK", arrival="KLAX")
    assert result.departure == "KJFK"
    assert result.arrival == "KLAX"
    assert result.expanded_text.startswith("Runway")
    assert result.impact_score >= 75
    assert result.severity in {"HIGH", "CRITICAL"}
    assert result.category == "Runway"
