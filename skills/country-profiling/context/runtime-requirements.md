# Runtime requirements

The Country Profiling retrieval MVP is designed to run in changing Agent environments with minimal setup.

## Required

- Python 3.10 or newer.
- Python standard library only.
- Outbound HTTPS access for live WHO retrieval.
- Write access to the output directory, defaulting to `skills/country-profiling/retrieval-output/`.

## Optional

- No optional Python packages are required for the MVP.
- MCP tooling is optional and documented separately in `mcp-integration-plan.md`.

## Mandatory preflight check

The Agent should normally run the combined preflight, which includes the environment check:

```bash
python3 skills/country-profiling/scripts/prepare_profile_run.py \
  --country "Romania" \
  --domain "immunization" \
  --dak-scope "WHO immunization DAK"
```

The preflight writes `profile-preflight-manifest.json`. The Agent must not draft a profile when `may_draft_profile` is `false`.

## Standalone environment check

Run this before retrieval if the Agent environment is unknown:

```bash
python3 skills/country-profiling/scripts/check_environment.py
```

Expected behavior:

- returns `0` if the minimum Python version and output directory checks pass;
- warns, but does not fail, when live network access cannot be confirmed;
- prints clear remediation notes.

## Retrieval command

Run from the repository root:

```bash
python3 skills/country-profiling/scripts/retrieve_who_sources.py --country "Romania" --domain "immunization"
```

To avoid network calls in restricted environments:

```bash
python3 skills/country-profiling/scripts/retrieve_who_sources.py --country "Romania" --domain "immunization" --offline
```

Offline mode still writes a retrieval bundle with candidate WHO sources and explicit "not checked" statuses.

## Content retrieval behavior

Live mode writes these artifacts:

- `<country>-<domain>-who-retrieval.md`;
- `<country>-<domain>-who-retrieval.json`;
- `content/*.txt` page text snapshots;
- `content/*-links.json` link inventories;
- `content/gho-*.json` country-filtered GHO data samples;
- downloaded document files when supported links are discovered and the file size is within the configured limit.

The runner uses size limits to avoid failing in constrained environments. Tune these only when the Agent environment can safely store larger files:

```bash
python3 skills/country-profiling/scripts/retrieve_who_sources.py \
  --country "Romania" \
  --domain "immunization" \
  --max-page-bytes 2000000 \
  --max-download-bytes 15000000
```
