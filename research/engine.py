"""Bar-based execution engine mirroring how the QB MQL5 EAs trade.

Conventions (must match mql5/Experts/QB/*):
  * bars are bid prices; ask = bid + spread * point (per-bar spread from MT5 history)
  * entries fill at the open of the entry bar (long at ask, short at bid)
  * SL/TP are distances from the fill price, checked intrabar on the same side the
    broker uses (long exits on bid, short exits on ask)
  * if SL and TP both fall inside one bar the SL is assumed hit first (conservative)
  * a bar opening beyond the stop/target fills at that open (gap)
  * time exit at the open of the bar where bars_held >= max_bars
  * one position at a time; a new entry may occur on the bar a time exit happens
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class Costs:
    point: float
    spread_mult: float = 1.0
    slippage_points: float = 0.0   # adverse, applied to entry and exit
    commission_price: float = 0.0  # round-trip commission expressed in price units


@dataclass
class Trade:
    entry_i: int
    exit_i: int
    entry_time: int
    exit_time: int
    direction: int
    entry: float
    exit: float
    stop_dist: float
    reason: str

    @property
    def r(self) -> float:
        return self.direction * (self.exit - self.entry) / self.stop_dist


def simulate(bars: np.ndarray, direction: np.ndarray, sl_dist: np.ndarray, tp_dist: np.ndarray,
             max_bars: int, costs: Costs, start: int = 0, end: int | None = None) -> list[Trade]:
    """direction[i] in {-1,0,1} is the signal to enter at the open of bar i."""
    o, h, l = bars["open"], bars["high"], bars["low"]
    t = bars["time"]
    spr = bars["spread"].astype(float) * costs.point * costs.spread_mult
    slip = costs.slippage_points * costs.point
    end = len(bars) if end is None else end
    trades: list[Trade] = []

    # Event-driven: jump to the next signal, then vector-search its exit window.
    sig = np.flatnonzero((direction[start:end] != 0) & (sl_dist[start:end] > 0)) + start
    free_from = start   # first bar at which a new entry is allowed
    while True:
        k = int(np.searchsorted(sig, free_from, side="left"))
        if k >= len(sig):
            break
        e_i = int(sig[k])
        pos = int(direction[e_i])
        e_px = (o[e_i] + spr[e_i] if pos > 0 else o[e_i]) + pos * slip
        sd = float(sl_dist[e_i])
        sl = e_px - pos * sd
        tp = e_px + pos * float(tp_dist[e_i])

        w_end = min(e_i + max_bars, end)          # bars e_i .. w_end-1 are held intrabar
        sl_o, sl_h, sl_l = o[e_i:w_end], h[e_i:w_end], l[e_i:w_end]
        if pos < 0:
            s = spr[e_i:w_end]
            sl_o, sl_h, sl_l = sl_o + s, sl_h + s, sl_l + s
        hit_sl = sl_l <= sl if pos > 0 else sl_h >= sl
        hit_tp = sl_h >= tp if pos > 0 else sl_l <= tp
        hit = np.flatnonzero(hit_sl | hit_tp)
        if len(hit):
            j = int(hit[0])
            x_i = e_i + j
            op = sl_o[j]
            if hit_sl[j]:
                gap = j > 0 and (op <= sl if pos > 0 else op >= sl)
                px, why = (op if gap else sl), "sl"
            else:
                gap = j > 0 and (op >= tp if pos > 0 else op <= tp)
                px, why = (op if gap else tp), "tp"
            trades.append(_close(e_i, x_i, t, pos, e_px, px - pos * slip, sd, costs, why))
            free_from = x_i + 1
        elif e_i + max_bars < end:
            x_i = e_i + max_bars
            px = (o[x_i] if pos > 0 else o[x_i] + spr[x_i]) - pos * slip
            trades.append(_close(e_i, x_i, t, pos, e_px, px, sd, costs, "time"))
            free_from = x_i                       # may re-enter on the time-exit bar
        else:
            break                                 # still open at end of data
    return trades


def _close(e_i, x_i, t, pos, e_px, x_px, sd, costs: Costs, why) -> Trade:
    x_px -= pos * costs.commission_price
    return Trade(e_i, x_i, int(t[e_i]), int(t[x_i]), pos, e_px, x_px, sd, why)


def atr_sma(bars: np.ndarray, period: int) -> np.ndarray:
    """MT5 iATR: simple moving average of true range; NaN until enough bars."""
    h, l, c = bars["high"], bars["low"], bars["close"]
    prev = np.concatenate(([c[0]], c[:-1]))
    tr = np.maximum(h, prev) - np.minimum(l, prev)
    tr[0] = h[0] - l[0]
    out = np.full(len(tr), np.nan)
    if len(tr) >= period:
        cs = np.cumsum(tr)
        out[period - 1:] = (cs[period - 1:] - np.concatenate(([0.0], cs[:-period]))) / period
    return out


def server_hour(bars: np.ndarray) -> np.ndarray:
    return (bars["time"] // 3600) % 24


def r_array(trades: list[Trade]) -> np.ndarray:
    return np.array([tr.r for tr in trades], dtype=float)
