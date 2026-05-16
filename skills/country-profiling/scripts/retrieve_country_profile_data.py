#!/usr/bin/env python3
"""Retrieve controlled baseline data and source leads for Country Profiling."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
REPO_ROOT = SKILL_DIR.parent.parent
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from data_sources import oecd, source_registry, who_gho, world_bank  # noqa: E402

DEFAULT_OUTPUT_DIR = SKILL_DIR / "retrieval-output" / "country-profile-data"
REGISTRY_PATH = SKILL_DIR / "data_sources" / "indicator_registry.json"


def now_utc() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def markdown_table_row(values: list[Any]) -> str:
    cells = []
    for value in values:
        text = "" if value is None else str(value)
        cells.append(text.replace("|", "\\|").replace("\n", " "))
    return "| " + " | ".join(cells) + " |"


def write_indicators_markdown(bundle: dict[str, Any], path: Path) -> None:
    lines = [
        f"# Retrieved baseline indicators: {bundle['country']} ({bundle['iso3']})",
        "",
        f"- Retrieval date: {bundle['retrieval_date']}",
        f"- Downstream focus: {bundle['focus'] or 'not specified'}",
        f"- Registry: {bundle['registry_path']}",
        "",
        "These indicators provide a small baseline context layer. They do not prove country-profile completeness and must be combined with reviewed country documents, source inventories, and evidence gaps.",
        "",
        "## World Bank indicators",
        "",
        "| Indicator | Code | Value | Unit | Year | Status | Source URL |",
        "|---|---|---|---|---|---|---|",
    ]
    for item in bundle["world_bank_indicators"]:
        lines.append(
            markdown_table_row(
                [
                    item.get("label"),
                    item.get("indicator_code"),
                    item.get("value"),
                    item.get("unit"),
                    item.get("year"),
                    item.get("status"),
                    item.get("url"),
                ]
            )
        )

    lines.extend(
        [
            "",
            "## Retrieval caveats",
            "",
            "- Use precise indicator source, code, year, and retrieval date in profile claims.",
            "- `missing_value` means the configured indicator did not return a non-empty country value.",
            "- `failed` means retrieval failed and should be recorded as an evidence gap.",
            "- WHO GHO and OECD values are not retrieved by this script unless stable source-specific configuration is added later.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_source_leads_markdown(bundle: dict[str, Any], path: Path) -> None:
    lines = [
        f"# Source leads: {bundle['country']} ({bundle['iso3']})",
        "",
        f"- Retrieval date: {bundle['retrieval_date']}",
        f"- Downstream focus: {bundle['focus'] or 'not specified'}",
        "",
        "Source leads are discovery artifacts. Mark a source `Reviewed` only after the actual PDF, dataset, official attachment, official full-text HTML, or local file has been opened and used as evidence.",
        "",
        "## Institutional source leads",
        "",
        "| Title | Publisher | Source type | Date | URL | Relevance | Status |",
        "|---|---|---|---|---|---|---|",
    ]
    for lead in bundle["source_leads"]:
        lines.append(
            markdown_table_row(
                [
                    lead.get("title"),
                    lead.get("publisher"),
                    lead.get("source_type"),
                    lead.get("date"),
                    lead.get("url"),
                    lead.get("relevance"),
                    lead.get("status"),
                ]
            )
        )

    lines.extend(
        [
            "",
            "## WHO GHO / OECD support status",
            "",
            "| Source | Title | Source type | URL | Status | Notes |",
            "|---|---|---|---|---|---|",
        ]
    )
    for lead in [*bundle["who_gho_candidates"], *bundle["oecd_candidates"]]:
        lines.append(
            markdown_table_row(
                [
                    lead.get("source"),
                    lead.get("title"),
                    lead.get("source_type"),
                    lead.get("url"),
                    lead.get("status"),
                    lead.get("notes"),
                ]
            )
        )

    lines.extend(
        [
            "",
            "## Web-assisted fallback note",
            "",
            "If Python scripts are unavailable, use `context/web-assisted-retrieval.md`: follow the approved source priority list, record provenance and status, separate reviewed evidence from candidate leads, and keep inaccessible PDFs or landing-page-only sources as evidence gaps.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_bundle(args: argparse.Namespace) -> dict[str, Any]:
    retrieval_date = now_utc()
    registry = world_bank.load_registry(REGISTRY_PATH)
    world_bank_results = world_bank.fetch_registry_indicators(
        args.iso3,
        registry,
        timeout=args.timeout,
        retrieval_date=retrieval_date,
    )
    who_candidates = who_gho.fetch_configured_indicators(args.country, args.iso3, args.focus)
    oecd_candidates = oecd.source_metadata(args.country, args.iso3, args.focus)
    leads = source_registry.recommended_source_leads(args.country, args.iso3, args.focus)

    return {
        "country": args.country,
        "iso3": args.iso3.upper(),
        "focus": args.focus,
        "retrieval_date": retrieval_date,
        "registry_path": display_path(REGISTRY_PATH),
        "world_bank_indicators": world_bank_results,
        "who_gho_candidates": who_candidates,
        "oecd_candidates": oecd_candidates,
        "source_leads": leads,
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Retrieve a controlled Country Profiling baseline bundle: World Bank indicators, "
            "WHO GHO/OECD candidate metadata, and institutional source leads."
        )
    )
    parser.add_argument("--country", required=True, help="Country name.")
    parser.add_argument("--iso3", required=True, help="ISO3 country code, e.g. ITA.")
    parser.add_argument("--focus", default="", help="Optional downstream focus, e.g. immunization.")
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory for retrieved-indicators.json, retrieved-indicators.md, and source-leads.md.",
    )
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout in seconds.")
    args = parser.parse_args(argv[1:])

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    bundle = build_bundle(args)
    indicators_json = output_dir / "retrieved-indicators.json"
    indicators_md = output_dir / "retrieved-indicators.md"
    source_leads_md = output_dir / "source-leads.md"

    indicators_json.write_text(json.dumps(bundle, indent=2, sort_keys=True), encoding="utf-8")
    write_indicators_markdown(bundle, indicators_md)
    write_source_leads_markdown(bundle, source_leads_md)

    retrieved = sum(1 for item in bundle["world_bank_indicators"] if item.get("status") == "retrieved")
    total = len(bundle["world_bank_indicators"])
    print(f"Wrote {display_path(indicators_json)}")
    print(f"Wrote {display_path(indicators_md)}")
    print(f"Wrote {display_path(source_leads_md)}")
    print(f"World Bank indicators retrieved: {retrieved}/{total}")
    if retrieved < total:
        print("Some indicators were missing or failed; carry them into evidence gaps.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
