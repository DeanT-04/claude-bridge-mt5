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
  * optional prop-firm execution rules (as QB_Host applies them): `blocked[i]` forbids an entry
    at bar i (news blackout, weekend window); `flat_at[i]` forces any open position closed at
    the close of bar i (the last bar before the Friday cutoff)
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
    # Broker history understates spreads (BTCUSD records 0 on most bars; XAUUSD 12 vs 22 live),
    # so each bar is charged at least this many points.
    min_spread_points: float = 0.0


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
             max_bars: int, costs: Costs, start: int = 0, end: int | None = None,
             blocked: np.ndarray | None = None, flat_at: np.ndarray | None = None) -> list[Trade]:
    """direction[i] in {-1,0,1} is the signal to enter at the open of bar i."""
    o, h, l, c = bars["open"], bars["high"], bars["low"], bars["close"]
    t = bars["time"]
    spr = np.maximum(bars["spread"].astype(float), costs.min_spread_points) * costs.point * costs.spread_mult
    slip = costs.slippage_points * costs.point
    end = len(bars) if end is None else end
    trades: list[Trade] = []

    # Event-driven: jump to the next signal, then vector-search its exit window.
    ok = (direction[start:end] != 0) & (sl_dist[start:end] > 0)
    if blocked is not None:
        ok &= ~blocked[start:end]
    sig = np.flatnonzero(ok) + start
    flats = np.flatnonzero(flat_at) if flat_at is not None else np.zeros(0, dtype=int)
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
        fk = int(np.searchsorted(flats, e_i))
        f_i = int(flats[fk]) if fk < len(flats) and flats[fk] < w_end else -1
        if f_i >= 0:
            w_end = f_i + 1                       # must be flat by the close of bar f_i
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
        elif f_i >= 0:
            px = (c[f_i] if pos > 0 else c[f_i] + spr[f_i]) - pos * slip
            trades.append(_close(e_i, f_i, t, pos, e_px, px, sd, costs, "flat"))
            free_from = f_i + 1
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


def weekend_masks(times: np.ndarray, flat_hour: int) -> tuple[np.ndarray, np.ndarray]:
    """(blocked, flat_at) for a Friday flat rule, matching QB_Host's WeekendWindow: no entries
    from Friday flat_hour:00 server time until Monday; a position must be closed at the close
    of the last bar opening before that cutoff (also when the market closes earlier)."""
    t = times.astype(np.int64)
    day = t // 86400
    week_start = (day - (day + 3) % 7) * 86400                  # Monday 00:00 (1970-01-01 = Thu)
    cutoff = week_start + 4 * 86400 + flat_hour * 3600
    blocked = t >= cutoff
    nxt = np.concatenate((t[1:], [np.iinfo(np.int64).min]))    # last bar: open-ended
    flat_at = ~blocked & (nxt >= cutoff)
    return blocked, flat_at


def server_hour(bars: np.ndarray) -> np.ndarray:
    return (bars["time"] // 3600) % 24


def r_array(trades: list[Trade]) -> np.ndarray:
    return np.array([tr.r for tr in trades], dtype=float)
