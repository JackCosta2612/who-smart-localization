#!/usr/bin/env python3
"""Prepare optional support artifacts for a country healthcare profile run.

This helper checks runtime readiness, runs optional WHO source retrieval, and
writes an input documentation inventory. It supports mixed retrieval workflows
but is not required for document-only profiling from user-supplied sources.
"""

from __future__ import annotations

import argparse
import datetime as dt
from html.parser import HTMLParser
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

DEFAULT_OUTPUT_DIR = Path("skills/country-profiling/profile-runs")
DEFAULT_FOCUS = "general healthcare overview"
DOCUMENT_EXTENSIONS = {".csv", ".doc", ".docx", ".pdf", ".xls", ".xlsx", ".zip"}
DOCUMENT_CONTENT_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/csv",
}
OFFICIAL_HTML_MATERIAL_PATTERNS = (
    "gazzettaufficiale.it/atto/serie_generale/caricaArticolo",
    "trovanorme.salute.gov.it/norme/dettaglioAtto",
)
REQUIRED_COUNTRY_DOCUMENT_CLASSES = [
    {
        "label": "Country health profile or national health strategy",
        "match_terms": ["country health profile", "national health strategy", "health system review", "health system summary"],
    },
    {
        "label": "Burden-of-disease, mortality, surveillance, census, or survey source",
        "match_terms": ["burden", "mortality", "surveillance", "census", "survey", "health statistics"],
    },
    {
        "label": "Health financing, UHC, insurance, expenditure, or financial protection source",
        "match_terms": ["financing", "uhc", "insurance", "expenditure", "financial protection"],
    },
    {
        "label": "WASH, sanitary conditions, or environmental health source",
        "match_terms": ["wash", "sanitary", "sanitation", "water", "environment", "environmental health", "climate"],
    },
    {
        "label": "Health workforce, facility-capacity, or service-availability source",
        "match_terms": ["workforce", "facility", "capacity", "service availability", "infrastructure"],
    },
    {
        "label": "Digital health, health information system, CRVS, or surveillance-system source",
        "match_terms": ["digital health", "health information", "crvs", "surveillance system", "electronic health"],
    },
]


class LinkExtractor(HTMLParser):
    """Collect links from an HTML source page."""

    def __init__(self, base_url: str) -> None:
        super().__init__()
        self.base_url = base_url
        self.links: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        attrs_map = {name.lower(): value or "" for name, value in attrs}
        href = attrs_map.get("href", "").strip()
        if not href:
            return
        text = " ".join(
            part
            for part in [
                attrs_map.get("title", "").strip(),
                attrs_map.get("aria-label", "").strip(),
            ]
            if part
        )
        self.links.append({"url": urljoin(self.base_url, href), "text": text})


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


def is_url(location: str) -> bool:
    parsed = urlparse(location)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def is_document_url(url: str) -> bool:
    parsed = urlparse(url)
    suffix = Path(parsed.path).suffix.lower()
    if suffix in DOCUMENT_EXTENSIONS:
        return True
    return "iris.who.int" in parsed.netloc and "/bitstreams/" in parsed.path and parsed.path.endswith("/content")


def is_official_html_material(url: str) -> bool:
    return any(pattern in url for pattern in OFFICIAL_HTML_MATERIAL_PATTERNS)


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


def classify_source_endpoint(
    location: str,
    *,
    offline: bool,
    timeout: int,
    max_bytes: int,
) -> dict[str, object]:
    if not location or location == "Not supplied":
        return {
            "status": "not supplied",
            "endpoint_type": "missing",
            "material_endpoint": "",
            "requires_follow_up": True,
            "note": "No source location was supplied.",
        }
    if not is_url(location):
        return {
            "status": "not checked",
            "endpoint_type": "local-or-non-url",
            "material_endpoint": location,
            "requires_follow_up": False,
            "note": "Local files must still be opened and reviewed before use as evidence.",
        }
    if offline:
        return {
            "status": "not checked",
            "endpoint_type": "url-not-checked",
            "material_endpoint": location if is_document_url(location) else "",
            "requires_follow_up": not is_document_url(location),
            "note": "Offline mode skipped endpoint resolution.",
        }

    try:
        request = Request(location, headers={"User-Agent": "who-smart-localization/0.1"})
        with urlopen(request, timeout=timeout) as response:
            final_url = response.geturl()
            content_type = response.headers.get("content-type", "")
            content_length = response.headers.get("content-length")
            if content_length and int(content_length) > max_bytes and "html" in content_type.lower():
                return {
                    "status": "skipped",
                    "endpoint_type": "html-too-large",
                    "url": final_url,
                    "content_type": content_type,
                    "material_endpoint": "",
                    "requires_follow_up": True,
                    "note": f"HTML page exceeds max bytes ({max_bytes}); resolve source material manually.",
                }
            data = response.read(max_bytes + 1)
    except Exception as exc:
        return {
            "status": "failed",
            "endpoint_type": "unresolved",
            "url": location,
            "material_endpoint": "",
            "requires_follow_up": True,
            "note": str(exc),
        }

    normalized_content_type = content_type.split(";")[0].strip().lower()
    if is_document_url(final_url) or normalized_content_type in DOCUMENT_CONTENT_TYPES:
        return {
            "status": "reachable",
            "endpoint_type": "direct-source-material",
            "url": final_url,
            "content_type": content_type,
            "material_endpoint": final_url,
            "requires_follow_up": False,
            "note": "Supplied URL resolves to downloadable source material.",
        }
    if is_official_html_material(final_url):
        return {
            "status": "reachable",
            "endpoint_type": "official-html-source-material",
            "url": final_url,
            "content_type": content_type,
            "material_endpoint": final_url,
            "requires_follow_up": False,
            "note": "Supplied URL resolves to official full-text or attachment HTML.",
        }
    if "html" not in content_type.lower():
        return {
            "status": "reachable",
            "endpoint_type": "unknown-file",
            "url": final_url,
            "content_type": content_type,
            "material_endpoint": final_url,
            "requires_follow_up": False,
            "note": "Supplied URL resolves to non-HTML content; review before use as evidence.",
        }

    html = decode_text(data[:max_bytes], content_type)
    extractor = LinkExtractor(final_url)
    extractor.feed(html)
    seen: set[str] = set()
    material_links = []
    for link in extractor.links:
        url = link["url"]
        if url in seen:
            continue
        if is_document_url(url) or is_official_html_material(url):
            material_links.append(link)
            seen.add(url)

    first_material = material_links[0]["url"] if material_links else ""
    return {
        "status": "reachable",
        "endpoint_type": "landing-page-or-index",
        "url": final_url,
        "content_type": content_type,
        "material_endpoint": first_material,
        "candidate_material_links": material_links[:10],
        "requires_follow_up": True,
        "note": (
            "Resolve and review the linked source material before marking this source Reviewed."
            if first_material
            else "No direct downloadable or official full-text material link was detected."
        ),
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
    for item in supplied:
        item["endpoint_resolution"] = classify_source_endpoint(
            item["location"],
            offline=args.offline,
            timeout=args.source_timeout,
            max_bytes=args.max_source_page_bytes,
        )
    supplied_types = {item["document_type"].casefold() for item in supplied}
    gaps = []

    for required in REQUIRED_COUNTRY_DOCUMENT_CLASSES:
        match_terms = [term.casefold() for term in required["match_terms"]]
        if not any(term in supplied_type for term in match_terms for supplied_type in supplied_types):
            gaps.append(
                {
                    "required_document_class": required["label"],
                    "status": "Needs retrieval",
                    "reason": "No matching country-specific document was supplied to the preparation run.",
                }
            )

    return {
        "country": args.country,
        "focus": args.focus,
        "supplied_country_documents": supplied,
        "missing_country_document_classes": gaps,
    }


def write_input_inventory_markdown(inventory: dict[str, object], path: Path) -> None:
    lines = [
        f"# Input documentation inventory: {inventory['country']} - {inventory['focus']}",
        "",
        f"- Optional downstream health-area focus: {inventory['focus']}",
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
            "## Supplied source endpoint resolution",
            "",
            "| Title | Endpoint type | Material endpoint | Follow-up required | Note |",
            "|---|---|---|---|---|",
        ]
    )
    if supplied:
        for item in supplied:
            resolution = item.get("endpoint_resolution", {})
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(item["title"]),
                        str(resolution.get("endpoint_type", "")),
                        str(resolution.get("material_endpoint", "")),
                        str(resolution.get("requires_follow_up", "")),
                        str(resolution.get("note", "")).replace("|", "\\|"),
                    ]
                )
                + " |"
            )
    else:
        lines.append("| No country documents supplied | missing |  | True | No source endpoint to resolve. |")

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
            "Do not infer country-specific health conditions, coverage, sanitary conditions, or policy readiness from generic WHO/global sources. Missing country documents should remain evidence gaps or human-review actions in the profile.",
            "",
            "A landing page, catalog page, search result, or download page is not by itself reviewed source material. Resolve it to the PDF, dataset, official attachment, or official full-text HTML before citing it as reviewed evidence.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Prepare optional source-inventory and WHO discovery support artifacts for Country Profiling."
    )
    parser.add_argument("--country", required=True, help="Country name or GHO country code.")
    parser.add_argument(
        "--focus",
        default=DEFAULT_FOCUS,
        help="Optional downstream health-area focus, region, population group, or downstream use.",
    )
    parser.add_argument(
        "--domain",
        dest="legacy_domain",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--dak-scope",
        dest="legacy_dak_scope",
        help=argparse.SUPPRESS,
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
    parser.add_argument(
        "--source-timeout",
        type=int,
        default=20,
        help="Network timeout in seconds for checking supplied country-document URLs.",
    )
    parser.add_argument(
        "--max-source-page-bytes",
        type=int,
        default=2_000_000,
        help="Maximum bytes to inspect when resolving supplied country-document landing pages.",
    )
    args = parser.parse_args(argv[1:])
    if args.legacy_domain and args.focus == DEFAULT_FOCUS:
        args.focus = args.legacy_domain

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    run_slug = f"{slugify(args.country)}-{slugify(args.focus)}"
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
        "--focus",
        args.focus,
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
        "focus": args.focus,
        "legacy_dak_scope": args.legacy_dak_scope,
        "run_dir": str(run_dir),
        "environment_gate": environment,
        "who_retrieval_gate": retrieval,
        "input_documentation_inventory": inventory,
        "input_inventory_path": str(inventory_path),
        "retrieval_assistance_complete": bool(environment["ok"] and retrieval["ok"]),
        "may_draft_profile": may_draft_from_manifest,
        "mode_guidance": mode_guidance,
        "drafting_constraints": [
            "Do not produce country-specific health, sanitary, coverage, or policy-readiness findings from missing documents.",
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
