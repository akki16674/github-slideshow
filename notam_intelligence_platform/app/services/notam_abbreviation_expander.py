"""Utilities for expanding common NOTAM abbreviations."""

from __future__ import annotations

import re
from collections.abc import Mapping

DEFAULT_NOTAM_ABBREVIATIONS: dict[str, str] = {
    "RWY": "Runway",
    "TWY": "Taxiway",
    "APRON": "Apron",
    "CLSD": "Closed",
    "WIP": "Work in Progress",
    "BTN": "Between",
    "SFC": "Surface",
    "FL": "Flight Level",
    "U/S": "Unserviceable",
    "NAV": "Navigation",
    "LGTS": "Lights",
    "PPR": "Prior Permission Required",
}


def expand_notam_abbreviations(
    text: str,
    abbreviations: Mapping[str, str] | None = None,
) -> str:
    """Expand NOTAM abbreviations found in ``text``.

    The matching is case-insensitive and only replaces complete terms.
    A custom abbreviation dictionary can be provided to override defaults.
    """
    if not text:
        return text

    terms = dict(DEFAULT_NOTAM_ABBREVIATIONS)
    if abbreviations:
        terms.update({k.upper(): v for k, v in abbreviations.items()})

    # Sort longest-first to avoid partial matches winning.
    escaped_terms = sorted((re.escape(term) for term in terms), key=len, reverse=True)
    pattern = re.compile(r"\b(" + "|".join(escaped_terms) + r")\b", flags=re.IGNORECASE)

    def _replace(match: re.Match[str]) -> str:
        token = match.group(0)
        return terms.get(token.upper(), token)

    return pattern.sub(_replace, text)
