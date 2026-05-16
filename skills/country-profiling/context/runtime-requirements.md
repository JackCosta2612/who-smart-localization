# Runtime requirements

The Country Profiling retrieval helpers are designed to run in changing Agent environments with minimal setup.

## Required for deterministic script-assisted retrieval

- Python 3.10 or newer.
- Python standard library only.
- Write access to the output directory, defaulting to `skills/country-profiling/retrieval-output/`.

## Optional

- Outbound HTTPS access for live World Bank and WHO retrieval.
- No optional Python packages are required for the current helper scripts.
- MCP tooling is optional and documented separately in `mcp-integration-plan.md`.

## Optional preparation check

The Agent can run the combined preparation command when document inventory and
WHO source-discovery support are useful:

```bash
python3 skills/country-profiling/scripts/prepare_profile_run.py \
  --country "Romania" \
  --focus "general healthcare overview"
```

The preparation command writes `profile-preflight-manifest.json`. Treat it as support for source inventory and gap tracking. If it fails, document-only mode can still proceed when enough user-provided source material is available.

## Standalone environment check

Run this before retrieval if the Agent environment is unknown:

```bash
python3 skills/country-profiling/scripts/check_environment.py
```

Expected behavior:

- returns `0` if the minimum Python version and output directory checks pass;
- warns, but does not fail, when live network access cannot be confirmed;
- prints clear remediation notes.

## Deterministic baseline retrieval command

Run from the repository root:

```bash
python3 skills/country-profiling/scripts/retrieve_country_profile_data.py \
  --country "Italy" \
  --iso3 "ITA" \
  --focus "immunization"
```

This writes `retrieved-indicators.json`, `retrieved-indicators.md`, and
`source-leads.md`. Treat these as source artifacts and gap-mapping support, not
as proof of country-profile completeness.

## WHO source-discovery command

Run from the repository root:

```bash
python3 skills/country-profiling/scripts/retrieve_who_sources.py \
  --country "Romania" \
  --focus "general healthcare overview"
```

To avoid network calls in restricted environments:

```bash
python3 skills/country-profiling/scripts/retrieve_who_sources.py \
  --country "Romania" \
  --focus "general healthcare overview" \
  --offline
```

Offline mode still writes a retrieval bundle with candidate WHO sources and explicit "not checked" statuses.

## Content retrieval behavior

Live mode writes these artifacts:

- `<country>-<focus>-who-retrieval.md`;
- `<country>-<focus>-who-retrieval.json`;
- `content/*.txt` page text snapshots;
- `content/*-links.json` link inventories;
- `content/gho-*.json` country-filtered GHO data samples;
- downloaded document files when supported links are discovered and the file size is within the configured limit.

The runner uses size limits to avoid failing in constrained environments. Tune these only when the Agent environment can safely store larger files:

```bash
python3 skills/country-profiling/scripts/retrieve_who_sources.py \
  --country "Romania" \
  --focus "general healthcare overview" \
  --max-page-bytes 2000000 \
  --max-download-bytes 15000000
```
