"""Static-drawdown challenge simulator (CFD firms such as FTMO / Blueberry Funded).

Model (all amounts in account USD; parameters come from a verified firm YAML):
  phases     sequence of evaluation phases, each with a profit target (vs the phase's starting
             balance), minimum trading days and an optional calendar time limit (0 = none).
  daily loss equity may never fall to (day-start balance - daily_loss). Day = our session
             (18:00 ET open = 00:00 CE(S)T, the usual CFD-firm reset).
  max loss   equity may never fall to (initial balance - max_loss): static, not trailing.
  funded     after the last phase: same loss rules on a fresh balance; every `payout_days`
             calendar days, profit above the initial balance is split (`split`) and withdrawn.
Pessimistic, like the Apex simulator: any touch of a limit (including open P&L) fails, and a
phase passes only on a session CLOSE at/above its target with enough trading days.
Input P&L is per "unit" (see the caller for what one unit means) with commissions/spread in.
"""

import numpy as np
from numba import njit, prange

PASS, FAIL, EXPIRED, NO_DATA = 1, 2, 3, 4


@njit(cache=True)
def _day(bal, floor_total, floor_day, size, d_close, d_low, a, b):
    """One session. Returns (balance, breached, traded)."""
    traded = False
    for i in range(a, b):
        if d_close[i] != 0.0 or d_low[i] != 0.0:
            traded = True
        lo = bal + d_low[i] * size
        if lo <= floor_total or lo <= floor_day:
            return min(floor_total, floor_day), True, True
        bal += d_close[i] * size
    return bal, False, traded


@njit(cache=True)
def sim_phase(d_close, d_low, sess_start, sess_day, s0, size, start, target, daily_loss,
              max_loss, min_days, time_limit):  # fmt: skip
    """Returns (outcome, last_session, sessions_used)."""
    bal, days = start, 0
    floor_total = start - max_loss
    n = len(sess_start) - 1
    for s in range(s0, n):
        if time_limit > 0 and sess_day[s] - sess_day[s0] >= time_limit:
            return EXPIRED, s, s - s0
        bal, breached, traded = _day(bal, floor_total, bal - daily_loss, size[s], d_close,
                                     d_low, sess_start[s], sess_start[s + 1])  # fmt: skip
        if breached:
            return FAIL, s, s - s0 + 1
        if traded:
            days += 1
        if bal >= start + target and days >= min_days:
            return PASS, s, s - s0 + 1
    return NO_DATA, n, n - s0


@njit(cache=True)
def sim_funded(d_close, d_low, sess_start, sess_day, s1, size, start, daily_loss, max_loss,
               split, payout_days, horizon_days):  # fmt: skip
    """Returns (outcome, payouts, total_paid_to_trader, first_payout_session)."""
    bal = start
    floor_total = start - max_loss
    n = len(sess_start) - 1
    k, paid, first = 0, 0.0, -1
    last_pay_day = sess_day[s1] if s1 < n else 0
    for s in range(s1, n):
        if sess_day[s] - sess_day[s1] >= horizon_days:
            return NO_DATA, k, paid, first
        bal, breached, _ = _day(bal, floor_total, bal - daily_loss, size[s], d_close, d_low,
                                sess_start[s], sess_start[s + 1])  # fmt: skip
        if breached:
            return FAIL, k, paid, first
        if sess_day[s] - last_pay_day >= payout_days and bal > start:
            paid += (bal - start) * split
            bal = start
            k += 1
            last_pay_day = sess_day[s]
            if first < 0:
                first = s
    return NO_DATA, k, paid, first


@njit(parallel=True, cache=True)
def run_many(d_close, d_low, sess_start, sess_day, starts, size, start, targets, min_days,
             time_limits, daily_loss, max_loss, split, payout_days, horizon_days):  # fmt: skip
    """One purchased challenge per start. Columns: outcome (PASS = all phases), sessions used
    for the evaluation, payouts, paid, sessions to first payout."""
    m = len(starts)
    out = np.zeros((m, 5))
    for j in prange(m):
        s = starts[j]
        used = 0
        res = PASS
        for ph in range(len(targets)):
            res, s_end, u = sim_phase(d_close, d_low, sess_start, sess_day, s, size, start,
                                      targets[ph], daily_loss, max_loss, min_days[ph],
                                      time_limits[ph])  # fmt: skip
            used += u
            if res != PASS:
                break
            s = s_end + 1
        out[j, 0], out[j, 1] = res, used
        if res == PASS:
            _r, k, paid, first = sim_funded(d_close, d_low, sess_start, sess_day, s, size, start,
                                            daily_loss, max_loss, split, payout_days,
                                            horizon_days)  # fmt: skip
            out[j, 2], out[j, 3] = k, paid
            out[j, 4] = first - starts[j] if first >= 0 else -1
    return out
