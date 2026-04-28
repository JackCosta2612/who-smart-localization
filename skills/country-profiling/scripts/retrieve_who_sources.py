#!/usr/bin/env python3
"""Generate a WHO source retrieval bundle for Country Profiling.

The script is deliberately conservative: every retrieval failure is captured as
status metadata so the Agent can continue with explicit evidence gaps.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import quote
from urllib.request import Request, urlopen

BASE_GHO_URL = "https://ghoapi.azureedge.net/api"
DEFAULT_OUTPUT_DIR = Path("skills/country-profiling/retrieval-output")

DOMAIN_CONFIG: dict[str, dict[str, Any]] = {
    "immunization": {
        "aliases": ["immunisation", "vaccination", "vaccine"],
        "gho_terms": ["immunization", "vaccination", "vaccine"],
        "dak_sources": [
            {
                "title": "Digital adaptation kit for immunizations",
                "url": "https://www.who.int/publications/i/item/9789240099456",
            }
        ],
    },
    "tuberculosis": {
        "aliases": ["tb"],
        "gho_terms": ["tuberculosis", "TB"],
        "dak_sources": [
            {
                "title": "Digital adaptation kit for tuberculosis",
                "url": "https://www.who.int/publications/i/item/9789240086616",
            }
        ],
    },
    "family planning": {
        "aliases": ["contraception"],
        "gho_terms": ["family planning", "contraception"],
        "dak_sources": [
            {
                "title": "Digital adaptation kit for family planning",
                "url": "https://www.who.int/publications/who-guidelines/9789240029743",
            }
        ],
    },
    "antenatal care": {
        "aliases": ["anc", "pregnancy"],
        "gho_terms": ["antenatal", "pregnancy"],
        "dak_sources": [
            {
                "title": "Digital adaptation kit for antenatal care",
                "url": "https://www.who.int/publications/i/item/9789240020306",
            }
        ],
    },
    "hiv": {
        "aliases": ["human immunodeficiency virus"],
        "gho_terms": ["HIV"],
        "dak_sources": [
            {
                "title": "Digital adaptation kit for HIV",
                "url": "https://www.who.int/publications/i/item/9789240054424",
            }
        ],
    },
}

GENERAL_WHO_SOURCES = [
    {
        "title": "WHO Country Cooperation Strategies",
        "source_type": "WHO country context",
        "url": "https://www.who.int/countries/country-cooperation-strategies",
        "relevance": "Country-level WHO cooperation priorities and strategic context.",
    },
    {
        "title": "WHO Global Health Observatory OData API",
        "source_type": "WHO data API",
        "url": "https://www.who.int/data/gho/info/gho-odata-api",
        "relevance": "Structured WHO indicators and country metadata.",
    },
    {
        "title": "WHO SCORE documents",
        "source_type": "WHO health information system context",
        "url": "https://www.who.int/data/data-collection-tools/score/documents",
        "relevance": "Health information system readiness and data system context.",
    },
    {
        "title": "Global Health Expenditure Database",
        "source_type": "WHO financing data",
        "url": "https://apps.who.int/nha/database/en",
        "relevance": "Comparable health expenditure and financing context.",
    },
    {
        "title": "National Health Workforce Accounts",
        "source_type": "WHO workforce data",
        "url": "https://www.who.int/publications-detail-redirect/national-health-workforce-accounts",
        "relevance": "Health workforce data framework and source class.",
    },
]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "unknown"


def now_utc() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()


def http_json(url: str, timeout: int) -> tuple[str, Any]:
    try:
        request = Request(url, headers={"User-Agent": "who-smart-localization/0.1"})
        with urlopen(request, timeout=timeout) as response:
            return "retrieved", json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        return "failed", {"error": str(exc), "url": url}


def http_check(url: str, timeout: int, offline: bool) -> dict[str, Any]:
    if offline:
        return {"status": "not checked", "url": url, "reason": "offline mode"}
    try:
        request = Request(url, headers={"User-Agent": "who-smart-localization/0.1"})
        with urlopen(request, timeout=timeout) as response:
            content_type = response.headers.get("content-type", "")
            return {
                "status": "reachable",
                "url": response.geturl(),
                "http_status": response.status,
                "content_type": content_type,
            }
    except Exception as exc:
        return {"status": "failed", "url": url, "error": str(exc)}


def normalize_domain(domain: str) -> tuple[str | None, dict[str, Any]]:
    candidate = domain.strip().lower()
    for key, config in DOMAIN_CONFIG.items():
        names = [key, *config.get("aliases", [])]
        if candidate in names:
            return key, config
    return None, {"aliases": [], "gho_terms": [domain], "dak_sources": []}


def find_country(country: str, timeout: int, offline: bool) -> dict[str, Any]:
    if offline:
        return {"status": "not checked", "query": country, "reason": "offline mode"}

    status, data = http_json(f"{BASE_GHO_URL}/DIMENSION/COUNTRY/DimensionValues", timeout)
    if status != "retrieved":
        return {"status": "failed", "query": country, "error": data.get("error")}

    query = country.casefold()
    matches = []
    for row in data.get("value", []):
        title = str(row.get("Title") or row.get("DimensionValue") or "")
        code = str(row.get("Code") or "")
        if query == title.casefold() or query == code.casefold():
            matches.insert(0, {"code": code, "title": title})
        elif query in title.casefold():
            matches.append({"code": code, "title": title})

    return {
        "status": "retrieved",
        "query": country,
        "matches": matches[:10],
        "selected": matches[0] if matches else None,
    }


def search_gho_indicators(terms: list[str], timeout: int, offline: bool) -> list[dict[str, Any]]:
    results = []
    for term in terms:
        if offline:
            results.append({"term": term, "status": "not checked", "reason": "offline mode"})
            continue
        escaped = term.replace("'", "''")
        filter_expr = quote(f"contains(IndicatorName,'{escaped}')", safe="(),'$")
        url = f"{BASE_GHO_URL}/Indicator?$filter={filter_expr}"
        status, data = http_json(url, timeout)
        if status != "retrieved":
            results.append({"term": term, "status": "failed", "error": data.get("error"), "url": url})
            continue
        indicators = [
            {
                "code": row.get("IndicatorCode"),
                "name": row.get("IndicatorName"),
            }
            for row in data.get("value", [])[:10]
        ]
        results.append({"term": term, "status": "retrieved", "url": url, "indicators": indicators})
    return results


def build_source_inventory(
    domain_key: str | None,
    config: dict[str, Any],
    timeout: int,
    offline: bool,
) -> list[dict[str, Any]]:
    sources = []
    for source in config.get("dak_sources", []):
        check = http_check(source["url"], timeout, offline)
        sources.append(
            {
                "title": source["title"],
                "source_type": "WHO DAK",
                "url": source["url"],
                "relevance": "Domain-specific WHO DAK candidate.",
                "retrieval": check,
            }
        )

    if domain_key is None:
        sources.append(
            {
                "title": "Domain-specific DAK not mapped in MVP",
                "source_type": "WHO DAK",
                "url": "",
                "relevance": "Agent should search WHO publications or SMART Implementation Guides manually.",
                "retrieval": {"status": "needs manual search"},
            }
        )

    for source in GENERAL_WHO_SOURCES:
        check = http_check(source["url"], timeout, offline)
        sources.append({**source, "retrieval": check})

    return sources


def markdown_table_row(values: list[str]) -> str:
    escaped = [value.replace("|", "\\|") for value in values]
    return "| " + " | ".join(escaped) + " |"


def write_markdown(bundle: dict[str, Any], path: Path) -> None:
    lines = [
        f"# WHO retrieval bundle: {bundle['country']} - {bundle['domain']}",
        "",
        f"- Generated at: {bundle['generated_at']}",
        f"- Offline mode: {bundle['offline']}",
        f"- Domain mapping: {bundle['domain_key'] or 'not mapped'}",
        "",
        "## Country metadata",
        "",
        f"- Query: {bundle['country_lookup'].get('query')}",
        f"- Status: {bundle['country_lookup'].get('status')}",
        f"- Selected GHO country: {bundle['country_lookup'].get('selected') or 'none'}",
        "",
        "## WHO source inventory",
        "",
        "| Source | Type | URL | Relevance | Retrieval status | Notes |",
        "|---|---|---|---|---|---|",
    ]

    for source in bundle["sources"]:
        retrieval = source["retrieval"]
        note = retrieval.get("error") or retrieval.get("reason") or ""
        lines.append(
            markdown_table_row(
                [
                    source["title"],
                    source["source_type"],
                    source.get("url", ""),
                    source["relevance"],
                    retrieval["status"],
                    str(note),
                ]
            )
        )

    lines.extend(["", "## GHO indicator search", ""])
    for result in bundle["gho_indicator_search"]:
        lines.append(f"### {result['term']}")
        lines.append("")
        lines.append(f"- Status: {result['status']}")
        if result.get("error"):
            lines.append(f"- Error: {result['error']}")
        indicators = result.get("indicators") or []
        if indicators:
            lines.append("")
            lines.append("| Code | Indicator |")
            lines.append("|---|---|")
            for indicator in indicators:
                lines.append(
                    markdown_table_row(
                        [str(indicator.get("code") or ""), str(indicator.get("name") or "")]
                    )
                )
        lines.append("")

    lines.extend(
        [
            "## Country-specific documentation still required",
            "",
            "- National health strategy or health sector plan.",
            "- Domain-specific national programme guideline.",
            "- Digital health or health information system strategy.",
            "- National schedule, formulary, registry, reporting form, or data dictionary relevant to the domain.",
            "",
            "## Use in the profile",
            "",
            "Treat this bundle as a starting inventory. Reachable sources still need content review before they become profile findings. Failed or skipped sources should be preserved as evidence gaps.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_bundle(args: argparse.Namespace) -> dict[str, Any]:
    domain_key, config = normalize_domain(args.domain)
    return {
        "country": args.country,
        "domain": args.domain,
        "domain_key": domain_key,
        "generated_at": now_utc(),
        "offline": args.offline,
        "country_lookup": find_country(args.country, args.timeout, args.offline),
        "sources": build_source_inventory(domain_key, config, args.timeout, args.offline),
        "gho_indicator_search": search_gho_indicators(
            list(config.get("gho_terms", [args.domain])), args.timeout, args.offline
        ),
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Generate a robust WHO source retrieval bundle for Country Profiling."
    )
    parser.add_argument("--country", required=True, help="Country name or GHO country code.")
    parser.add_argument("--domain", required=True, help="Target health domain.")
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory for generated markdown and JSON retrieval bundles.",
    )
    parser.add_argument("--offline", action="store_true", help="Skip live network retrieval.")
    parser.add_argument("--timeout", type=int, default=20, help="Network timeout in seconds.")
    args = parser.parse_args(argv[1:])

    output_dir = Path(args.output_dir)
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        bundle = build_bundle(args)
        stem = f"{slugify(args.country)}-{slugify(args.domain)}-who-retrieval"
        json_path = output_dir / f"{stem}.json"
        md_path = output_dir / f"{stem}.md"
        json_path.write_text(json.dumps(bundle, indent=2, sort_keys=True), encoding="utf-8")
        write_markdown(bundle, md_path)
    except Exception as exc:
        print(f"Error: could not write retrieval bundle: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote retrieval JSON: {json_path}")
    print(f"Wrote retrieval markdown: {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
