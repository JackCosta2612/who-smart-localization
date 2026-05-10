# Country Profiling Skill

The Country Profiling skill creates a source-backed textual healthcare overview for a target country.

It helps the team understand the country's population health context, main health concerns, health system organization, access and coverage, sanitary and environmental health conditions, financing, workforce, infrastructure, digital health environment, equity issues, and evidence gaps before moving into policy-specific comparison.

## Why this matters

Policy comparison and localization depend on country context. A policy excerpt can look aligned or divergent for reasons that are invisible without knowing the health system, coverage model, service delivery constraints, disease burden, WASH conditions, data systems, and regional inequalities. The country profile makes that context explicit first.

## Execution modes

### Document-only mode

Use this by default when the user provides enough source material in the prompt, attached files, local files, or conversation context.

The Agent should:

- identify the target country and optional health focus;
- build a source inventory from supplied material;
- draft the profile using only the supplied sources;
- mark missing information as evidence gaps.

### Retrieval-assisted mode

Use this when scripts or tools are available and the user asks for or allows retrieval help.

The scripts can check the environment, prepare a run folder, retrieve candidate WHO sources, and write an input documentation inventory. They are optional support artifacts. They are not mandatory for every use of the skill.

## Optional scripts

Check the local environment:

```bash
python3 skills/country-profiling/scripts/check_environment.py
```

Prepare a retrieval-assisted run:

```bash
python3 skills/country-profiling/scripts/prepare_profile_run.py \
  --country "<country>" \
  --focus "<optional health focus>"
```

Add known country documents when available:

```bash
python3 skills/country-profiling/scripts/prepare_profile_run.py \
  --country "Romania" \
  --focus "general healthcare overview" \
  --country-document "Document title|Document type|/path/or/url|2024"
```

Run WHO retrieval directly when useful:

```bash
python3 skills/country-profiling/scripts/retrieve_who_sources.py \
  --country "<country>" \
  --focus "<optional health focus>"
```

If scripts fail but the user has supplied enough sources, the Agent can still draft in document-only mode. If sources are insufficient, the Agent should ask for more sources or produce only a skeleton/gap-analysis profile when requested.

## Validate a profile

```bash
python3 skills/country-profiling/scripts/validate_profile.py <profile.md>
```

The validator checks structure, required sections, table headers, and controlled values. It does not validate epidemiological correctness, national policy correctness, country facts, WHO interpretation, WASH interpretation, or legal suitability.

## What this skill does not do

- It does not make clinical decisions.
- It does not provide patient advice.
- It does not draft final national policy.
- It does not compare WHO policy with country policy.
- It does not invent missing country context.
- It does not replace WHO, national, clinical, legal, policy, epidemiological, WASH, environmental health, or country expert review.

## Folder structure

```text
country-profiling/
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
│   └── example-format.md
├── scripts/
│   ├── check_environment.py
│   ├── prepare_profile_run.py
│   ├── retrieve_who_sources.py
│   ├── validate_profile.py
│   └── who_gho_client.py
└── tests/
```

## Current status

Pivoted documentation draft. The skill contract, schema, optional retrieval helpers, and structural validator are aligned to healthcare country profiling. Real examples are intentionally not included yet.
