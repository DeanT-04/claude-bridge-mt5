"""Bar history with an on-disk cache (runtime/cache) so research doesn't hammer the terminal."""
from __future__ import annotations

from datetime import datetime, timezone

import numpy as np

from bridge import config, mt5_client

CACHE = config.ROOT / "runtime" / "cache"


def bars(symbol: str, timeframe: str, start: datetime | None = None, end: datetime | None = None,
         refresh: bool = False) -> np.ndarray:
    CACHE.mkdir(parents=True, exist_ok=True)
    start = start or datetime.fromisoformat(str(config.settings()["research"]["history_start"]))
    end = end or datetime.now(timezone.utc).replace(tzinfo=None)
    f = CACHE / f"{symbol}_{timeframe}.npy"
    if f.exists() and not refresh:
        cached = np.load(f)
        t0, t1 = _ts(start), _ts(end)
        # Serve from cache when it covers the request (allow 7 days of staleness at the end).
        if len(cached) and cached["time"][0] <= t0 + 7 * 86400 and cached["time"][-1] >= t1 - 7 * 86400:
            return cached[(cached["time"] >= t0) & (cached["time"] < t1)]
    data = mt5_client.get_bars(symbol, timeframe, start, end)
    np.save(f, data)
    return data


def index_at(b: np.ndarray, when: datetime) -> int:
    return int(np.searchsorted(b["time"], _ts(when)))


def _ts(dt: datetime) -> int:
    return int(dt.replace(tzinfo=timezone.utc).timestamp()) if dt.tzinfo is None else int(dt.timestamp())
