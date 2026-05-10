# Input documentation guidance

The skill should work from supplied documents first. Retrieval can support the workflow, but country-specific sources should be treated as explicit inputs whenever possible.

## Minimum input request

Ask for:

- country name;
- optional health focus, region, population group, or intended downstream use;
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

## Recommended source classes

- WHO country profile, country cooperation strategy, regional observatory profile, or equivalent country health overview.
- National health strategy or health sector strategic plan.
- Recent burden-of-disease, mortality, surveillance, health statistics, census, DHS/MICS, or household survey source.
- Health financing, UHC, insurance, expenditure, or financial protection source.
- Health workforce and facility-capacity source.
- WASH, sanitary conditions, environmental health, pollution, climate, or vector-risk source.
- Digital health strategy, health information system strategy, CRVS source, surveillance-system source, or data-quality report.
- Domain-specific national programme documents only when a focus area is requested.
- Downstream policy documents only when the profile is being used to prepare later policy comparison.

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
