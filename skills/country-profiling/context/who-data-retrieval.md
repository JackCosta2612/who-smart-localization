# WHO documentation and data retrieval guidance

This note records initial web lookup findings for sources that can support Country Profiling. Accessed on 2026-04-28.

## Recommended WHO sources

### WHO Digital Adaptation Kits

WHO describes DAKs as software-neutral, operational, structured documentation based on WHO clinical, health system, and data-use recommendations. DAKs include workflow processes, core data needs, decision support, indicators, and functional requirements for a health domain.

Use DAKs as the main WHO input for domain-specific implementation context.

Source: https://www.who.int/publications/m/item/who-digital-accelerator-kits

### SMART Implementation Guides

SMART DAK Implementation Guides state that DAK content is generic and software-neutral, and must be adapted to local needs before it informs local digital system design.

Use these pages to identify DAK components such as concepts, personas, user scenarios, business processes, data dictionary, decision support, indicators, system requirements, transactions, testing, and downloads.

Example source: https://smart.who.int/dak-bds/adapting.html

### WHO Global Health Observatory OData API

The Global Health Observatory exposes WHO health data through an OData API. Useful endpoints include:

```text
https://ghoapi.azureedge.net/api/Dimension
https://ghoapi.azureedge.net/api/DIMENSION/COUNTRY/DimensionValues
https://ghoapi.azureedge.net/api/Indicator
https://ghoapi.azureedge.net/api/<INDICATOR_CODE>
```

Use this for structured country indicators that may contextualize DAK implementation.

Source: https://www.who.int/data/gho/info/gho-odata-api

### WHO Country Cooperation Strategies

WHO Country Cooperation Strategies are medium-term strategic frameworks for WHO work in and with a country. They identify priorities aligned with national and global health goals.

Use this source class to understand national health priorities, WHO country collaboration priorities, and broad health system context.

Source: https://www.who.int/countries/country-cooperation-strategies

### WHO SCORE documents

SCORE country summaries describe health information system strengths and weaknesses. This is useful for profiling data system readiness and implementation risks.

Source: https://www.who.int/data/data-collection-tools/score/documents

### Global Health Expenditure Database

The Global Health Expenditure Database provides comparable health expenditure data for 195 countries and territories since 2000. WHO notes that the database is updated annually and includes spending indicators relevant to health financing context.

Use this when DAK implementation depends on financing, public spending, out-of-pocket spending, or primary health care expenditure context.

Source: https://apps.who.int/nha/database/en

### National Health Workforce Accounts

WHO describes the National Health Workforce Accounts as a standardized system for improving availability, quality, and use of health workforce data.

Use this when workforce roles, facility staffing, or service delivery capacity matters for DAK implementation.

Source: https://www.who.int/publications-detail-redirect/national-health-workforce-accounts

## Sample DAK sources discovered

| Health domain | Source |
|---|---|
| Immunization | https://www.who.int/publications/i/item/9789240099456 |
| Tuberculosis | https://www.who.int/publications/i/item/9789240086616 |
| Family planning | https://www.who.int/publications/who-guidelines/9789240029743 |
| Antenatal care | https://www.who.int/publications/i/item/9789240020306 |
| HIV | https://www.who.int/publications/i/item/9789240054424 |

## Suggested retrieval workflow

1. Identify the target DAK or SMART Implementation Guide.
2. Record DAK title, version, publication date, URL, and downloadable annexes.
3. Search WHO country pages and WHO IRIS for the country's Country Cooperation Strategy.
4. Query GHO for basic country indicators relevant to the domain.
5. Add SCORE, GHED, and health workforce sources only when they are relevant to the implementation question.
6. Add country-specific documents as supplied inputs or as clearly marked candidate sources.
7. Record every retrieval date and distinguish official sources from secondary sources.

## Country-specific documentation note

For now, country-specific documentation is needed only for examples and testing. In final skill use, country-specific documents should be supplied as inputs or retrieved through an explicit retrieval step with source verification.
