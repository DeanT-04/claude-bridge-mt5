"""Indicator templates (entry x exit), each on 5m and 15m bars, plus inbox-derived ideas.

Signals are computed at a bar's close; market orders fill at the next bar's open. Stops and
targets are ATR multiples measured on the strategy's own bars. Entries only inside the regular
session window; everything is flat by 15:55.
"""

from typing import ClassVar

import numpy as np

from propquant.engine import core
from propquant.engine.backtest import MarketData, Orders
from propquant.strategies import features as F
from propquant.strategies import indicators as ind
from propquant.strategies.base import REGISTRY, Strategy

WIN0, WIN1, EXIT = 575, 900, 955  # entries 09:35-15:00 ET, flat 15:55


def shift(x: np.ndarray, k: int = 1) -> np.ndarray:
    out = np.full(len(x), np.nan)
    out[k:] = x[:-k]
    return out


def window(md: MarketData, m0: int = WIN0, m1: int = WIN1) -> np.ndarray:
    return (md.minute >= m0) & (md.minute < m1)


def enter(o: Orders, go: np.ndarray, direction: np.ndarray, sl: np.ndarray, tp: np.ndarray):
    go = go & np.isfinite(sl) & (sl > 0)
    o.order_type[go] = core.MARKET
    o.order_dir[go] = direction[go].astype(np.int64)
    o.sl_pts[go] = sl[go]
    o.tp_pts[go] = np.where(np.isfinite(tp), tp, np.nan)[go]


def finish(o: Orders, md: MarketData) -> Orders:
    o.exit_sig |= F.last_bar_before(md, EXIT)
    return o


class Technical(Strategy):
    """Base for timeframe-templated strategies (not registered itself)."""

    template: ClassVar[str] = ""
    max_trades_per_session = 3

    def __init_subclass__(cls, **kw) -> None:
        if cls.__dict__.get("template") and "timeframe" not in cls.__dict__:
            return  # the template itself: concrete 5m/15m classes are made by `timeframes`
        super().__init_subclass__(**kw)

    def atr(self, md: MarketData) -> np.ndarray:
        return ind.atr(md.high, md.low, md.close, 14)


def timeframes(template: type[Technical], tfs=("5m", "15m")) -> list[type[Strategy]]:
    out = []
    for tf in tfs:
        name = f"{template.template}_{tf}"
        if name in REGISTRY:
            out.append(REGISTRY[name])
            continue
        out.append(type(name, (template,), {"name": name, "timeframe": tf,
                                            "family": template.template}))  # fmt: skip
    return out


class EmaCross(Technical):
    template = "ema_cross"
    defaults = {"pair": (20, 50), "sl_atr": 1.0, "tp_atr": 2.0}
    param_space = {"pair": [(9, 21), (20, 50), (50, 200)], "sl_atr": [1.0, 2.0],
                   "tp_atr": [2.0, 4.0]}  # fmt: skip

    def orders(self, md):
        p = self.params
        f, s = ind.ema(md.close, p["pair"][0]), ind.ema(md.close, p["pair"][1])
        a = self.atr(md)
        up, dn = ind.cross_up(f, s), ind.cross_down(f, s)
        o = Orders.empty(md.n)
        enter(o, (up | dn) & window(md), np.where(up, 1, -1), a * p["sl_atr"], a * p["tp_atr"])
        return finish(o, md)


class DonchianBreak(Technical):
    template = "donchian_break"
    defaults = {"n": 20, "sl_atr": 1.0, "tp_atr": 2.0}
    param_space = {"n": [20, 55], "sl_atr": [1.0, 2.0], "tp_atr": [2.0, 4.0]}

    def orders(self, md):
        p = self.params
        hi, lo = ind.donchian(md.high, md.low, p["n"])
        hi, lo = shift(hi), shift(lo)  # channel of the PREVIOUS n bars
        a = self.atr(md)
        up, dn = md.close > hi, md.close < lo
        o = Orders.empty(md.n)
        enter(o, (up | dn) & window(md), np.where(up, 1, -1), a * p["sl_atr"], a * p["tp_atr"])
        return finish(o, md)


class BollingerSqueeze(Technical):
    template = "bb_squeeze"
    defaults = {"q": 0.1, "sl_atr": 1.0, "tp_atr": 2.0}
    param_space = {"q": [0.1, 0.2], "sl_atr": [1.0, 2.0], "tp_atr": [2.0, 4.0]}

    def orders(self, md):
        p = self.params
        lo, mid, hi = ind.bollinger(md.close, 20, 2.0)
        width = (hi - lo) / mid
        # squeeze: previous bar's width in the lowest q of the last 100 bars
        thr = np.full(md.n, np.nan)
        for i in range(100, md.n):
            thr[i] = np.nanquantile(width[i - 100 : i], p["q"])
        squeezed = shift(width) <= shift(thr)
        a = self.atr(md)
        up, dn = squeezed & (md.close > hi), squeezed & (md.close < lo)
        o = Orders.empty(md.n)
        enter(o, (up | dn) & window(md), np.where(up, 1, -1), a * p["sl_atr"], a * p["tp_atr"])
        return finish(o, md)


class Rsi2Pullback(Technical):
    template = "rsi2_pullback"
    defaults = {"trend": 200, "lo": 10, "sl_atr": 1.5, "tp_atr": 1.0}
    param_space = {"trend": [100, 200], "lo": [5, 10], "sl_atr": [1.0, 2.0],
                   "tp_atr": [1.0, 2.0]}  # fmt: skip

    def orders(self, md):
        p = self.params
        r = ind.rsi(md.close, 2)
        e = ind.ema(md.close, p["trend"])
        a = self.atr(md)
        up = (md.close > e) & (r < p["lo"])
        dn = (md.close < e) & (r > 100 - p["lo"])
        o = Orders.empty(md.n)
        enter(o, (up | dn) & window(md), np.where(up, 1, -1), a * p["sl_atr"], a * p["tp_atr"])
        return finish(o, md)


class KeltnerFade(Technical):
    template = "keltner_fade"
    defaults = {"k": 2.0, "adx_max": 20, "sl_atr": 1.0}
    param_space = {"k": [2.0, 2.5], "adx_max": [20, 25], "sl_atr": [1.0, 1.5]}

    def orders(self, md):
        p = self.params
        lo, mid, hi = ind.keltner(md.high, md.low, md.close, 20, p["k"])
        adx = ind.adx(md.high, md.low, md.close, 14)
        a = self.atr(md)
        calm = adx < p["adx_max"]
        up, dn = calm & (md.close < lo), calm & (md.close > hi)  # fade back to the middle
        o = Orders.empty(md.n)
        enter(o, (up | dn) & window(md), np.where(up, 1, -1), a * p["sl_atr"],
              np.abs(md.close - mid))  # fmt: skip
        return finish(o, md)


class SupertrendFollow(Technical):
    template = "supertrend"
    defaults = {"mult": 3.0, "sl_atr": 2.0, "align": False}
    param_space = {"mult": [2.0, 3.0], "sl_atr": [2.0, 3.0], "align": [False, True]}

    def orders(self, md):
        p = self.params
        _, d = ind.supertrend(md.high, md.low, md.close, 10, p["mult"])
        flip_up = (d == 1) & (shift(d) == -1)
        flip_dn = (d == -1) & (shift(d) == 1)
        if p["align"]:
            e = ind.ema(md.close, 200)
            flip_up &= md.close > e
            flip_dn &= md.close < e
        a = self.atr(md)
        o = Orders.empty(md.n)
        enter(o, (flip_up | flip_dn) & window(md), np.where(flip_up, 1, -1), a * p["sl_atr"],
              np.full(md.n, np.nan))  # fmt: skip
        o.exit_sig |= flip_up | flip_dn  # opposite flip closes the open position
        return finish(o, md)


class MacdTrend(Technical):
    template = "macd_trend"
    defaults = {"align": True, "sl_atr": 1.0, "tp_atr": 2.0}
    param_space = {"align": [False, True], "sl_atr": [1.0, 2.0], "tp_atr": [2.0, 4.0]}

    def orders(self, md):
        p = self.params
        _, _, h = ind.macd(md.close)
        up, dn = (h > 0) & (shift(h) <= 0), (h < 0) & (shift(h) >= 0)
        if p["align"]:
            e = ind.ema(md.close, 200)
            up &= md.close > e
            dn &= md.close < e
        a = self.atr(md)
        o = Orders.empty(md.n)
        enter(o, (up | dn) & window(md), np.where(up, 1, -1), a * p["sl_atr"], a * p["tp_atr"])
        return finish(o, md)


TEMPLATES = [EmaCross, DonchianBreak, BollingerSqueeze, Rsi2Pullback, KeltnerFade,
             SupertrendFollow, MacdTrend]  # fmt: skip
CLASSES = [c for t in TEMPLATES for c in timeframes(t)]


# ---------------- inbox-derived (1m) ----------------


def session_twap(md: MarketData, start: int = F.RTH_OPEN) -> np.ndarray:
    """Time-weighted average of closes since `start` in each session (known at each close).
    Used instead of VWAP: proxy volume is tick activity, not contracts."""
    live = (md.minute >= start) & (md.minute < 1080)
    x = np.where(live, md.close, 0.0)
    c = np.where(live, 1.0, 0.0)
    out = np.full(md.n, np.nan)
    for s in range(F.n_sessions(md)):
        a, b = md.sess_start[s], md.sess_start[s + 1]
        cs, cc = np.cumsum(x[a:b]), np.cumsum(c[a:b])
        with np.errstate(invalid="ignore", divide="ignore"):
            out[a:b] = np.where(cc > 0, cs / cc, np.nan)
    return out


class TwapReversion(Strategy):
    name = "twap_reversion"
    family = "twap_reversion"
    max_trades_per_session = 2
    defaults = {"k": 0.3, "sl_mult": 0.5, "start": 600}
    param_space = {"k": [0.3, 0.5], "sl_mult": [0.5, 1.0], "start": [600, 630]}

    def orders(self, md):
        p = self.params
        tw = session_twap(md)
        atr_d = F.to_bars(md, F.atr_prev(md, 14))
        dev = md.close - tw
        go = window(md, p["start"], WIN1) & (np.abs(dev) >= p["k"] * atr_d)
        o = Orders.empty(md.n)
        enter(o, go, -np.sign(dev), p["sl_mult"] * p["k"] * atr_d, np.abs(dev))
        return finish(o, md)


class NarrowRangeBreakout(Strategy):
    name = "nr_breakout"
    family = "narrow_range"
    max_trades_per_session = 1
    defaults = {"nr": 7, "sl_frac": 0.5, "tp_mult": 1.0}
    param_space = {"nr": [4, 7], "sl_frac": [0.5, 1.0], "tp_mult": [1.0, 2.0]}

    def orders(self, md):
        p = self.params
        d = F.rth_daily(md)
        rng = d["high"] - d["low"]
        narrow = np.zeros(len(rng), dtype=bool)
        for i in range(p["nr"], len(rng)):
            w = rng[i - p["nr"] + 1 : i + 1]
            narrow[i] = np.all(np.isfinite(w)) and rng[i] <= w.min()
        # yesterday was the narrowest of the last `nr` days -> today break its high/low
        ok = F.prev(narrow.astype(float)) == 1
        hi, lo, r = F.prev(d["high"]), F.prev(d["low"]), F.prev(rng)
        live = window(md, F.RTH_OPEN, 720) & F.to_bars(md, ok)
        o = Orders.empty(md.n)
        o.order_type[live] = core.STOP
        o.order_dir[live] = 0
        o.order_px[live] = F.to_bars(md, hi)[live]
        o.order_px2[live] = F.to_bars(md, lo)[live]
        o.sl_pts[live] = F.to_bars(md, r * p["sl_frac"])[live]
        o.tp_pts[live] = F.to_bars(md, r * p["tp_mult"])[live]
        return finish(o, md)


class PriorDaySweep(Strategy):
    """ICT/SMC 'liquidity sweep': price runs the prior day's high (low), then closes back
    inside -> fade toward the middle of yesterday's range."""

    name = "pd_sweep"
    family = "liquidity_sweep"
    max_trades_per_session = 1
    defaults = {"end": 720, "buf": 0.05, "tp_frac": 0.5}
    param_space = {"end": [720, 900], "buf": [0.05, 0.1], "tp_frac": [0.5, 1.0]}

    def orders(self, md):
        p = self.params
        d = F.rth_daily(md)
        pdh, pdl = F.to_bars(md, F.prev(d["high"])), F.to_bars(md, F.prev(d["low"]))
        rng = pdh - pdl
        atr_d = F.to_bars(md, F.atr_prev(md, 14))
        live = window(md, F.RTH_OPEN, p["end"])
        short = live & (md.high > pdh) & (md.close < pdh)
        long_ = live & (md.low < pdl) & (md.close > pdl)
        sl = np.where(short, md.high - md.close, md.close - md.low) + p["buf"] * atr_d
        o = Orders.empty(md.n)
        enter(o, short | long_, np.where(short, -1, 1), sl, rng * p["tp_frac"])
        return finish(o, md)


class IbTwapBreak(Strategy):
    """Initial-balance breakout only on the side of the session TWAP at the end of the IB
    (the 'IB + VWAP' idea from the inbox, with TWAP standing in for VWAP)."""

    name = "ib_twap"
    family = "initial_balance"
    max_trades_per_session = 1
    defaults = {"sl_frac": 0.5, "tp_mult": 1.0}
    param_space = {"sl_frac": [0.5, 1.0], "tp_mult": [1.0, 2.0]}

    def orders(self, md):
        p = self.params
        end = F.RTH_OPEN + 60
        hi, lo = F.window_high_low(md, F.RTH_OPEN, end)
        rng = hi - lo
        tw = F.at_minute(md, session_twap(md), end - 1)
        px = F.at_minute(md, md.close, end - 1)
        side = np.sign(px - tw)  # known at the 10:30 close
        ok = np.isfinite(rng) & np.isfinite(side) & (side != 0)  # no TWAP/price -> no trade
        live = window(md, end - 1, 840) & F.to_bars(md, ok)
        o = Orders.empty(md.n)
        o.order_type[live] = core.STOP
        o.order_dir[live] = F.to_bars(md, side)[live].astype(np.int64)
        o.order_px[live] = F.to_bars(md, np.where(side > 0, hi, lo))[live]
        o.sl_pts[live] = F.to_bars(md, rng * p["sl_frac"])[live]
        o.tp_pts[live] = F.to_bars(md, rng * p["tp_mult"])[live]
        return finish(o, md)
