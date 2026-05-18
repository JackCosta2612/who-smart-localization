# Runtime requirements

The Country Profiling retrieval helpers are designed to run in changing Agent environments with minimal setup.

## Required for deterministic script-assisted retrieval

- Python 3.10 or newer.
- Python standard library only.
- Write access to the output directory, defaulting to `skills/country-profiling/retrieval-output/`.

## Optional

- Outbound HTTPS access for live World Bank retrieval.
- Outbound HTTPS access for live WHO GHO and manifest-supplied institutional web/PDF retrieval.
- `pypdf>=6.0` for PDF text extraction. Without it, PDFs can still be
  downloaded and checksummed, but their status is `downloaded_parse_failed`.
- MCP tooling is optional and documented separately in `mcp-integration-plan.md`.

## Deterministic baseline retrieval command

Run from the repository root:

```bash
python3 skills/country-profiling/sourcing_scripts/retrieve_country_profile_data.py \
  --country "<country>" \
  --iso3 "<ISO3>" \
  --focus "<optional downstream focus>" \
  --source-manifest "<optional Agent-discovered source manifest>"
```

This writes `retrieved-indicators.json`, `retrieved-indicators.md`,
`web-reviewed-sources.json`, `web-reviewed-sources.md`, and `source-leads.md`.
Treat these as source artifacts and gap-mapping support, not as proof of
country-profile completeness.

Use `--strict` when a workflow should fail fast if all configured
network-backed indicator retrieval fails. Source manifests follow
`context/source-manifest-schema.md` and are the preferred way to pass
country-specific official URLs to the resolver.

## Structural validation command

```bash
python3 skills/country-profiling/sourcing_scripts/validate_profile.py \
  skills/country-profiling/examples/example_1/reference-output.md
```
