# Semi-deterministic web-assisted retrieval

Use this protocol when Country Profiling scripts are unavailable but web access
is available. The goal is controlled source retrieval for a draft profile that
requires human review, not extensive manual source construction.

Web-assisted retrieval should remain structured and source-prioritized. It is
not open-ended browsing.

## Source priority

Search source classes in this order:

1. WHO country / regional pages and WHO data sources.
2. European Observatory / OECD / EU country profiles where relevant.
3. World Bank Data / World Bank country indicators.
4. National Ministry of Health.
5. National public health institute.
6. National medicines agency / vaccine authority, where relevant.
7. National statistics office.
8. Peer-reviewed or institutional publications only if official sources are
   unavailable or insufficient.

Prefer official and institutional sources. Use peer-reviewed or secondary
institutional literature to fill context gaps only when official sources are
missing, stale, inaccessible, or insufficient.

## Retrieval record

For every reviewed source or candidate source lead, record:

- source title;
- publisher;
- URL;
- publication or dataset date;
- retrieval date;
- source type;
- status;
- whether the source was actually reviewed or only identified.

Allowed statuses should map to the profile schema:

- `Reviewed`;
- `Candidate source`;
- `Needs retrieval`;
- `Needs expert validation`;
- `Not available in supplied material`.

## Landing page rule

Do not use a landing page as if it were the PDF, dataset, official attachment,
or full-text source.

If a landing page links to a PDF, record the landing page as a landing page
unless the actual PDF URL is retrieved and reviewed. If the PDF or dataset is
missing or inaccessible, mark it as an evidence gap.

Generic dashboards, topic pages, institutional home pages, publication catalogs,
search pages, and download pages are source leads. They can support source
discovery but cannot support precise country claims unless their contents were
actually reviewed and are specific enough for the claim.

## Reviewed evidence versus candidate leads

Separate:

- reviewed evidence used in the profile;
- datasets retrieved or reviewed;
- web-reviewed sources;
- candidate source leads identified but not reviewed;
- landing pages requiring PDF, dataset, or attachment retrieval;
- inaccessible sources and missing documents.

This distinction should appear in the source inventory, source notes, and
evidence gaps.

## Italy recommended source leads

For Italy, prioritize:

- European Observatory / WHO health system review or health system summary;
- State of Health in the EU Italy Country Health Profile;
- World Bank Data for baseline indicators;
- Italian Ministry of Health;
- Istituto Superiore di Sanita;
- AIFA;
- National Vaccine Prevention Plan 2023-2025;
- OECD / Eurostat where relevant.

For immunization-focused downstream work, also look for Ministry/ISS coverage
datasets, official circulars, national vaccine calendar attachments, regional
implementation documents, pharmacovigilance material, registry/reporting
specifications, and digital health data-flow sources. Country Profiling should
identify these as source classes and gaps; it should not compare Italian policy
with WHO guidance.

If the shared local DAK exists at `shared/assets/who-immunizations-dak.pdf`,
include it as an available WHO SMART / DAK artifact for later Policy Comparison.
Do not treat it as evidence about the target country's health system or
implementation context.

## Drafting rules

- Prefer latest sources, but do not discard authoritative older health-system
  reviews if still relevant for structure, governance, or implementation
  context.
- Do not claim completeness from web retrieval alone.
- Do not make precise statistics unless a reviewed source or retrieved dataset
  supports the value, year, and definition.
- Keep WHO/global guidance separate from country-specific evidence.
- Mark missing or inaccessible documents as evidence gaps.
- Ask for human review of the draft and source inventory, not for manual source
  construction unless key source classes remain missing after controlled
  retrieval.
