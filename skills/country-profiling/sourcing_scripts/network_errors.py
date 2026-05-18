"""Shared network error classification for retrieval scripts."""

from __future__ import annotations

import socket
from typing import Any
from urllib.error import URLError


DNS_ERROR_NUMBERS = {-3, -2, 8}


def _errno(value: Any) -> int | None:
    try:
        return int(getattr(value, "errno"))
    except (TypeError, ValueError):
        return None


def classify_exception(exc: BaseException) -> str:
    """Return a stable retrieval failure category for an exception."""

    reason = getattr(exc, "reason", None)
    candidates = [exc, reason]
    text = f"{exc} {reason}".casefold()

    if any(isinstance(candidate, TimeoutError | socket.timeout) for candidate in candidates):
        return "timeout"
    if any(isinstance(candidate, socket.gaierror) for candidate in candidates):
        return "dns_error"
    if any(_errno(candidate) in DNS_ERROR_NUMBERS for candidate in candidates):
        return "dns_error"
    if "nodename nor servname" in text or "name or service not known" in text:
        return "dns_error"
    if isinstance(exc, URLError):
        return "network_error"
    return "request_error"


def status_for_exception(exc: BaseException) -> str:
    """Map an exception to a retrieval status suitable for artifacts."""

    category = classify_exception(exc)
    if category in {"dns_error", "timeout", "network_error"}:
        return "network_failed"
    return "failed"
