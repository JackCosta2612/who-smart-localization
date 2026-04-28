---
name: who-smart-localization
description: Supports localization of WHO SMART Guidelines by comparing WHO global guidance or SMART Guideline components with country-specific policy material. Use when asked to identify alignment, divergence, missing elements, terminology differences, localization gaps, or country adaptation issues in health guidance.
license: MIT
compatibility: Model-neutral Agent Skill. Optional MCP/FHIR terminology tools may be used when available.
metadata:
  project: "USI NLP WHO SMART Guidelines project"
  team: "Giacomo Costantino, Leonardo Gravellone, Marionne Blanco Herrera"
  version: "0.1"
---

# WHO SMART Localization Skill

## Purpose

Use this skill to compare WHO global guidance or SMART Guideline components with country-specific policy material and produce a structured localization matrix for human review.

The goal is traceable comparison, not autonomous policy or clinical decision-making.

## When to use this skill

Use this skill when the task asks you to:

- compare WHO guidance with local policy text;
- identify alignment, partial alignment, divergence, missing content, or terminology gaps;
- summarize localization findings in a structured table;
- prepare material for expert review during country adaptation work.

## When not to use this skill

Do not use this skill to:

- give patient-specific medical advice;
- invent or finalize national policy;
- judge clinical correctness without source evidence;
- replace legal, policy, or clinical expert review;
- build a full FHIR workflow unless that is explicitly requested.

## Required inputs

Provide:

1. A WHO source statement, recommendation, or structured SMART Guideline component.
2. A local policy excerpt or country-specific implementation statement.
3. Source identifiers or citations when available.
4. Enough surrounding context to interpret the excerpt safely.

If the local source is missing, incomplete, or ambiguous, state that explicitly instead of inferring content.

## Workflow

1. Read the WHO source and local source closely.
2. Separate claims, constraints, and terminology in each source.
3. Compare meaning, not just wording.
4. Classify the relationship using the controlled alignment categories in `context/localization-categories.md`.
5. Extract direct evidence from both sources.
6. Record uncertainty and assign a confidence level.
7. Recommend a human review action when the row needs follow-up.

## Alignment categories

Use only these controlled categories unless the project maintainers explicitly change them:

- `Aligned`
- `Partially aligned`
- `Divergent`
- `Missing in local policy`
- `More specific in local policy`
- `More restrictive in local policy`
- `Unclear or requires expert review`

See `context/localization-categories.md` for definitions and examples.

## Expected output format

Return a markdown localization matrix with the header defined in `context/output-schema.md`.

Minimum required columns:

- `WHO source statement`
- `Local policy statement`
- `Alignment status`
- `Difference type`
- `Explanation`
- `Evidence from WHO source`
- `Evidence from local source`
- `Confidence`
- `Human review action`

## Safety and uncertainty rules

- Preserve traceability to the provided source text.
- Do not invent local policy content, WHO guidance, codes, or citations.
- If evidence is incomplete, say so directly.
- Use `Unclear or requires expert review` when classification is not well supported.
- Treat the output as a review aid, not as a final policy decision.

## Optional MCP-aware behavior

If terminology or FHIR-aware tools are available, you may optionally:

1. Identify relevant WHO concepts, codes, or terminology bindings.
2. Inspect ValueSets or code lookups that clarify local terminology mapping.
3. Flag uncertain mappings for expert review instead of forcing a conclusion.

This behavior is optional. The default workflow must still work with plain documents only.
