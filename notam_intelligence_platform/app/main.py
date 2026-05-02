"""Application entry point for NOTAM Intelligence Platform."""

from __future__ import annotations

from app.services.notam_analyzer import NotamAnalysis, analyze_notam
from app.services.notam_parser import parse_notam


def process_notam(notam_text: str, departure: str, arrival: str) -> NotamAnalysis:
    """Run the full NOTAM pipeline: validate -> expand -> score."""
    parsed = parse_notam(notam_text)
    return analyze_notam(parsed, departure=departure.strip().upper(), arrival=arrival.strip().upper())


def main() -> None:
    """Run a small demo pipeline execution."""
    sample = "RWY 09/27 CLSD. ILS U/S."
    result = process_notam(sample, departure="KJFK", arrival="KLAX")
    print(result)


if __name__ == "__main__":
    main()
