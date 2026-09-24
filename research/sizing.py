"""Position sizing from the measured R distribution, and small-account feasibility."""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize_scalar

from .montecarlo import simulate_drawdowns


def kelly_fraction(r: np.ndarray) -> float:
    """Growth-optimal risk fraction: argmax_f mean(log(1 + f*R)). 0 if no edge."""
    if len(r) == 0 or r.mean() <= 0:
        return 0.0
    worst = r.min()
    hi = 0.99 / -worst if worst < 0 else 1.0
    res = minimize_scalar(lambda f: -np.mean(np.log1p(f * r)), bounds=(0.0, hi), method="bounded")
    return float(max(res.x, 0.0))


def choose_risk(r: np.ndarray, cfg: dict, dd95_max: float) -> dict:
    """Fractional Kelly, clamped to [min,max] risk %, then reduced until MC dd_p95 <= dd95_max."""
    k = kelly_fraction(r)
    risk = min(k * cfg["kelly_fraction"], cfg["max_risk_pct"] / 100)
    if risk < cfg["min_risk_pct"] / 100:
        return {"kelly": k, "risk": 0.0, "reason": "edge too small for minimum risk"}
    while risk >= cfg["min_risk_pct"] / 100:
        mc = simulate_drawdowns(r, risk, runs=500)
        if mc["dd_p95"] <= dd95_max:
            return {"kelly": k, "risk": risk, "mc_dd_p95": mc["dd_p95"]}
        risk *= 0.8
    return {"kelly": k, "risk": 0.0, "reason": "drawdown cap unreachable at minimum risk"}


def min_lot_risk_pct(spec: dict, stop_dist: float, balance: float, acct_per_quote: float = 1.0) -> float:
    """Risk % of `balance` implied by trading the minimum lot with a given stop distance.

    spec: from mt5_client.symbol_spec (tick_size, tick_value in the *terminal account* currency).
    acct_per_quote: converts the terminal account currency to the target account currency
    (e.g. USD->GBP when the demo is USD but the target live account is GBP).
    """
    loss = stop_dist / spec["tick_size"] * spec["tick_value"] * spec["volume_min"] * acct_per_quote
    return 100.0 * loss / balance


def feasibility(spec: dict, stop_dists: np.ndarray, risk: float, balance: float,
                acct_per_quote: float = 1.0) -> dict:
    """Share of trades whose min-lot risk exceeds the chosen risk (those would be skipped)."""
    if len(stop_dists) == 0:
        return {"feasible": False, "skipped_share": 1.0}
    pct = np.array([min_lot_risk_pct(spec, s, balance, acct_per_quote) for s in stop_dists])
    skipped = float(np.mean(pct > risk * 100 + 1e-9))
    return {"feasible": skipped <= 0.1, "skipped_share": skipped,
            "min_lot_risk_pct_median": float(np.median(pct))}
