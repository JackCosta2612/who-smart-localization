# Country Profiling Skill

The Country Profiling skill creates a source-backed healthcare overview for a target country. It summarizes the health situation, health system structure, implementation environment, data and digital health context, equity issues, risks, and readiness for later policy comparison or SMART Guidelines localization.

## Why this comes first

Policy comparison depends on context. A national policy excerpt is hard to interpret without knowing the country's service delivery model, coverage rules, financing constraints, workforce and infrastructure limits, WASH conditions, data systems, and regional inequalities. This skill makes that context explicit before the future Policy Comparison skill compares WHO/SMART content with national policy material.

## Output

The skill produces a narrative markdown profile using `context/profile-schema.md`. It includes:

- healthcare country context and major health issues;
- health system organization, access, coverage, financing, workforce, infrastructure, and supplies;
- sanitary and environmental health context;
- digital health and health information system context;
- equity, vulnerable groups, regional variation, current risks, and watchpoints;
- policy-analysis readiness and optional policy-comparison handoff notes;
- source inventory, evidence gaps, expert-review needs, and sources.

## Sources

Minimum input is a country name. Better profiles use country-specific sources such as country health profiles, national health strategies, health sector plans, financing or UHC reports, workforce and infrastructure sources, WASH/environmental health sources, digital health or HIS documents, surveillance outputs, and survey or burden-of-disease sources.

Domain-specific policy documents are useful only when the next step is policy comparison. They are not required to create the country profile.

## Execution modes

### Document-only mode

Use this by default when the user provides enough source material in the prompt, attached files, local files, or conversation context. Draft only from supplied material and turn missing source classes into explicit evidence gaps.

### Retrieval-assisted mode

Use this only when scripts or tools are available and retrieval support is useful. The scripts can check the environment, prepare a run folder, retrieve candidate WHO sources, and write an input documentation inventory. These artifacts support source discovery; they are not mandatory and do not replace reading the actual sources.

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

Run WHO retrieval directly when useful:

```bash
python3 skills/country-profiling/scripts/retrieve_who_sources.py \
  --country "<country>" \
  --focus "<optional health focus>"
```

## Validation

Validate a completed profile:

```bash
python3 skills/country-profiling/scripts/validate_profile.py <profile.md>
```

The validator checks headings, table headers, optional handoff structure, and controlled source-status values. It does not validate factual correctness, epidemiology, policy interpretation, clinical correctness, source interpretation, WASH interpretation, or WHO interpretation.

## What this skill does not do

- It does not make clinical decisions or provide patient advice.
- It does not draft final national policy.
- It does not compare WHO guidance with national policy.
- It does not produce final DAK localization decisions.
- It does not invent missing country facts.
- It does not replace WHO, national, legal, clinical, policy, WASH, epidemiological, environmental health, or country expert review.

## Policy Comparison handoff

The profile should identify which health areas matter for later comparison, which national policy source classes are needed, which systems affect policy interpretation, what gaps block safe comparison, and what expert inputs are required. If the evidence base is too thin, the profile should state `Not ready for policy comparison`.

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
│   ├── README.md
│   ├── example-format.md
│   ├── italy-reference-draft-1/
│   ├── italy-reference-draft-2/
│   └── italy-reference-draft-3/
├── scripts/
│   ├── check_environment.py
│   ├── prepare_profile_run.py
│   ├── retrieve_who_sources.py
│   ├── validate_profile.py
│   └── who_gho_client.py
└── tests/
```

## Current status

Ready for manual review of draft Italy reference examples.

## Reference examples

The `examples/italy-reference-draft-*` folders contain behavior-shaping
reference examples, not benchmarks or tests. They show alternative ways to
normalize inputs, draft source-backed profiles, represent uncertainty, and
prepare downstream Policy Comparison without performing it.
