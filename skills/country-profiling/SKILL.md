---
name: who-smart-country-profiling
description: Build a source-backed healthcare country profile for a target country and optional downstream health-area focus, including health situation, health system context, implementation environment, evidence gaps, and readiness for later WHO SMART Guidelines localization or policy comparison.
license: MIT
compatibility: Model-neutral Agent Skill. Uses supplied documents by default. Optional WHO/open data retrieval may be used when available.
metadata:
  project: "USI NLP WHO SMART Guidelines project"
  team: "Giacomo Costantino, Leonardo Gravellone"
  version: "0.3"
---

# WHO SMART Country Profiling Skill

## Purpose

Create a concise, source-backed healthcare country profile for a target country.

The profile explains the country's health situation and health system context before detailed policy comparison, DAK localization, or SMART Guidelines adaptation. It should cover the main health issues, health system organization, implementation environment, access and coverage, sanitary and environmental health conditions, financing and affordability, workforce and infrastructure, digital health and data systems, equity concerns, and current risks or uncertainties.

The output is designed as an input to the future Policy Comparison skill. It should identify which downstream health areas may need later comparison, which national policy source classes are still needed, and what country context constrains interpretation of national policy. It should not compare policies, assess alignment with WHO guidance, or draft localization recommendations.

## When to use

Use this skill for:

- healthcare country overviews;
- regional or national health context summaries;
- identifying main health issues, health system constraints, coverage gaps, or sanitary conditions;
- preparing background context before policy comparison, DAK localization, or SMART Guidelines adaptation;
- determining what documents or expert input are needed before policy-specific analysis.

## When not to use

Do not use this skill for:

- clinical decision-making or patient advice;
- final national policy drafting;
- direct WHO-versus-country policy comparison;
- unsourced country, health system, sanitary, policy, clinical, or WHO claims;
- replacing WHO, national, legal, policy, clinical, epidemiological, WASH, environmental health, or country expert review.

## Expected inputs

Minimum expected input:

1. Target country.

Helpful inputs:

- optional downstream health-area focus, region, population group, or use case;
- source documents pasted into the prompt, attached as files, or already present in the conversation;
- national health strategies, country health profiles, programme reports, census or survey outputs, health financing reports, health workforce documents, WASH or environmental health sources, digital health strategies, and health information system documents;
- WHO SMART Guidelines or DAK scope if known, as downstream context rather than a required profiling input;
- WHO, World Bank, UNICEF, UNAIDS, GBD, OECD, regional observatory, or other reputable public-health sources;
- source URLs, local file paths, publication dates, retrieval dates, and language notes when available.

Inputs may be unstructured. Normalize the prompt, attached files, conversation context, and optional retrieval outputs into a source inventory before writing the profile.

The optional downstream health-area focus can name an area such as immunization, HIV, tuberculosis, or maternal health when the profile is being prepared for later policy comparison. It should guide source discovery and readiness notes, but the country profile should still describe the country's healthcare system and context overall.

## Execution modes

Use document-only mode by default when the user provides enough source material directly.

Use retrieval-assisted mode only when scripts or tools are available and the user asks for, allows, or clearly needs retrieval support. Retrieval and preflight scripts can prepare a run, create an inventory, retrieve candidate WHO sources, or check environment readiness. They are optional support, not mandatory blockers.

If scripts fail, continue in document-only mode when enough user-provided source material is available. If scripts fail and source material is insufficient, ask for sources or produce only a limited skeleton/gap-analysis profile with explicit evidence gaps.

See `context/execution-modes.md` for the decision rules.

## Workflow

1. Identify the target country and any optional downstream health-area focus, region, population group, or intended downstream use.
2. Build a source inventory from user-provided material and any optional retrieved material.
3. Classify source types as country-specific, regional, global, candidate, or missing.
4. Decide whether a full profile, limited profile, or skeleton/gap-analysis profile is appropriate.
5. Draft the textual profile using `context/profile-schema.md`.
6. Keep the profile narrative and readable.
7. Mark missing information as evidence gaps.
8. Separate facts, uncertainties, assumptions, and expert-review needs.
9. Include a `Policy-analysis readiness` section and, when useful, a `Policy-comparison handoff` table.
10. State how the output can feed the future Policy Comparison skill.
11. Do not fabricate missing country context.

## Output requirements

Always follow `context/profile-schema.md`.

The output is primarily narrative. Tables are used for source inventory, evidence gaps, and policy-comparison handoff when appropriate.

Every substantive country, health system, health burden, coverage, sanitary condition, access, financing, workforce, infrastructure, digital health, or data claim should include:

- source name;
- source type;
- source URL, local file path, or dataset identifier;
- publication or retrieval date when available;
- confidence level or uncertainty note;
- review need when the claim affects later policy analysis.

## Optional script usage

Scripts in `scripts/` may be used to prepare or validate work:

```bash
python3 skills/country-profiling/scripts/check_environment.py

python3 skills/country-profiling/scripts/prepare_profile_run.py \
  --country "<country>" \
  --focus "<optional downstream health-area focus>"

python3 skills/country-profiling/scripts/validate_profile.py <profile.md>
```

The WHO retrieval helper can also be run directly when retrieval assistance is useful:

```bash
python3 skills/country-profiling/scripts/retrieve_who_sources.py \
  --country "<country>" \
  --focus "<optional downstream health-area focus>"
```

Script outputs are support artifacts. A failed retrieval or preflight run does not automatically prevent profile drafting if supplied sources are adequate. A successful retrieval does not prove that all country-specific evidence exists; generic WHO source discovery must not be treated as country evidence.

## Safety and uncertainty

- Preserve traceability from claims to sources.
- Use explicit source references wherever possible.
- Label missing, stale, conflicting, or uncertain content.
- Keep global or regional evidence separate from country-specific evidence.
- Do not infer national policy, service availability, sanitary conditions, or coverage from missing documents.
- Recommend human expert review where evidence is incomplete, ambiguous, conflicting, stale, locally sensitive, or likely to affect later policy comparison.
