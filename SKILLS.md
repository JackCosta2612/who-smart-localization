# Localization Skills Index

This repository contains Agent Skills for WHO SMART Guidelines localization. Each skill lives in its own folder under `skills/`.

| Skill | Status | Location | Purpose | Notes |
|---|---|---|---|---|
| Country Profiling | Active / MVP polish | `skills/country-profiling/` | Builds a source-backed healthcare country profile from minimal country input, supplied documents, deterministic baseline retrieval, or controlled web-assisted retrieval. | Output should feed later policy comparison by identifying context, source gaps, and readiness. |
| Policy Comparison | Planned / migrated starting point | `skills/policy-comparison/` | Will compare WHO/SMART content with national policy material. | Should use country profile output as context. |
| Terminology Mapping | Possible future extension | Not implemented | Would support terminology, code, formulary, schedule, or data-element mapping. | Optional and likely requires MCP/FHIR tooling. |

## Notes

- Country Profiling is the currently active skill.
- Country Profiling has a retrieval-assisted Italy reference example for manual
  review. It is a behavior reference, not a benchmark or test case.
- Validators check structure only.
- Skills are review aids and do not replace expert review.
