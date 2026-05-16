# Agent behavior notes

This example should shape Country Profiling behavior for Italy-like requests.

## Expected behavior

- Resolve supplied source URLs to source material before marking sources
  `Reviewed`.
- Keep a balanced country profile even when a downstream focus such as
  immunization is supplied.
- Treat immunization policy sources as handoff material unless the user asks for
  the future Policy Comparison skill.
- Separate national policy text, regional implementation, coverage evidence,
  digital data flows, operational capacity, and expert validation.
- Prefer explicit evidence gaps over assumptions.

## Boundary to enforce

The Country Profiling skill may say that PNPV 2023-2025 and the national
vaccination calendar are the core Italian immunization source family for later
comparison. It should not decide whether Italian policy aligns with WHO
guidance, recommend schedule changes, or make clinical judgments.

## Reliability pattern

When a user supplies a URL like an OECD publication page with a "Download PDF"
button, the Agent should answer the implicit question this example is designed
to catch:

- if the PDF or full-text material endpoint is opened, the source can become
  `Reviewed`;
- if only the landing page is opened, the source remains a candidate or
  retrieval gap;
- if the direct material endpoint is not reachable, the Agent should record the
  failure and avoid evidence claims that require that source.
