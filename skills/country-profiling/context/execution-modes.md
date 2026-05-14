# Execution modes

Country Profiling supports two execution modes. Preflight and retrieval scripts are optional assistance, not mandatory gates for every profile.

## Document-only mode

Use document-only mode by default when the user provides enough source material in the prompt, attached files, local files, or conversation context.

In this mode, the Agent should:

- identify the target country and optional downstream health-area focus, region, population group, or downstream use;
- normalize the supplied material into the source inventory from `profile-schema.md`;
- draft only from the supplied material;
- mark missing source classes and missing facts as evidence gaps;
- avoid using assumptions to fill country context.

## Retrieval-assisted mode

Use retrieval-assisted mode when scripts or tools are available and the user asks for, allows, or clearly needs assistance finding candidate sources.

The helper command is:

```bash
python3 skills/country-profiling/scripts/prepare_profile_run.py \
  --country "<country>" \
  --focus "<optional downstream health-area focus>"
```

Country documents can be listed with repeated `--country-document` arguments:

```text
title|document type|path-or-url|date
```

The command can write:

- `profile-preflight-manifest.json`;
- `input-documentation-inventory.md`;
- a `who-retrieval/` directory with candidate retrieval artifacts.

Treat these outputs as source-inventory support. They can improve traceability, but they do not replace reading and citing the actual sources. Generic WHO or global pages are discovery surfaces; they are not country-specific evidence unless they resolve to country-specific documents or country-filtered datasets.

## Proceeding with a profile

Use this decision rule:

| Output type | When to use |
|---|---|
| Full profile | The country is known and enough country-specific sources are available to support several major profile sections. |
| Limited profile | The country is known and some relevant evidence is available, but important sections depend on missing, stale, generic, or uncertain sources. |
| Skeleton/gap-analysis profile | The country is known, little evidence is available, and the user asks for planning, source discovery, or gap analysis. |
| Pause and ask for sources | No country is specified, or no relevant source is available and the user did not request a skeleton/gap-analysis profile. |

If scripts are unavailable or fail, the Agent may still proceed in document-only mode when user-provided sources satisfy the conditions above. If both scripts fail and sources are insufficient, ask for source material or produce only a limited skeleton/gap-analysis profile if the user requested one.

## Downstream policy-comparison decision

A profile can feed the future Policy Comparison skill only if it identifies enough country context and at least suggests which national policy documents are needed. It does not need to include the policy documents themselves unless the user is preparing an immediate comparison.

If the profile cannot support downstream comparison, write `Not ready for policy comparison` in the `Policy-analysis readiness` section and explain why. Common reasons include missing national policy sources, no country-specific health system evidence, unresolved source conflicts, stale documents, or insufficient context for interpreting policy text.

## Handling missing sources

Missing content should become evidence gaps, not assumptions. This keeps later policy comparison work honest about what still requires retrieval, review, or local expertise.

Examples of evidence gaps:

- missing country health profile or national health strategy;
- missing recent burden-of-disease or surveillance source;
- missing health financing or coverage source;
- missing WASH, sanitary, or environmental health source;
- missing health workforce or facility-capacity source;
- missing digital health or health information system documentation;
- missing authoritative policy documents for the downstream comparison topic.

## Handling conflicting sources

When sources conflict:

- record both sources in the source inventory;
- describe the conflict in `Evidence gaps and expert input needed`;
- avoid choosing one source as authoritative unless the provided evidence clearly supports that choice;
- assign a human expert review action.

## Retrieval cautions

Retrieved WHO/global sources may be globally relevant without being country-specific evidence. Generic WHO landing pages, broad dashboards, empty datasets, or unresolved source discovery should be recorded as candidate sources or evidence gaps, not as proof of national health conditions, coverage, sanitary conditions, or implementation context.
