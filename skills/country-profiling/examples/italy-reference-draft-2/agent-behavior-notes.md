# Agent behavior notes

Draft 2 demonstrates how to produce a country profile when the user has a clear
downstream immunization focus.

## What this example teaches

- Keep the output as country profiling even when a policy topic is known.
- Cover general SSN structure before discussing immunization, because regional
  implementation affects vaccination policy interpretation.
- Identify the main national immunization source family: PNPV, national
  vaccination calendar, Ministry material, ISS sources, AIFA sources, coverage
  data, and regional implementation acts.
- Avoid stating exact vaccine schedules or target groups unless the official
  calendar has been reviewed.
- Separate access/entitlement context from policy comparison findings.

## What to imitate

- More detail on vaccination governance than Draft 1.
- Clear distinction between national policy, regional implementation, coverage
  evidence, pharmacovigilance, and digital reporting.
- Handoff rows that tell the Policy Comparison skill exactly what to retrieve
  next.

## What not to imitate

- Do not perform WHO-versus-Italy immunization comparison.
- Do not treat the ISS explanatory page as a substitute for the official
  Gazzetta/Ministry policy text.
- Do not infer current target groups from general vaccine knowledge.
- Do not claim that AIFA regulatory material proves service availability.

## Boundary before policy comparison

The draft identifies PNPV 2023-2025 as the core downstream national policy
source, but it does not assess alignment with WHO schedules, recommendations,
indicators, or SMART data elements.

## Reuse by Policy Comparison

Use this draft as the starting source checklist for an immunization comparison.
The next skill should retrieve official attachments, legal texts, regional
implementation material, coverage datasets, reporting forms, and WHO/SMART
source material before analysis.

## Weaknesses requiring manual review

- The official national calendar is not extracted.
- Regional implementation is not reviewed.
- Coverage sources are identified but not analyzed.
- Digital registry and reporting workflows remain uncertain.
