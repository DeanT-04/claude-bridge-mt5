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
    trailing_basis: str = "equity"        # equity | balance (closed) | eod_balance (end-of-day high)
    daily_loss_ref: str = "initial"       # the daily % applies to: initial balance | baseline (day start)
    ea_max_size: float = 0                # largest size where EAs are allowed (0 = every size)
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

    def size_options(self, ea_only: bool = False) -> list[float]:
        """Sizes offered (ea_only: only those where the firm allows EAs, which is what we trade)."""
        return [float(x["size"]) for x in self.sizes
                if not (ea_only and self.ea_max_size and float(x["size"]) > self.ea_max_size)]

    def fee(self, size: float) -> float | None:
        """Fee for an account size (None if the size isn't offered or the fee is unpublished)."""
        for x in self.sizes:
            if float(x["size"]) == float(size):
                return x.get("fee")
        return None

    def default_size(self) -> float:
        """The research account size if offered (and EA-eligible), else the largest such size
        not above it."""
        want = float(config.settings()["account"]["deposit"])
        opts = sorted(self.size_options(ea_only=True))
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


def variant(profile: Profile) -> str:
    """Name of the trade set a program is evaluated on: its firm's execution costs plus its
    weekend/news rules, e.g. 'ftmo', 'the5ers_nb2' ('base' is BlackBull's own costs)."""
    h, n = profile.weekend_flat_hour, profile.news_blackout_min
    return profile.firm.lower() + (f"_wf{h}" if h else "") + (f"_nb{n}" if n else "")


def trade_days(trades: list[Trade]) -> list[np.ndarray]:
    """Group R-multiples by exit day, in time order within each day."""
    days: dict[int, list[tuple[int, float]]] = {}
    for t in trades:
        days.setdefault(t.exit_time // 86400, []).append((t.exit_time, t.r))
    return [np.array([r for _, r in sorted(v)]) for _, v in sorted(days.items())]


def _day_matrix(days: list[np.ndarray]) -> np.ndarray:
    """Trade days padded with zero-R trades to one [n_days, max_trades] matrix (a zero trade
    changes nothing, so padding is exact)."""
    k = max(len(d) for d in days)
    mat = np.zeros((len(days), max(k, 1)))
    for i, d in enumerate(days):
        mat[i, :len(d)] = d
    return mat


def simulate_grid(days: list[np.ndarray], active_share: float, profile: Profile, risks,
                  runs: int = 3000, seed: int = 11) -> list[dict]:
    """simulate() for several risk levels at once, vectorised over runs x risks. Every risk level
    sees the same bootstrapped days (common random numbers), so their P(pass) compare cleanly."""
    risks = np.asarray(risks, dtype=float)
    if not days:
        return [{"pass_prob": 0.0, "fail_prob": 1.0, "reason": "no trades", "risk_pct": r * 100} for r in risks]
    rng = np.random.default_rng(seed)
    mat = _day_matrix(days)
    p = profile
    n_ph = len(p.phase_targets)
    targets = 1 + np.asarray(p.phase_targets, dtype=float) / 100
    horizon = p.max_days or MAX_SIM_DAYS
    dl, dd = p.max_daily_loss_pct / 100, p.max_total_dd_pct / 100
    shape = (len(risks), runs)
    risk = risks[:, None]

    phase = np.zeros(shape, dtype=int)
    eq, bal, peak = np.ones(shape), np.ones(shape), np.ones(shape)
    eod = p.trailing_basis == "eod_balance"      # floor from the highest end-of-day balance
    eod_peak = np.ones(shape)
    traded, profitable, in_phase, elapsed = (np.zeros(shape, dtype=int) for _ in range(4))
    best, pos_sum = np.zeros(shape), np.zeros(shape)
    done = np.zeros(shape, dtype=bool)
    outcome = np.full(shape, "", dtype=object)
    days_to_pass = np.zeros(shape, dtype=int)
    phase_pass = np.zeros((len(risks), n_ph), dtype=int)

    for _ in range(horizon * n_ph):
        live = ~done
        if not live.any():
            break
        sod = {"balance": bal, "equity": eq, "max": np.maximum(bal, eq)}[p.daily_loss_basis]
        floor_day = sod - (dl * sod if p.daily_loss_ref == "baseline" else dl)
        start = eq.copy()
        act = live & (rng.random(runs) < active_share)[None, :]
        rows = mat[rng.integers(len(days), size=runs)]           # same day for every risk level
        trading = act.copy()
        for k in range(mat.shape[1]):
            r = rows[:, k][None, :]
            eq = np.where(trading, eq * (1 + risk * r), eq)
            if p.max_dd_mode == "static":
                floor_total = 1 - dd
            else:
                floor_total = (eod_peak if eod else peak) - dd
                if p.trailing_locks_at_initial:
                    floor_total = np.minimum(floor_total, 1.0)
            hit_d = trading & (eq <= floor_day)
            hit_t = trading & ~hit_d & (eq <= floor_total)
            outcome[hit_d], outcome[hit_t] = "daily", "total"
            done |= hit_d | hit_t
            trading &= ~(hit_d | hit_t)
            peak = np.where(trading, np.maximum(peak, eq), peak)
        in_phase += live
        live &= ~done
        traded += act
        bal = np.where(act, eq, bal)                              # positions close within the day
        eod_peak = np.maximum(eod_peak, bal)
        pnl = np.where(act, eq - start, 0.0)
        best = np.where(act & (pnl > 0), np.maximum(best, pnl), best)
        pos_sum += np.where(act & (pnl > 0), pnl, 0.0)
        if p.min_profitable_days:
            profitable += act & (pnl >= p.profitable_day_pct / 100)
        best_ok = True if p.best_day_max_share <= 0 else (pos_sum > 0) & (best <= p.best_day_max_share * pos_sum)
        passed = (live & (eq >= targets[phase]) & (traded >= p.min_trading_days)
                  & (profitable >= p.min_profitable_days) & best_ok)
        for k in range(n_ph):
            phase_pass[:, k] += (passed & (phase == k)).sum(axis=1)
        final = passed & (phase == n_ph - 1)
        outcome[final] = "pass"
        days_to_pass[final] = (elapsed + in_phase)[final]
        done |= final
        nxt = passed & ~final                                     # next phase from a fresh balance
        if nxt.any():
            phase[nxt] += 1
            elapsed[nxt] += in_phase[nxt]
            for a in (eq, bal, peak, eod_peak):
                a[nxt] = 1.0
            for a in (traded, profitable, in_phase):
                a[nxt] = 0
            best[nxt] = pos_sum[nxt] = 0.0
        out = live & ~passed & (in_phase >= horizon)
        outcome[out] = "timeout"
        done |= out
    outcome[~done] = "timeout"

    res = []
    for i, r in enumerate(risks):
        o = outcome[i]
        n_pass = int((o == "pass").sum())
        res.append({"pass_prob": n_pass / runs, "fail_prob": 1 - n_pass / runs,
                    "phase_pass_prob": [int(x) / runs for x in phase_pass[i]],
                    "median_days_to_pass": float(np.median(days_to_pass[i][o == "pass"])) if n_pass else None,
                    "fail_breakdown": {k: float((o == k).sum()) / runs for k in ("daily", "total", "timeout")},
                    "risk_pct": float(r) * 100})
    return res


def simulate(days: list[np.ndarray], active_share: float, profile: Profile, risk: float,
             runs: int = 3000, seed: int = 11) -> dict:
    """risk = fraction of CURRENT equity risked per trade (as QB_Host sizes)."""
    return simulate_grid(days, active_share, profile, [risk], runs, seed)[0]


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
    curve = simulate_grid(days, active_share, profile, [r / 100 for r in grid_pct], runs)
    best = max(curve, key=lambda x: (x["pass_prob"], -x["risk_pct"]))
    return {"profile": profile.name, "firm": profile.firm, "program": profile.program, "best": best,
            "size": size, "fee": profile.fee(size), "fee_currency": profile.fee_currency,
            "cost_per_pass": cost_per_pass(profile, best["pass_prob"], size),
            "curve": [{"risk_pct": c["risk_pct"], "pass_prob": c["pass_prob"],
                       "median_days": c.get("median_days_to_pass")} for c in curve]}


def demeaned(days: list[np.ndarray]) -> list[np.ndarray]:
    """The same trade days with the edge removed (every R shifted so the mean is zero): the same
    volatility, clustering and trade count. Its P(pass) is what luck alone achieves."""
    mu = float(np.concatenate(days).mean()) if days else 0.0
    return [d - mu for d in days]


def evaluate(days: list[np.ndarray], active_share: float, profile: Profile, runs: int = 1500,
             size: float | None = None, grid_pct: tuple | None = None) -> dict:
    """best_risk() plus `lift`: P(pass) minus the edge-removed baseline's best P(pass).
    A high P(pass) with no lift is a volatility bet, not an edge."""
    kw = {"grid_pct": grid_pct} if grid_pct else {}
    res = best_risk(days, active_share, profile, size, runs=runs, **kw)
    base = best_risk(demeaned(days), active_share, profile, size, runs=runs, **kw)
    res["baseline_pass_prob"] = base["best"]["pass_prob"]
    res["lift"] = res["best"]["pass_prob"] - base["best"]["pass_prob"]
    return res


def rank_programs(days: list[np.ndarray], active_share: float, names: list[str] | None = None,
                  runs: int = 1500) -> list[dict]:
    """Best-risk result for every program, highest P(pass) first."""
    progs = profiles()
    res = [best_risk(days, active_share, progs[n], runs=runs) for n in (names or progs)]
    return sorted(res, key=lambda r: r["best"]["pass_prob"], reverse=True)


def sleeve_days(sleeves: list[dict], years: float = 3.0, variant_name: str = "base"
                ) -> tuple[list[np.ndarray], float, float, str]:
    """Trade days for a set of sleeves. Each sleeve's R is weighted by its risk relative to the
    largest, so `risk` in simulate() means the largest sleeve's risk per trade. Uses the stored
    walk-forward OOS trades (in `variant_name`) over the common OOS period; gauntlets without
    them fall back to the tuned params on pre-holdout data (optimistic).
    Returns (days, active_share, largest risk %, source)."""
    top = max(s.get("risk_pct", 1.0) for s in sleeves)
    if all("id" in s for s in sleeves):
        from registry import db
        from .challenge import combined_days, load_sleeves, overlap
        oos = load_sleeves(db.connect(), [s["id"] for s in sleeves], variant_name)
        if len(oos) == len(sleeves):
            lo, hi = overlap(oos)
            if hi > lo:
                days, active = combined_days(oos, [s.get("risk_pct", 1.0) / top for s in sleeves], lo, hi)
                return days, active, top, "walk-forward OOS"
    from . import data
    from .gauntlet import _month_ts, costs_for
    from .strategies import get_family
    per_day: dict[int, list[tuple[int, float]]] = {}
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
    return days, active, top, "tuned params (in-sample)"
