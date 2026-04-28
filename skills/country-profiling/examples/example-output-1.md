# Country profile: Romania - Immunization

Illustrative example for workflow testing only. Not a validated country profile.

## Profile metadata

- Country: Romania
- Target health domain: Immunization
- DAK or WHO artifact scope: WHO immunization DAK
- Profile date: 2026-04-28
- Profile author or agent: Example scaffold
- Known input limitations: National immunization and digital health documents are listed as candidate sources but were not reviewed in this example.

## Executive summary

This example shows the expected structure of a country profile. It does not make validated findings about Romania. The profile identifies candidate sources that would support later DAK localization and flags missing national documents for retrieval.

## Source inventory

| Source | Source type | Publisher | Date | URL or file path | Relevance | Status |
|---|---|---|---|---|---|---|
| Digital adaptation kit for immunizations | WHO DAK | WHO | 2025 | https://www.who.int/publications/i/item/9789240099456 | Defines generic immunization DAK implementation content. | Candidate source |
| WHO Country Cooperation Strategy, Romania 2024-2030 | WHO country document | WHO Regional Office for Europe | 2024 | https://iris.who.int/handle/10665/376618 | Provides broad country and health system context. | Candidate source |
| Romania National Health Strategy 2023-2030 | National strategy | Romania Ministry of Health | Unknown | To be supplied or retrieved | Needed for national priorities and implementation context. | Needs retrieval |

## Country and health system context

No validated country-level findings are included in this scaffold. The final profile should summarize governance, national health priorities, delivery structure, financing context, and implementation constraints only after reviewing source documents.

## DAK implementation context

The immunization DAK should be reviewed for personas, workflows, data elements, decision support, indicators, and functional requirements. Country-specific adaptation should then identify where national immunization schedules, reporting systems, registries, facility workflows, and terminology differ from the generic DAK.

## Domain-specific considerations

Potential immunization-specific inputs include national immunization schedule, vaccine registry rules, stock reporting procedures, adverse event reporting guidance, service delivery policies, and relevant data dictionaries.

## Data and digital health context

The final profile should assess whether national digital health, health information system, and immunization information system documents are available and current.

## Known facts

| Area | Finding | Evidence | Source | Confidence | Review need |
|---|---|---|---|---|---|
| Source availability | A WHO immunization DAK exists as a candidate global input. | WHO publication page for the immunization DAK. | Digital adaptation kit for immunizations | High | No immediate review |
| Country context | A WHO Country Cooperation Strategy exists as a candidate country context source. | WHO IRIS record for Romania CCS 2024-2030. | WHO Country Cooperation Strategy, Romania 2024-2030 | High | No immediate review |
| National source gap | National immunization and digital health documents still need to be supplied or retrieved. | Not present in the example input. | Example input | Medium | Confirm with country expert |

## Uncertainties and evidence gaps

| Gap or uncertainty | Why it matters for DAK implementation | Suggested next source | Review owner |
|---|---|---|---|
| Current national immunization schedule not reviewed | Schedule differences may affect decision support and workflows. | Official national immunization programme document | Domain expert |
| National immunization registry context not reviewed | Registry availability affects data elements, reporting, and workflow design. | National digital health or immunization information system documentation | Digital health expert |
| Local terminology and coding systems not reviewed | Terminology gaps can create mapping errors during localization. | National data dictionary or reporting forms | Terminology reviewer |

## Human expert input needed

- Confirm the current official national immunization schedule.
- Identify official national immunization information system documentation.
- Validate whether WHO DAK workflow assumptions fit Romanian service delivery.

## Reuse opportunities for regional adaptation

Potential reuse should be assessed only after validated profiles exist for multiple countries in the same region. Candidate reusable elements may include regional reporting standards, shared WHO regional priorities, or similar digital health constraints.

## Sources

- Digital adaptation kit for immunizations: https://www.who.int/publications/i/item/9789240099456
- WHO Country Cooperation Strategy, Romania 2024-2030: https://iris.who.int/handle/10665/376618
- WHO Global Health Observatory OData API: https://www.who.int/data/gho/info/gho-odata-api
