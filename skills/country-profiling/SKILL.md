---
name: who-smart-country-profiling
description: Builds a source-backed textual healthcare country profile. Use when asked to understand a country's health context, main health issues, health system, coverage, sanitary conditions, access constraints, health data environment, or readiness for later policy comparison and localization work.
license: MIT
compatibility: Model-neutral Agent Skill. Uses supplied documents by default. Optional WHO/open data retrieval may be used when available.
metadata:
  project: "USI NLP WHO SMART Guidelines project"
  team: "Giacomo Costantino, Leonardo Gravellone"
  version: "0.2"
---

# WHO SMART Country Profiling Skill

## Purpose

Create a concise, source-backed textual profile of a country from a healthcare perspective.

The profile should explain the country's health context before any detailed policy comparison is attempted. It should cover the main health issues, health system organization, access and coverage, sanitary and environmental health conditions, financing and affordability, workforce and infrastructure, digital health and data systems, equity concerns, and current risks or uncertainties.

Policy-specific analysis is conditional on this profile. Do not compare policies, assess alignment with WHO guidance, or draft localization recommendations unless the user explicitly asks for that as a later step and the country profile identifies adequate sources for doing it.

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

- optional health focus, region, population group, or use case;
- source documents pasted into the prompt, attached as files, or already present in the conversation;
- national health strategies, country health profiles, programme reports, census or survey outputs, health financing reports, health workforce documents, WASH or environmental health sources, digital health strategies, and health information system documents;
- WHO, World Bank, UNICEF, UNAIDS, GBD, OECD, regional observatory, or other reputable public-health sources;
- source URLs, local file paths, publication dates, retrieval dates, and language notes when available.

Inputs may be unstructured. Normalize the prompt, attached files, conversation context, and optional retrieval outputs into a source inventory before writing the profile.

## Execution modes

Use document-only mode by default when the user provides enough source material directly.

Use retrieval-assisted mode only when scripts or tools are available and the user asks for, allows, or clearly needs retrieval support. Retrieval and preflight scripts can prepare a run, create an inventory, retrieve candidate WHO sources, or check environment readiness. They are optional support, not mandatory blockers.

If scripts fail, continue in document-only mode when enough user-provided source material is available. If scripts fail and source material is insufficient, ask for sources or produce only a limited skeleton/gap-analysis profile with explicit evidence gaps.

See `context/execution-modes.md` for the decision rules.

## Workflow

1. Identify the target country and any optional health focus, region, or intended downstream use.
2. Build a source inventory from user-provided material and any optional retrieved material.
3. Decide whether the available sources are sufficient for a preliminary healthcare country profile.
4. Draft the textual profile using `context/profile-schema.md`.
5. Mark missing information as evidence gaps.
6. Separate facts, uncertainties, assumptions, and expert-review needs.
7. Include a policy-analysis readiness section that says what policy comparison can or cannot safely follow from the profile.
8. Do not fabricate missing country context.

## Output requirements

Always follow `context/profile-schema.md`.

The output is primarily narrative. Tables are used only for source inventory, evidence gaps, and review needs.

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
  --focus "<optional health focus>"

python3 skills/country-profiling/scripts/validate_profile.py <profile.md>
```

The WHO retrieval helper can also be run directly when retrieval assistance is useful:

```bash
python3 skills/country-profiling/scripts/retrieve_who_sources.py \
  --country "<country>" \
  --focus "<optional health focus>"
```

Script outputs are support artifacts. A failed retrieval or preflight run does not automatically prevent profile drafting if supplied sources are adequate. A successful retrieval does not prove that all country-specific evidence exists; generic WHO source discovery must not be treated as country evidence.

## Safety and uncertainty

- Preserve traceability from claims to sources.
- Use explicit source references wherever possible.
- Label missing, stale, conflicting, or uncertain content.
- Keep global or regional evidence separate from country-specific evidence.
- Do not infer national policy, service availability, sanitary conditions, or coverage from missing documents.
- Recommend human expert review where evidence is incomplete, ambiguous, conflicting, stale, locally sensitive, or likely to affect later policy comparison.
