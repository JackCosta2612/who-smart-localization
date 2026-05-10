---
name: who-smart-policy-comparison
description: Transitional starting point for a future WHO SMART policy-comparison skill, migrated from the previous policy-oriented country-profiling package. Use later when developing comparison of WHO guidance, DAK context, and country-specific policy material.
license: MIT
compatibility: Model-neutral Agent Skill. Uses supplied documents by default. Optional WHO/open data retrieval and MCP/FHIR tooling may be used when available.
metadata:
  project: "USI NLP WHO SMART Guidelines project"
  team: "Giacomo Costantino, Leonardo Gravellone"
  version: "0.1"
---

# WHO SMART Policy Comparison Skill

This package is a migrated starting point from the previous policy-oriented country-profiling skill. It has not yet been redesigned as the final policy-comparison skill.

## Purpose

Create a structured, source-backed country profile to support WHO SMART Guidelines localization and DAK adaptation preparation.

The profile should identify what is known, what is missing, what is uncertain, what may matter for localization, and where human expert review is needed.

## When to use

Use this skill for:

- country profiling before DAK localization;
- DAK localization preparation;
- national policy, health system, or implementation context extraction;
- implementation context review for a target health domain;
- reusable inputs for later policy comparison or adaptation work.

## When not to use

Do not use this skill for:

- clinical decision-making or patient advice;
- final national policy drafting;
- unsourced country, policy, clinical, or WHO claims;
- replacing WHO, national, legal, policy, clinical, or country expert review.

## Expected inputs

Minimum expected inputs:

1. Target country.
2. Health domain.
3. DAK scope, SMART Guidelines area, WHO guideline, or implementation topic.

Helpful inputs:

- source documents pasted into the prompt, attached as files, or already present in the conversation;
- national health strategies, programme guidance, digital health documents, schedules, forms, registries, data dictionaries, or datasets;
- WHO or global sources relevant to the DAK or health domain;
- source URLs, local file paths, publication dates, retrieval dates, and language notes when available.

Inputs may be unstructured. Normalize the prompt, attached files, conversation context, and optional retrieval outputs into a source inventory before writing the profile.

## Execution modes

Use document-only mode by default when the user provides enough source material directly.

Use retrieval-assisted mode only when scripts or tools are available and the user asks for, allows, or clearly needs retrieval support. Retrieval and preflight scripts can prepare a run, create an inventory, retrieve candidate WHO sources, or check environment readiness. They are optional support, not mandatory blockers.

If scripts fail, continue in document-only mode when enough user-provided source material is available. If scripts fail and source material is insufficient, ask for sources or produce only a limited skeleton/gap-analysis profile with explicit evidence gaps.

See `context/execution-modes.md` for the decision rules.

## Workflow

1. Identify the target country, health domain, and DAK or SMART Guidelines scope.
2. Build a source inventory from user-provided material and any optional retrieved material.
3. Decide whether the available sources are sufficient for a preliminary profile.
4. Draft the profile using `context/profile-schema.md`.
5. Mark missing information as evidence gaps.
6. Separate facts, uncertainties, assumptions, and expert-review needs.
7. Do not fabricate missing country context.

## Output requirements

Always follow `context/profile-schema.md`.

Every substantive country, policy, implementation, or data claim should include:

- source name;
- source type;
- source URL, local file path, or dataset identifier;
- publication or retrieval date when available;
- confidence level;
- review need.

## Optional script usage

Scripts in `scripts/` may be used to prepare or validate work:

```bash
python3 skills/policy-comparison/scripts/check_environment.py

python3 skills/policy-comparison/scripts/prepare_profile_run.py \
  --country "<country>" \
  --domain "<health-domain>" \
  --dak-scope "<DAK or WHO artifact scope>"

python3 skills/policy-comparison/scripts/validate_profile.py <profile.md>
```

The WHO retrieval helper can also be run directly when retrieval assistance is useful:

```bash
python3 skills/policy-comparison/scripts/retrieve_who_sources.py \
  --country "<country>" \
  --domain "<health-domain>"
```

Script outputs are support artifacts. A failed retrieval or preflight run does not automatically prevent profile drafting if supplied sources are adequate. A successful retrieval does not prove that country-specific evidence exists; generic WHO source discovery must not be treated as country evidence.

## Safety and uncertainty

- Preserve traceability from claims to sources.
- Use explicit source references wherever possible.
- Label missing, stale, conflicting, or uncertain content.
- Keep WHO/global guidance separate from country-specific evidence.
- Do not infer national policy from missing country documents.
- Recommend human expert review where evidence is incomplete, ambiguous, conflicting, or locally sensitive.
