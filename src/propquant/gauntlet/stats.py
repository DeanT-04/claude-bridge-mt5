"""Performance statistics that account for luck and multiple testing.

PSR / DSR follow Bailey & Lopez de Prado, "The Deflated Sharpe Ratio" (2014). Sharpe ratios
here are per-period (daily) unless annualised explicitly.
"""

import numpy as np
from scipy import stats

EULER_GAMMA = 0.5772156649015329
TRADING_DAYS = 252


def sharpe(x: np.ndarray) -> float:
    s = np.std(x, ddof=1)
    return float(np.mean(x) / s) if s > 0 else 0.0


def annualised_sharpe(daily: np.ndarray) -> float:
    return sharpe(daily) * np.sqrt(TRADING_DAYS)


def psr(x: np.ndarray, sr_benchmark: float = 0.0) -> float:
    """P(true Sharpe > benchmark), correcting for sample length, skew and fat tails."""
    n = len(x)
    if n < 3:
        return 0.0
    sr = sharpe(x)
    g3 = stats.skew(x)
    g4 = stats.kurtosis(x, fisher=False)
    denom = np.sqrt(max(1 - g3 * sr + (g4 - 1) / 4 * sr**2, 1e-12))
    return float(stats.norm.cdf((sr - sr_benchmark) * np.sqrt(n - 1) / denom))


def expected_max_sharpe(n_trials: int, sr_variance: float) -> float:
    """Expected best per-period Sharpe among ``n_trials`` skill-less trials."""
    if n_trials <= 1 or sr_variance <= 0:
        return 0.0
    z1 = stats.norm.ppf(1 - 1 / n_trials)
    z2 = stats.norm.ppf(1 - 1 / (n_trials * np.e))
    return float(np.sqrt(sr_variance) * ((1 - EULER_GAMMA) * z1 + EULER_GAMMA * z2))


def dsr(x: np.ndarray, n_trials: int, sr_variance: float) -> float:
    """Deflated Sharpe: PSR against the Sharpe that luck alone would produce across trials."""
    return psr(x, expected_max_sharpe(n_trials, sr_variance))


def block_bootstrap_means(x: np.ndarray, n: int, block: int, seed: int) -> np.ndarray:
    """Stationary-ish moving-block bootstrap of the mean (keeps serial dependence)."""
    rng = np.random.default_rng(seed)
    m = len(x)
    if m == 0:
        return np.zeros(n)
    block = max(1, min(block, m))
    k = int(np.ceil(m / block))
    starts = rng.integers(0, m - block + 1, size=(n, k))
    idx = (starts[:, :, None] + np.arange(block)[None, None, :]).reshape(n, -1)[:, :m]
    return x[idx].mean(axis=1)
