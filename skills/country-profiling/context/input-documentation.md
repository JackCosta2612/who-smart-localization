# Input documentation guidance

The skill should work from supplied documents first. Retrieval can support the workflow, but country-specific sources should be treated as explicit inputs whenever possible.

## Minimum input request

Ask for:

- country name.

Helpful but not required:

- health focus or downstream use;
- region or population group;
- WHO SMART Guidelines or DAK scope, if known;
- any country-specific health documents already available.

When retrieval-assisted mode is useful, these values can be passed into the preparation command:

```bash
python3 skills/country-profiling/scripts/prepare_profile_run.py \
  --country "<country>" \
  --focus "<optional health focus>"
```

If country documents are available, pass each one with `--country-document` in this format:

```text
title|document type|path-or-url|date
```

Domain-specific policy documents are not mandatory for Country Profiling. They become important when the profile is used to prepare the future Policy Comparison skill.

## Recommended source classes by profile section

### General country and health overview

- WHO country profile, country cooperation strategy, regional observatory profile, or equivalent country health overview.
- National health strategy or health sector strategic plan.

### Population health and burden

- Recent burden-of-disease, mortality, surveillance, health statistics, census, DHS/MICS, or household survey source.

### Health system organization

- Health sector plan, health system review, service delivery assessment, emergency preparedness review, or ministry of health annual report.

### Access and coverage

- UHC monitoring source, insurance or entitlement documentation, benefit package summary, service availability assessment, or access/quality survey.

### Financing

- Health financing, UHC, insurance, expenditure, or financial protection source.

### Workforce and infrastructure

- Health workforce and facility-capacity source.

### WASH and environmental health

- WASH, sanitary conditions, environmental health, pollution, climate, or vector-risk source.

### Digital health and health information systems

- Digital health strategy, health information system strategy, CRVS source, surveillance-system source, or data-quality report.

### Equity and vulnerable groups

- Equity analysis, poverty or social determinants source, migrant/refugee source, disability source, subnational health source, or humanitarian assessment.

### Current risks

- Recent outbreak reports, emergency updates, climate risk assessments, medicine shortage notices, workforce-strain reports, or financing-risk reports.

### Policy-comparison source classes

Collect these only if the profile is preparing a later comparison:

- national health strategy;
- domain-specific national guideline;
- service delivery model or operational manual;
- financing, eligibility, or coverage rules;
- reporting forms, registers, indicators, or data dictionaries;
- terminology, coding, formulary, schedule, or product-list source;
- implementation guidance or programme monitoring document.

## Input quality checklist

Before profiling, record:

- whether each source is official, draft, archived, secondary, modelled, or survey-based;
- publication year;
- retrieval date;
- language;
- country ministry, agency, or organization responsible;
- whether the source covers the country nationally or only a region/population group;
- whether the source covers the optional health focus directly;
- whether a newer version may exist.

## Handling missing inputs

If a country source is missing:

- mark it as `Needs retrieval`;
- do not infer national health conditions from global guidance alone;
- propose likely source owners, such as ministry of health, national statistics office, public health institute, WHO country office, UNICEF, World Bank, regional observatory, or relevant programme authority;
- flag the gap for human follow-up.

The optional preparation script writes `input-documentation-inventory.md` with supplied documents and missing source classes. The profile should reflect missing source classes as evidence gaps whether they are identified by the script or manually from the supplied material.
