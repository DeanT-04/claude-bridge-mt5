"""Random-entry benchmark: could the same trading *pattern* make this money by chance?

Each run keeps every OOS trade's session and holding time, but draws a random entry bar inside
the strategy's own entry window (minutes of day) and a random direction. Costs are charged the
same way. The strategy's total OOS P&L is ranked against these runs.
"""

import numpy as np
from numba import njit, prange

from propquant.engine.backtest import session_minutes

# numba only supports the legacy global RNG inside jitted code (seeded per run below).
# ruff: noqa: NPY002


@njit(parallel=True, cache=True)
def _runs(open_, close, minute, sess, sess_start, entry_i, exit_i, lo_min, hi_min, flat_minute,
          point_value, cost_rt, runs, seed):  # fmt: skip
    out = np.zeros(runs)
    m = len(entry_i)
    for r in prange(runs):
        np.random.seed(seed + r)
        total = 0.0
        for k in range(m):
            s = sess[entry_i[k]]
            a, b = sess_start[s], sess_start[s + 1]
            hold = exit_i[k] - entry_i[k]
            j = -1
            for _ in range(64):
                c = np.random.randint(a, b)
                if lo_min <= minute[c] <= hi_min and minute[c] < flat_minute:
                    j = c
                    break
            if j < 0:
                j = entry_i[k]
            e = j + hold
            while e > j and (e >= b or minute[e] >= flat_minute):
                e -= 1
            d = 1.0 if np.random.random() < 0.5 else -1.0
            total += (close[e] - open_[j]) * d * point_value - cost_rt
        out[r] = total
    return out


def benchmark(md, trades: np.ndarray, point_value: float, cost_rt: float, runs: int, seed: int,
              flat_minute: int) -> np.ndarray:  # fmt: skip
    """Total P&L of each random run (USD per micro)."""
    if len(trades) == 0:
        return np.zeros(runs)
    entry_i = trades[:, 0].astype(np.int64)
    exit_i = trades[:, 1].astype(np.int64)
    smin = session_minutes(md.minute)
    mins = smin[entry_i]
    return _runs(
        md.open, md.close, smin, md.sess, md.sess_start, entry_i, exit_i,
        int(mins.min()), int(mins.max()), int(session_minutes(flat_minute)), point_value,
        cost_rt, runs, seed,
    )  # fmt: skip


def percentile(strategy_total: float, runs: np.ndarray) -> float:
    """Share of random runs the strategy beat."""
    return float(np.mean(runs < strategy_total))
