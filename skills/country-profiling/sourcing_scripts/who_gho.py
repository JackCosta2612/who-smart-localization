"""Conservative WHO GHO helper for Country Profiling.

This pass does not configure stable GHO indicator codes. The helper records
candidate source metadata and explicit statuses so the Agent never invents WHO
GHO values.
"""

from __future__ import annotations

import datetime as dt
from typing import Any

BASE_GHO_URL = "https://ghoapi.azureedge.net/api"


def now_utc() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()


def candidate_metadata(country: str, iso3: str, focus: str | None = None) -> list[dict[str, Any]]:
    retrieval_date = now_utc()
    terms = [
        "life expectancy",
        "mortality",
        "universal health coverage",
        "health expenditure",
        "health workforce",
        "water",
        "sanitation",
    ]
    if focus:
        terms.append(focus)
    return [
        {
            "source": "WHO Global Health Observatory",
            "title": "WHO Global Health Observatory OData API",
            "publisher": "World Health Organization",
            "source_type": "Dataset candidate source lead",
            "country": country,
            "iso3": iso3,
            "url": BASE_GHO_URL,
            "query_terms": terms,
            "retrieval_date": retrieval_date,
            "status": "candidate_source_lead",
            "notes": (
                "No stable GHO indicator codes are configured in this pass. "
                "Use as a candidate source lead or add reviewed indicator codes before retrieving values."
            ),
        }
    ]


def fetch_configured_indicators(
    country: str,
    iso3: str,
    focus: str | None = None,
) -> list[dict[str, Any]]:
    """Return explicit non-retrieval statuses until stable codes are configured."""

    return candidate_metadata(country, iso3, focus)
