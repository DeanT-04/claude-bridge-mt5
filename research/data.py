"""Bar history with an on-disk cache (runtime/cache) so research doesn't hammer the terminal."""
from __future__ import annotations

import json
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
    meta = f.with_suffix(".json")
    t0, t1 = _ts(start), _ts(end)
    if f.exists() and meta.exists() and not refresh:
        m = json.loads(meta.read_text())
        # Cache covers the request if it was fetched from at least as early (history may simply
        # start later) and is at most 7 days stale at the end.
        if m["requested_from"] <= t0 and m["fetched_to"] >= t1 - 7 * 86400:
            cached = np.load(f)
            return cached[(cached["time"] >= t0) & (cached["time"] < t1)]
    data = mt5_client.get_bars(symbol, timeframe, start, end)
    np.save(f, data)
    meta.write_text(json.dumps({"requested_from": t0, "fetched_to": t1}))
    return data


def spec(symbol: str, refresh: bool = False) -> dict:
    """Contract spec, cached on disk so research workers never need the MT5 connection."""
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / "specs.json"
    specs = json.loads(f.read_text()) if f.exists() else {}
    if refresh or symbol not in specs:
        specs[symbol] = mt5_client.symbol_spec(symbol)
        f.write_text(json.dumps(specs, indent=1))
    return specs[symbol]


def index_at(b: np.ndarray, when: datetime) -> int:
    return int(np.searchsorted(b["time"], _ts(when)))


def _ts(dt: datetime) -> int:
    return int(dt.replace(tzinfo=timezone.utc).timestamp()) if dt.tzinfo is None else int(dt.timestamp())
