"""Symbol discovery and filtering across everything the broker offers.

For each tradable symbol, from the last ~2 years of H1 bars:
  * history_years   – depth of H1 history available
  * cost_atr        – median spread / median ATR(14) on H1 (round-trip cost in ATR units)
  * minlot_risk_pct – % of the target account (£100) lost by the minimum lot at a 1.5×ATR stop
A symbol is 'researchable' when costs are low enough and history is deep enough, and
'small_account' when its minimum lot also fits the target account's risk cap.
"""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone

import MetaTrader5 as mt5
import numpy as np

from bridge import config, mt5_client
from registry import db

from .engine import atr_sma

DEFAULT_GROUPS = ["Forex", "Metals", "Indices", "Cryptos", "Commodities", "Futures", "Crypto Perpetuals"]
MAX_COST_ATR = 0.15          # spread must be <= 15% of an H1 ATR
MIN_HISTORY_YEARS = 3.0
STOP_ATR = 1.5


def _rate_to_target(acct_ccy: str, target: str) -> float:
    if acct_ccy == target:
        return 1.0
    for sym, inv in ((target + acct_ccy, True), (acct_ccy + target, False)):
        info = mt5.symbol_info(sym)
        if info and info.bid:
            return 1 / info.bid if inv else info.bid
    raise RuntimeError(f"no {acct_ccy}->{target} rate")


def scan(groups: list[str] | None = None, include_equities: bool = False, progress=print) -> list[dict]:
    groups = list(groups or DEFAULT_GROUPS) + (["Equities"] if include_equities else [])
    acc = config.settings()["account"]
    sizing = config.gauntlet()["sizing"]
    out = []
    with mt5_client.session():
        rate = _rate_to_target(mt5.account_info().currency, acc["currency"])
        syms = [s for s in mt5.symbols_get() if s.path.split("\\")[0] in groups
                and s.trade_mode == mt5.SYMBOL_TRADE_MODE_FULL]
        progress(f"scanning {len(syms)} symbols")
        cutoff = int(time.time()) - 730 * 86400
        for k, s in enumerate(syms):
            mt5.symbol_select(s.name, True)
            bars = mt5.copy_rates_from_pos(s.name, mt5.TIMEFRAME_H1, 0, 99999)  # count must be < max bars
            if bars is None or len(bars) < 500:
                continue
            years = (bars["time"][-1] - bars["time"][0]) / (365.25 * 86400)
            recent = bars[bars["time"] >= cutoff]
            if len(recent) < 500:
                continue
            atr = np.nanmedian(atr_sma(recent, 14))
            spread = float(np.median(recent["spread"])) * s.point
            if not atr or atr <= 0:
                continue
            tick_value = s.trade_tick_value_loss or s.trade_tick_value
            loss = STOP_ATR * atr / s.trade_tick_size * tick_value * s.volume_min * rate if s.trade_tick_size else np.inf
            risk_pct = 100 * loss / acc["deposit"]
            row = {
                "symbol": s.name, "group": s.path.split("\\")[0], "path": s.path,
                "history_years": round(float(years), 2), "cost_atr": round(spread / atr, 4),
                "atr_h1": float(atr), "spread_median": spread, "minlot_risk_pct": round(float(risk_pct), 2),
                "volume_min": s.volume_min, "bars_per_day": round(len(recent) / 730 * 7 / 5, 1),
            }
            row["researchable"] = row["cost_atr"] <= MAX_COST_ATR and years >= MIN_HISTORY_YEARS
            row["small_account"] = row["researchable"] and risk_pct <= sizing["max_risk_pct"]
            out.append(row)
            if k % 25 == 0:
                progress(f"  {k}/{len(syms)}")
    out.sort(key=lambda r: (not r["researchable"], not r["small_account"], r["cost_atr"]))
    save(out)
    return out


def save(rows: list[dict], con=None) -> None:
    con = con or db.connect()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    con.executemany("INSERT OR REPLACE INTO universe(symbol, grp, researchable, small_account, metrics, updated) "
                    "VALUES (?,?,?,?,?,?)",
                    [(r["symbol"], r["group"], int(r["researchable"]), int(r["small_account"]),
                      json.dumps(r), now) for r in rows])
    con.commit()


def load(researchable_only: bool = True, small_account_only: bool = False, con=None) -> list[dict]:
    con = con or db.connect()
    q = "SELECT metrics FROM universe WHERE 1=1"
    if researchable_only:
        q += " AND researchable=1"
    if small_account_only:
        q += " AND small_account=1"
    rows = [json.loads(r["metrics"]) for r in con.execute(q)]
    return sorted(rows, key=lambda r: r["cost_atr"])
