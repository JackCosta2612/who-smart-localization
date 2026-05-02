# Input documentation guidance

The skill should work from supplied documents first. Retrieval can support the workflow, but country-specific policy documents should be treated as explicit inputs whenever possible.

## Minimum input request

Ask for:

- country name;
- target health domain;
- DAK or WHO guideline scope;
- any country-specific documents already available.

When retrieval-assisted mode is useful, these values can be passed into the preparation command:

```bash
python3 skills/country-profiling/scripts/prepare_profile_run.py \
  --country "<country>" \
  --domain "<health-domain>" \
  --dak-scope "<DAK or WHO guideline scope>"
```

If country documents are available, pass each one with `--country-document` in this format:

```text
title|document type|path-or-url|date
```

## Recommended WHO or global inputs

- Relevant DAK or SMART Implementation Guide.
- WHO guideline or normative source behind the DAK.
- WHO Global Health Observatory indicators relevant to the domain.
- WHO Country Cooperation Strategy or country brief.
- WHO SCORE country summary, when the task needs health information system context.
- Global Health Expenditure Database outputs, when financing context matters.
- National Health Workforce Accounts or health workforce indicators, when workforce context matters.

## Recommended country-specific inputs

- National health strategy or health sector strategic plan.
- Domain-specific national programme guideline.
- Digital health strategy or health information system strategy.
- National health information system policy.
- National immunization, HIV, TB, maternal health, or other programme plans depending on the target domain.
- National formulary, schedule, registry, reporting form, or data dictionary when relevant to the DAK.

## Input quality checklist

Before profiling, record:

- whether each source is official, draft, archived, or secondary;
- publication year;
- retrieval date;
- language;
- country ministry or agency responsible;
- whether the source covers the target domain directly;
- whether a newer version may exist.

## Handling missing inputs

If a country document is missing:

- mark it as `Needs retrieval`;
- do not infer national policy from global guidance;
- propose likely source owners, such as ministry of health, national public health institute, or WHO country office;
- flag the gap for human follow-up.

The optional preparation script writes `input-documentation-inventory.md` with supplied documents and missing document classes. The profile should reflect missing document classes as evidence gaps whether they are identified by the script or manually from the supplied material.
