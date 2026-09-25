"""Prop-firm challenge simulation.

Monte Carlo over a strategy's own trade days: each simulated day is a real historical day's
trade sequence (bootstrapped), applied trade by trade so intraday breaches are caught. The
simulator checks the daily loss limit (vs start-of-day balance/equity/max), the static or
trailing max drawdown, the profit target with minimum trading days, and the time limit.

It answers: at risk r per trade, P(pass), P(fail), expected days, and the r that maximises
P(pass). That differs from growth-optimal (Kelly) sizing.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import numpy as np
import yaml

from bridge import config

from .engine import Trade

MAX_SIM_DAYS = 250          # cap for 'unlimited' challenges (about one trading year)


@dataclass(frozen=True)
class Profile:
    name: str
    account_size: float
    profit_target_pct: float
    max_daily_loss_pct: float
    daily_loss_basis: str
    max_total_dd_pct: float
    max_dd_mode: str
    min_trading_days: int
    max_days: int
    weekend_flat_hour: int
    news_blackout_min: int
    description: str = ""


@lru_cache
def profiles() -> dict[str, Profile]:
    raw = yaml.safe_load((config.CONFIG_DIR / "propfirms.yaml").read_text(encoding="utf-8"))
    return {k: Profile(name=k, **v) for k, v in raw.items()}


def trade_days(trades: list[Trade], calendar_days: float) -> tuple[list[np.ndarray], float]:
    """Group R-multiples by exit day. Returns (non-empty days, share of trading days that had trades)."""
    if not trades:
        return [], 0.0
    days: dict[int, list[float]] = {}
    for t in trades:
        days.setdefault(t.exit_time // 86400, []).append(t.r)
    trading_days = max(calendar_days * 5 / 7, 1)
    return [np.array(v) for _, v in sorted(days.items())], min(len(days) / trading_days, 1.0)


def simulate(days: list[np.ndarray], active_share: float, profile: Profile, risk: float,
             runs: int = 3000, seed: int = 11) -> dict:
    """risk = fraction of CURRENT equity risked per trade (as QB_Host sizes)."""
    rng = np.random.default_rng(seed)
    p = profile
    horizon = p.max_days or MAX_SIM_DAYS
    target = 1 + p.profit_target_pct / 100 if p.profit_target_pct > 0 else None
    dl, dd = p.max_daily_loss_pct / 100, p.max_total_dd_pct / 100
    passed = failed = 0
    days_to_pass, fail_reasons = [], {"daily": 0, "total": 0, "timeout": 0}
    n_days = len(days)
    if n_days == 0:
        return {"pass_prob": 0.0, "fail_prob": 1.0, "reason": "no trades"}
    for _ in range(runs):
        eq = bal = 1.0
        peak = 1.0
        traded = 0
        outcome = None
        for d in range(horizon):
            sod = {"balance": bal, "equity": eq, "max": max(bal, eq)}[p.daily_loss_basis]
            floor_day = sod - dl * 1.0           # limits are % of the initial balance (1.0)
            if rng.random() < active_share:
                traded += 1
                for r in days[rng.integers(n_days)]:
                    eq *= 1 + risk * r
                    floor_total = (1 - dd) if p.max_dd_mode == "static" else peak - dd
                    if eq <= floor_day:
                        outcome = "daily"; break
                    if eq <= floor_total:
                        outcome = "total"; break
                    peak = max(peak, eq)
                bal = eq                          # trades are closed intraday
                if outcome:
                    break
            if target and eq >= target and traded >= p.min_trading_days:
                outcome = "pass"; break
        if outcome is None:
            outcome = "pass" if target is None else "timeout"   # no-target profile = survive the horizon
        if outcome == "pass":
            passed += 1
            days_to_pass.append(d + 1)
        else:
            failed += 1
            fail_reasons[outcome] += 1
    return {"pass_prob": passed / runs, "fail_prob": failed / runs,
            "median_days_to_pass": float(np.median(days_to_pass)) if days_to_pass else None,
            "fail_breakdown": {k: v / runs for k, v in fail_reasons.items()}, "risk_pct": risk * 100}


def sleeve_days(sleeves: list[dict], years: float = 3.0) -> tuple[list[np.ndarray], float, float]:
    """Trade days for a set of sleeves on pre-holdout data (holdouts stay untouched).
    Each sleeve's R is weighted by its risk relative to the largest, so `risk` in simulate()
    means the largest sleeve's risk per trade. Returns (days, active_share, weight_sum)."""
    from . import data
    from .gauntlet import _month_ts, costs_for
    from .strategies import get_family
    per_day: dict[int, list[tuple[int, float]]] = {}
    top = max(s.get("risk_pct", 1.0) for s in sleeves)
    span = 0.0
    for s in sleeves:
        fam = get_family(s["family"])
        bars = data.bars(s["symbol"], s["timeframe"])
        end_t = _month_ts(int(bars["time"][-1]), -config.settings()["research"]["holdout_months"])
        a = int(np.searchsorted(bars["time"], end_t - years * 365.25 * 86400))
        z = int(np.searchsorted(bars["time"], end_t))
        span = max(span, (bars["time"][z - 1] - bars["time"][a]) / 86400)
        p = fam.Params(**{k: v for k, v in s["params"].items() if k in fam.Params.__dataclass_fields__})
        w = s.get("risk_pct", 1.0) / top
        for t in fam.backtest(bars, p, costs_for(data.spec(s["symbol"])), a, z):
            per_day.setdefault(t.exit_time // 86400, []).append((t.exit_time, t.r * w))
    days = [np.array([r for _, r in sorted(v)]) for _, v in sorted(per_day.items())]
    active = min(len(days) / max(span * 5 / 7, 1), 1.0)
    return days, active, top


def best_risk(days: list[np.ndarray], active_share: float, profile: Profile,
              grid_pct: tuple = (0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0), runs: int = 2000) -> dict:
    """Risk per trade that maximises P(pass), with the whole curve for context."""
    curve = [simulate(days, active_share, profile, r / 100, runs) for r in grid_pct]
    best = max(curve, key=lambda x: (x["pass_prob"], -x["risk_pct"]))
    return {"profile": profile.name, "best": best, "curve": [{"risk_pct": c["risk_pct"],
            "pass_prob": c["pass_prob"], "median_days": c.get("median_days_to_pass")} for c in curve]}
