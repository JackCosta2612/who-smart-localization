# Preflight enforcement

The Country Profiling skill must run a preflight before drafting a country profile.

## Required command

Run from the repository root:

```bash
python3 skills/country-profiling/scripts/prepare_profile_run.py \
  --country "<country>" \
  --domain "<health-domain>" \
  --dak-scope "<DAK or WHO artifact scope>"
```

The command enforces three gates:

- runtime environment check;
- WHO source and data retrieval;
- country-specific input documentation inventory.

## Country document inputs

Country documents can be supplied with repeated `--country-document` arguments:

```bash
python3 skills/country-profiling/scripts/prepare_profile_run.py \
  --country "Romania" \
  --domain "immunization" \
  --dak-scope "WHO immunization DAK" \
  --country-document "Romania National Health Strategy|National health strategy or health sector plan|/path/to/strategy.pdf|2023"
```

Format:

```text
title|document type|path-or-url|date
```

## Generated outputs

The preflight writes:

- `profile-preflight-manifest.json`;
- `input-documentation-inventory.md`;
- a `who-retrieval/` directory containing the WHO retrieval bundle and content artifacts.

## Enforcement rules for the Agent

- Do not draft a profile if `may_draft_profile` is `false`.
- If country document classes are missing, preserve them as evidence gaps and human-review actions.
- Do not infer country policy from WHO/global sources.
- Use retrieved WHO content as evidence inputs, not as final interpretation.
- If the preflight cannot run because the environment lacks Python or write access, report the failed gate instead of drafting the profile.
