"""Prop-account simulator: evaluation -> performance account (PA) -> payouts.

Input is a strategy's per-bar P&L for ONE micro contract (commissions already deducted):
  d_close[i]  equity change from the previous bar's close to this bar's close
  d_low[i]    worst equity point inside bar i, relative to the previous close (<= min(0, d_close))
  d_high[i]   best equity point inside bar i, relative to the previous close (>= max(0, d_close))
plus session boundaries ``sess_start`` (bar index where each session starts; one extra entry
at the end) and ``sess_day`` (calendar day number of each session).

Pessimistic by construction:
  - Intraday trailing: inside a bar the peak is assumed to happen BEFORE the trough.
  - Any touch of the threshold (including unrealised P&L) fails / closes the account.
  - A daily-loss-limit hit liquidates exactly at the limit and ends the session.
  - The eval passes only if the session CLOSE balance reaches the target.
"""

import numpy as np
from numba import njit, prange

from propquant.firms.base import TRAIL_INTRADAY, ChallengeSpec

OK, DLL_HIT, BREACH = 0, 1, 2
# Evaluation outcomes
PASS, FAIL, EXPIRED, NO_DATA = 1, 2, 3, 4
# PA outcomes (FAIL/NO_DATA reused)
MAXED = 5


@njit(cache=True)
def _session(bal, thr, peak, trail, cap, dd, dll, size, d_close, d_low, d_high, a, b):
    day_start = bal
    for i in range(a, b):
        lo = bal + d_low[i] * size
        if trail == TRAIL_INTRADAY:
            hi = bal + d_high[i] * size
            if hi > peak:
                peak = hi
            t = min(peak - dd, cap)
            if t > thr:
                thr = t
        if dll > 0.0:
            lvl = day_start - dll
            if lo <= lvl and lvl > thr:
                return lvl, thr, peak, DLL_HIT
        if lo <= thr:
            return thr, thr, peak, BREACH
        bal += d_close[i] * size
    return bal, thr, peak, OK


NO_POLICY = (0.0, 0.0, 0.0)  # (alpha, beta, mu): fixed sizing


@njit(cache=True)
def _policy_size(base, bal, thr, dd, remaining, days_left, pol, max_micros):
    """Size for the coming session from account state known at the open.

    alpha: size x (cushion / max drawdown)^alpha, trading smaller near the threshold.
    beta:  if the expected profit over the days left (mu x size x trading days) falls short of
           the remaining target, scale up by (shortfall ratio)^beta, capped at 3x.
    mu:    expected daily P&L per micro, estimated on TRAINING data only.
    """
    alpha, beta, mu = pol[0], pol[1], pol[2]
    f = 1.0
    if alpha > 0.0:
        c = max(bal - thr, 0.0) / dd
        f *= min(c, 1.5) ** alpha
    if beta > 0.0 and mu > 0.0 and remaining > 0.0 and days_left > 0:
        expected = mu * base * max(days_left * 5.0 / 7.0, 1.0)
        if expected < remaining:
            f *= min(remaining / expected, 3.0) ** beta
    sz = int(round(base * f))  # noqa: RUF046 (numba needs the explicit int)
    return max(1, min(sz, max_micros))


@njit(cache=True)
def sim_eval(d_close, d_low, d_high, sess_start, sess_day, s0, size, start, target, dd, dll,
             max_micros, trail, cap, access_days, pol):  # fmt: skip
    """Returns (outcome, last_session, sessions_used, largest_day_share_of_profit).

    ``size`` is the number of micros per session (array, one entry per session).
    """
    bal, thr, peak = start, start - dd, start
    best_day = 0.0
    n = len(sess_start) - 1
    for s in range(s0, n):
        if sess_day[s] - sess_day[s0] >= access_days:
            return EXPIRED, s, s - s0, 0.0
        day_start = bal
        days_left = access_days - (sess_day[s] - sess_day[s0])
        sz = _policy_size(size[s], bal, thr, dd, start + target - bal, days_left, pol[s],
                          max_micros)  # fmt: skip
        bal, thr, peak, code = _session(
            bal, thr, peak, trail, cap, dd, dll, sz, d_close, d_low, d_high,
            sess_start[s], sess_start[s + 1],
        )  # fmt: skip
        if code == BREACH:
            return FAIL, s, s - s0 + 1, 0.0
        best_day = max(best_day, bal - day_start)
        if trail != TRAIL_INTRADAY:
            thr = max(thr, min(bal - dd, cap))
        if bal >= start + target:
            return PASS, s, s - s0 + 1, best_day / (bal - start)
    return NO_DATA, n, n - s0, 0.0


@njit(cache=True)
def sim_pa(d_close, d_low, d_high, sess_start, s1, size, start, dd, trail, cap, tier_from,
           tier_micros, tier_dll, min_daily, min_days, consistency, min_amount, caps,
           safety_net, pol):  # fmt: skip
    """Returns (outcome, payouts, total_paid, first_payout_session, last_session, balance)."""
    bal, thr, peak = start, start - dd, start
    base, qual, best_day = start, 0, 0.0
    k, paid, first = 0, 0.0, -1
    n = len(sess_start) - 1
    for s in range(s1, n):
        tier = 0
        for t in range(len(tier_from)):
            if bal - start >= tier_from[t]:
                tier = t
        # in the PA only cushion scaling applies (no deadline)
        sz = _policy_size(size[s], bal, thr, dd, 0.0, 0, pol[s], tier_micros[tier])
        day_start = bal
        bal, thr, peak, code = _session(
            bal, thr, peak, trail, cap, dd, tier_dll[tier], sz, d_close, d_low, d_high,
            sess_start[s], sess_start[s + 1],
        )  # fmt: skip
        if code == BREACH:
            return FAIL, k, paid, first, s, bal
        day = bal - day_start
        if day >= min_daily:
            qual += 1
        if day > best_day:
            best_day = day
        if trail != TRAIL_INTRADAY:
            thr = max(thr, min(bal - dd, cap))
        net = bal - base
        if (
            qual >= min_days
            and net > 0.0
            and best_day / net < consistency
            and bal >= safety_net + min_amount
        ):
            amount = min(caps[k], bal - safety_net)
            bal -= amount
            paid += amount
            k += 1
            if first < 0:
                first = s
            base, qual, best_day = bal, 0, 0.0
            if k == len(caps):
                return MAXED, k, paid, first, s, bal
    return NO_DATA, k, paid, first, n, bal


@njit(parallel=True, cache=True)
def _run_many(d_close, d_low, d_high, sess_start, sess_day, starts, size, e_args, p_args,
              tier_from, tier_micros, tier_dll, caps, pol):  # fmt: skip
    m = len(starts)
    out = np.zeros((m, 9))
    start, target, dd, dll, max_micros, e_trail, e_cap, access = e_args
    p_trail, p_cap, min_daily, min_days, consistency, min_amount, safety = p_args
    for j in prange(m):
        e, s_end, used, share = sim_eval(
            d_close, d_low, d_high, sess_start, sess_day, starts[j], size, start, target, dd,
            dll, int(max_micros), int(e_trail), e_cap, int(access), pol,
        )  # fmt: skip
        out[j, 0], out[j, 1], out[j, 2] = e, used, share
        if e == PASS:
            p, k, paid, first, last, _bal = sim_pa(
                d_close, d_low, d_high, sess_start, s_end + 1, size, start, dd, int(p_trail),
                p_cap, tier_from, tier_micros, tier_dll, min_daily, int(min_days), consistency,
                min_amount, caps, safety, pol,
            )  # fmt: skip
            out[j, 3], out[j, 4], out[j, 5] = p, k, paid
            out[j, 6] = first - s_end if first >= 0 else -1
            out[j, 7] = last - s_end
        out[j, 8] = s_end
    return out


COLUMNS = (
    "eval_outcome",
    "eval_sessions",
    "eval_best_day_share",
    "pa_outcome",
    "payouts",
    "paid",
    "sessions_to_first_payout",
    "pa_sessions",
    "eval_end_session",
)


def policy_rows(n_sessions: int, policy) -> np.ndarray:
    """(alpha, beta, mu) per session: a tuple for all sessions or an (n, 3) array."""
    return np.ascontiguousarray(
        np.broadcast_to(np.asarray(policy, dtype=np.float64), (n_sessions, 3))
    )


def run_many(pnl: dict[str, np.ndarray], starts: np.ndarray, size_micros, spec: ChallengeSpec,
             policy=NO_POLICY):  # fmt: skip
    """Simulate one purchased challenge per start session. Returns an (m, 9) array (COLUMNS).

    ``size_micros``: an int, or an array with one size per session (walk-forward folds).
    ``policy``: (alpha, beta, mu) for challenge-aware sizing, or one row per session.
    """
    n_sess = len(pnl["sess_start"]) - 1
    sizes = np.broadcast_to(np.asarray(size_micros, dtype=np.int64), (n_sess,)).copy()
    tier_from, tier_micros, tier_dll = spec.tiers()
    e_args = (
        spec.balance, spec.target, spec.drawdown, spec.eval_dll, float(spec.eval_max_micros),
        float(spec.eval_trail), spec.eval_trail_cap, float(spec.access_days),
    )  # fmt: skip
    p_args = (
        float(spec.pa_trail), spec.pa_trail_cap, spec.min_daily_profit,
        float(spec.payout_min_days), spec.payout_consistency, spec.payout_min_amount,
        spec.safety_net,
    )  # fmt: skip
    return _run_many(
        pnl["d_close"], pnl["d_low"], pnl["d_high"], pnl["sess_start"], pnl["sess_day"],
        np.asarray(starts, dtype=np.int64), sizes, e_args, p_args,
        tier_from, tier_micros, tier_dll, np.asarray(spec.payout_caps, dtype=np.float64),
        policy_rows(n_sess, policy),
    )  # fmt: skip


@njit(cache=True)
def eval_path(d_close, d_low, d_high, sess_start, sess_day, s0, size, start, target, dd, dll,
              max_micros, trail, cap, access_days, pol):  # fmt: skip
    """Same rules as ``sim_eval`` but records the closing balance and threshold each session.

    Report-only (fan charts). A test pins it to ``sim_eval``'s outcome.
    """
    bal_out = np.full(access_days + 1, np.nan)
    thr_out = np.full(access_days + 1, np.nan)
    bal, thr, peak = start, start - dd, start
    bal_out[0], thr_out[0] = bal, thr
    n = len(sess_start) - 1
    k = 0
    for s in range(s0, n):
        if sess_day[s] - sess_day[s0] >= access_days:
            return EXPIRED, bal_out, thr_out
        days_left = access_days - (sess_day[s] - sess_day[s0])
        sz = _policy_size(size[s], bal, thr, dd, start + target - bal, days_left, pol[s],
                          max_micros)  # fmt: skip
        bal, thr, peak, code = _session(
            bal, thr, peak, trail, cap, dd, dll, sz, d_close, d_low, d_high,
            sess_start[s], sess_start[s + 1],
        )  # fmt: skip
        k += 1
        if trail != TRAIL_INTRADAY:
            thr = max(thr, min(bal - dd, cap))
        if k <= access_days:
            bal_out[k], thr_out[k] = bal, thr
        if code == BREACH:
            return FAIL, bal_out, thr_out
        if bal >= start + target:
            return PASS, bal_out, thr_out
    return NO_DATA, bal_out, thr_out
