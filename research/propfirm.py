"""Prop-firm challenge simulation.

Monte Carlo over a strategy's own trade days: each simulated day is a real historical day's
trade sequence (bootstrapped), applied trade by trade so intraday breaches are caught. Checks,
per phase: the daily loss limit (vs start-of-day balance/equity/max), the static or trailing
max drawdown, the profit target with minimum trading days, minimum profitable days, the
best-day consistency rule, and the time limit. 2-step programs must pass both phases, each
starting from the initial balance.

It answers: at risk r per trade, P(pass all phases), expected days, and the r that maximises
P(pass). That differs from growth-optimal (Kelly) sizing.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache

import numpy as np
import yaml

from bridge import config

from .engine import Trade

MAX_SIM_DAYS = 250          # cap for 'unlimited' phases (about one trading year)


@dataclass(frozen=True)
class Profile:
    name: str
    firm: str
    program: str
    phase_targets: tuple
    max_daily_loss_pct: float
    daily_loss_basis: str
    max_total_dd_pct: float
    max_dd_mode: str
    min_trading_days: int
    sizes: tuple = field(default_factory=tuple)          # ({"size": 50000, "fee": 299}, ...)
    fee_currency: str = "USD"
    trailing_locks_at_initial: bool = False
    min_profitable_days: int = 0
    profitable_day_pct: float = 0.0
    best_day_max_share: float = 0.0
    max_days: int = 0
    weekend_flat_hour: int = 0
    news_blackout_min: int = 0
    leverage: int = 100
    ea_policy: str = ""
    verify: tuple = field(default_factory=tuple)
    sources: tuple = field(default_factory=tuple)

    def size_options(self) -> list[float]:
        return [float(x["size"]) for x in self.sizes]

    def fee(self, size: float) -> float | None:
        """Fee for an account size (None if the size isn't offered or the fee is unpublished)."""
        for x in self.sizes:
            if float(x["size"]) == float(size):
                return x.get("fee")
        return None

    def default_size(self) -> float:
        """The research account size if offered, else the largest size not above it."""
        want = float(config.settings()["account"]["deposit"])
        opts = sorted(self.size_options())
        below = [x for x in opts if x <= want]
        return want if want in opts else (below[-1] if below else opts[0])


@lru_cache
def profiles() -> dict[str, Profile]:
    raw = yaml.safe_load((config.CONFIG_DIR / "propfirms.yaml").read_text(encoding="utf-8"))
    out = {}
    for k, v in raw.items():
        v = dict(v)
        for t in ("phase_targets", "verify", "sources", "sizes"):
            v[t] = tuple(v.get(t) or ())
        out[k] = Profile(name=k, **v)
    return out


def trade_days(trades: list[Trade]) -> list[np.ndarray]:
    """Group R-multiples by exit day, in time order within each day."""
    days: dict[int, list[tuple[int, float]]] = {}
    for t in trades:
        days.setdefault(t.exit_time // 86400, []).append((t.exit_time, t.r))
    return [np.array([r for _, r in sorted(v)]) for _, v in sorted(days.items())]


def _phase(days, n_days, active_share, p: Profile, target_pct: float, risk: float, rng) -> tuple[str, int]:
    """One phase from a fresh initial balance (1.0). Returns (outcome, calendar trading days)."""
    horizon = p.max_days or MAX_SIM_DAYS
    target = 1 + target_pct / 100
    dl, dd = p.max_daily_loss_pct / 100, p.max_total_dd_pct / 100
    eq = bal = peak = 1.0
    traded = profitable = 0
    day_profits: list[float] = []
    for d in range(horizon):
        sod = {"balance": bal, "equity": eq, "max": max(bal, eq)}[p.daily_loss_basis]
        floor_day = sod - dl
        start = eq
        if rng.random() < active_share:
            traded += 1
            for r in days[rng.integers(n_days)]:
                eq *= 1 + risk * r
                if p.max_dd_mode == "static":
                    floor_total = 1 - dd
                else:
                    floor_total = peak - dd
                    if p.trailing_locks_at_initial:
                        floor_total = min(floor_total, 1.0)
                if eq <= floor_day:
                    return "daily", d + 1
                if eq <= floor_total:
                    return "total", d + 1
                peak = max(peak, eq)
            bal = eq                                   # positions close within the day
            pnl = eq - start
            day_profits.append(pnl)
            if p.min_profitable_days and pnl >= p.profitable_day_pct / 100:
                profitable += 1
        if (eq >= target and traded >= p.min_trading_days and profitable >= p.min_profitable_days
                and _best_day_ok(day_profits, p.best_day_max_share)):
            return "pass", d + 1
    return "timeout", horizon


def _best_day_ok(day_profits: list[float], share: float) -> bool:
    if share <= 0:
        return True
    pos = [x for x in day_profits if x > 0]
    return bool(pos) and max(pos) <= share * sum(pos)


def simulate(days: list[np.ndarray], active_share: float, profile: Profile, risk: float,
             runs: int = 3000, seed: int = 11) -> dict:
    """risk = fraction of CURRENT equity risked per trade (as QB_Host sizes)."""
    if not days:
        return {"pass_prob": 0.0, "fail_prob": 1.0, "reason": "no trades", "risk_pct": risk * 100}
    rng = np.random.default_rng(seed)
    n_days = len(days)
    passed, total_days = 0, []
    fails = {"daily": 0, "total": 0, "timeout": 0}
    phase_pass = [0] * len(profile.phase_targets)
    for _ in range(runs):
        elapsed = 0
        for k, tgt in enumerate(profile.phase_targets):
            outcome, used = _phase(days, n_days, active_share, profile, tgt, risk, rng)
            elapsed += used
            if outcome != "pass":
                fails[outcome] += 1
                break
            phase_pass[k] += 1
        else:
            passed += 1
            total_days.append(elapsed)
    return {"pass_prob": passed / runs, "fail_prob": 1 - passed / runs,
            "phase_pass_prob": [x / runs for x in phase_pass],
            "median_days_to_pass": float(np.median(total_days)) if total_days else None,
            "fail_breakdown": {k: v / runs for k, v in fails.items()}, "risk_pct": risk * 100}


def cost_per_pass(profile: Profile, pass_prob: float, size: float | None = None) -> float | None:
    """Expected fees spent per funded account (fee / P(pass)), in the firm's fee currency;
    None if the fee is unpublished. Rules are %-based, so P(pass) is the same for every size."""
    fee = profile.fee(size or profile.default_size())
    if fee is None or pass_prob <= 0:
        return None
    return fee / pass_prob


def best_risk(days: list[np.ndarray], active_share: float, profile: Profile, size: float | None = None,
              grid_pct: tuple = (0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0), runs: int = 2000) -> dict:
    """Risk per trade that maximises P(pass), with the whole curve for context. P(pass) doesn't
    depend on account size (rules are %); the size only sets the fee for cost_per_pass."""
    size = size or profile.default_size()
    curve = [simulate(days, active_share, profile, r / 100, runs) for r in grid_pct]
    best = max(curve, key=lambda x: (x["pass_prob"], -x["risk_pct"]))
    return {"profile": profile.name, "firm": profile.firm, "program": profile.program, "best": best,
            "size": size, "fee": profile.fee(size), "fee_currency": profile.fee_currency,
            "cost_per_pass": cost_per_pass(profile, best["pass_prob"], size),
            "curve": [{"risk_pct": c["risk_pct"], "pass_prob": c["pass_prob"],
                       "median_days": c.get("median_days_to_pass")} for c in curve]}


def rank_programs(days: list[np.ndarray], active_share: float, names: list[str] | None = None,
                  runs: int = 1500) -> list[dict]:
    """Best-risk result for every program, highest P(pass) first."""
    progs = profiles()
    res = [best_risk(days, active_share, progs[n], runs=runs) for n in (names or progs)]
    return sorted(res, key=lambda r: r["best"]["pass_prob"], reverse=True)


def sleeve_days(sleeves: list[dict], years: float = 3.0) -> tuple[list[np.ndarray], float, float]:
    """Trade days for a set of sleeves on pre-holdout data (holdouts stay untouched).
    Each sleeve's R is weighted by its risk relative to the largest, so `risk` in simulate()
    means the largest sleeve's risk per trade. Returns (days, active_share, largest risk %)."""
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
