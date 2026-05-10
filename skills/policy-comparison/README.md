# Policy Comparison Skill

This package is a migrated starting point from the previous policy-oriented country-profiling skill. It has not yet been redesigned as the final policy-comparison skill.

The current contents create a structured, source-backed country profile for WHO SMART Guidelines localization and DAK adaptation preparation.

It helps the team understand what is already known about a country and health domain, what is missing, what may affect localization, and what needs human expert review before detailed policy comparison or adaptation work.

## Why this matters

WHO SMART Guidelines and Digital Adaptation Kits are global starting points. Local use depends on country context: policy, service delivery, reporting systems, terminology, digital health infrastructure, and available data. A country profile makes that context visible before the team starts adapting content.

## Execution modes

### Document-only mode

Use this by default when the user provides enough source material in the prompt, attached files, local files, or conversation context.

The Agent should:

- identify the target country, health domain, and DAK or SMART Guidelines scope;
- build a source inventory from supplied material;
- draft the profile using only the supplied sources;
- mark missing information as evidence gaps.

### Retrieval-assisted mode

Use this when scripts or tools are available and the user asks for or allows retrieval help.

The scripts can check the environment, prepare a run folder, retrieve candidate WHO sources, and write an input documentation inventory. They are optional support artifacts. They are not mandatory for every use of the skill.

## Optional scripts

Check the local environment:

```bash
python3 skills/policy-comparison/scripts/check_environment.py
```

Prepare a retrieval-assisted run:

```bash
python3 skills/policy-comparison/scripts/prepare_profile_run.py \
  --country "<country>" \
  --domain "<health-domain>" \
  --dak-scope "<DAK or WHO artifact scope>"
```

Add known country documents when available:

```bash
python3 skills/policy-comparison/scripts/prepare_profile_run.py \
  --country "Romania" \
  --domain "immunization" \
  --dak-scope "WHO immunization DAK" \
  --country-document "Document title|Document type|/path/or/url|2024"
```

Run WHO retrieval directly when useful:

```bash
python3 skills/policy-comparison/scripts/retrieve_who_sources.py \
  --country "<country>" \
  --domain "<health-domain>"
```

If scripts fail but the user has supplied enough sources, the Agent can still draft in document-only mode. If sources are insufficient, the Agent should ask for more sources or produce only a skeleton/gap-analysis profile when requested.

## Validate a profile

```bash
python3 skills/policy-comparison/scripts/validate_profile.py <profile.md>
```

The validator checks structure, required sections, table headers, and controlled values. It does not validate clinical correctness, national policy correctness, country facts, WHO interpretation, or legal suitability.

## What this skill does not do

- It does not make clinical decisions.
- It does not provide patient advice.
- It does not draft final national policy.
- It does not invent missing country context.
- It does not replace WHO, national, clinical, legal, policy, or country expert review.

## Folder structure

```text
policy-comparison/
├── SKILL.md
├── README.md
├── context/
│   ├── execution-modes.md
│   ├── input-documentation.md
│   ├── mcp-integration-plan.md
│   ├── profile-schema.md
│   ├── retrieval-limitations.md
│   ├── runtime-requirements.md
│   └── who-data-retrieval.md
├── examples/
│   ├── example-input-1.md
│   └── example-output-1.md
├── scripts/
│   ├── check_environment.py
│   ├── prepare_profile_run.py
│   ├── retrieve_who_sources.py
│   ├── validate_profile.py
│   └── who_gho_client.py
└── tests/
```

## Current status

MVP polish. The skill contract, schema, optional retrieval helpers, and structural validator are in place. Final examples and first evaluation tests are the next phase.
