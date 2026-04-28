---
name: who-smart-country-profiling
description: Builds a structured, verifiable country profile for WHO SMART Guidelines and DAK localization. Use when asked to contextualize a country for DAK implementation, gather health system context, identify country-specific documentation needs, or prepare inputs for later localization comparison work.
license: MIT
compatibility: Model-neutral Agent Skill. Uses plain documents by default. WHO/open data retrieval and MCP/FHIR tooling may be used when available.
metadata:
  project: "USI NLP WHO SMART Guidelines project"
  team: "Giacomo Costantino, Leonardo Gravellone, Marionne Blanco Herrera"
  version: "0.1"
---

# WHO SMART Country Profiling Skill

## Purpose

Use this skill to produce a structured, source-backed profile of a country's health system context for a target health domain and DAK implementation.

The profile should help later localization work by identifying known facts, missing evidence, uncertain mappings, reusable regional context, and areas needing human expert input.

## When to use this skill

Use this skill when the task asks you to:

- contextualize a country for DAK implementation;
- prepare a country profile before localizing WHO SMART content;
- gather open WHO and country health system evidence;
- identify country-specific implementation constraints;
- create reusable inputs for a later policy comparison or adaptation task.

## When not to use this skill

Do not use this skill to:

- make clinical decisions;
- produce final national policy;
- rank countries clinically or politically;
- invent country context where evidence is missing;
- treat open data as a substitute for local expert validation.

## Required inputs

Minimum input:

1. Country name.
2. Target health domain.
3. DAK, WHO guidance, or SMART artifact scope.

Recommended input:

1. National health strategy or health sector plan.
2. Domain-specific national policy or programme document.
3. Country Cooperation Strategy or equivalent WHO country document.
4. Relevant WHO indicators or open datasets.
5. Retrieval date and source URLs for every document or dataset.

See `context/input-documentation.md` for input guidance.

## Workflow

1. Confirm the country, target health domain, and DAK scope.
2. Run the predefined WHO retrieval task before writing conclusions:

```bash
python3 skills/country-profiling/scripts/retrieve_who_sources.py --country "<country>" --domain "<health-domain>"
```

3. Review the generated retrieval bundle and add any user-supplied country documents to the source inventory.
4. Separate WHO/global sources from country-specific sources.
5. Extract facts relevant to DAK implementation, including health system structure, governance, financing, workforce, digital health, data systems, and domain-specific service delivery.
6. Record each finding with source evidence and retrieval date.
7. Label each finding as known, uncertain, missing, or requiring expert review.
8. Produce the profile using the schema in `context/profile-schema.md`.
9. Preserve gaps and uncertainty for later localization skills instead of resolving them by assumption.

## Output requirements

Return a markdown country profile with the required sections in `context/profile-schema.md`.

Every substantive claim should include:

- source name;
- source type;
- source URL or local file path;
- retrieval or publication date when available;
- confidence level;
- review need.

## WHO data access

For general deployment, this skill includes a predefined WHO retrieval runner:

```bash
python3 skills/country-profiling/scripts/retrieve_who_sources.py --country "<country>" --domain "<health-domain>"
```

The runner produces a markdown and JSON retrieval bundle under `skills/country-profiling/retrieval-output/` by default. It checks candidate DAK and WHO source pages, queries WHO Global Health Observatory metadata when available, and records retrieval failures as reviewable evidence gaps instead of stopping the skill.

The lower-level helper `scripts/who_gho_client.py` can still be used for direct GHO OData lookups.

See `context/who-data-retrieval.md` for recommended WHO sources and retrieval patterns.

## MCP-aware behavior

MCP integration is recommended later for structured SMART/FHIR artifacts and terminology-aware retrieval, but it should not block the first prototype.

See `context/mcp-integration-plan.md` for the proposed implementation plan.

## Safety and uncertainty rules

- Do not invent health system facts, policy statements, indicators, or citations.
- Prefer "not found in provided sources" over speculation.
- Keep country-specific documentation separate from WHO global sources.
- Flag stale, unclear, or conflicting evidence.
- Treat all outputs as preparation for human review.
