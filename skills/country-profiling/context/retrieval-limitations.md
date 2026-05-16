# Retrieval limitations

The retrieval runners are source-discovery and baseline-data helpers for country
profiling. The deterministic baseline runner can retrieve selected World Bank
indicator values and institutional source leads. The WHO runner can retrieve
reachable WHO pages, link inventories, downloadable files, and selected GHO JSON
samples. In all cases, reachability is not the same as country-specific
evidence.

Retrieval output cannot prove that a profile is complete. Missing or unresolved
retrieval outputs should become evidence gaps, not hidden assumptions. Retrieved
baseline indicators must be combined with official or institutional documents,
source inventories, implementation context, and human review.

## Deterministic baseline limitations

The deterministic baseline layer intentionally retrieves only a small controlled
indicator set. It does not retrieve regional implementation, national policy
text, digital registry specifications, service delivery workflows, or expert
interpretation. WHO GHO and OECD values may be recorded as candidate/manual
review sources unless stable retrieval is configured.

## Known limitations

### Generic source pages

Some source classes are broad discovery surfaces:

- WHO country and regional source pages
- WHO Country Cooperation Strategies
- WHO SCORE documents
- Global Health Expenditure Database
- National Health Workforce Accounts
- WASH or environmental health landing pages

The runner may fetch a landing page and record discovered links without resolving the exact country-specific document or dataset. Generic landing pages use a `discover-links-only` policy so the script does not download arbitrary documents just because they are linked from an accessible page.

### Landing pages versus source material

Publication pages and download pages are useful for discovery, but they are not
always the evidence-bearing material. If a source row points to a page whose
main function is "Download PDF", "view attachment", search, catalog navigation,
or language selection, the Agent must follow the page to the PDF, dataset,
official attachment, official full-text HTML, or local file before marking the
source `Reviewed`.

Examples:

- OECD country profile pages should be resolved to the direct `content/dam`
  PDF when the profile relies on the publication contents.
- Gazzetta Ufficiale top-level act pages should be resolved to the relevant
  full-text attachment pages when the plan or schedule attachment is being used.
- Dataset portals should be resolved to country-filtered rows or an export
  before making country-specific quantitative claims.

If only the landing page was checked, use `Candidate source` or `Needs
retrieval` and carry the unresolved material endpoint into the evidence gaps.

### GHO indicator metadata versus country data

The GHO indicator search returns candidate indicator codes by search term. The follow-up country-filtered requests can return zero rows even when the indicator exists and the country code was resolved.

This can happen when:

- the indicator has no rows for the country;
- the indicator uses dimensions beyond `SpatialDim` that require additional filtering;
- the indicator code is legacy or exposed differently from the searchable metadata;
- the selected candidate indicators are topic-relevant but not populated for the country.

Zero rows are marked as `retrieved_empty` and should be treated as a data gap, not as proof that the indicator is irrelevant.

## Needed future retrieval improvements

| Source class | Needed resolver behavior |
|---|---|
| Country health profile or country cooperation strategy | Search or filter WHO/region/country pages for the requested country and retrieve the matching document. |
| SCORE documents | Resolve the requested country summary or explicitly report that no country summary was found. |
| GHED | Use a data endpoint or export path that returns country-level expenditure data, not only the GHED landing page. |
| Workforce data | Retrieve country-specific workforce data or record that only the framework/source class was retrieved. |
| WASH and environmental health | Retrieve country-specific sanitation, water, hygiene, pollution, or environmental risk indicators. |
| GHO indicators | Distinguish candidate indicator discovery from country-row retrieval; record zero-row datasets as `retrieved_empty`. |

## Documentation rule for Agents

When reviewing a retrieval bundle, the Agent must distinguish:

- `source reachable`;
- `generic source content retrieved`;
- `country-specific document retrieved`;
- `country-specific structured data retrieved`;
- `retrieved but empty`;
- `not resolved and requires human/source-specific follow-up`.

The profile must not present generic WHO landing-page retrieval as country-specific evidence.

The retrieval bundle also must not be used to perform policy alignment or divergence analysis. That work belongs in the future Policy Comparison skill after country context and source readiness are established.
