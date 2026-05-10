# Execution modes

Country Profiling supports two execution modes. Preflight and retrieval scripts are optional assistance, not mandatory gates for every profile.

## Document-only mode

Use document-only mode when the user provides enough source material in the prompt, attached files, local files, or conversation context.

In this mode, the Agent should:

- identify the target country, health domain, and DAK or SMART Guidelines scope;
- normalize the supplied material into the source inventory from `profile-schema.md`;
- draft only from the supplied material;
- mark missing document classes and missing facts as evidence gaps;
- avoid using assumptions to fill country context.

## Retrieval-assisted mode

Use retrieval-assisted mode when scripts or tools are available and the user asks for, allows, or clearly needs assistance finding candidate sources.

The helper command is:

```bash
python3 skills/policy-comparison/scripts/prepare_profile_run.py \
  --country "<country>" \
  --domain "<health-domain>" \
  --dak-scope "<DAK or WHO artifact scope>"
```

Country documents can be listed with repeated `--country-document` arguments:

```text
title|document type|path-or-url|date
```

The command can write:

- `profile-preflight-manifest.json`;
- `input-documentation-inventory.md`;
- a `who-retrieval/` directory with candidate retrieval artifacts.

Treat these outputs as source-inventory support. They can improve traceability, but they do not replace reading and citing the actual sources.

## Proceeding with a profile

Profile drafting may proceed when:

- a target country is known;
- a health domain or DAK scope is known;
- at least one relevant country-specific source is available, or the user explicitly requests a skeleton/gap-analysis profile.

Profile drafting should be limited or paused when:

- no country is specified;
- no health domain or DAK scope is specified;
- no country-specific source is available and the user did not ask for a skeleton;
- the provided material is not relevant to the country or domain.

If scripts are unavailable or fail, the Agent may still proceed in document-only mode when user-provided sources satisfy the conditions above. If both scripts fail and sources are insufficient, ask for source material or produce only a limited skeleton/gap-analysis profile if the user requested one.

## Handling missing sources

Missing content should become evidence gaps, not assumptions. This keeps later localization work honest about what still requires retrieval, review, or local expertise.

Examples of evidence gaps:

- missing national health strategy;
- missing domain-specific national programme guidance;
- missing digital health or health information system documentation;
- missing local schedule, registry, reporting form, data dictionary, or terminology source.

## Handling conflicting sources

When sources conflict:

- record both sources in the source inventory;
- describe the conflict in `Uncertainties and evidence gaps`;
- avoid choosing one source as authoritative unless the provided evidence clearly supports that choice;
- assign a human expert review action.

## Retrieval cautions

Retrieved WHO/global sources may be globally relevant without being country-specific evidence. Generic WHO landing pages, broad dashboards, empty datasets, or unresolved source discovery should be recorded as candidate sources or evidence gaps, not as proof of national policy or implementation context.
