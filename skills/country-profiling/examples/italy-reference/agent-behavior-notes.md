# Agent behavior notes

This example demonstrates the preferred minimal-input Country Profiling pattern:
country plus optional downstream focus, not a human-built source packet.

## Expected behavior

- Use deterministic retrieval to produce a baseline indicator bundle when
  scripts are available.
- Use semi-deterministic web-assisted retrieval when scripts are unavailable,
  following the source priority and provenance rules in
  `context/web-assisted-retrieval.md`.
- Treat source leads carefully. A source lead is not reviewed evidence until the
  PDF, dataset, official attachment, official full-text HTML, or local file is
  opened and used.
- Use retrieved indicators as context, not as proof of completeness.
- Ask for human review of the draft and source inventory, not for manual source
  construction, unless key source classes remain missing.
- Feed the Policy Comparison skill by identifying context, likely source
  classes, and gaps without performing comparison.

## Boundary to enforce

Country Profiling may identify Italy's SSN structure, baseline indicators,
regional implementation risk, and immunization source classes. It should not
compare Italian immunization policy with WHO guidance, recommend schedule
changes, make clinical judgments, or claim policy readiness without source
support.

## Reliability pattern

When scripts are available, the agent should preserve indicator source, code,
value, year, URL, retrieval date, and status.

When scripts are unavailable, the agent should use the approved source priority
list, record publisher/title/date/URL/retrieval date/source type/status, and
separate reviewed evidence from candidate leads. Landing pages and inaccessible
PDFs become evidence gaps, not hidden assumptions.
