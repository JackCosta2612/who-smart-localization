"""Configured source targets and unresolved gaps for Country Profiling."""

from __future__ import annotations

from typing import Any

EUROHEALTH_ROOT = "https://eurohealthobservatory.who.int/overview"


def configured_source_targets(country: str, iso3: str, focus: str | None = None) -> list[dict[str, Any]]:
    """Return source targets that the deterministic runner should actually resolve."""

    focus_text = focus or ""
    if country.casefold() == "italy" or iso3.upper() == "ITA":
        targets: list[dict[str, Any]] = [
            {
                "target_type": "html",
                "title": "EuroHealthObservatory Italy country page",
                "publisher": "European Observatory on Health Systems and Policies",
                "source_type": "Web-reviewed institutional country page",
                "url": "https://eurohealthobservatory.who.int/countries/italy",
                "root_url": EUROHEALTH_ROOT,
                "date": "Latest available",
                "download_pdfs": True,
                "max_downloads": 3,
                "excerpt_keywords": [
                    "Country overview",
                    "Italy's National Health Service",
                    "The SSN is regionally based",
                ],
            },
            {
                "target_type": "html",
                "title": "National Vaccine Prevention Plan 2023-2025 official act",
                "publisher": "Gazzetta Ufficiale / Italian Ministry of Health",
                "source_type": "Official full-text HTML",
                "url": (
                    "https://www.gazzettaufficiale.it/atto/vediMenuHTML?"
                    "atto.dataPubblicazioneGazzetta=2023-08-21&"
                    "atto.codiceRedazionale=23A04685&tipoSerie=serie_generale&"
                    "tipoVigenza=originario"
                ),
                "date": "2023",
                "download_pdfs": False,
                "excerpt_keywords": [
                    "Piano nazionale prevenzione vaccinale",
                    "vaccinale",
                    "immunizzazione",
                ],
            },
        ]
        if "immun" in focus_text.casefold():
            targets.append(
                {
                    "target_type": "local_pdf",
                    "title": "WHO SMART Guidelines Digital Adaptation Kit for Immunization",
                    "publisher": "World Health Organization",
                    "source_type": "WHO SMART / DAK artifact",
                    "path": "shared/assets/who-immunizations-dak.pdf",
                    "date": "Local shared source",
                }
            )
        return targets
    return []


def unresolved_source_gaps(country: str, iso3: str, focus: str | None = None) -> list[dict[str, Any]]:
    """Return a short actionable gap list instead of a broad candidate inventory."""

    focus_text = focus or ""
    if country.casefold() == "italy" or iso3.upper() == "ITA":
        gaps = [
            {
                "source_class": "Current Ministry/ISS immunization coverage dataset",
                "why_needed": "Needed for vaccine, dose, cohort, year, and regional coverage beyond GHO national estimates.",
                "suggested_action": "Resolve current Ministry of Health or ISS coverage tables if the comparison question needs uptake or equity detail.",
                "status": "Needs retrieval",
            },
            {
                "source_class": "Regional implementation or registry specifications",
                "why_needed": "Italy's SSN is regionally implemented, and SMART localization may depend on regional workflows and data flows.",
                "suggested_action": "Retrieve only after the downstream immunization comparison scope identifies priority regions or data elements.",
                "status": "Needs retrieval",
            },
            {
                "source_class": "AIFA pharmacovigilance or vaccine safety source",
                "why_needed": "Relevant if the downstream comparison includes safety monitoring, adverse event reporting, or product governance.",
                "suggested_action": "Retrieve AIFA material only for safety-focused comparison scope.",
                "status": "Conditional retrieval",
            },
        ]
        if "immun" not in focus_text.casefold():
            return gaps[:2]
        return gaps

    gaps = [
        {
            "source_class": "National Ministry of Health source",
            "why_needed": "Needed for national health-system ownership, strategies, policy source classes, and implementation context.",
            "suggested_action": "Use the controlled web-assisted retrieval protocol to resolve the official ministry page or document.",
            "status": "Needs retrieval",
        },
        {
            "source_class": "National public health institute or equivalent",
            "why_needed": "Needed for surveillance, programme monitoring, and health-system implementation context.",
            "suggested_action": "Resolve only official or institutional sources; mark absent or inaccessible sources as gaps.",
            "status": "Needs retrieval",
        },
        {
            "source_class": "National statistics or country health-system profile",
            "why_needed": "Needed to supplement World Bank and WHO GHO baseline indicators with country-specific context.",
            "suggested_action": "Prefer WHO regional, Observatory, World Bank, or official national statistics sources.",
            "status": "Needs retrieval",
        },
    ]
    return gaps
