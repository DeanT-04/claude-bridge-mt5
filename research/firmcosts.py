"""Per-firm execution costs (plan P2): what a strategy's trades cost at each prop firm, built on
BlackBull's bar spreads.

  spread     = BlackBull bar spread x the firm/BlackBull spread ratio (from snapshots of the
               firm's published live spreads, config/spread_snapshots.jsonl)
  commission = the firm's round-trip commission (config/firmcosts.yaml): flat USD per lot,
               converted to price units with BlackBull's tick value, or % of the entry price

A symbol the firm doesn't list returns None: that firm's programs aren't evaluated for it.
"""
from __future__ import annotations

import json
from functools import lru_cache

import numpy as np
import yaml

from bridge import config

from .engine import Costs

# Firm symbol codes whose BlackBull name differs (after dropping "/", ".cash", ".c").
ALIASES = {"US100": "NAS100", "NDX100": "NAS100", "USTEC": "NAS100", "US500": "SPX500",
           "DJI30": "US30", "GER30": "GER40", "DE40": "GER40", "JP225": "JPN225",
           "EU50": "ESTX50", "EUSTX50": "ESTX50", "STX50": "ESTX50", "SPN35": "ESP35",
           "FTSE100": "UK100", "UKOIL": "BRENT", "UKOUSD": "BRENT", "USOIL": "WTI", "USOUSD": "WTI",
           "DOGUSD": "DOGEUSD", "AVAUSD": "AVAXUSD", "LNKUSD": "LINKUSD"}
PUBLISHED = ("FTMO", "FundedNext", "FundingPips")    # firms whose symbol lists are public
METALS = ("XAU", "XAG", "XPT", "XPD", "XCU")
RATIO_CLAMP = (0.05, 5.0)


@lru_cache
def firms() -> dict:
    return yaml.safe_load((config.CONFIG_DIR / "firmcosts.yaml").read_text(encoding="utf-8"))


@lru_cache
def snapshots() -> list[dict]:
    f = config.CONFIG_DIR / "spread_snapshots.jsonl"
    if not f.exists():
        return []
    return [json.loads(ln) for ln in f.read_text(encoding="utf-8").splitlines() if ln.strip()]


def normalize(code: str) -> str:
    s = code.upper().replace("/", "")
    for suf in (".CASH", ".C"):
        s = s.removesuffix(suf)
    return ALIASES.get(s, s)


def asset_class(symbol: str, spec: dict | None = None) -> str | None:
    """Forex | Metals | Energies | Indices | Crypto, or None for BlackBull-only products
    (futures CFDs '.f', alternative pricing 'p' symbols)."""
    group = (spec or {}).get("group") or _group(symbol)
    if symbol.endswith(".f") or group == "Futures" or (symbol.endswith("p") and symbol[:-1].isupper()):
        return None
    if group == "Forex":
        return "Forex"
    if group in ("Cryptos", "Crypto Perpetuals"):
        return "Crypto"
    if group == "Indices":
        return "Indices"
    if group == "Commodities":
        return "Metals" if symbol.startswith(METALS) else "Energies"
    return None


def _group(symbol: str) -> str:
    from research import data
    try:
        return data.spec(symbol).get("group", "")
    except Exception:
        return ""


@lru_cache
def symbol_set(firm: str) -> frozenset:
    """BlackBull names the firm lists. Unpublished lists: symbols at least two public lists share."""
    f = firms()[firm]
    if f.get("symbols"):
        return frozenset(normalize(s) for s in f["symbols"])
    counts: dict[str, int] = {}
    for other in PUBLISHED:
        for s in symbol_set(other):
            counts[s] = counts.get(s, 0) + 1
    return frozenset(s for s, n in counts.items() if n >= 2)


def offered(firm: str, symbol: str, spec: dict | None = None) -> bool:
    return asset_class(symbol, spec) is not None and symbol in symbol_set(firm)


def spread_ratio(firm: str, symbol: str, cls: str) -> tuple[float, str]:
    """(firm spread / BlackBull spread, where it came from)."""
    f = firms()[firm]
    if cls in f.get("spread_only_classes", []):
        return 1.0, "spread-only pricing (assumed like BlackBull)"
    snaps = [r for r in snapshots() if r["bb_spread"] > 0]

    def med(rows):
        return float(np.clip(np.median([r["firm_spread"] / r["bb_spread"] for r in rows]), *RATIO_CLAMP))

    own = [r for r in snaps if r["firm"] == firm and r["symbol"] == symbol]
    if own:
        return med(own), f"{len(own)} snapshot(s)"
    same_class = [r for r in snaps if r["firm"] == firm and asset_class(r["symbol"]) == cls]
    if same_class:
        return med(same_class), f"{firm} {cls} median"
    raw = [r for r in snaps if firms()[r["firm"]].get("pricing") == "raw" and asset_class(r["symbol"]) == cls]
    if raw:
        return med(raw), f"raw-spread firms' {cls} median"
    return 1.0, "no data (BlackBull spread)"


def commission(firm: str, cls: str) -> dict:
    return firms()[firm]["commission_rt"].get(cls, {})


def costs(firm: str, symbol: str, spec: dict, spread_mult: float = 1.0, slip: float = 0.0) -> Costs | None:
    """Engine costs for trading `symbol` at `firm` (None if the firm doesn't list it)."""
    cls = asset_class(symbol, spec)
    if cls is None or not offered(firm, symbol, spec):
        return None
    ratio, _ = spread_ratio(firm, symbol, cls)
    c = commission(firm, cls)
    value_per_price = spec["tick_value"] / spec["tick_size"] if spec.get("tick_size") else 0.0
    comm_price = c.get("usd", 0.0) / value_per_price if value_per_price else 0.0
    return Costs(point=spec["point"], spread_mult=ratio * spread_mult, slippage_points=slip,
                 commission_price=comm_price, commission_rate=c.get("pct", 0.0) / 100,
                 min_spread_points=float(spec.get("spread", 0)))


def describe(symbol: str, spec: dict) -> dict:
    """Per-firm cost summary for a symbol, in BlackBull points (for reports and the MCP)."""
    out = {}
    cls = asset_class(symbol, spec)
    for firm in firms():
        c = costs(firm, symbol, spec)
        if c is None:
            out[firm] = {"offered": False}
            continue
        ratio, src = spread_ratio(firm, symbol, cls)
        price = float(spec.get("bid") or 0)
        comm_pts = (c.commission_price + c.commission_rate * price) / spec["point"]
        out[firm] = {"offered": True, "class": cls, "spread_ratio": round(ratio, 3), "spread_source": src,
                     "spread_points": round(float(spec.get("spread", 0)) * ratio, 1),
                     "commission_points": round(comm_pts, 1),
                     "total_points": round(float(spec.get("spread", 0)) * ratio + comm_pts, 1),
                     "blackbull_points": float(spec.get("spread", 0))}
    return out


def record_snapshot(firm: str, spreads: dict[str, float], source: str = "published live spread table") -> dict:
    """Append a firm's published live spreads (firm symbol code -> spread in price units, read
    from its public spread table) to config/spread_snapshots.jsonl, each paired with BlackBull's
    live spread taken now. Take snapshots at different sessions (London, New York) so the
    ratios aren't driven by one quiet hour."""
    from datetime import datetime, timezone
    import MetaTrader5 as mt5
    from bridge import mt5_client
    if firm not in firms():
        raise ValueError(f"unknown firm {firm!r}; one of {list(firms())}")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rows, skipped = [], []
    with mt5_client.session():
        for code, sp in spreads.items():
            sym = normalize(code)
            mt5.symbol_select(sym, True)
            tick = mt5.symbol_info_tick(sym)
            if tick is None or tick.ask <= tick.bid or sp is None:
                skipped.append(code)
                continue
            rows.append({"time": now, "bb_time": now, "firm": firm, "symbol": sym, "firm_spread": float(sp),
                         "bb_spread": round(tick.ask - tick.bid, 8), "source": source})
    with open(config.CONFIG_DIR / "spread_snapshots.jsonl", "a", encoding="utf-8") as fh:
        fh.writelines(json.dumps(r) + "\n" for r in rows)
    snapshots.cache_clear()
    return {"recorded": len(rows), "skipped": skipped}
