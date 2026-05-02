#!/usr/bin/env python3
"""Prepare optional support artifacts for a country profile run.

This helper checks runtime readiness, runs optional WHO source retrieval, and
writes an input documentation inventory. It supports retrieval-assisted mode
but is not required for document-only profiling from user-supplied sources.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

DEFAULT_OUTPUT_DIR = Path("skills/country-profiling/profile-runs")
REQUIRED_COUNTRY_DOCUMENT_CLASSES = [
    "National health strategy or health sector plan",
    "Domain-specific national programme guideline",
    "Digital health or health information system strategy",
    "Relevant schedule, formulary, registry, reporting form, or data dictionary",
]


def now_utc() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()


def slugify(value: str) -> str:
    cleaned = "".join(char.lower() if char.isalnum() else "-" for char in value)
    return "-".join(part for part in cleaned.split("-") if part) or "unknown"


def run_command(command: list[str]) -> dict[str, object]:
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "ok": completed.returncode == 0,
    }


def parse_country_document(raw: str) -> dict[str, str]:
    parts = [part.strip() for part in raw.split("|")]
    while len(parts) < 4:
        parts.append("")
    title, document_type, location, date = parts[:4]
    return {
        "title": title or "Untitled country document",
        "document_type": document_type or "Unspecified",
        "location": location or "Not supplied",
        "date": date or "Unknown",
        "status": "Supplied" if location else "Needs retrieval",
    }


def build_input_inventory(args: argparse.Namespace) -> dict[str, object]:
    supplied = [parse_country_document(item) for item in args.country_document]
    supplied_types = {item["document_type"].casefold() for item in supplied}
    gaps = []

    for required in REQUIRED_COUNTRY_DOCUMENT_CLASSES:
        if not any(required.casefold() in supplied_type for supplied_type in supplied_types):
            gaps.append(
                {
                    "required_document_class": required,
                    "status": "Needs retrieval",
                    "reason": "No matching country-specific document was supplied to the preparation run.",
                }
            )

    return {
        "country": args.country,
        "domain": args.domain,
        "dak_scope": args.dak_scope,
        "supplied_country_documents": supplied,
        "missing_country_document_classes": gaps,
    }


def write_input_inventory_markdown(inventory: dict[str, object], path: Path) -> None:
    lines = [
        f"# Input documentation inventory: {inventory['country']} - {inventory['domain']}",
        "",
        f"- DAK or WHO scope: {inventory['dak_scope']}",
        "",
        "## Supplied country documents",
        "",
        "| Title | Type | Location | Date | Status |",
        "|---|---|---|---|---|",
    ]

    supplied = inventory["supplied_country_documents"]
    if supplied:
        for item in supplied:
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(item["title"]),
                        str(item["document_type"]),
                        str(item["location"]),
                        str(item["date"]),
                        str(item["status"]),
                    ]
                )
                + " |"
            )
    else:
        lines.append("| No country documents supplied |  |  |  | Needs retrieval |")

    lines.extend(
        [
            "",
            "## Missing country document classes",
            "",
            "| Required document class | Status | Reason |",
            "|---|---|---|",
        ]
    )
    for gap in inventory["missing_country_document_classes"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(gap["required_document_class"]),
                    str(gap["status"]),
                    str(gap["reason"]),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Profiling rule",
            "",
            "Do not infer country-specific policy from WHO/global sources. Missing country documents should remain evidence gaps or human-review actions in the profile.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Prepare optional retrieval-assisted support artifacts for Country Profiling."
    )
    parser.add_argument("--country", required=True, help="Country name or GHO country code.")
    parser.add_argument("--domain", required=True, help="Target health domain.")
    parser.add_argument(
        "--dak-scope",
        required=True,
        help="DAK, WHO guideline, or SMART artifact scope for the profile.",
    )
    parser.add_argument(
        "--country-document",
        action="append",
        default=[],
        help=(
            "Country document in 'title|document type|path-or-url|date' format. "
            "May be repeated."
        ),
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory for the preparation manifest and optional retrieval bundle.",
    )
    parser.add_argument("--offline", action="store_true", help="Run retrieval in offline mode.")
    args = parser.parse_args(argv[1:])

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    run_slug = f"{slugify(args.country)}-{slugify(args.domain)}"
    run_dir = output_dir / run_slug
    retrieval_dir = run_dir / "who-retrieval"
    run_dir.mkdir(parents=True, exist_ok=True)

    env_command = [
        sys.executable,
        "skills/country-profiling/scripts/check_environment.py",
        "--output-dir",
        str(retrieval_dir),
    ]
    if args.offline:
        env_command.append("--skip-network")

    retrieval_command = [
        sys.executable,
        "skills/country-profiling/scripts/retrieve_who_sources.py",
        "--country",
        args.country,
        "--domain",
        args.domain,
        "--output-dir",
        str(retrieval_dir),
    ]
    if args.offline:
        retrieval_command.append("--offline")

    environment = run_command(env_command)
    retrieval = run_command(retrieval_command) if environment["ok"] else {
        "command": retrieval_command,
        "returncode": None,
        "stdout": "",
        "stderr": "Skipped because the optional script environment check failed.",
        "ok": False,
    }

    inventory = build_input_inventory(args)
    supplied_country_documents = inventory["supplied_country_documents"]
    has_supplied_country_documents = bool(supplied_country_documents)
    inventory_path = run_dir / "input-documentation-inventory.md"
    write_input_inventory_markdown(inventory, inventory_path)

    may_draft_from_manifest = has_supplied_country_documents
    if not may_draft_from_manifest:
        mode_guidance = (
            "The manifest does not include a reviewed country-specific source. "
            "Draft only a skeleton/gap-analysis profile unless the prompt, attached files, "
            "or conversation context provide sufficient country-specific source material."
        )
    elif retrieval["ok"]:
        mode_guidance = (
            "Retrieval-assisted artifacts and supplied country documents are available. "
            "Draft only source-backed content and keep missing document classes as gaps."
        )
    else:
        mode_guidance = (
            "Proceed in document-only mode from supplied country documents if they are relevant "
            "and sufficient. Treat retrieval failure as an evidence gap, not as a profile blocker."
        )

    manifest = {
        "generated_at": now_utc(),
        "country": args.country,
        "domain": args.domain,
        "dak_scope": args.dak_scope,
        "run_dir": str(run_dir),
        "environment_gate": environment,
        "who_retrieval_gate": retrieval,
        "input_documentation_inventory": inventory,
        "input_inventory_path": str(inventory_path),
        "retrieval_assistance_complete": bool(environment["ok"] and retrieval["ok"]),
        "may_draft_profile": may_draft_from_manifest,
        "mode_guidance": mode_guidance,
        "drafting_constraints": [
            "Do not produce country-specific findings from missing documents.",
            "Carry missing country document classes into evidence gaps.",
            "Use any WHO retrieval bundle as source evidence, not as final interpretation.",
            "If this script fails but user-provided sources are sufficient, document-only mode may still proceed.",
        ],
    }

    manifest_path = run_dir / "profile-preflight-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")

    print(f"Wrote preparation manifest: {manifest_path}")
    print(f"Wrote input documentation inventory: {inventory_path}")
    print(f"WHO retrieval output directory: {retrieval_dir}")

    if not environment["ok"]:
        print(
            "Preparation script environment check failed. Retrieval-assisted artifacts may be unavailable, "
            "but document-only mode can still be used if sufficient sources are supplied outside this script."
        )
        return 1

    if not retrieval["ok"]:
        print(
            "WHO retrieval assistance did not complete. Continue in document-only mode if sufficient "
            "user-provided sources are available; otherwise record retrieval as an evidence gap."
        )

    if not manifest["may_draft_profile"]:
        print(
            "No country-specific documents were supplied to this preparation run. Draft only a skeleton "
            "or gap-analysis profile unless other supplied sources are available in the prompt, files, or context."
        )
        return 0

    if inventory["missing_country_document_classes"]:
        print("Preparation completed with country-document gaps that should be carried into the profile.")
    else:
        print("Preparation completed with supplied country documentation inventory.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
