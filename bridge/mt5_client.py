"""Read-side access to the BlackBull terminal via the MetaTrader5 package.

Deliberately exposes no order-sending functions: trading goes through the
approval-gated deployment flow (M3), never ad hoc.
"""
from __future__ import annotations

import threading
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone

import MetaTrader5 as mt5
import numpy as np

from . import config

TIMEFRAMES = {
    "M1": mt5.TIMEFRAME_M1, "M5": mt5.TIMEFRAME_M5, "M15": mt5.TIMEFRAME_M15,
    "M30": mt5.TIMEFRAME_M30, "H1": mt5.TIMEFRAME_H1, "H4": mt5.TIMEFRAME_H4,
    "D1": mt5.TIMEFRAME_D1,
}

_lock = threading.Lock()


class MT5Error(RuntimeError):
    pass


@contextmanager
def session(target: str = "demo"):
    """Connect to the demo or live terminal. The MT5 package holds one global connection, so
    access is serialised. Market data always comes from the demo terminal (the default)."""
    exe, portable = config.target_terminal(target)
    with _lock:
        if not mt5.initialize(path=str(exe), portable=portable):
            raise MT5Error(f"initialize {target} terminal failed: {mt5.last_error()}")
        try:
            yield mt5
        finally:
            mt5.shutdown()


def account_info(target: str = "demo") -> dict:
    with session(target):
        a = mt5.account_info()
        if a is None:
            raise MT5Error(f"account_info: {mt5.last_error()}")
        d = a._asdict()
        d["is_demo"] = a.trade_mode == mt5.ACCOUNT_TRADE_MODE_DEMO
        return {k: d[k] for k in ("login", "server", "is_demo", "currency", "leverage",
                                  "balance", "equity", "margin_free", "company")}


def _spec(s) -> dict:
    return {
        "name": s.name, "path": s.path, "group": s.path.split("\\")[0],
        "description": s.description, "digits": s.digits, "point": s.point,
        "spread": s.spread, "spread_float": s.spread_float,
        "contract_size": s.trade_contract_size, "tick_size": s.trade_tick_size,
        "tick_value": s.trade_tick_value, "volume_min": s.volume_min,
        "volume_step": s.volume_step, "volume_max": s.volume_max,
        "swap_long": s.swap_long, "swap_short": s.swap_short,
        "currency_profit": s.currency_profit, "currency_margin": s.currency_margin,
        "trade_mode": s.trade_mode, "bid": s.bid, "ask": s.ask,
    }


def list_symbols(group: str | None = None) -> list[dict]:
    with session():
        syms = mt5.symbols_get() or ()
        out = [_spec(s) for s in syms]
    if group:
        out = [s for s in out if s["group"].lower() == group.lower()]
    return out


def symbol_spec(name: str) -> dict:
    with session():
        mt5.symbol_select(name, True)
        s = mt5.symbol_info(name)
        if s is None:
            raise MT5Error(f"unknown symbol {name!r}")
        return _spec(s)


def get_bars(symbol: str, timeframe: str, start: datetime, end: datetime) -> np.ndarray:
    """Structured array with fields time, open, high, low, close, tick_volume, spread, real_volume."""
    tf = TIMEFRAMES[timeframe]
    start, end = _utc(start), _utc(end)
    # The terminal rejects requests spanning more than its "max bars" setting, so page through time.
    step = _CHUNK.get(timeframe, timedelta(days=365))
    parts = []
    with session():
        mt5.symbol_select(symbol, True)
        t = start
        while t < end:
            u = min(t + step, end)
            rates = mt5.copy_rates_range(symbol, tf, t, u)
            if rates is None:
                code, msg = mt5.last_error()
                raise MT5Error(f"copy_rates_range {symbol} {timeframe} {t:%Y-%m-%d}: {code} {msg}")
            if len(rates):
                parts.append(rates)
            t = u
    if not parts:
        return np.zeros(0, dtype=[("time", "<i8")])
    out = np.concatenate(parts)
    _, idx = np.unique(out["time"], return_index=True)
    return out[idx]


_CHUNK = {"M1": timedelta(days=60), "M5": timedelta(days=300)}


def _utc(dt: datetime) -> datetime:
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
