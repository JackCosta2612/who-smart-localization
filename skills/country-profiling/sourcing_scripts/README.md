# Country Profiling sourcing scripts

This directory contains the maintained sourcing and validation tooling for the
Country Profiling skill. Retrieval is used to collect selected baseline
indicators and source metadata. It is not a complete country evidence base, a
full data platform, or proof that a country profile is complete.

The preferred minimal-input path is:

1. target country;
2. optional ISO3 code;
3. optional downstream focus;
4. deterministic retrieval of configured baseline indicators and stable WHO
   artifacts;
5. optional source-manifest resolution for Agent-discovered country-specific
   official URLs or local files;
6. profile drafting with explicit evidence gaps and human review.

If Python scripts are unavailable, the skill may fall back to
semi-deterministic web-assisted retrieval using the protocol in
`../context/web-assisted-retrieval.md`.

All retrieved or reviewed values must preserve:

- source;
- indicator code where applicable;
- label;
- value;
- unit when available;
- year;
- retrieval date;
- URL;
- status.

## Implemented and optional sources

| Source | Current support | Notes |
|---|---|---|
| World Bank Data API | Implemented | Fetches the latest available non-empty value for configured baseline indicators. |
| WHO GHO OData API | Implemented for configured immunization indicators | Retrieves DTP3, MCV1, MCV2, and PCV3 when the focus is immunization. |
| Manifest-supplied institutional web/PDF sources | Implemented | Resolves Agent- or user-supplied country-specific URLs/local files, downloads PDFs, parses text when `pypdf` is available, and records checksums and statuses. |
| OECD SDMX | Not active | Re-evaluate only if a narrow dataset-specific need is proven; OECD/EU context may enter through reviewed institutional profiles. |

Deterministic retrieval should be small and controlled. Add indicators only when
their public codes and interpretation are stable enough for repeated use.
Do not add national ministry, institute, policy, or programme URLs as
country-specific code branches; discover them per run and pass them through a
source manifest.

## Maintained files

| File | Purpose |
|---|---|
| `retrieve_country_profile_data.py` | Orchestrates World Bank, WHO GHO, reviewed web/PDF artifacts, and short source-gap creation. |
| `indicator_registry.json` | Small controlled indicator list. |
| `world_bank.py` | World Bank API helper. |
| `who_gho.py` | Configured WHO GHO OData helper. |
| `web_sources.py` | Institutional HTML/PDF resolver and PDF parser wrapper. |
| `source_registry.py` | Country-agnostic source classes, stable WHO artifacts, source manifest loading, and short unresolved source gaps. |
| `validate_profile.py` | Structural validator for Country Profiling outputs. |
| `requirements.txt` | Optional runtime dependency list for PDF parsing. |
