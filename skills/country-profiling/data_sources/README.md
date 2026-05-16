# Country Profiling deterministic data sources

This directory contains a small deterministic retrieval layer for the Country
Profiling skill. Retrieval is used to collect selected baseline indicators and
source metadata. It is not a complete country evidence base, a full data
platform, or proof that a country profile is complete.

The preferred minimal-input path is:

1. target country;
2. optional ISO3 code;
3. optional downstream focus;
4. deterministic retrieval of configured baseline indicators and institutional
   source leads;
5. profile drafting with explicit evidence gaps and human review.

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
| WHO GHO / Athena | Conservative placeholder | Returns configured candidate metadata only. Do not fabricate GHO values. |
| OECD / EU / European Observatory | Source-lead registry | OECD SDMX retrieval is not implemented in this pass. Use source leads and reviewed documents. |

Deterministic retrieval should be small and controlled. Add indicators only when
their public codes and interpretation are stable enough for repeated use.
