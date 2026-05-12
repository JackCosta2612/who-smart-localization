# Agent behavior notes

Draft 1 demonstrates the default Country Profiling behavior for a broad
health-system overview.

## What this example teaches

- Normalize a concise user request into a full country profile with an explicit
  downstream use.
- Use a balanced source inventory that distinguishes reviewed sources from
  candidate or missing source classes.
- Keep narrative sections concise while still covering every required schema
  section.
- Treat Italy's regionalized SSN as a central implementation context.
- Include immunization as a relevant future domain without letting it dominate.
- Use `Policy-analysis readiness` and `Policy-comparison handoff` to prepare the
  next skill rather than performing comparison.

## What to imitate

- Source-backed claims with source names in the surrounding prose.
- Cautious quantitative use: include only a small number of sourced statistics
  and mark where newer extraction is needed.
- Explicit evidence gaps for WASH, regional implementation, workforce detail,
  digital implementation performance, and coverage data.
- A clear statement that the profile is only partially ready for downstream
  comparison.

## What not to imitate

- Do not copy Italian facts into another country profile.
- Do not turn candidate sources into reviewed evidence.
- Do not infer regional implementation from national policy text.
- Do not compare Italian policies with WHO recommendations.
- Do not add clinical or policy recommendations.

## Boundary before policy comparison

The draft intentionally stops after identifying immunization, regionalization,
coverage, financing, digital health, and expert validation as handoff needs. It
does not assess whether Italy aligns with WHO immunization guidance.

## Reuse by Policy Comparison

Use this output as context for system structure, source classes, and evidence
gaps. The Policy Comparison skill should retrieve topic-specific policy text and
WHO/SMART material before making alignment or divergence claims.

## Weaknesses requiring manual review

- Some current indicators are not extracted.
- Environmental health and WASH are under-sourced.
- Regional implementation evidence is not reviewed.
- The PNPV is identified but not parsed.
