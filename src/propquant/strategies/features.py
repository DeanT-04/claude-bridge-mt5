"""Causal session-level features for 1m bars (times in minutes since midnight ET).

Every per-session value documents WHEN it becomes known; strategies may only act on bars at or
after that minute. Bars are labelled by their open time: the bar at minute 599 closes at 10:00.
The lookahead tests re-verify every strategy built on these helpers.
"""

import numpy as np

from propquant.engine.backtest import MarketData

RTH_OPEN, RTH_LAST = 570, 959  # 09:30 bar ... 15:59 bar (closes 16:00)


def n_sessions(md: MarketData) -> int:
    return len(md.sess_start) - 1


def at_minute(md: MarketData, values: np.ndarray, minute: int) -> np.ndarray:
    """Per-session value of ``values`` on the bar at ``minute`` (NaN if that bar is missing).
    Known at the close of that bar."""
    out = np.full(n_sessions(md), np.nan)
    idx = np.flatnonzero(md.minute == minute)
    out[md.sess[idx]] = values[idx]
    return out


def window_high_low(md: MarketData, m0: int, m1: int) -> tuple[np.ndarray, np.ndarray]:
    """Per-session high/low of bars with m0 <= minute < m1. Known at the close of bar m1-1."""
    k = n_sessions(md)
    hi, lo = np.full(k, -np.inf), np.full(k, np.inf)
    idx = np.flatnonzero((md.minute >= m0) & (md.minute < m1))
    np.maximum.at(hi, md.sess[idx], md.high[idx])
    np.minimum.at(lo, md.sess[idx], md.low[idx])
    hi[~np.isfinite(hi)] = np.nan
    lo[~np.isfinite(lo)] = np.nan
    return hi, lo


def prev(x: np.ndarray, k: int = 1) -> np.ndarray:
    """Value from k sessions earlier (known before today starts)."""
    out = np.full_like(x, np.nan, dtype=np.float64)
    out[k:] = x[:-k]
    return out


def rolling_mean_prev(x: np.ndarray, n: int) -> np.ndarray:
    """Mean of the previous n sessions (excludes today), ignoring NaNs."""
    out = np.full(len(x), np.nan)
    for i in range(n, len(x)):
        w = x[i - n : i]
        w = w[~np.isnan(w)]
        if len(w) >= max(2, n // 2):
            out[i] = w.mean()
    return out


def last_bar_before(md: MarketData, minute: int) -> np.ndarray:
    """True on each session's last bar that opens before clock `minute` (RTH-side minutes),
    so an exit signal there fills at the first bar opening at/after `minute`."""
    ok = (md.minute < minute) & (md.minute >= 0) & (md.minute < 1080)
    nxt = np.r_[md.minute[1:], -1]
    same = np.r_[md.sess[1:] == md.sess[:-1], False]
    return ok & (~same | (nxt >= minute) | (nxt >= 1080))


def to_bars(md: MarketData, per_session: np.ndarray) -> np.ndarray:
    """Broadcast a per-session array to every bar of that session."""
    return per_session[md.sess]


def last_in_window(md: MarketData, values: np.ndarray, m0: int, m1: int) -> np.ndarray:
    """Per-session value on the LAST bar with m0 <= minute < m1 (handles half-day closes).
    Known at the close of that bar."""
    out = np.full(n_sessions(md), np.nan)
    idx = np.flatnonzero((md.minute >= m0) & (md.minute < m1))
    out[md.sess[idx]] = values[idx]  # later bars overwrite earlier ones
    return out


def ffill(x: np.ndarray) -> np.ndarray:
    """Carry the last known value forward (never backward: leading NaNs stay NaN)."""
    out = x.astype(np.float64).copy()
    for i in range(1, len(out)):
        if np.isnan(out[i]):
            out[i] = out[i - 1]
    return out


def rth_daily(md: MarketData) -> dict[str, np.ndarray]:
    """Regular-session open/close/high/low per session.
    open: known at the 09:30 bar open; close/high/low: known at the session's last RTH bar
    (15:59, or 12:59 on half days)."""
    hi, lo = window_high_low(md, RTH_OPEN, RTH_LAST + 1)
    return {
        "open": at_minute(md, md.open, RTH_OPEN),
        "close": last_in_window(md, md.close, RTH_OPEN, RTH_LAST + 1),
        "high": hi,
        "low": lo,
    }


def atr_prev(md: MarketData, n: int = 14) -> np.ndarray:
    """Average RTH range of the previous n sessions (known before today)."""
    d = rth_daily(md)
    return rolling_mean_prev(d["high"] - d["low"], n)
