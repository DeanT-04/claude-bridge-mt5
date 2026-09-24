"""Performance metrics on R-multiple trade series, plus the Deflated Sharpe Ratio."""
from __future__ import annotations

import math

import numpy as np
from scipy import stats as st

from .engine import Trade

SECONDS_PER_YEAR = 365.25 * 86400


def daily_r(trades: list[Trade]) -> tuple[np.ndarray, np.ndarray]:
    """Sum of R per UTC day of exit -> (day_index, r). Days without trades are omitted."""
    if not trades:
        return np.zeros(0, dtype=np.int64), np.zeros(0)
    days = np.array([tr.exit_time // 86400 for tr in trades])
    r = np.array([tr.r for tr in trades])
    u, inv = np.unique(days, return_inverse=True)
    return u, np.bincount(inv, weights=r)


def equity_curve(r: np.ndarray, risk: float) -> np.ndarray:
    """Compounded equity (start 1.0) risking `risk` fraction per trade."""
    return np.cumprod(1.0 + risk * r) if len(r) else np.ones(0)


def max_drawdown(equity: np.ndarray) -> float:
    if len(equity) == 0:
        return 0.0
    eq = np.concatenate(([1.0], equity))
    peak = np.maximum.accumulate(eq)
    return float(np.max(1.0 - eq / peak))


def metrics(trades: list[Trade], risk: float = 0.01, span_days: float | None = None) -> dict:
    r = np.array([tr.r for tr in trades], dtype=float)
    n = len(r)
    if n == 0:
        return {"trades": 0, "expectancy_r": 0.0, "profit_factor": 0.0, "sharpe": 0.0,
                "win_rate": 0.0, "max_dd": 0.0, "cagr": 0.0, "r_per_year": 0.0}
    wins, losses = r[r > 0].sum(), -r[r < 0].sum()
    pf = float(wins / losses) if losses > 0 else float("inf")
    if span_days is None:
        span_days = max((trades[-1].exit_time - trades[0].entry_time) / 86400, 1.0)
    years = span_days / 365.25
    # Sharpe on calendar days (zero-filled) so sparse strategies aren't flattered.
    _, dr = daily_r(trades)
    total_days = max(int(round(span_days)), len(dr))
    full = np.concatenate((dr, np.zeros(total_days - len(dr))))
    sd = full.std(ddof=1)
    sharpe = float(full.mean() / sd * math.sqrt(365.25)) if sd > 0 else 0.0
    eq = equity_curve(r, risk)
    cagr = float(eq[-1] ** (1 / years) - 1) if years > 0 and eq[-1] > 0 else -1.0
    return {
        "trades": n, "expectancy_r": float(r.mean()), "profit_factor": pf, "sharpe": sharpe,
        "win_rate": float((r > 0).mean()), "max_dd": max_drawdown(eq), "cagr": cagr,
        "r_per_year": float(r.sum() / years) if years > 0 else 0.0,
        "trades_per_year": n / years if years > 0 else 0.0,
    }


def trade_sharpe(r: np.ndarray) -> float:
    """Per-trade (non-annualised) Sharpe used by PSR/DSR."""
    if len(r) < 2 or r.std(ddof=1) == 0:
        return 0.0
    return float(r.mean() / r.std(ddof=1))


def probabilistic_sharpe(r: np.ndarray, sr_benchmark: float = 0.0) -> float:
    """P(true SR > benchmark) — Bailey & López de Prado (2012)."""
    n = len(r)
    if n < 3:
        return 0.0
    sr = trade_sharpe(r)
    skew = float(st.skew(r))
    kurt = float(st.kurtosis(r, fisher=False))
    denom = math.sqrt(max(1e-12, 1 - skew * sr + (kurt - 1) / 4 * sr * sr))
    return float(st.norm.cdf((sr - sr_benchmark) * math.sqrt(n - 1) / denom))


def expected_max_sharpe(n_trials: int, sr_variance: float) -> float:
    """Expected maximum SR among n_trials unskilled strategies (the DSR hurdle)."""
    if n_trials <= 1 or sr_variance <= 0:
        return 0.0
    g = 0.5772156649
    z1 = st.norm.ppf(1 - 1 / n_trials)
    z2 = st.norm.ppf(1 - 1 / (n_trials * math.e))
    return math.sqrt(sr_variance) * ((1 - g) * z1 + g * z2)


def deflated_sharpe(r: np.ndarray, n_trials: int, trial_sharpes: np.ndarray | None = None) -> dict:
    """DSR = PSR against the expected max SR given how many configurations were tried."""
    if trial_sharpes is not None and len(trial_sharpes) > 1:
        var = float(np.var(trial_sharpes, ddof=1))
    else:
        var = 1.0 / max(len(r) - 1, 1)   # SR sampling variance under the null
    hurdle = expected_max_sharpe(n_trials, var)
    return {"dsr": probabilistic_sharpe(r, hurdle), "sr_trade": trade_sharpe(r),
            "sr_hurdle": hurdle, "n_trials": n_trials}
