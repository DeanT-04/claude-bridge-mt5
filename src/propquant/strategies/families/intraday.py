"""First batch: classic intraday index-futures families (pre-registered in vault Ideas/).

Minutes are ET bar-open minutes; an order written on bar m (decided at its close) acts from
bar m+1. All session features come from `features`, which documents when each is known.
"""

import numpy as np

from propquant.engine import core
from propquant.engine.backtest import MarketData, Orders
from propquant.strategies import features as F
from propquant.strategies.base import Strategy

EXIT_MINUTE = 955  # leave by 15:55 (exit signal on the 15:54 bar -> fills at 15:55 open)


def _time_exit(o: Orders, md: MarketData, minute: int) -> None:
    o.exit_sig |= F.last_bar_before(md, minute)


class OpeningRangeBreakout(Strategy):
    """OCO stop orders at the opening-range high/low; one trade a day."""

    name = "orb"
    family = "opening_range"
    max_trades_per_session = 1
    defaults = {"or_min": 15, "sl_frac": 1.0, "tp_mult": 2.0, "last_entry": 660}
    param_space = {"or_min": [5, 15, 30], "sl_frac": [0.5, 1.0], "tp_mult": [1.0, 2.0]}

    def orders(self, md: MarketData) -> Orders:
        p = self.params
        o = Orders.empty(md.n)
        end = F.RTH_OPEN + p["or_min"]  # range known at the close of bar end-1
        hi, lo = F.window_high_low(md, F.RTH_OPEN, end)
        rng = hi - lo
        live = (md.minute >= end - 1) & (md.minute < p["last_entry"])
        live &= np.isfinite(F.to_bars(md, rng)) & (F.to_bars(md, rng) > 0)
        o.order_type[live] = core.STOP
        o.order_dir[live] = 0
        o.order_px[live] = F.to_bars(md, hi)[live]
        o.order_px2[live] = F.to_bars(md, lo)[live]
        o.sl_pts[live] = (F.to_bars(md, rng) * p["sl_frac"])[live]
        o.tp_pts[live] = (F.to_bars(md, rng) * p["tp_mult"])[live]
        _time_exit(o, md, EXIT_MINUTE)
        return o


class IntradayMomentum(Strategy):
    """Gao-Han-Li-Zhou: the first half-hour return predicts the last half-hour return."""

    name = "intraday_momentum"
    family = "intraday_momentum"
    max_trades_per_session = 1
    defaults = {"threshold": 0.0, "confirm_r12": False, "sl_pct": np.nan}
    param_space = {"threshold": [0.0, 0.001, 0.0025], "confirm_r12": [False, True],
                   "sl_pct": [np.nan, 0.005]}  # fmt: skip

    def orders(self, md: MarketData) -> Orders:
        p = self.params
        d = F.rth_daily(md)
        prev_close = F.prev(d["close"])
        r1 = F.at_minute(md, md.close, 599) / prev_close - 1  # known 10:00
        r12 = F.at_minute(md, md.close, 929) / F.at_minute(md, md.close, 899) - 1  # at 15:30
        side = np.sign(r1)
        ok = np.isfinite(r1) & (np.abs(r1) > p["threshold"])
        if p["confirm_r12"]:
            ok &= np.sign(r12) == side
        o = Orders.empty(md.n)
        go = (md.minute == 929) & F.to_bars(md, ok)
        o.order_type[go] = core.MARKET
        o.order_dir[go] = F.to_bars(md, side)[go].astype(np.int64)
        if np.isfinite(p["sl_pct"]):
            o.sl_pts[go] = md.close[go] * p["sl_pct"]
        o.exit_sig |= md.minute == 958  # out at the 15:59 open (~the close)
        return o


class GapFade(Strategy):
    """Fade a moderate opening gap back toward the prior regular-session close."""

    name = "gap_fade"
    family = "gap"
    max_trades_per_session = 1
    defaults = {"g_min": 0.001, "g_max": 0.006, "sl_mult": 1.0, "exit_min": 660}
    param_space = {"g_min": [0.001, 0.0025], "g_max": [0.006, 0.012],
                   "sl_mult": [0.5, 1.0], "exit_min": [660, 720]}  # fmt: skip

    def orders(self, md: MarketData) -> Orders:
        p = self.params
        d = F.rth_daily(md)
        prev_close = F.prev(d["close"])
        gap = d["open"] - prev_close
        gp = np.abs(gap / prev_close)
        ref = F.at_minute(md, md.close, F.RTH_OPEN)  # decided at the 09:31 close
        to_fill = (ref - prev_close) * np.sign(gap)  # distance still to fill
        ok = np.isfinite(gp) & (gp >= p["g_min"]) & (gp <= p["g_max"]) & (to_fill > 0)
        o = Orders.empty(md.n)
        go = (md.minute == F.RTH_OPEN) & F.to_bars(md, ok)
        o.order_type[go] = core.MARKET
        o.order_dir[go] = -F.to_bars(md, np.sign(gap))[go].astype(np.int64)
        o.tp_pts[go] = F.to_bars(md, to_fill)[go]
        o.sl_pts[go] = F.to_bars(md, np.abs(gap) * p["sl_mult"])[go]
        _time_exit(o, md, p["exit_min"])
        return o


class InitialBalanceBreakout(Strategy):
    """Market Profile initial balance: trade the break of the first-hour range, optionally only
    when that range is narrow versus recent days (compressed -> expansion)."""

    name = "ib_breakout"
    family = "initial_balance"
    max_trades_per_session = 1
    defaults = {"ib_min": 60, "narrow": np.inf, "tp_mult": 1.0, "sl_frac": 0.5}
    param_space = {"ib_min": [30, 60], "narrow": [np.inf, 0.8], "tp_mult": [1.0, 2.0],
                   "sl_frac": [0.5, 1.0]}  # fmt: skip

    def orders(self, md: MarketData) -> Orders:
        p = self.params
        end = F.RTH_OPEN + p["ib_min"]
        hi, lo = F.window_high_low(md, F.RTH_OPEN, end)
        rng = hi - lo
        rel = rng / F.rolling_mean_prev(rng, 20)
        ok = np.isfinite(rng) & (rng > 0) & ((rel <= p["narrow"]) | ~np.isfinite(p["narrow"]))
        live = (md.minute >= end - 1) & (md.minute < 840) & F.to_bars(md, ok)
        o = Orders.empty(md.n)
        o.order_type[live] = core.STOP
        o.order_dir[live] = 0
        o.order_px[live] = F.to_bars(md, hi)[live]
        o.order_px2[live] = F.to_bars(md, lo)[live]
        o.sl_pts[live] = F.to_bars(md, rng * p["sl_frac"])[live]
        o.tp_pts[live] = F.to_bars(md, rng * p["tp_mult"])[live]
        _time_exit(o, md, EXIT_MINUTE)
        return o


class LateDayTrend(Strategy):
    """If the day has already moved k x ATR from the open by the afternoon, ride it to the close
    (late-day flows chase the day's direction)."""

    name = "late_trend"
    family = "late_trend"
    max_trades_per_session = 1
    defaults = {"decide": 840, "k": 0.5, "sl_atr": 0.25}
    param_space = {"decide": [780, 840], "k": [0.3, 0.5, 0.8], "sl_atr": [0.25, 0.5]}

    def orders(self, md: MarketData) -> Orders:
        p = self.params
        d = F.rth_daily(md)
        atr = F.atr_prev(md, 14)
        px = F.at_minute(md, md.close, p["decide"] - 1)
        move = px - d["open"]
        ok = np.isfinite(move) & np.isfinite(atr) & (np.abs(move) >= p["k"] * atr)
        o = Orders.empty(md.n)
        go = (md.minute == p["decide"] - 1) & F.to_bars(md, ok)
        o.order_type[go] = core.MARKET
        o.order_dir[go] = F.to_bars(md, np.sign(move))[go].astype(np.int64)
        o.sl_pts[go] = F.to_bars(md, atr * p["sl_atr"])[go]
        _time_exit(o, md, EXIT_MINUTE)
        return o
