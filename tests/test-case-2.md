# Test case 2

Purpose: verify that the validator rejects a malformed or non-compliant matrix.

Suggested manual checks:

1. Copy `examples/example-output-1.md` to a temporary file.
2. Change `Medium` to an invalid confidence value such as `Certain`.
3. Run the validator on the modified file.

Suggested command:

```bash
python3 scripts/validate_matrix.py /path/to/modified-example.md
```

Expected result:

- non-zero exit code
- clear error about the invalid `Confidence` value
- reminder that the script checks structure only
