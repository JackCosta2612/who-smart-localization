"""OECD and European institutional source-lead helpers.

Full OECD SDMX retrieval is intentionally not implemented in this pass. OECD,
EU, Eurostat, and European Observatory sources are represented as institutional
source leads for review or document retrieval.
"""

from __future__ import annotations

import datetime as dt
from typing import Any


def now_utc() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()


def source_metadata(country: str, iso3: str, focus: str | None = None) -> list[dict[str, Any]]:
    retrieval_date = now_utc()
    return [
        {
            "source": "OECD / European Observatory / European Commission",
            "title": f"State of Health in the EU Country Health Profile - {country}",
            "publisher": "OECD / European Observatory / European Commission",
            "source_type": "Institutional profile candidate source lead",
            "country": country,
            "iso3": iso3,
            "url": "https://health.ec.europa.eu/state-health-eu/country-health-profiles_en",
            "retrieval_date": retrieval_date,
            "status": "manual_review_needed",
            "notes": (
                "Resolve the country-specific publication and direct PDF before marking reviewed. "
                "Do not treat this landing page as the PDF."
            ),
        },
        {
            "source": "European Observatory on Health Systems and Policies",
            "title": f"Health system review or health system summary - {country}",
            "publisher": "European Observatory on Health Systems and Policies",
            "source_type": "Institutional profile candidate source lead",
            "country": country,
            "iso3": iso3,
            "url": "https://eurohealthobservatory.who.int/countries",
            "retrieval_date": retrieval_date,
            "status": "manual_review_needed",
            "notes": "Resolve the country page to the relevant reviewed PDF or official profile before citing.",
        },
    ]
