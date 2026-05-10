# Country profile output schema

The Country Profiling skill should produce a markdown document with the sections below.

The profile may be produced from user-provided documents, retrieval-assisted outputs, or a combination of both. If a document class is missing, record it as an evidence gap rather than filling it from assumption.

## Required sections

```md
# Country profile: <Country> - <Health domain>

## Profile metadata

## Executive summary

## Source inventory

## Country and health system context

## DAK implementation context

## Domain-specific considerations

## Data and digital health context

## Known facts

## Uncertainties and evidence gaps

## Human expert input needed

## Reuse opportunities for regional adaptation

## Sources
```

## Profile metadata

Include:

- country;
- target health domain;
- DAK or WHO artifact scope;
- profile date;
- profile author or agent;
- known input limitations.

## Source inventory

Use this table:

```md
| Source | Source type | Publisher | Date | URL or file path | Relevance | Status |
|---|---|---|---|---|---|---|
```

Allowed `Status` values:

- `Reviewed`
- `Candidate source`
- `Needs retrieval`
- `Needs expert validation`

Use `Reviewed` only when the profile actually uses the source as evidence. Use `Candidate source` for sources identified but not fully reviewed.

## Context sections

Use the context sections to summarize only source-backed material relevant to later localization:

- `Country and health system context`: governance, delivery, financing, workforce, or system constraints when sourced.
- `DAK implementation context`: workflows, personas, data elements, indicators, decision logic, or operational requirements that may need adaptation.
- `Domain-specific considerations`: health-domain facts or implementation constraints found in sources.
- `Data and digital health context`: registries, reporting systems, interoperability, data quality, terminology, or digital strategy context when sourced.

If a context area has no supporting source, write a brief evidence-gap note instead of inventing content.

## Known facts

Use this table for claims that are supported by the available sources:

```md
| Area | Finding | Evidence | Source | Confidence | Review need |
|---|---|---|---|---|---|
```

Allowed `Confidence` values:

- `High`
- `Medium`
- `Low`

Allowed `Review need` values:

- `No immediate review`
- `Confirm with country expert`
- `Check newer source`
- `Validate domain interpretation`
- `Resolve conflicting evidence`

## Uncertainties and evidence gaps

Use this table:

```md
| Gap or uncertainty | Why it matters for DAK implementation | Suggested next source | Review owner |
|---|---|---|---|
```

Include missing source classes, conflicting evidence, stale documents, unclear applicability, and country/domain facts that could not be supported.

## Human expert input needed

List review actions that require local, WHO, policy, clinical, legal, terminology, digital health, or implementation expertise. Do not use this section to hide unsupported conclusions.

## Reuse opportunities for regional adaptation

Identify possible reuse only when supported by sources, such as common regional guidance, shared reporting requirements, or comparable implementation constraints. If reuse cannot be assessed yet, state the evidence gap.

## Sources

List every source used. Include URLs, local file paths, or dataset identifiers. Record retrieval dates for web sources.

## Validation expectations

The structural validator checks for:

- all required sections;
- a source inventory table;
- at least one known facts row;
- an uncertainties and evidence gaps table;
- controlled values for source status, confidence, and review need.

The validator does not check whether the country profile is clinically, legally, or policy correct.
