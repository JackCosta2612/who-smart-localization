"""Institutional source leads for Country Profiling."""

from __future__ import annotations

import datetime as dt
from typing import Any


def now_utc() -> str:
    return dt.datetime.now(dt.UTC).date().isoformat()


ITALY_SOURCE_LEADS: list[dict[str, str]] = [
    {
        "title": "Italy health system review or health system summary",
        "publisher": "European Observatory on Health Systems and Policies",
        "source_type": "Institutional profile",
        "url": "https://eurohealthobservatory.who.int/countries/italy",
        "date": "Latest available",
        "relevance": "Health system organization, governance, financing, workforce, infrastructure, regionalization, and reform context.",
        "status": "Candidate source lead",
    },
    {
        "title": "State of Health in the EU: Italy Country Health Profile",
        "publisher": "OECD / European Observatory / European Commission",
        "source_type": "Institutional profile",
        "url": "https://health.ec.europa.eu/state-health-eu/country-health-profiles_en",
        "date": "Latest available",
        "relevance": "Current EU-comparable health status, access, system performance, resilience, and risk context.",
        "status": "Candidate source lead",
    },
    {
        "title": "World Bank Data: Italy",
        "publisher": "World Bank",
        "source_type": "Dataset",
        "url": "https://data.worldbank.org/country/italy",
        "date": "Latest available",
        "relevance": "Baseline demographic, health expenditure, workforce, beds, WASH, and selected immunization indicators.",
        "status": "Candidate source lead",
    },
    {
        "title": "Italian Ministry of Health",
        "publisher": "Ministero della Salute",
        "source_type": "National ministry",
        "url": "https://www.salute.gov.it/",
        "date": "Current",
        "relevance": "National strategies, prevention plans, immunization policy, circulars, health system and digital-health material.",
        "status": "Candidate source lead",
    },
    {
        "title": "Istituto Superiore di Sanita",
        "publisher": "Istituto Superiore di Sanita",
        "source_type": "National public health institute",
        "url": "https://www.iss.it/",
        "date": "Current",
        "relevance": "Surveillance, public health guidance, EpiCentro topic pages, vaccination coverage, and epidemiological context.",
        "status": "Candidate source lead",
    },
    {
        "title": "Italian Medicines Agency vaccines page",
        "publisher": "AIFA",
        "source_type": "National medicines agency",
        "url": "https://www.aifa.gov.it/en/vaccini",
        "date": "Current",
        "relevance": "Vaccine authorization, quality, safety, and pharmacovigilance context.",
        "status": "Candidate source lead",
    },
    {
        "title": "National Vaccine Prevention Plan 2023-2025",
        "publisher": "Italian Ministry of Health / Conferenza Stato-Regioni / Gazzetta Ufficiale",
        "source_type": "Official document",
        "url": "https://www.gazzettaufficiale.it/eli/id/2023/08/21/23A04685/sg",
        "date": "2023",
        "relevance": "Core immunization policy source class for later Policy Comparison. Resolve plan and calendar attachments before reviewed use.",
        "status": "Candidate source lead",
    },
    {
        "title": "OECD, Eurostat, and EU health datasets",
        "publisher": "OECD / Eurostat / European Union",
        "source_type": "Dataset candidate source lead",
        "url": "https://ec.europa.eu/eurostat/web/health",
        "date": "Latest available",
        "relevance": "Comparable EU indicators, workforce, expenditure, access, demography, and regional context where relevant.",
        "status": "Candidate source lead",
    },
]


GENERIC_SOURCE_PRIORITY: list[dict[str, str]] = [
    {
        "title": "WHO country, regional, and WHO data sources",
        "publisher": "World Health Organization",
        "source_type": "WHO source class",
        "url": "https://www.who.int/countries",
        "date": "Latest available",
        "relevance": "WHO country and regional context, WHO data source discovery, and global source classes.",
        "status": "Candidate source lead",
    },
    {
        "title": "World Bank Data country page",
        "publisher": "World Bank",
        "source_type": "Dataset",
        "url": "https://data.worldbank.org/",
        "date": "Latest available",
        "relevance": "Comparable baseline development and public-health indicators.",
        "status": "Candidate source lead",
    },
    {
        "title": "National Ministry of Health",
        "publisher": "National government",
        "source_type": "National ministry",
        "url": "",
        "date": "Current",
        "relevance": "National strategies, policies, plans, circulars, reports, and official health system material.",
        "status": "Needs retrieval",
    },
    {
        "title": "National public health institute",
        "publisher": "National public health institute",
        "source_type": "National public health institute",
        "url": "",
        "date": "Current",
        "relevance": "Surveillance, health statistics, programme monitoring, outbreak, and implementation context.",
        "status": "Needs retrieval",
    },
    {
        "title": "National statistics office",
        "publisher": "National statistics office",
        "source_type": "National statistics office",
        "url": "",
        "date": "Current",
        "relevance": "Demography, mortality, regional statistics, and source triangulation.",
        "status": "Needs retrieval",
    },
]


def recommended_source_leads(country: str, iso3: str, focus: str | None = None) -> list[dict[str, Any]]:
    retrieval_date = now_utc()
    if country.casefold() == "italy" or iso3.upper() == "ITA":
        leads = ITALY_SOURCE_LEADS
    else:
        leads = GENERIC_SOURCE_PRIORITY

    output = []
    for lead in leads:
        enriched = dict(lead)
        enriched["country"] = country
        enriched["iso3"] = iso3
        enriched["focus"] = focus or ""
        enriched["retrieval_date"] = retrieval_date
        output.append(enriched)
    if focus and "immun" in focus.casefold():
        output.append(
            {
                "title": "WHO SMART Guidelines Digital Adaptation Kit for Immunization",
                "publisher": "World Health Organization",
                "source_type": "WHO SMART / DAK artifact",
                "url": "shared/assets/who-immunizations-dak.pdf",
                "date": "Local shared source",
                "relevance": "Available immunization DAK source for later Policy Comparison. Country Profiling should identify it as downstream comparison material without comparing it to national policy.",
                "status": "Candidate source lead",
                "country": country,
                "iso3": iso3,
                "focus": focus or "",
                "retrieval_date": retrieval_date,
            }
        )
    return output
