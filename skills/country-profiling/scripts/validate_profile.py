#!/usr/bin/env python3
"""Validate the structure of a Country Profiling markdown output.

This validator checks format and controlled values only. It does not assess
epidemiological, policy, country, legal, WASH, or WHO interpretation correctness.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "# Country healthcare profile:",
    "## Profile metadata",
    "## Executive summary",
    "## Source inventory",
    "## Country context snapshot",
    "## Population health overview",
    "## Main health issues and burden",
    "## Health system organization and capacity",
    "## Healthcare access and coverage",
    "## Sanitary conditions and environmental health",
    "## Health financing and affordability",
    "## Health workforce, infrastructure, and supply availability",
    "## Digital health and health information systems",
    "## Equity, vulnerable groups, and regional variation",
    "## Current concerns, risks, and watchpoints",
    "## Policy-analysis readiness",
    "## Evidence gaps and expert input needed",
    "## Sources",
]

SOURCE_COLUMNS = [
    "Source",
    "Source type",
    "Publisher",
    "Date",
    "URL or file path",
    "Relevance",
    "Status",
]

GAP_COLUMNS = [
    "Gap or uncertainty",
    "Why it matters",
    "Suggested next source or action",
    "Review owner",
]

HANDOFF_COLUMNS = [
    "Downstream need",
    "Why it matters",
    "Available evidence",
    "Missing source or uncertainty",
    "Suggested next action",
]

ALLOWED_SOURCE_STATUS = {
    "Reviewed",
    "Candidate source",
    "Needs retrieval",
    "Needs expert validation",
    "Not available in supplied material",
}


def parse_markdown_row(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return []
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def find_table(lines: list[str], columns: list[str]) -> int | None:
    for index, line in enumerate(lines):
        if parse_markdown_row(line) == columns:
            return index
    return None


def separator_is_valid(line: str, expected_columns: int) -> bool:
    cells = parse_markdown_row(line)
    return len(cells) == expected_columns and all(
        cell and set(cell) <= {"-", ":"} for cell in cells
    )


def table_rows(lines: list[str], header_index: int) -> list[tuple[int, list[str]]]:
    rows: list[tuple[int, list[str]]] = []
    for line_number, line in enumerate(lines[header_index + 2 :], start=header_index + 3):
        if not line.strip():
            break
        row = parse_markdown_row(line)
        if not row:
            break
        rows.append((line_number, row))
    return rows


def validate_table(
    lines: list[str],
    columns: list[str],
    table_name: str,
    *,
    require_rows: bool = False,
) -> tuple[list[str], list[tuple[int, list[str]]]]:
    errors: list[str] = []
    header_index = find_table(lines, columns)
    if header_index is None:
        return [f"{table_name} table header was not found."], []

    if header_index + 1 >= len(lines) or not separator_is_valid(
        lines[header_index + 1], len(columns)
    ):
        errors.append(f"{table_name} table separator row is missing or malformed.")
        return errors, []

    rows = table_rows(lines, header_index)
    if require_rows and not rows:
        errors.append(f"{table_name} table has no data rows.")
    return errors, rows


def section_exists(content: str, heading: str) -> bool:
    return heading in content


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate the markdown structure of a Country Profiling output. "
            "This does not validate epidemiological, policy, country, legal, WASH, or WHO correctness."
        )
    )
    parser.add_argument("markdown_file", help="Country profile markdown file to validate.")
    args = parser.parse_args(argv[1:])

    target = Path(args.markdown_file)
    if not target.is_file():
        print(f"Error: file not found: {target}")
        print(
            "Note: this validator checks structure only, not epidemiological, policy, country, legal, WASH, or WHO correctness."
        )
        return 1

    content = target.read_text(encoding="utf-8")
    lines = content.splitlines()
    errors: list[str] = []

    for section in REQUIRED_SECTIONS:
        if section not in content:
            errors.append(f"Required section missing: {section}")

    source_errors, source_rows = validate_table(lines, SOURCE_COLUMNS, "Source inventory")
    errors.extend(source_errors)
    for line_number, row in source_rows:
        if len(row) != len(SOURCE_COLUMNS):
            errors.append(f"Line {line_number}: source row has {len(row)} columns.")
            continue
        if row[6] not in ALLOWED_SOURCE_STATUS:
            errors.append(f"Line {line_number}: invalid source Status '{row[6]}'.")

    gap_errors, _gap_rows = validate_table(
        lines, GAP_COLUMNS, "Evidence gaps and expert input needed"
    )
    errors.extend(gap_errors)

    if section_exists(content, "## Policy-comparison handoff"):
        handoff_errors, _handoff_rows = validate_table(
            lines, HANDOFF_COLUMNS, "Policy-comparison handoff"
        )
        errors.extend(handoff_errors)

    if errors:
        print("Structural validation failed:")
        for error in errors:
            print(f"- {error}")
        print(
            "Note: this validator checks structure only, not epidemiological, policy, country, legal, WASH, or WHO correctness."
        )
        return 1

    print(f"Structural validation passed for {target}.")
    print(
        "Note: this validator checks structure only, not epidemiological, policy, country, legal, WASH, or WHO correctness."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
