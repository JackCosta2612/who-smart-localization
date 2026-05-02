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
2. Run the mandatory preflight before writing conclusions:

```bash
python3 skills/country-profiling/scripts/prepare_profile_run.py \
  --country "<country>" \
  --domain "<health-domain>" \
  --dak-scope "<DAK or WHO artifact scope>"
```

3. Read `profile-preflight-manifest.json`. If `may_draft_profile` is `false`, stop and report the failed gate instead of drafting the profile.
4. Review the generated WHO retrieval bundle and `input-documentation-inventory.md`.
5. Carry missing country document classes into evidence gaps and human-review actions.
6. Separate WHO/global sources from country-specific sources.
7. Extract facts relevant to DAK implementation, including health system structure, governance, financing, workforce, digital health, data systems, and domain-specific service delivery.
8. Record each finding with source evidence and retrieval date.
9. Label each finding as known, uncertain, missing, or requiring expert review.
10. Produce the profile using the schema in `context/profile-schema.md`.
11. Preserve gaps and uncertainty for later localization skills instead of resolving them by assumption.

See `context/preflight-enforcement.md` for enforcement rules.

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

Direct use of this runner is allowed for debugging. During normal skill execution, the Agent must use `scripts/prepare_profile_run.py` so runtime checks, WHO retrieval, and input documentation inventory are all enforced together.

The runner produces a markdown and JSON retrieval bundle under `skills/country-profiling/retrieval-output/` by default. It retrieves more than URLs:

- WHO HTML source pages are fetched and saved as text snapshots under a `content/` subfolder.
- Links discovered on source pages are saved as JSON link inventories.
- Supported downloadable files, such as PDFs and spreadsheets, are downloaded when they are below the configured size limit.
- WHO Global Health Observatory indicator searches are followed by country-filtered data sample retrieval when a country code is found.

If any source cannot be fetched, the runner records the failure as a reviewable evidence gap instead of stopping the skill.

The Agent must distinguish retrieved generic WHO source pages from country-specific evidence. A reachable landing page is not enough to support a country-specific profile finding unless the retrieval bundle includes a matching country document, country-filtered dataset, or user-supplied country source.

The retrieval bundle includes `evidence_scope` and `download_policy` metadata. Treat `generic-source-discovery` as a pointer for follow-up retrieval, not as profile evidence about the country.

The lower-level helper `scripts/who_gho_client.py` can still be used for direct GHO OData lookups.

See `context/who-data-retrieval.md` for recommended WHO sources and retrieval patterns.
See `context/retrieval-limitations.md` for known MVP retrieval gaps.

## MCP-aware behavior

MCP integration is recommended later for structured SMART/FHIR artifacts and terminology-aware retrieval, but it should not block the first prototype.

See `context/mcp-integration-plan.md` for the proposed implementation plan.

## Safety and uncertainty rules

- Do not invent health system facts, policy statements, indicators, or citations.
- Prefer "not found in provided sources" over speculation.
- Keep country-specific documentation separate from WHO global sources.
- Do not draft a profile if the required preflight failed.
- Do not infer country-specific policy from missing country documents.
- Flag stale, unclear, or conflicting evidence.
- Treat all outputs as preparation for human review.
