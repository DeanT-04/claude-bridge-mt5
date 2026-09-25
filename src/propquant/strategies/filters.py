"""Regime filters: per-session booleans known BEFORE the session opens (18:00 ET the day before),
except where a filter states otherwise (overnight filters are known at 09:29 ET and may only
gate entries at/after 09:30).

`filtered(base, name)` makes a registered strategy that only opens positions on sessions the
filter allows; exits are untouched. Each filtered variant is its own pre-registered idea and
its own trials.
"""

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
import polars as pl

from propquant.engine.backtest import MarketData, Orders
from propquant.strategies import features as F
from propquant.strategies import indicators as ind
from propquant.strategies.base import REGISTRY, Strategy


def _pct_rank_prev(x: np.ndarray, n: int) -> np.ndarray:
    """Percentile of today's (already-lagged) value within the previous n values."""
    out = np.full(len(x), np.nan)
    for i in range(n, len(x)):
        w = x[i - n : i]
        w = w[~np.isnan(w)]
        if len(w) >= n // 2 and not np.isnan(x[i]):
            out[i] = (w < x[i]).mean()
    return out


def daily_close_prev(md: MarketData) -> np.ndarray:
    """Previous regular-session close per session (known before the session)."""
    return F.prev(F.rth_daily(md)["close"])


def vix_prev(md: MarketData) -> np.ndarray:
    """Latest VIX close strictly before each session date (Yahoo ^VIX, daily)."""
    from propquant.data import yfin

    try:
        v = yfin.load("VIX", "1d")
    except FileNotFoundError:
        return np.full(len(md.sess_day), np.nan)
    days = v["ts"].dt.convert_time_zone("America/New_York").dt.date().cast(pl.Int64).to_numpy()
    closes = v["close"].to_numpy()
    idx = np.searchsorted(days, md.sess_day, side="left") - 1  # strictly earlier date
    out = np.where(idx >= 0, closes[np.clip(idx, 0, None)], np.nan)
    return out.astype(np.float64)


@dataclass(frozen=True)
class Filter:
    name: str
    known: str  # when the mask is known
    rationale: str
    fn: Callable[[MarketData], np.ndarray]


def _vol_rank(md):
    return _pct_rank_prev(F.atr_prev(md, 14), 252)


def _on_valid(fn, x: np.ndarray, *args) -> np.ndarray:
    """Apply an indicator to the forward-filled series, starting at its first valid value
    (no backfill, so nothing from the future leaks in)."""
    x = F.ffill(x)
    out = np.full(len(x), np.nan)
    ok = np.flatnonzero(~np.isnan(x))
    if len(ok):
        out[ok[0] :] = fn(x[ok[0] :], *args)
    return out


def _trend(md):
    c = F.ffill(daily_close_prev(md))
    return c, _on_valid(ind.sma, c, 50)


def _er(md):
    return _on_valid(ind.efficiency_ratio, daily_close_prev(md), 10)


def _overnight_rel(md):
    """Overnight (18:00-09:29) range / ATR14. Known at the 09:29 close."""
    k = F.n_sessions(md)
    hi, lo = np.full(k, -np.inf), np.full(k, np.inf)
    idx = np.flatnonzero((md.minute >= 1080) | (md.minute < F.RTH_OPEN))
    np.maximum.at(hi, md.sess[idx], md.high[idx])
    np.minimum.at(lo, md.sess[idx], md.low[idx])
    return (hi - lo) / F.atr_prev(md, 14)


FILTERS: dict[str, Filter] = {
    f.name: f
    for f in [
        Filter("vol_high", "pre-session", "Breakout/trend edges need movement: trade only when "
               "ATR14 is in the top half of its 1-year range.",
               lambda md: _vol_rank(md) >= 0.5),
        Filter("vol_low", "pre-session", "Mean-reversion edges prefer calm markets: trade only "
               "when ATR14 is in the bottom half of its 1-year range.",
               lambda md: _vol_rank(md) < 0.5),
        Filter("vol_expanding", "pre-session", "Volatility clusters: trade when the 5-day ATR "
               "exceeds the 20-day ATR (expanding regime).",
               lambda md: F.atr_prev(md, 5) > F.atr_prev(md, 20)),
        Filter("trend_up", "pre-session", "Trade only when the prior close is above its 50-day "
               "SMA (bull regime; buy-the-dip and long breakouts work better).",
               lambda md: np.greater(*_trend(md))),
        Filter("trend_down", "pre-session", "Trade only when the prior close is below its 50-day "
               "SMA (bear regime: larger ranges, stronger intraday trends).",
               lambda md: np.less(*_trend(md))),
        Filter("trending", "pre-session", "Kaufman efficiency ratio of the last 10 daily closes "
               ">= 0.3: the market has been moving directionally.",
               lambda md: _er(md) >= 0.3),
        Filter("choppy", "pre-session", "Efficiency ratio < 0.3: directionless, mean-reverting "
               "tape.",
               lambda md: _er(md) < 0.3),
        Filter("vix_high", "pre-session", "Prior-day VIX >= 20: fear regime with larger intraday "
               "moves.",
               lambda md: vix_prev(md) >= 20),
        Filter("vix_low", "pre-session", "Prior-day VIX < 20: calm regime.",
               lambda md: vix_prev(md) < 20),
        Filter("quiet_overnight", "09:29 ET", "Overnight range below 0.5 x ATR: the cash open "
               "has not been pre-empted, so opening breakouts have room to run.",
               lambda md: _overnight_rel(md) < 0.5),
        Filter("not_monday", "pre-session", "Mondays carry weekend-gap dynamics; exclude them.",
               lambda md: ((md.sess_day + 3) % 7) != 0),  # Monday = 0 (1970-01-01 = Thursday)
    ]
}  # fmt: skip


def mask(md: MarketData, name: str) -> np.ndarray:
    m = FILTERS[name].fn(md)
    return np.asarray(m, dtype=bool) & ~np.isnan(np.asarray(m, dtype=float))


def filtered(base: type[Strategy], fname: str) -> type[Strategy]:
    """Register `<base>__<filter>`: the base strategy, entries gated by the filter."""
    flt = FILTERS[fname]
    name = f"{base.name}__{fname}"
    if name in REGISTRY:
        return REGISTRY[name]

    def orders(self, md: MarketData) -> Orders:
        o = base.orders(self, md)
        allow = F.to_bars(md, mask(md, fname))
        if flt.known != "pre-session":  # intraday-known filters may only gate RTH entries
            allow &= (md.minute >= F.RTH_OPEN - 1) & (md.minute < 1080)  # from the 09:29 close
        o.order_type[~allow] = 0
        return o

    cls = type(
        name.replace("__", "_"),
        (base,),
        {"name": name, "family": base.family, "orders": orders,
         "base_strategy": base.name, "filter_name": fname},
    )  # fmt: skip
    return cls
