"""Rate-limit de login fallido (in-memory; portable fuera de nginx)."""

from __future__ import annotations

import time
from collections import defaultdict
from threading import Lock

_MAX_PER_IDENTITY = 5
_MAX_PER_IP = 20
_WINDOW_SEC = 15 * 60
_DELAY_AFTER = 3
_DELAY_CAP = 8.0

_lock = Lock()
_by_key: dict[str, list[float]] = defaultdict(list)
_by_ip: dict[str, list[float]] = defaultdict(list)


def _prune(bucket: list[float], now: float) -> list[float]:
    return [t for t in bucket if now - t < _WINDOW_SEC]


def is_locked(ip: str, email: str | None) -> tuple[bool, int]:
    """Return (locked, retry_after_seconds)."""
    now = time.time()
    email_n = (email or "").strip().lower()
    with _lock:
        ip_hits = _prune(_by_ip[ip], now)
        _by_ip[ip] = ip_hits
        if len(ip_hits) >= _MAX_PER_IP:
            oldest = min(ip_hits) if ip_hits else now
            return True, max(1, int(_WINDOW_SEC - (now - oldest)))
        if email_n:
            key = f"{ip}|{email_n}"
            hits = _prune(_by_key[key], now)
            _by_key[key] = hits
            if len(hits) >= _MAX_PER_IDENTITY:
                oldest = min(hits)
                return True, max(1, int(_WINDOW_SEC - (now - oldest)))
    return False, 0


def record_failure(ip: str, email: str | None) -> float:
    """Record failure; return seconds to sleep before responding."""
    now = time.time()
    email_n = (email or "").strip().lower()
    with _lock:
        _by_ip[ip] = _prune(_by_ip[ip], now) + [now]
        delay = 0.0
        if email_n:
            key = f"{ip}|{email_n}"
            hits = _prune(_by_key[key], now) + [now]
            _by_key[key] = hits
            if len(hits) >= _DELAY_AFTER:
                delay = min(_DELAY_CAP, float(len(hits) - _DELAY_AFTER + 1))
        return delay


def record_success(ip: str, email: str | None) -> None:
    email_n = (email or "").strip().lower()
    with _lock:
        if email_n:
            _by_key.pop(f"{ip}|{email_n}", None)
