# Retrieval limitations and current Romania test assessment

This note records the known limitation identified from the saved Romania immunization retrieval artifacts. It is documentation only; no test was rerun for this assessment.

## Summary

The current retrieval runner successfully checks accessible WHO source pages and retrieves page snapshots, link inventories, downloadable documents, and selected GHO JSON samples. The Romania test is partially failing because some accessible source pages are generic landing pages, not country-specific data endpoints.

Reachability is therefore not the same as successful country-specific retrieval.

## Identified causes

### Generic WHO source pages

These sources are included as broad source classes:

- WHO Country Cooperation Strategies
- WHO SCORE documents
- Global Health Expenditure Database
- National Health Workforce Accounts

The runner now fetches the landing page and records discovered links for generic source classes, but it does not treat those discovered links as country-specific evidence. Generic landing pages use a `discover-links-only` download policy so the script does not download arbitrary documents just because they are linked from an accessible page.

For Romania, this means the script may retrieve accessible WHO source discovery pages without resolving the Romania-specific Country Cooperation Strategy, SCORE country summary, GHED country data, or workforce data.

### GHO indicator metadata versus country data

The GHO indicator search returns candidate indicator codes by domain term. The follow-up country-filtered requests can return zero rows for some indicators even though the indicator exists and the country code was resolved.

This can happen when:

- the indicator has no Romania rows in that endpoint;
- the indicator uses dimensions beyond `SpatialDim` that require additional filtering;
- the indicator code is legacy or exposed differently from the searchable metadata;
- the selected candidate indicators are domain-relevant but not populated for the country.

Zero rows are now marked as `retrieved_empty` and should be treated as a data gap, not as proof that the indicator is irrelevant.

## Required next retrieval phase

The next implementation should add source-specific resolvers:

| Source class | Needed resolver behavior |
|---|---|
| Country Cooperation Strategies | Search or filter WHO IRIS/WHO country pages for the requested country and retrieve the matching document. |
| SCORE documents | Resolve the requested country summary or explicitly report that no country summary was found. |
| GHED | Use a data endpoint or export path that returns country-level expenditure data, not only the GHED landing page. |
| National Health Workforce Accounts | Retrieve country-specific workforce data or record that only the framework/source class was retrieved. |
| GHO indicators | Distinguish candidate indicator discovery from country-row retrieval; record zero-row datasets as `retrieved_empty`. |

## Current code behavior

The retrieval output now distinguishes:

- `global-domain-source`: a WHO source that is globally relevant to the target health domain, such as a DAK;
- `generic-source-discovery`: a WHO source page that helps discover possible documents or datasets but is not country-specific evidence by itself;
- `unresolved-source-discovery`: a source class that still requires manual or source-specific resolution.

The code also uses source-level download policies:

- `download-supported-documents` for domain-specific WHO source pages such as mapped DAKs;
- `discover-links-only` for generic source pages such as CCS, SCORE, GHED, and NHWA.

## Documentation rule for Agents

When reviewing a retrieval bundle, the Agent must distinguish:

- `source reachable`;
- `generic source content retrieved`;
- `country-specific document retrieved`;
- `country-specific structured data retrieved`;
- `retrieved but empty`;
- `not resolved and requires human/source-specific follow-up`.

The profile must not present generic WHO landing-page retrieval as country-specific evidence.
