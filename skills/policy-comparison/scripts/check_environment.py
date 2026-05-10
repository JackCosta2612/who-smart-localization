#!/usr/bin/env python3
"""Check the runtime environment for optional Country Profiling retrieval scripts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from urllib.request import urlopen

MIN_VERSION = (3, 10)
DEFAULT_OUTPUT_DIR = Path("skills/policy-comparison/retrieval-output")
NETWORK_TEST_URL = "https://www.who.int/"


def check_python() -> tuple[bool, str]:
    current = sys.version_info[:3]
    if current >= MIN_VERSION:
        return True, f"Python version OK: {current[0]}.{current[1]}.{current[2]}"
    return False, (
        "Python version too old: "
        f"{current[0]}.{current[1]}.{current[2]} "
        f"(requires {MIN_VERSION[0]}.{MIN_VERSION[1]}+)"
    )


def check_output_dir(path: Path) -> tuple[bool, str]:
    try:
        path.mkdir(parents=True, exist_ok=True)
        probe = path / ".write-test"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
    except OSError as exc:
        return False, f"Output directory is not writable: {path} ({exc})"
    return True, f"Output directory writable: {path}"


def check_network(timeout: int) -> tuple[bool, str]:
    try:
        with urlopen(NETWORK_TEST_URL, timeout=timeout) as response:
            return True, f"WHO network check OK: HTTP {response.status}"
    except Exception as exc:
        return False, f"WHO network check warning: {exc}"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Check runtime requirements for optional Country Profiling retrieval assistance."
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory that optional retrieval scripts should be able to write to.",
    )
    parser.add_argument(
        "--skip-network",
        action="store_true",
        help="Skip live WHO network reachability check.",
    )
    parser.add_argument("--timeout", type=int, default=10, help="Network timeout in seconds.")
    args = parser.parse_args(argv[1:])

    checks = [check_python(), check_output_dir(Path(args.output_dir))]
    hard_failures = [message for ok, message in checks if not ok]

    for ok, message in checks:
        prefix = "OK" if ok else "ERROR"
        print(f"{prefix}: {message}")

    if args.skip_network:
        print("WARN: Network check skipped.")
    else:
        ok, message = check_network(args.timeout)
        print(("OK" if ok else "WARN") + f": {message}")

    if hard_failures:
        print(
            "Environment check failed for optional retrieval assistance. "
            "Document-only profiling can still be used when sufficient sources are supplied."
        )
        return 1

    print("Environment check passed for optional retrieval assistance.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
