"""Bar-by-bar execution engine (numba). One position at a time, 1 micro contract per unit.

No lookahead by construction: an order written at bar i was decided with data up to the CLOSE
of bar i and can only fill from bar i+1 onward.

Pessimistic fill model:
  market   fills at the next bar's open, `slip` ticks adverse
  stop     fills at max(stop, open) for buys (gap-through = worse), `slip` ticks adverse
  limit    fills only if price trades THROUGH the limit (strictly), at the limit (or a better
           open), no slippage
  SL / TP  if both could be hit inside one bar, the stop wins. On the entry bar only the stop
           is checked (the target is never credited on the bar of entry). Stops that gap are
           filled at the open.
  signal   an exit signal at bar i closes the position at bar i+1's open, `slip` adverse
  flat     positions are closed at the close of the last bar before `flat_minute` (ET), or at
           the last bar of the session, `slip` ticks adverse.
Per-bar outputs (USD per micro, commissions included) feed `propquant.firms.sim` directly:
  d_close = equity change close-to-close; d_low / d_high = worst / best point inside the bar.
"""

import numpy as np
from numba import njit

NONE, MARKET, STOP, LIMIT = 0, 1, 2, 3
EXIT_SL, EXIT_TP, EXIT_SIGNAL, EXIT_FLAT = 1, 2, 3, 4


@njit(cache=True)
def run(open_, high, low, close, minute, sess, order_type, order_dir, order_px, sl_pts, tp_pts,
        exit_sig, flat_minute, tick, point_value, slip_ticks, commission_side):  # fmt: skip
    n = len(open_)
    d_close = np.zeros(n)
    d_low = np.zeros(n)
    d_high = np.zeros(n)
    # trades: entry_i, exit_i, dir, entry_px, exit_px, pnl_usd, reason
    trades = np.zeros((n // 2 + 1, 7))
    nt = 0
    slip = slip_ticks * tick

    pos, entry_px, sl, tp, entry_i = 0, 0.0, np.nan, np.nan, -1
    mark = 0.0  # price the open position was last marked at
    for i in range(1, n):
        new_session = sess[i] != sess[i - 1]
        eq_lo, eq_hi, eq_cl = 0.0, 0.0, 0.0  # relative to the previous bar close (USD/micro)

        # ---- 1. new entry from the order decided at bar i-1 ----
        entered = False
        j = i - 1
        if pos == 0 and order_type[j] != NONE and not new_session and minute[i] < flat_minute:
            d = order_dir[j]
            fill = np.nan
            if order_type[j] == MARKET:
                fill = open_[i] + d * slip
            elif order_type[j] == STOP:
                px = order_px[j]
                if d == 1 and high[i] >= px:
                    fill = max(px, open_[i]) + slip
                elif d == -1 and low[i] <= px:
                    fill = min(px, open_[i]) - slip
            elif order_type[j] == LIMIT:
                px = order_px[j]
                if d == 1 and low[i] < px:
                    fill = min(px, open_[i])
                elif d == -1 and high[i] > px:
                    fill = max(px, open_[i])
            if not np.isnan(fill):
                pos, entry_px, entry_i, entered = d, fill, i, True
                sl = fill - d * sl_pts[j] if not np.isnan(sl_pts[j]) else np.nan
                tp = fill + d * tp_pts[j] if not np.isnan(tp_pts[j]) else np.nan
                mark = fill
                eq_cl -= commission_side
                eq_lo = eq_cl

        # ---- 2. manage the open position inside bar i ----
        if pos != 0:
            if not entered:
                mark_prev = mark
            else:
                mark_prev = entry_px
            exit_px, reason = np.nan, 0
            # exit signal decided at the previous close -> out at this bar's open
            if not entered and exit_sig[i - 1]:
                exit_px, reason = open_[i] - pos * slip, EXIT_SIGNAL
            # stop: gap-through fills at the open
            if reason == 0 and not np.isnan(sl):
                if pos == 1 and low[i] <= sl:
                    exit_px, reason = (min(sl, open_[i]) if not entered else sl) - slip, EXIT_SL
                elif pos == -1 and high[i] >= sl:
                    exit_px, reason = (max(sl, open_[i]) if not entered else sl) + slip, EXIT_SL
            if reason == 0 and not entered and not np.isnan(tp):
                if pos == 1 and high[i] > tp:
                    exit_px, reason = max(tp, open_[i]), EXIT_TP
                elif pos == -1 and low[i] < tp:
                    exit_px, reason = min(tp, open_[i]), EXIT_TP
            last_bar = i + 1 >= n or sess[i + 1] != sess[i] or minute[i + 1] >= flat_minute
            if reason == 0 and last_bar:
                exit_px, reason = close[i] - pos * slip, EXIT_FLAT

            # path extremes while holding (pessimistic: worst of the bar's range up to the exit)
            worst = low[i] if pos == 1 else high[i]
            best = high[i] if pos == 1 else low[i]
            if reason == EXIT_SL:
                worst = exit_px
            if reason == EXIT_TP:
                best = exit_px
            if reason == EXIT_SIGNAL:
                worst, best = exit_px, exit_px
            lo_move = (worst - mark_prev) * pos * point_value
            hi_move = (best - mark_prev) * pos * point_value
            base = eq_cl
            eq_lo = min(eq_lo, base + min(lo_move, 0.0))
            eq_hi = max(eq_hi, base + max(hi_move, 0.0))

            if reason != 0:
                move = (exit_px - mark_prev) * pos * point_value
                eq_cl = base + move - commission_side
                trades[nt, 0], trades[nt, 1], trades[nt, 2] = entry_i, i, pos
                trades[nt, 3], trades[nt, 4] = entry_px, exit_px
                trades[nt, 5] = (exit_px - entry_px) * pos * point_value - 2 * commission_side
                trades[nt, 6] = reason
                nt += 1
                pos, sl, tp = 0, np.nan, np.nan
            else:
                eq_cl = base + (close[i] - mark_prev) * pos * point_value
                mark = close[i]

        d_close[i] = eq_cl
        d_low[i] = min(eq_lo, eq_cl, 0.0)
        d_high[i] = max(eq_hi, eq_cl, 0.0)
    return d_close, d_low, d_high, trades[:nt]
