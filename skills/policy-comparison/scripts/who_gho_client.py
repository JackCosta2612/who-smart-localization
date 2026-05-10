#!/usr/bin/env python3
"""Small helper for read-only WHO Global Health Observatory API lookups.

This script is intentionally lightweight and uses only the Python standard
library. It is a scaffold for retrieval experiments, not a full data pipeline.
"""

from __future__ import annotations

import argparse
import json
import sys
from urllib.parse import quote
from urllib.request import urlopen

BASE_URL = "https://ghoapi.azureedge.net/api"


def fetch_json(url: str) -> dict:
    with urlopen(url, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def print_json(data: dict) -> None:
    print(json.dumps(data, indent=2, sort_keys=True))


def list_countries() -> int:
    print_json(fetch_json(f"{BASE_URL}/DIMENSION/COUNTRY/DimensionValues"))
    return 0


def search_indicators(query: str) -> int:
    escaped = query.replace("'", "''")
    filter_expr = quote(f"contains(IndicatorName,'{escaped}')", safe="(),'$")
    print_json(fetch_json(f"{BASE_URL}/Indicator?$filter={filter_expr}"))
    return 0


def get_indicator(indicator_code: str, country_code: str | None) -> int:
    url = f"{BASE_URL}/{quote(indicator_code, safe='')}"
    if country_code:
        filter_expr = quote(f"SpatialDim eq '{country_code}'", safe="(),'$")
        url = f"{url}?$filter={filter_expr}"
    print_json(fetch_json(url))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read-only helper for WHO Global Health Observatory OData lookups."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("countries", help="List GHO country dimension values.")

    search = subparsers.add_parser("search-indicators", help="Search indicators by text.")
    search.add_argument("query", help="Text to search in WHO indicator names.")

    indicator = subparsers.add_parser("indicator", help="Fetch data for an indicator code.")
    indicator.add_argument("indicator_code", help="WHO GHO indicator code.")
    indicator.add_argument("--country", help="Optional GHO country code, such as ROU.")

    return parser


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv[1:])

    try:
        if args.command == "countries":
            return list_countries()
        if args.command == "search-indicators":
            return search_indicators(args.query)
        if args.command == "indicator":
            return get_indicator(args.indicator_code, args.country)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
