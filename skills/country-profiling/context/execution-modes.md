# Execution modes

Country Profiling creates a country context layer for WHO / SMART / DAK
localization work. It is not only for countries missing from WHO databases. A
country may have strong WHO, World Bank, OECD, EU, or national data coverage and
still require localization because implementation depends on health-system
structure, governance, regional variation, digital infrastructure, service
delivery, policy ownership, and source gaps.

The skill supports three execution modes.

## 1. Document-only mode

Use document-only mode when the user provides source documents, excerpts,
attachments, local files, or conversation context that are sufficient to draft
from supplied material.

In this mode, the Agent should:

- identify the target country and optional downstream health-area focus;
- normalize supplied material into the source inventory from
  `profile-schema.md`;
- draft only from supplied material;
- mark missing source classes and missing facts as evidence gaps;
- avoid using web search or deterministic scripts unless the user asks for mixed
  retrieval support.

Supplied URLs are not automatically reviewed evidence. A catalog page,
publication landing page, search result, or download page remains a candidate
until the PDF, dataset, official attachment, official full-text HTML, or local
file has been opened and reviewed.

## 2. Deterministic script-assisted retrieval mode

Use deterministic script-assisted retrieval when Python scripts are available
and the user provides only a country and optional downstream focus. This is the
preferred assistance path for minimal-input profiling.

The baseline retrieval command is:

```bash
python3 skills/country-profiling/sourcing_scripts/retrieve_country_profile_data.py \
  --country "<country>" \
  --iso3 "<ISO3>" \
  --focus "<optional downstream health-area focus>"
```

The script writes:

- `retrieved-indicators.json`;
- `retrieved-indicators.md`;
- `web-reviewed-sources.json`;
- `web-reviewed-sources.md`;
- `source-leads.md`.

The deterministic layer is intentionally small. It retrieves selected World Bank
baseline indicators, configured WHO GHO indicators, configured institutional
web/PDF sources, and short unresolved source gaps. OECD SDMX retrieval is not
active in this mode; OECD/EU context should come from reviewed institutional
profiles unless a future narrow dataset-specific retriever is added.

Use deterministic outputs as source artifacts. Precise data claims must include
indicator source, code, year, source URL, and retrieval date. Successful
retrieval does not prove completeness; it only provides a baseline context
bundle.

## 3. Semi-deterministic web-assisted retrieval mode

Use semi-deterministic web-assisted retrieval when Python scripts are
unavailable but web access is available. Follow
`web-assisted-retrieval.md`.

This mode is structured source discovery and review, not open-ended browsing.
The Agent should:

- follow the predefined source priority list;
- search only for specific approved source classes;
- prefer official and institutional sources;
- record publisher, title, URL, date, retrieval date, source type, and status;
- separate reviewed evidence from candidate source leads;
- treat landing pages as landing pages unless the evidence-bearing material is
  retrieved and reviewed;
- mark inaccessible PDFs, missing datasets, and unresolved national/regional
  sources as evidence gaps.

## Mixed mode

Use mixed mode when supplied documents are combined with deterministic retrieval
or controlled web-assisted retrieval. This is common when the user supplies a
few national documents but still needs baseline indicators, reviewed source
artifacts, or gap mapping.

## What counts as enough evidence

| Output type | When to use |
|---|---|
| Full profile | The country is known and several major sections are supported by reviewed documents, retrieved indicators, or reviewed web sources. |
| Limited profile | Some relevant evidence is available, but important sections rely on missing, stale, landing-page-only, inaccessible, or unreviewed source classes. |
| Skeleton/gap-analysis profile | The country is known but there is too little reviewed evidence; the useful output is a source plan, evidence-gap map, and policy-comparison readiness assessment. |
| Pause and ask for sources | No country is specified, or neither scripts, web access, nor sufficient supplied documents are available and the user did not request a skeleton/gap analysis. |

Baseline indicators alone are not enough for a full profile. A full profile also
needs health-system context, source inventory, evidence gaps, and implementation
context. Official or institutional documents are usually required for system
organization, policy ownership, digital health, regional implementation, and
downstream policy-comparison readiness.

## When scripts are unavailable

If scripts are unavailable but web access exists, switch to semi-deterministic
web-assisted retrieval. Do not ask the user to construct a source package before
attempting controlled retrieval unless the task is high risk, the country is
ambiguous, or web access is blocked.

If scripts fail but supplied source material is adequate, proceed in
document-only or mixed mode and record the script failure as a retrieval gap
only if it affects the profile.

## When neither scripts nor enough documents are available

If there is no web access, no usable script path, and insufficient source
material, do not draft unsupported country facts. Ask for source material or
produce only a skeleton/gap-analysis profile if that is useful.

## Evidence gaps

Missing content should become evidence gaps, not assumptions. Include gaps from:

- missing data;
- unavailable indicator values;
- failed retrieval;
- landing-page-only sources;
- inaccessible PDFs or datasets;
- national, regional, or programme sources not reviewed;
- digital health or registry source classes not reviewed;
- policy sources needed later for comparison but not yet retrieved.

## Downstream policy-comparison decision

A profile can feed the future Policy Comparison skill only if it identifies
enough country context and at least suggests which national policy source
classes are needed. It does not need to include policy documents unless the user
is preparing an immediate comparison.

If the profile cannot support downstream comparison, write `Not ready for
policy comparison` in the `Policy-analysis readiness` section and explain why.
Common reasons include missing national policy sources, no country-specific
health system evidence, unresolved source conflicts, stale documents, or
insufficient context for interpreting policy text.
