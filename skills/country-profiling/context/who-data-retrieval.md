# WHO documentation and data retrieval guidance

This note records source classes that can support healthcare country profiling.
Retrieval is optional assistance for source discovery and evidence collection;
it is not a substitute for source review.

For minimal-input profiling, prefer
`scripts/retrieve_country_profile_data.py` when Python scripts are available.
That script retrieves selected World Bank baseline indicators and institutional
source leads with provenance. The older WHO retrieval helper remains useful for
WHO source discovery, but generic WHO pages must not be treated as
country-specific evidence unless a country-specific document or country-filtered
dataset is actually retrieved and reviewed.

Country profiling comes first. Later policy comparison may use the profile to decide which national policies, guidelines, reporting artifacts, or terminology sources to retrieve next.

## Recommended WHO source classes

### WHO country and regional sources

Use WHO country pages, country cooperation strategies, regional observatory profiles, and country health overviews to identify national priorities, broad health system context, and WHO-country collaboration priorities.

### WHO Global Health Observatory OData API

The Global Health Observatory exposes WHO health data through an OData API. Useful endpoints include:

```text
https://ghoapi.azureedge.net/api/Dimension
https://ghoapi.azureedge.net/api/DIMENSION/COUNTRY/DimensionValues
https://ghoapi.azureedge.net/api/Indicator
https://ghoapi.azureedge.net/api/<INDICATOR_CODE>
```

Use this for structured country indicators related to mortality, morbidity,
service coverage, financing, workforce, WASH, and the optional downstream
health-area focus only when stable indicator codes and country filters are
configured. If indicator codes are uncertain, record GHO as a candidate source
lead rather than inventing values.

### WHO SCORE documents

SCORE country summaries describe health information system strengths and weaknesses. This is useful for profiling data system readiness, CRVS, reporting, surveillance, and data-use risks.

### Global Health Expenditure Database

The Global Health Expenditure Database provides comparable health expenditure data. Use this when the profile needs financing, public spending, out-of-pocket spending, or financial protection context.

### National Health Workforce Accounts

Use National Health Workforce Accounts or related workforce sources when workforce distribution, capacity, or service delivery feasibility matters.

### WHO/UNICEF WASH and environmental health sources

Use WASH, sanitation, drinking water, hygiene, air pollution, climate, and environmental health sources when sanitary conditions or environmental risks are relevant to country health context.

## Optional downstream-focus sources

When the user provides a downstream health-area focus, add topic-specific WHO sources and indicator searches. Examples:

| Focus | Search terms |
|---|---|
| Immunization | immunization, vaccination, vaccine |
| Tuberculosis | tuberculosis, TB |
| HIV | HIV |
| Maternal health | maternal, antenatal, birth |
| Child health | child mortality, neonatal, under-five |
| WASH | water, sanitation, hygiene |
| NCDs | cardiovascular, diabetes, cancer, noncommunicable |

## Suggested retrieval workflow

When deterministic baseline retrieval is useful, run:

```bash
python3 skills/country-profiling/scripts/retrieve_country_profile_data.py \
  --country "<country>" \
  --iso3 "<ISO3>" \
  --focus "<optional downstream health-area focus>"
```

When WHO-specific source discovery is useful, run:

```bash
python3 skills/country-profiling/scripts/retrieve_who_sources.py \
  --country "<country>" \
  --focus "<optional downstream health-area focus>"
```

The retrieval runner should:

1. Resolve country metadata where possible.
2. Build a WHO source inventory with country, GHO, SCORE, expenditure, workforce, WASH, and optional downstream-focus source classes.
3. Fetch WHO HTML source pages and save extracted text snapshots under `content/`.
4. Save discovered page links as JSON link inventories.
5. Download supported linked documents when file sizes are within the configured limit.
6. Search WHO GHO indicators using general health terms plus optional downstream-focus terms.
7. Retrieve country-filtered GHO data samples for selected indicators when possible.
8. Write a markdown retrieval report and a machine-readable JSON bundle.
9. Record every failed or skipped retrieval as an explicit evidence gap.

The runner retrieves available page text and structured data. For PDFs and spreadsheets, it retrieves files for later parsing by a PDF, spreadsheet, or document-processing tool. It does not claim to fully interpret binary document contents by itself.

The runner also does not guarantee country-specific retrieval for every source class or prove evidence completeness. Some WHO sources are represented by generic landing pages. For those sources, reachable content must be treated as source discovery unless a country-specific document or dataset is explicitly resolved.

After the retrieval bundle is generated, the Agent should:

1. Review source titles, dates, URLs, and local content paths.
2. Distinguish country-specific evidence from generic source discovery.
3. Use country-filtered GHO rows only when the country code and indicator are clear.
4. Add non-WHO sources supplied by the user or retrieved through approved tools.
5. Record every retrieval date and distinguish official sources from secondary sources.
6. Carry unresolved source classes into evidence gaps.
7. Avoid using retrieval output to perform policy comparison; use it only to support country profiling and downstream-readiness notes.

## Country-specific documentation note

For final profile use, country-specific documents should be supplied as inputs or retrieved through an explicit retrieval step with source verification. Generic WHO pages are not enough to support claims about country health conditions, sanitary coverage, service availability, or policy readiness.
