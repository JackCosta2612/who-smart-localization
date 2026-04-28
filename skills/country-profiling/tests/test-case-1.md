# Test case 1

Purpose: verify that the Country Profiling validator accepts a structurally complete profile using controlled values.

Suggested command:

```bash
python3 skills/country-profiling/scripts/validate_profile.py skills/country-profiling/examples/example-output-1.md
```

Expected result:

- exit code `0`;
- message indicating structural validation passed;
- reminder that the validator does not check policy or clinical correctness.
