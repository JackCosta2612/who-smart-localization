# Test retrieval MVP

Purpose: verify that the predefined WHO retrieval task produces a markdown and JSON bundle without requiring external Python packages.

Offline structural test:

```bash
python3 skills/country-profiling/scripts/retrieve_who_sources.py --country "Romania" --domain "immunization" --offline --output-dir /tmp/who-profile-retrieval
```

Live smoke test:

```bash
python3 skills/country-profiling/scripts/retrieve_who_sources.py --country "Romania" --domain "immunization" --output-dir /tmp/who-profile-retrieval
```

Expected result:

- exit code `0`;
- one `.json` bundle is written;
- one `.md` retrieval report is written;
- failed or unavailable network sources are recorded in the bundle rather than causing an unhandled exception.
