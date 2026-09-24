"""Benchmarks a strategy must beat: random entries with the same exits, and buy-and-hold."""
from __future__ import annotations

import math

import numpy as np

from .engine import Costs, simulate


def random_entry_pvalue(bars: np.ndarray, direction: np.ndarray, sl: np.ndarray, tp: np.ndarray,
                        max_bars: int, costs: Costs, start: int, end: int, actual_exp_r: float,
                        runs: int = 500, seed: int = 11) -> dict:
    """Keep the strategy's stop/target sizing and signal frequency, randomise timing and side.

    p-value = share of random runs whose expectancy (R) >= the strategy's.
    """
    rng = np.random.default_rng(seed)
    eligible = np.zeros(len(bars), dtype=bool)
    eligible[start:end] = sl[start:end] > 0
    n_elig = int(eligible.sum())
    n_sig = int(np.count_nonzero(direction[start:end]))
    if n_elig == 0 or n_sig == 0:
        return {"p_value": 1.0, "random_exp_mean": 0.0, "runs": 0}
    p = n_sig / n_elig
    exps = np.empty(runs)
    for k in range(runs):
        pick = eligible & (rng.random(len(bars)) < p)
        d = np.where(pick, rng.choice(np.array([-1, 1], dtype=np.int8), len(bars)), 0).astype(np.int8)
        trades = simulate(bars, d, sl, tp, max_bars, costs, start, end)
        exps[k] = np.mean([t.r for t in trades]) if trades else 0.0
    return {"p_value": float((np.sum(exps >= actual_exp_r) + 1) / (runs + 1)),
            "random_exp_mean": float(exps.mean()), "random_exp_p95": float(np.percentile(exps, 95)),
            "runs": runs}


def buy_hold_sharpe(bars: np.ndarray, start: int, end: int) -> float:
    """Annualised Sharpe of holding the asset over [start, end), from daily closes."""
    t = bars["time"][start:end]
    c = bars["close"][start:end]
    if len(c) < 3:
        return 0.0
    day = t // 86400
    last = np.flatnonzero(np.diff(day)) if len(day) > 1 else np.array([], dtype=int)
    closes = np.concatenate((c[last], c[-1:]))
    rets = np.diff(np.log(closes))
    if len(rets) < 2 or rets.std(ddof=1) == 0:
        return 0.0
    return float(rets.mean() / rets.std(ddof=1) * math.sqrt(365.25 if _is_24_7(day) else 252))


def _is_24_7(day: np.ndarray) -> bool:
    # Crypto trades weekends; FX/CFDs don't. Weekday of epoch day: (day + 3) % 7, 5/6 = Sat/Sun.
    return bool(np.any(((np.unique(day) + 3) % 7) >= 5))
