# Country profile output schema

The Country Profiling skill should produce a markdown document with the sections below.

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

## Sources

List every source used. Include URLs, local file paths, or dataset identifiers. Record retrieval dates for web sources.

## Validation expectations

The structural validator checks for:

- all required sections;
- a source inventory table;
- at least one known facts row;
- controlled values for source status, confidence, and review need.

The validator does not check whether the country profile is clinically, legally, or policy correct.
