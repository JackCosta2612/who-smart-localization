# Test preflight enforcement

Purpose: verify that the Country Profiling preflight creates a manifest, runs WHO retrieval, and records missing country input documentation classes before profile drafting.

Offline structural test:

```bash
python3 skills/country-profiling/scripts/prepare_profile_run.py \
  --country "Romania" \
  --domain "immunization" \
  --dak-scope "WHO immunization DAK" \
  --offline \
  --output-dir /tmp/who-profile-preflight
```

Expected result:

- exit code `0`;
- `profile-preflight-manifest.json` is written;
- `input-documentation-inventory.md` is written;
- WHO retrieval output is written under `who-retrieval/`;
- missing country document classes are listed as gaps.
