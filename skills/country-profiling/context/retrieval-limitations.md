# Retrieval limitations

The retrieval runner is a source-discovery helper. It can retrieve reachable WHO pages, link inventories, downloadable files, and selected GHO JSON samples, but reachability is not the same as country-specific evidence.

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
