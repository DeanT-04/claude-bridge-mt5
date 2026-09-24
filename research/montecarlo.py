"""Monte Carlo on trade sequences: bootstrap resampling with random skipped trades."""
from __future__ import annotations

import numpy as np


def simulate_drawdowns(r: np.ndarray, risk: float, runs: int = 2000, skip_prob: float = 0.05,
                       ruin_dd: float = 0.5, seed: int = 7) -> dict:
    """Resample trades with replacement (same count), drop each with skip_prob.

    Returns percentile max-drawdowns, final-equity percentiles and P(max DD >= ruin_dd).
    """
    rng = np.random.default_rng(seed)
    n = len(r)
    if n == 0:
        return {"dd_p50": 0.0, "dd_p95": 0.0, "dd_p99": 0.0, "ruin_prob": 0.0,
                "final_p5": 1.0, "final_p50": 1.0}
    idx = rng.integers(0, n, size=(runs, n))
    rr = r[idx] * (rng.random((runs, n)) >= skip_prob)
    eq = np.cumprod(1.0 + risk * rr, axis=1)
    eq = np.concatenate((np.ones((runs, 1)), eq), axis=1)
    peak = np.maximum.accumulate(eq, axis=1)
    dd = np.max(1.0 - eq / peak, axis=1)
    final = eq[:, -1]
    return {
        "dd_p50": float(np.percentile(dd, 50)), "dd_p95": float(np.percentile(dd, 95)),
        "dd_p99": float(np.percentile(dd, 99)), "ruin_prob": float(np.mean(dd >= ruin_dd)),
        "final_p5": float(np.percentile(final, 5)), "final_p50": float(np.percentile(final, 50)),
    }
