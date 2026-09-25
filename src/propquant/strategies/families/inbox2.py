"""Batch 4: inbox-derived ideas (triaged from the research inbox; see Ideas/ notes for sources).

All on 1m bars. IB = 09:30-10:29 (known at the 10:29 bar close). Overnight (ON) = 18:00-09:29.
"""

import numpy as np
from numba import njit

from propquant.engine import core
from propquant.engine.backtest import MarketData, Orders
from propquant.strategies import features as F
from propquant.strategies.base import Strategy
from propquant.strategies.families.technical import enter, finish, shift

TICK = 0.25
IB_END = 630  # first bar after the IB


def _ib(md: MarketData):
    hi, lo = F.window_high_low(md, F.RTH_OPEN, IB_END)
    return hi, lo, hi - lo


def _overnight(md: MarketData):
    k = F.n_sessions(md)
    hi, lo = np.full(k, -np.inf), np.full(k, np.inf)
    idx = np.flatnonzero((md.minute >= 1080) | (md.minute < F.RTH_OPEN))
    np.maximum.at(hi, md.sess[idx], md.high[idx])
    np.minimum.at(lo, md.sess[idx], md.low[idx])
    hi[~np.isfinite(hi)] = np.nan
    lo[~np.isfinite(lo)] = np.nan
    return hi, lo


def _since_ib_extremes(md: MarketData):
    """Running low/high of RTH bars from 10:30 up to each bar (inclusive); NaN elsewhere."""
    lo, hi = np.full(md.n, np.nan), np.full(md.n, np.nan)
    live = (md.minute >= IB_END) & (md.minute < 1080)
    for s in range(F.n_sessions(md)):
        a, b = md.sess_start[s], md.sess_start[s + 1]
        m = live[a:b]
        if m.any():
            idx = np.flatnonzero(m) + a
            lo[idx] = np.minimum.accumulate(md.low[idx])
            hi[idx] = np.maximum.accumulate(md.high[idx])
    return lo, hi


class OvernightFailureFade(Strategy):
    name = "overnight_failure_fade"
    family = "overnight_failure"
    max_trades_per_session = 1
    defaults = {"k": 0.3, "c": 0.25, "ib_mid": False}
    param_space = {"k": [0.3, 0.5], "c": [0.25, 0.40], "ib_mid": [False, True]}

    def orders(self, md):
        p = self.params
        d = F.rth_daily(md)
        prev_close = F.prev(d["close"])
        on_hi, on_lo = _overnight(md)
        on_close = F.at_minute(md, md.close, F.RTH_OPEN - 1)
        atr = F.atr_prev(md, 14)
        move = on_close - prev_close
        pos = (on_close - on_lo) / (on_hi - on_lo)
        ib_hi, ib_lo, ibr = _ib(md)
        px = F.at_minute(md, md.close, IB_END - 1)  # decision at the 10:30 close
        up = (move >= p["k"] * atr) & (pos >= 1 - p["c"]) & (ib_hi <= on_hi)
        dn = (move <= -p["k"] * atr) & (pos <= p["c"]) & (ib_lo >= on_lo)
        if p["ib_mid"]:
            up &= px < ib_lo + ibr / 2
            dn &= px > ib_lo + ibr / 2
        side = np.where(up, -1.0, np.where(dn, 1.0, 0.0))  # fade the overnight move
        stop = np.where(up, np.maximum(on_hi, ib_hi) + 2 * TICK - px,
                        px - (np.minimum(on_lo, ib_lo) - 2 * TICK))  # fmt: skip
        tgt = np.abs(px - prev_close)
        ok = (side != 0) & np.isfinite(stop) & np.isfinite(tgt) & (tgt > 0)
        ok &= np.sign(prev_close - px) == side  # target still in the trade's direction
        go = (md.minute == IB_END - 1) & F.to_bars(md, ok)
        o = Orders.empty(md.n)
        enter(o, go, F.to_bars(md, side), F.to_bars(md, stop), F.to_bars(md, tgt))
        return finish(o, md)


class IbFailedAuction(Strategy):
    name = "ib_failed_auction"
    family = "failed_auction"
    max_trades_per_session = 2
    defaults = {"block": 5, "t": 0.25, "double_sweep": False}
    param_space = {"block": [5, 30], "t": [0.25, 0.5], "double_sweep": [False, True]}

    def orders(self, md):
        p = self.params
        B = p["block"]
        ib_hi, ib_lo, ibr = (F.to_bars(md, x) for x in _ib(md))
        on_hi, on_lo = (F.to_bars(md, x) for x in _overnight(md))
        run_lo, run_hi = _since_ib_extremes(md)
        # confirmation-block closes: clock-aligned B-minute blocks from 10:30
        rel = md.minute - IB_END
        block_end = (rel >= B - 1) & ((rel + 1) % B == 0) & (md.minute < 900)
        blk_lo = np.full(md.n, np.nan)
        blk_hi = np.full(md.n, np.nan)
        for j in np.flatnonzero(block_end):
            a = max(j - B + 1, md.sess_start[md.sess[j]])
            blk_lo[j], blk_hi[j] = md.low[a : j + 1].min(), md.high[a : j + 1].max()
        long_ = block_end & (blk_lo < ib_lo - 2 * TICK) & (md.close > ib_lo)
        short = block_end & (blk_hi > ib_hi + 2 * TICK) & (md.close < ib_hi)
        if p["double_sweep"]:
            long_ &= run_lo < on_lo
            short &= run_hi > on_hi
        sl = np.where(long_, md.close - (run_lo - 2 * TICK), (run_hi + 2 * TICK) - md.close)
        tp = np.where(long_, ib_lo + p["t"] * ibr - md.close, md.close - (ib_hi - p["t"] * ibr))
        go = (long_ | short) & (tp > 0)
        o = Orders.empty(md.n)
        enter(o, go, np.where(long_, 1, -1), sl, tp)
        return finish(o, md)


@njit(cache=True)
def _right_side_v(minute, sess, high, low, close, atr_bars, m, f, hold):
    """Per bar: entry flag, stop pts, target pts, and exit flag (time stop)."""
    n = len(close)
    go = np.zeros(n, np.bool_)
    sl = np.full(n, np.nan)
    tp = np.full(n, np.nan)
    ex = np.zeros(n, np.bool_)
    s_prev = -1
    armed = False
    done = False
    v_low = 0.0
    h60 = 0.0
    prev_blk_hi = np.nan
    cur_blk_hi = -1e18
    exit_at = -1
    for i in range(n):
        if sess[i] != s_prev:
            s_prev, armed, done = sess[i], False, False
            prev_blk_hi, cur_blk_hi, exit_at = np.nan, -1e18, -1
        if i == exit_at:
            ex[i] = True
        mi = minute[i]
        if mi < 570 or mi >= 1080:
            continue
        cur_blk_hi = max(cur_blk_hi, high[i])
        block_close = (mi - 570) % 5 == 4
        if not done and 600 <= mi <= 870:
            a = max(i - 59, 0)
            while sess[a] != sess[i]:
                a += 1
            hh = high[a : i + 1].max()
            if not armed and hh - low[i] >= m * atr_bars[i]:
                armed, v_low, h60 = True, low[i], hh
            elif armed:
                v_low = min(v_low, low[i])
            if armed and block_close and not np.isnan(prev_blk_hi) and close[i] > prev_blk_hi:
                go[i] = True
                sl[i] = close[i] - (v_low - 0.5)
                tp[i] = v_low + f * (h60 - v_low) - close[i]
                exit_at = i + hold
                done = True
        if block_close:
            prev_blk_hi, cur_blk_hi = cur_blk_hi, -1e18
    return go, sl, tp, ex


class RightSideOfTheV(Strategy):
    name = "right_side_v"
    family = "capitulation_reversal"
    max_trades_per_session = 1
    defaults = {"m": 0.5, "f": 0.5, "hold": 90}
    param_space = {"m": [0.35, 0.5, 0.7], "f": [0.5, 1.0], "hold": [30, 90]}

    def orders(self, md):
        p = self.params
        atr = F.to_bars(md, F.atr_prev(md, 14))
        go, sl, tp, ex = _right_side_v(md.minute, md.sess, md.high, md.low, md.close,
                                       np.nan_to_num(atr, nan=1e18), p["m"], p["f"],
                                       p["hold"])  # fmt: skip
        go &= tp > 0
        o = Orders.empty(md.n)
        enter(o, go, np.ones(md.n), sl, tp)
        o.exit_sig |= ex
        return finish(o, md)


class OpeningRangeReversal(Strategy):
    name = "opening_range_reversal"
    family = "opening_reversal"
    max_trades_per_session = 1
    defaults = {"p": 0.3, "g": 0.5, "bias": True}
    param_space = {"p": [0.2, 0.3, 0.4], "g": [0.5, 1.0], "bias": [True, False]}

    def orders(self, md):
        p = self.params
        d = F.rth_daily(md)
        atr = F.to_bars(md, F.atr_prev(md, 14))
        op = F.to_bars(md, d["open"])
        prev_c = F.ffill(F.prev(d["close"]))
        from propquant.strategies import indicators as ind
        from propquant.strategies.filters import _on_valid

        sma50 = _on_valid(ind.sma, prev_c, 50)
        up_bias = F.to_bars(md, prev_c > sma50)
        dn_bias = F.to_bars(md, prev_c < sma50)
        # running RTH low/high since 09:30 and the last completed 5-minute block's high/low
        live = (md.minute >= F.RTH_OPEN) & (md.minute < 1080)
        run_lo, run_hi = np.full(md.n, np.nan), np.full(md.n, np.nan)
        blk_hi, blk_lo = np.full(md.n, np.nan), np.full(md.n, np.nan)
        for s in range(F.n_sessions(md)):
            a, b = md.sess_start[s], md.sess_start[s + 1]
            idx = np.flatnonzero(live[a:b]) + a
            if not len(idx):
                continue
            run_lo[idx] = np.minimum.accumulate(md.low[idx])
            run_hi[idx] = np.maximum.accumulate(md.high[idx])
            for j in idx:
                if (md.minute[j] - F.RTH_OPEN) % 5 == 4:
                    k0 = max(j - 4, a)
                    blk_hi[j], blk_lo[j] = md.high[k0 : j + 1].max(), md.low[k0 : j + 1].min()
        blk_hi, blk_lo = F.ffill(blk_hi), F.ffill(blk_lo)
        drop_ok = (op - run_lo >= p["p"] * atr) & (md.minute < 660)
        rise_ok = (run_hi - op >= p["p"] * atr) & (md.minute < 660)
        # once triggered before 11:00 the setup stays armed until 11:30
        armed_l, armed_s = np.zeros(md.n, bool), np.zeros(md.n, bool)
        for s in range(F.n_sessions(md)):
            a, b = md.sess_start[s], md.sess_start[s + 1]
            armed_l[a:b] = np.maximum.accumulate(drop_ok[a:b])
            armed_s[a:b] = np.maximum.accumulate(rise_ok[a:b])
        win = (md.minute >= F.RTH_OPEN) & (md.minute < 690)
        long_ = win & armed_l & np.isfinite(blk_hi)
        short = win & armed_s & np.isfinite(blk_lo) & ~long_
        if p["bias"]:
            long_ &= up_bias
            short &= dn_bias
        o = Orders.empty(md.n)
        px = np.where(long_, blk_hi + TICK, blk_lo - TICK)
        sl = np.where(long_, px - (run_lo - 2 * TICK), (run_hi + 2 * TICK) - px)
        tp = np.where(long_, run_lo + p["g"] * (op - run_lo) - px,
                      px - (run_hi - p["g"] * (run_hi - op)))  # fmt: skip
        go = (long_ | short) & (sl > 0) & (tp > 0)
        o.order_type[go] = core.STOP
        o.order_dir[go] = np.where(long_, 1, -1)[go]
        o.order_px[go] = px[go]
        o.sl_pts[go] = sl[go]
        o.tp_pts[go] = tp[go]
        return finish(o, md)


class WideIbRotation(Strategy):
    name = "wide_ib_rotation"
    family = "ib_rotation"
    max_trades_per_session = 2
    defaults = {"q": 1.3, "s": 0.1, "target": "mid"}
    param_space = {"q": [1.3, 1.6], "s": [0.1, 0.2], "target": ["mid", "far25"]}

    def orders(self, md):
        p = self.params
        ib_hi, ib_lo, ibr = _ib(md)
        med = np.full(len(ibr), np.nan)
        for i in range(20, len(ibr)):
            w = ibr[i - 20 : i]
            w = w[np.isfinite(w)]
            if len(w) >= 10:
                med[i] = np.median(w)
        wide = F.to_bars(md, np.isfinite(ibr) & (ibr >= p["q"] * med))
        H, L, R = F.to_bars(md, ib_hi), F.to_bars(md, ib_lo), F.to_bars(md, ibr)
        live = wide & (md.minute >= IB_END - 1) & (md.minute < 870)
        above_mid = md.close > L + R / 2
        o = Orders.empty(md.n)
        o.order_type[live] = core.LIMIT
        o.order_dir[live] = np.where(above_mid, -1, 1)[live]  # sell the top / buy the bottom
        o.order_px[live] = np.where(above_mid, H, L)[live]
        o.sl_pts[live] = (p["s"] * R)[live]
        tgt = 0.5 * R if p["target"] == "mid" else 0.75 * R
        o.tp_pts[live] = tgt[live]
        return finish(o, md)


class SessionRangeSweep(Strategy):
    name = "session_range_sweep"
    family = "liquidity_sweep"
    max_trades_per_session = 1
    defaults = {"range": "premarket", "target": "mid"}
    param_space = {"range": ["premarket", "h8", "london"], "target": ["mid", "far"]}
    RANGES = {"premarket": (180, 570), "h8": (480, 540), "london": (120, 300)}

    def orders(self, md):
        p = self.params
        m0, m1 = self.RANGES[p["range"]]
        hi, lo = F.window_high_low(md, m0, m1)
        atr = F.atr_prev(md, 14)
        ok = np.isfinite(hi) & (hi - lo >= 0.15 * atr)
        H, L = F.to_bars(md, hi), F.to_bars(md, lo)
        win = (md.minute >= F.RTH_OPEN) & (md.minute < 690) & F.to_bars(md, ok)
        short = win & (md.high > H + TICK) & (md.close < H)
        long_ = win & (md.low < L - TICK) & (md.close > L) & ~short
        mid = (H + L) / 2
        tp = np.where(short, md.close - (mid if p["target"] == "mid" else L),
                      (mid if p["target"] == "mid" else H) - md.close)  # fmt: skip
        sl = np.where(short, md.high + 2 * TICK - md.close, md.close - (md.low - 2 * TICK))
        o = Orders.empty(md.n)
        enter(o, (short | long_) & (tp > 0), np.where(short, -1, 1), sl, tp)
        o.exit_sig |= F.last_bar_before(md, 720)
        return finish(o, md)


_ = shift  # re-exported helper (keeps the import explicit for readers)
