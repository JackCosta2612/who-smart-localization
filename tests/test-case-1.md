# Test case 1

Purpose: verify that the validator accepts a structurally correct localization matrix with allowed controlled values.

Suggested command:

```bash
python3 scripts/validate_matrix.py examples/example-output-1.md
```

Expected result:

- exit code `0`
- message indicating structural validation passed
- reminder that the script does not validate clinical correctness
