"""Portfolio construction across sleeves: correlation, risk allocation, combined Monte Carlo.

Sleeves are combined on calendar days in R units, then risk-weighted. The R series are each
gauntlet's walk-forward OOS trades over the sleeves' common OOS period; only gauntlets from
before those were stored fall back to re-running the tuned params (in-sample, optimistic).
"""
from __future__ import annotations

import math

import numpy as np

from bridge import config

from . import data
from .gauntlet import _month_ts, costs_for
from .strategies import FAMILIES, get_family

DAY = 86400


def _month_back(ts: int, months: int) -> int:
    return _month_ts(ts, -months)


def oos_matrix(sleeves: list[dict]) -> tuple[np.ndarray, np.ndarray] | None:
    """(days, R matrix) from the sleeves' stored walk-forward OOS trades over their common OOS
    period, or None if any sleeve lacks them or the periods don't overlap."""
    from registry import db
    from .challenge import daily_matrix, load_sleeves, overlap
    if not all("id" in s for s in sleeves):
        return None
    oos = load_sleeves(db.connect(), [s["id"] for s in sleeves])
    if len(oos) != len(sleeves):
        return None
    lo, hi = overlap(oos)
    if hi - lo < 30 * DAY:
        return None
    return np.arange(lo // DAY, hi // DAY + 1), daily_matrix(oos, lo, hi)


def daily_r_matrix(sleeves: list[dict], years: float = 3.0) -> tuple[np.ndarray, np.ndarray]:
    """(days, R matrix [days x sleeves]) from tuned params over the window every sleeve's data
    covers (fallback when OOS trades aren't stored)."""
    series, lo, hi = [], -math.inf, math.inf
    for s in sleeves:
        fam = get_family(s["family"])
        bars = data.bars(s["symbol"], s["timeframe"])
        # Stop where the gauntlet's holdout begins: allocation must not peek at it.
        end = _month_back(int(bars["time"][-1]), config.settings()["research"]["holdout_months"])
        lo, hi = max(lo, end - years * 365.25 * DAY), min(hi, end)
        p = fam.Params(**{k: v for k, v in s["params"].items() if k in fam.Params.__dataclass_fields__})
        series.append((bars, fam, p))
    days = np.arange(int(lo // DAY), int(hi // DAY) + 1)
    mat = np.zeros((len(days), len(sleeves)))
    for j, (bars, fam, p) in enumerate(series):
        start = int(np.searchsorted(bars["time"], lo))
        stop = int(np.searchsorted(bars["time"], hi + DAY))
        for t in fam.backtest(bars, p, costs_for(data.spec(sleeves[j]["symbol"])), start, stop):
            k = t.exit_time // DAY - days[0]
            if 0 <= k < len(days):
                mat[k, j] += t.r
    return days, mat


def allocate(mat: np.ndarray, max_risks: np.ndarray, budget: float, dd95_max: float,
             runs: int = 2000, seed: int = 5) -> dict:
    """Inverse-volatility weights scaled to the open-risk budget, each capped by its own
    (gauntlet) risk, then shrunk until the portfolio's bootstrap 95th-pct drawdown fits."""
    vol = mat.std(axis=0, ddof=1)
    w = np.where(vol > 0, 1 / np.where(vol > 0, vol, 1), 0)
    risks = np.minimum(w / w.sum() * budget if w.sum() > 0 else w, max_risks)
    rng = np.random.default_rng(seed)
    for _ in range(40):
        daily = mat @ risks
        idx = rng.integers(0, len(daily), size=(runs, len(daily)))
        eq = np.cumprod(1 + daily[idx], axis=1)
        dd = np.max(1 - eq / np.maximum.accumulate(eq, axis=1), axis=1)
        dd95 = float(np.percentile(dd, 95))
        if dd95 <= dd95_max:
            break
        risks *= 0.85
    daily = mat @ risks
    sd = daily.std(ddof=1)
    return {"risks": risks, "portfolio_sharpe": float(daily.mean() / sd * math.sqrt(365.25)) if sd > 0 else 0.0,
            "dd95": dd95, "annual_return": float(np.prod(1 + daily) ** (365.25 / len(daily)) - 1)}


def build(sleeves: list[dict], budget_pct: float, dd95_max: float, years: float = 3.0) -> dict:
    """sleeves: dicts with family/symbol/timeframe/params/risk_pct. Returns allocation + stats."""
    oos = oos_matrix(sleeves)
    days, mat = oos if oos else daily_r_matrix(sleeves, years)
    corr = np.corrcoef(mat.T) if len(sleeves) > 1 else np.ones((1, 1))
    caps = np.array([s.get("risk_pct", budget_pct) / 100 for s in sleeves])
    res = allocate(mat, caps, budget_pct / 100, dd95_max)
    per = []
    for j, s in enumerate(sleeves):
        col = mat[:, j]
        sd = col.std(ddof=1)
        per.append({"sleeve": f"{s['family']} {s['symbol']} {s['timeframe']}",
                    "risk_pct": round(float(res["risks"][j]) * 100, 4),
                    "sharpe": float(col.mean() / sd * math.sqrt(365.25)) if sd > 0 else 0.0})
    return {"days": len(days), "source": "walk-forward OOS" if oos else "tuned params (in-sample)",
            "sleeves": per, "correlation": np.round(corr, 3).tolist(),
            "portfolio_sharpe": res["portfolio_sharpe"], "dd95": res["dd95"],
            "annual_return": res["annual_return"]}
