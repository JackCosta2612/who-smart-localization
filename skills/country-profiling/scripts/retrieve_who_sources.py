#!/usr/bin/env python3
"""Generate a WHO source retrieval bundle for Country Profiling.

The script is deliberately conservative: every retrieval failure is captured as
status metadata so the Agent can continue with explicit evidence gaps.
"""

from __future__ import annotations

import argparse
import datetime as dt
from html.parser import HTMLParser
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import quote, urljoin, urlparse
from urllib.request import Request, urlopen

BASE_GHO_URL = "https://ghoapi.azureedge.net/api"
DEFAULT_OUTPUT_DIR = Path("skills/country-profiling/retrieval-output")
DEFAULT_FOCUS = "general healthcare overview"
DOCUMENT_EXTENSIONS = {".csv", ".doc", ".docx", ".pdf", ".xls", ".xlsx", ".zip"}
CONTENT_TYPE_EXTENSIONS = {
    "application/pdf": ".pdf",
    "application/vnd.ms-excel": ".xls",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "text/csv": ".csv",
}

FOCUS_CONFIG: dict[str, dict[str, Any]] = {
    "immunization": {
        "aliases": ["immunisation", "vaccination", "vaccine"],
        "gho_terms": ["immunization", "vaccination", "vaccine"],
        "focus_sources": [
            {
                "title": "WHO immunization topic page",
                "url": "https://www.who.int/health-topics/vaccines-and-immunization",
                "evidence_scope": "global-focus-source",
                "download_policy": "download-supported-documents",
            }
        ],
    },
    "tuberculosis": {
        "aliases": ["tb"],
        "gho_terms": ["tuberculosis", "TB"],
        "focus_sources": [
            {
                "title": "WHO tuberculosis topic page",
                "url": "https://www.who.int/health-topics/tuberculosis",
                "evidence_scope": "global-focus-source",
                "download_policy": "download-supported-documents",
            }
        ],
    },
    "family planning": {
        "aliases": ["contraception"],
        "gho_terms": ["family planning", "contraception"],
        "focus_sources": [
            {
                "title": "WHO contraception topic page",
                "url": "https://www.who.int/health-topics/contraception",
                "evidence_scope": "global-focus-source",
                "download_policy": "download-supported-documents",
            }
        ],
    },
    "maternal health": {
        "aliases": ["antenatal care", "anc", "pregnancy"],
        "gho_terms": ["maternal", "antenatal", "pregnancy"],
        "focus_sources": [
            {
                "title": "WHO maternal health topic page",
                "url": "https://www.who.int/health-topics/maternal-health",
                "evidence_scope": "global-focus-source",
                "download_policy": "download-supported-documents",
            }
        ],
    },
    "hiv": {
        "aliases": ["human immunodeficiency virus"],
        "gho_terms": ["HIV"],
        "focus_sources": [
            {
                "title": "WHO HIV topic page",
                "url": "https://www.who.int/health-topics/hiv-aids",
                "evidence_scope": "global-focus-source",
                "download_policy": "download-supported-documents",
            }
        ],
    },
    "wash": {
        "aliases": ["water sanitation hygiene", "sanitation", "hygiene"],
        "gho_terms": ["water", "sanitation", "hygiene"],
        "focus_sources": [
            {
                "title": "WHO water, sanitation and hygiene topic page",
                "url": "https://www.who.int/health-topics/water-sanitation-and-hygiene-wash",
                "evidence_scope": "global-focus-source",
                "download_policy": "download-supported-documents",
            }
        ],
    },
}

GENERAL_WHO_SOURCES = [
    {
        "title": "WHO Country Cooperation Strategies",
        "source_type": "WHO country context",
        "url": "https://www.who.int/countries/country-cooperation-strategies",
        "relevance": "Country-level WHO cooperation priorities and broad health-system context.",
        "evidence_scope": "generic-source-discovery",
        "download_policy": "discover-links-only",
    },
    {
        "title": "WHO Global Health Observatory OData API",
        "source_type": "WHO data API",
        "url": "https://www.who.int/data/gho/info/gho-odata-api",
        "relevance": "Structured WHO indicators and country metadata.",
        "evidence_scope": "generic-source-discovery",
        "download_policy": "discover-links-only",
    },
    {
        "title": "WHO SCORE documents",
        "source_type": "WHO health information system context",
        "url": "https://www.who.int/data/data-collection-tools/score/documents",
        "relevance": "Health information system readiness and data system context.",
        "evidence_scope": "generic-source-discovery",
        "download_policy": "discover-links-only",
    },
    {
        "title": "Global Health Expenditure Database",
        "source_type": "WHO financing data",
        "url": "https://apps.who.int/nha/database/en",
        "relevance": "Comparable health expenditure and financing context.",
        "evidence_scope": "generic-source-discovery",
        "download_policy": "discover-links-only",
    },
    {
        "title": "National Health Workforce Accounts",
        "source_type": "WHO workforce data",
        "url": "https://www.who.int/publications-detail-redirect/national-health-workforce-accounts",
        "relevance": "Health workforce data framework and source class.",
        "evidence_scope": "generic-source-discovery",
        "download_policy": "discover-links-only",
    },
    {
        "title": "WHO water, sanitation and hygiene",
        "source_type": "WHO WASH context",
        "url": "https://www.who.int/health-topics/water-sanitation-and-hygiene-wash",
        "relevance": "Sanitary conditions, drinking water, sanitation, and hygiene source discovery.",
        "evidence_scope": "generic-source-discovery",
        "download_policy": "discover-links-only",
    },
    {
        "title": "WHO air pollution",
        "source_type": "WHO environmental health context",
        "url": "https://www.who.int/health-topics/air-pollution",
        "relevance": "Environmental health and pollution source discovery.",
        "evidence_scope": "generic-source-discovery",
        "download_policy": "discover-links-only",
    },
]


class PageExtractor(HTMLParser):
    """Extract page text and links with standard-library HTML parsing."""

    def __init__(self, base_url: str) -> None:
        super().__init__()
        self.base_url = base_url
        self.links: list[dict[str, str]] = []
        self.text_chunks: list[str] = []
        self.title_chunks: list[str] = []
        self._ignored_depth = 0
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "noscript", "svg"}:
            self._ignored_depth += 1
        if tag == "title":
            self._in_title = True
        if tag == "a":
            attrs_map = {name.lower(): value or "" for name, value in attrs}
            href = attrs_map.get("href", "").strip()
            if href:
                self.links.append(
                    {
                        "url": urljoin(self.base_url, href),
                        "text": " ".join(attrs_map.get("title", "").split()),
                    }
                )

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "noscript", "svg"} and self._ignored_depth:
            self._ignored_depth -= 1
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        text = " ".join(data.split())
        if not text or self._ignored_depth:
            return
        if self._in_title:
            self.title_chunks.append(text)
        self.text_chunks.append(text)

    def summary(self, max_chars: int) -> dict[str, Any]:
        seen = set()
        unique_links = []
        for link in self.links:
            url = link["url"]
            if url in seen:
                continue
            seen.add(url)
            unique_links.append(link)
        return {
            "title": " ".join(self.title_chunks).strip(),
            "text": "\n".join(self.text_chunks)[:max_chars],
            "links": unique_links,
        }


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


def fetch_response_bytes(url: str, timeout: int, max_bytes: int) -> tuple[dict[str, Any], bytes]:
    request = Request(url, headers={"User-Agent": "who-smart-localization/0.1"})
    with urlopen(request, timeout=timeout) as response:
        content_length = response.headers.get("content-length")
        if content_length and int(content_length) > max_bytes:
            metadata = {
                "status": "skipped",
                "url": response.geturl(),
                "http_status": response.status,
                "content_type": response.headers.get("content-type", ""),
                "reason": f"content-length exceeds max bytes ({max_bytes})",
            }
            return metadata, b""
        data = response.read(max_bytes + 1)
        if len(data) > max_bytes:
            metadata = {
                "status": "skipped",
                "url": response.geturl(),
                "http_status": response.status,
                "content_type": response.headers.get("content-type", ""),
                "reason": f"response exceeds max bytes ({max_bytes})",
            }
            return metadata, b""
        metadata = {
            "status": "retrieved",
            "url": response.geturl(),
            "http_status": response.status,
            "content_type": response.headers.get("content-type", ""),
            "bytes": len(data),
        }
        return metadata, data


def decode_text(data: bytes, content_type: str) -> str:
    match = re.search(r"charset=([^;]+)", content_type, flags=re.IGNORECASE)
    encodings = [match.group(1).strip()] if match else []
    encodings.extend(["utf-8", "latin-1"])
    for encoding in encodings:
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def is_download_link(url: str) -> bool:
    parsed = urlparse(url)
    suffix = Path(parsed.path).suffix.lower()
    if suffix in DOCUMENT_EXTENSIONS:
        return True
    return "iris.who.int" in parsed.netloc and "/bitstreams/" in parsed.path and parsed.path.endswith("/content")


def suffix_for_download(url: str, content_type: str) -> str:
    parsed = urlparse(url)
    suffix = Path(parsed.path).suffix
    if suffix:
        return suffix
    normalized_content_type = content_type.split(";")[0].strip().lower()
    return CONTENT_TYPE_EXTENSIONS.get(normalized_content_type, ".bin")


def save_download(
    url: str,
    content_dir: Path,
    timeout: int,
    max_bytes: int,
) -> dict[str, Any]:
    try:
        metadata, data = fetch_response_bytes(url, timeout, max_bytes)
        if metadata["status"] != "retrieved":
            return metadata
        parsed = urlparse(metadata["url"])
        suffix = suffix_for_download(metadata["url"], metadata.get("content_type", ""))
        name_source = Path(parsed.path).stem
        if not name_source or name_source == "content":
            parts = [part for part in parsed.path.split("/") if part and part != "content"]
            name_source = parts[-1] if parts else "download"
        path = content_dir / f"{slugify(name_source)}{suffix}"
        path.write_bytes(data)
        return {**metadata, "local_path": str(path)}
    except Exception as exc:
        return {"status": "failed", "url": url, "error": str(exc)}


def retrieve_source_content(
    source: dict[str, Any],
    content_dir: Path,
    timeout: int,
    offline: bool,
    max_page_bytes: int,
    max_text_chars: int,
    max_download_bytes: int,
    download_documents: bool,
) -> dict[str, Any]:
    url = source.get("url", "")
    if not url:
        return {"status": "not available", "reason": "source has no URL"}
    if offline:
        return {"status": "not checked", "reason": "offline mode", "url": url}

    content_dir.mkdir(parents=True, exist_ok=True)
    try:
        metadata, data = fetch_response_bytes(url, timeout, max_page_bytes)
        if metadata["status"] != "retrieved":
            return metadata

        content_type = metadata.get("content_type", "")
        stem = slugify(source["title"])
        if "html" not in content_type.lower():
            suffix = Path(urlparse(metadata["url"]).path).suffix or ".bin"
            path = content_dir / f"{stem}{suffix}"
            path.write_bytes(data)
            return {**metadata, "content_kind": "downloaded-file", "local_path": str(path)}

        html = decode_text(data, content_type)
        extractor = PageExtractor(metadata["url"])
        extractor.feed(html)
        page = extractor.summary(max_text_chars)

        text_path = content_dir / f"{stem}.txt"
        links_path = content_dir / f"{stem}-links.json"
        text_path.write_text(page["text"] + "\n", encoding="utf-8")
        links_path.write_text(json.dumps(page["links"], indent=2, sort_keys=True), encoding="utf-8")

        download_links = [link["url"] for link in page["links"] if is_download_link(link["url"])]
        downloads = []
        source_download_policy = source.get("download_policy", "discover-links-only")
        if download_documents and source_download_policy == "download-supported-documents":
            for link in download_links[:5]:
                downloads.append(save_download(link, content_dir, timeout, max_download_bytes))

        return {
            **metadata,
            "content_kind": "html-text-snapshot",
            "title": page["title"],
            "local_text_path": str(text_path),
            "local_links_path": str(links_path),
            "text_chars": len(page["text"]),
            "download_links_found": download_links[:20],
            "download_policy": source_download_policy,
            "downloads": downloads,
        }
    except Exception as exc:
        return {"status": "failed", "url": url, "error": str(exc)}


def normalize_focus(focus: str) -> tuple[str | None, dict[str, Any]]:
    candidate = focus.strip().lower()
    for key, config in FOCUS_CONFIG.items():
        names = [key, *config.get("aliases", [])]
        if candidate in names:
            return key, config
    if candidate and candidate != "general healthcare overview":
        return None, {"aliases": [], "gho_terms": [focus], "focus_sources": []}
    return None, {
        "aliases": [],
        "gho_terms": [
            "life expectancy",
            "mortality",
            "universal health coverage",
            "health expenditure",
            "health workforce",
            "water",
            "sanitation",
        ],
        "focus_sources": [],
    }


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


def fetch_gho_country_data(
    indicator_results: list[dict[str, Any]],
    country_lookup: dict[str, Any],
    content_dir: Path,
    timeout: int,
    offline: bool,
    max_datasets: int,
) -> list[dict[str, Any]]:
    selected = country_lookup.get("selected") or {}
    country_code = selected.get("code")
    if not country_code:
        return [
            {
                "status": "skipped",
                "reason": "no GHO country code selected",
            }
        ]
    if offline:
        return [{"status": "not checked", "reason": "offline mode", "country_code": country_code}]

    content_dir.mkdir(parents=True, exist_ok=True)
    datasets = []
    seen_codes = set()
    for result in indicator_results:
        for indicator in result.get("indicators", []):
            code = indicator.get("code")
            if not code or code in seen_codes:
                continue
            seen_codes.add(code)
            filter_expr = quote(f"SpatialDim eq '{country_code}'", safe="(),'$")
            url = f"{BASE_GHO_URL}/{quote(code, safe='')}?$filter={filter_expr}"
            status, data = http_json(url, timeout)
            path = content_dir / f"gho-{slugify(country_code)}-{slugify(code)}.json"
            if status == "retrieved":
                path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
                rows = len(data.get("value", [])) if isinstance(data, dict) else 0
                datasets.append(
                    {
                        "status": "retrieved" if rows else "retrieved_empty",
                        "indicator_code": code,
                        "indicator_name": indicator.get("name"),
                        "country_code": country_code,
                        "url": url,
                        "local_path": str(path),
                        "rows": rows,
                    }
                )
            else:
                datasets.append(
                    {
                        "status": "failed",
                        "indicator_code": code,
                        "country_code": country_code,
                        "url": url,
                        "error": data.get("error"),
                    }
                )
            if len(datasets) >= max_datasets:
                return datasets
    return datasets


def build_source_inventory(
    focus_key: str | None,
    config: dict[str, Any],
    timeout: int,
    offline: bool,
) -> list[dict[str, Any]]:
    sources = []
    for source in config.get("focus_sources", []):
        check = http_check(source["url"], timeout, offline)
        sources.append(
            {
                "title": source["title"],
                "source_type": "WHO focus source",
                "url": source["url"],
                "relevance": "Topic-specific WHO source candidate.",
                "evidence_scope": source.get("evidence_scope", "global-focus-source"),
                "download_policy": source.get("download_policy", "download-supported-documents"),
                "retrieval": check,
            }
        )

    if focus_key is None and config.get("focus_sources") == []:
        sources.append(
            {
                "title": "Focus-specific WHO source not mapped in retrieval helper",
                "source_type": "WHO focus source",
                "url": "",
                "relevance": "Agent should search WHO, regional observatory, or public-health sources manually if the focus is important.",
                "evidence_scope": "unresolved-source-discovery",
                "download_policy": "discover-links-only",
                "retrieval": {"status": "needs manual search"},
            }
        )

    for source in GENERAL_WHO_SOURCES:
        check = http_check(source["url"], timeout, offline)
        sources.append({**source, "retrieval": check})

    return sources


def attach_source_contents(
    sources: list[dict[str, Any]],
    content_dir: Path,
    args: argparse.Namespace,
) -> list[dict[str, Any]]:
    enriched = []
    for source in sources:
        content = retrieve_source_content(
            source,
            content_dir,
            args.timeout,
            args.offline,
            args.max_page_bytes,
            args.max_text_chars,
            args.max_download_bytes,
            not args.no_download_documents,
        )
        enriched.append({**source, "content": content})
    return enriched


def markdown_table_row(values: list[str]) -> str:
    escaped = [value.replace("|", "\\|") for value in values]
    return "| " + " | ".join(escaped) + " |"


def write_markdown(bundle: dict[str, Any], path: Path) -> None:
    lines = [
        f"# WHO retrieval bundle: {bundle['country']} - {bundle['focus']}",
        "",
        f"- Generated at: {bundle['generated_at']}",
        f"- Offline mode: {bundle['offline']}",
        f"- Focus mapping: {bundle['focus_key'] or 'not mapped'}",
        "",
        "## Country metadata",
        "",
        f"- Query: {bundle['country_lookup'].get('query')}",
        f"- Status: {bundle['country_lookup'].get('status')}",
        f"- Selected GHO country: {bundle['country_lookup'].get('selected') or 'none'}",
        "",
        "## WHO source inventory",
        "",
        "| Source | Type | Evidence scope | URL | Relevance | URL status | Content status | Local content | Notes |",
        "|---|---|---|---|---|---|---|---|---|",
    ]

    for source in bundle["sources"]:
        retrieval = source["retrieval"]
        content = source.get("content", {})
        note = content.get("error") or retrieval.get("error") or content.get("reason") or retrieval.get("reason") or ""
        local_content = (
            content.get("local_text_path")
            or content.get("local_path")
            or ""
        )
        lines.append(
            markdown_table_row(
                [
                    source["title"],
                    source["source_type"],
                    source.get("evidence_scope", ""),
                    source.get("url", ""),
                    source["relevance"],
                    retrieval["status"],
                    content.get("status", "not checked"),
                    local_content,
                    str(note),
                ]
            )
        )

    lines.extend(["", "## Downloaded or discovered documents", ""])
    for source in bundle["sources"]:
        content = source.get("content", {})
        download_links = content.get("download_links_found") or []
        downloads = content.get("downloads") or []
        lines.append(f"### {source['title']}")
        lines.append("")
        lines.append(f"- Text snapshot: {content.get('local_text_path') or 'none'}")
        lines.append(f"- Link inventory: {content.get('local_links_path') or 'none'}")
        lines.append(f"- Evidence scope: {source.get('evidence_scope', 'unknown')}")
        lines.append(f"- Download policy: {content.get('download_policy') or source.get('download_policy', 'unknown')}")
        lines.append(f"- Download links found: {len(download_links)}")
        if downloads:
            lines.append("")
            lines.append("| URL | Status | Local path | Notes |")
            lines.append("|---|---|---|---|")
            for download in downloads:
                lines.append(
                    markdown_table_row(
                        [
                            download.get("url", ""),
                            download.get("status", ""),
                            download.get("local_path", ""),
                            download.get("error") or download.get("reason") or "",
                        ]
                    )
                )
        lines.append("")

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

    lines.extend(["## GHO country data samples", ""])
    for dataset in bundle.get("gho_country_data_samples", []):
        lines.append(
            f"- {dataset.get('indicator_code', 'n/a')}: {dataset.get('status')} "
            f"({dataset.get('rows', 0)} rows) {dataset.get('local_path', '')}"
        )
    lines.append("")

    lines.extend(
        [
            "## Country-specific documentation still required",
            "",
            "- Country health profile or national health strategy.",
            "- Burden-of-disease, mortality, surveillance, census, or survey source.",
            "- Health financing, UHC, insurance, expenditure, or financial protection source.",
            "- WASH, sanitary conditions, or environmental health source.",
            "- Health workforce, facility-capacity, or service-availability source.",
            "- Digital health, health information system, CRVS, or surveillance-system source.",
            "",
            "## Use in the profile",
            "",
            "Treat this bundle as a starting inventory. Reachable sources still need content review before they become profile findings. Failed or skipped sources should be preserved as evidence gaps.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_bundle(args: argparse.Namespace) -> dict[str, Any]:
    focus_key, config = normalize_focus(args.focus)
    content_dir = Path(args.output_dir) / "content"
    country_lookup = find_country(args.country, args.timeout, args.offline)
    indicator_search = search_gho_indicators(
        list(config.get("gho_terms", [args.focus])), args.timeout, args.offline
    )
    sources = build_source_inventory(focus_key, config, args.timeout, args.offline)
    sources = attach_source_contents(sources, content_dir, args)
    return {
        "country": args.country,
        "focus": args.focus,
        "focus_key": focus_key,
        "generated_at": now_utc(),
        "offline": args.offline,
        "content_dir": str(content_dir),
        "country_lookup": country_lookup,
        "sources": sources,
        "gho_indicator_search": indicator_search,
        "gho_country_data_samples": fetch_gho_country_data(
            indicator_search,
            country_lookup,
            content_dir,
            args.timeout,
            args.offline,
            args.max_gho_datasets,
        ),
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Generate a robust WHO source retrieval bundle for Country Profiling."
    )
    parser.add_argument("--country", required=True, help="Country name or GHO country code.")
    parser.add_argument(
        "--focus",
        default=DEFAULT_FOCUS,
        help="Optional health focus, region, population group, or downstream use.",
    )
    parser.add_argument(
        "--domain",
        dest="legacy_domain",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory for generated markdown and JSON retrieval bundles.",
    )
    parser.add_argument("--offline", action="store_true", help="Skip live network retrieval.")
    parser.add_argument("--timeout", type=int, default=20, help="Network timeout in seconds.")
    parser.add_argument(
        "--max-page-bytes",
        type=int,
        default=2_000_000,
        help="Maximum bytes to read from an HTML/source page.",
    )
    parser.add_argument(
        "--max-text-chars",
        type=int,
        default=80_000,
        help="Maximum extracted text characters to save per source page.",
    )
    parser.add_argument(
        "--max-download-bytes",
        type=int,
        default=15_000_000,
        help="Maximum bytes for each discovered downloadable document.",
    )
    parser.add_argument(
        "--max-gho-datasets",
        type=int,
        default=5,
        help="Maximum country-filtered GHO indicator datasets to fetch.",
    )
    parser.add_argument(
        "--no-download-documents",
        action="store_true",
        help="Discover downloadable document links but do not download them.",
    )
    args = parser.parse_args(argv[1:])
    if args.legacy_domain and args.focus == DEFAULT_FOCUS:
        args.focus = args.legacy_domain

    output_dir = Path(args.output_dir)
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        bundle = build_bundle(args)
        stem = f"{slugify(args.country)}-{slugify(args.focus)}-who-retrieval"
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
