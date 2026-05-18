# Localization Skills Index

This repository contains Agent Skills for WHO SMART Guidelines localization.
Each skill lives in its own folder under `skills/`.

## Skill inventory

### Country Profiling

- Status: Active / MVP polish.
- Location: `skills/country-profiling/`.
- Purpose: Builds a source-backed healthcare country profile from minimal
  country input, supplied documents, deterministic baseline retrieval, or
  controlled web-assisted retrieval.
- Notes: Output should feed later policy comparison by identifying context,
  source gaps, and readiness.

### Policy Comparison

- Status: Planned / migrated starting point.
- Location: `skills/policy-comparison/`.
- Purpose: Will compare WHO/SMART content with national policy material.
- Notes: Should use country profile output as context.

### Terminology Mapping

- Status: Possible future extension.
- Location: Not implemented.
- Purpose: Would support terminology, code, formulary, schedule, or
  data-element mapping.
- Notes: Optional and likely requires MCP/FHIR tooling.

## Notes

- Country Profiling is the currently active skill.
- Country Profiling has a retrieval-assisted reference example for manual
  review. It is a behavior reference, not a benchmark or test case.
- Validators check structure only.
- Skills are review aids and do not replace expert review.
