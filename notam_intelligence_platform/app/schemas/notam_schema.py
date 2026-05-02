"""Validation schemas for NOTAM payloads."""

from __future__ import annotations


def validate_notam_text(notam_text: str) -> str:
    """Validate incoming NOTAM text and return a normalized string."""
    if not isinstance(notam_text, str):
        raise TypeError("NOTAM text must be a string")

    normalized = notam_text.strip()
    if not normalized:
        raise ValueError("NOTAM text cannot be empty")

    return normalized
