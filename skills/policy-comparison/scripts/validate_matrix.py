#!/usr/bin/env python3
"""Validate the structure of a localization matrix in a markdown file.

This script performs structural validation only. It does not assess clinical,
policy, terminology, or alignment correctness.
"""

from __future__ import annotations

import sys
from pathlib import Path

REQUIRED_COLUMNS = [
    "WHO source statement",
    "Local policy statement",
    "Alignment status",
    "Difference type",
    "Explanation",
    "Evidence from WHO source",
    "Evidence from local source",
    "Confidence",
    "Human review action",
]

ALLOWED_ALIGNMENT_STATUSES = {
    "Aligned",
    "Partially aligned",
    "Divergent",
    "Missing in local policy",
    "More specific in local policy",
    "More restrictive in local policy",
    "Unclear or requires expert review",
}

ALLOWED_CONFIDENCE = {"High", "Medium", "Low"}

ALLOWED_REVIEW_ACTIONS = {
    "No action needed",
    "Confirm interpretation",
    "Check missing local evidence",
    "Resolve divergence",
    "Validate terminology mapping",
    "Escalate to clinical or policy expert",
}


def parse_markdown_row(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return []
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def find_matrix(lines: list[str]) -> tuple[int, list[str]] | None:
    for index, line in enumerate(lines):
        row = parse_markdown_row(line)
        if row == REQUIRED_COLUMNS:
            return index, row
    return None


def separator_is_valid(line: str, expected_columns: int) -> bool:
    cells = parse_markdown_row(line)
    if len(cells) != expected_columns:
        return False
    return all(cell and set(cell) <= {"-", ":"} for cell in cells)


def validate_rows(lines: list[str], start_index: int) -> list[str]:
    errors: list[str] = []
    data_row_count = 0

    for line_number, line in enumerate(lines[start_index + 2 :], start=start_index + 3):
        if not line.strip():
            if data_row_count:
                break
            continue

        row = parse_markdown_row(line)
        if not row:
            if data_row_count:
                break
            continue

        if len(row) != len(REQUIRED_COLUMNS):
            errors.append(
                f"Line {line_number}: expected {len(REQUIRED_COLUMNS)} columns, found {len(row)}."
            )
            continue

        data_row_count += 1
        alignment_status = row[2]
        confidence = row[7]
        review_action = row[8]

        if alignment_status not in ALLOWED_ALIGNMENT_STATUSES:
            errors.append(
                f"Line {line_number}: invalid Alignment status '{alignment_status}'."
            )

        if confidence not in ALLOWED_CONFIDENCE:
            errors.append(f"Line {line_number}: invalid Confidence '{confidence}'.")

        if review_action not in ALLOWED_REVIEW_ACTIONS:
            errors.append(
                f"Line {line_number}: invalid Human review action '{review_action}'."
            )

    if data_row_count == 0:
        errors.append("No localization matrix data rows found after the header.")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(
            "Usage: python3 skills/policy-comparison/scripts/validate_matrix.py <markdown-file>"
        )
        print("Note: this validator checks structure only, not clinical correctness.")
        return 2

    target = Path(argv[1])
    if not target.is_file():
        print(f"Error: file not found: {target}")
        print("Note: this validator checks structure only, not clinical correctness.")
        return 1

    lines = target.read_text(encoding="utf-8").splitlines()
    matrix = find_matrix(lines)
    if matrix is None:
        print("Error: required localization matrix header was not found.")
        print("Note: this validator checks structure only, not clinical correctness.")
        return 1

    header_index, _header = matrix
    if header_index + 1 >= len(lines) or not separator_is_valid(
        lines[header_index + 1], len(REQUIRED_COLUMNS)
    ):
        print("Error: markdown separator row is missing or malformed.")
        print("Note: this validator checks structure only, not clinical correctness.")
        return 1

    errors = validate_rows(lines, header_index)
    if errors:
        print("Structural validation failed:")
        for error in errors:
            print(f"- {error}")
        print("Note: this validator checks structure only, not clinical correctness.")
        return 1

    print(f"Structural validation passed for {target}.")
    print("Note: this validator checks structure only, not clinical correctness.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
