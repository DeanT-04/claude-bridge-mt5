"""The validation gauntlet: walk-forward -> robustness -> benchmarks -> sizing -> prop gate -> holdout -> MT5.

Research runs on the fast Python engine; MT5 confirms the finalist (parity + cost stress).
Every configuration evaluated is logged as a trial so the Deflated Sharpe hurdle is honest.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import numpy as np

from bridge import config
from registry import db

from . import benchmarks, montecarlo, sizing, stats
from .engine import Costs, Trade, simulate
from .strategies import FAMILIES, get_family

# Walk-forward window lengths (in-sample, out-of-sample months) per timeframe. Lower timeframes
# have less history on BlackBull (terminal max-bars cap) but more trades per month.
WF_MONTHS = {"M15": (12, 3), "M30": (18, 4), "H1": (24, 6), "H4": (36, 9)}
MIN_IS_TRADES = 30
SCREEN_CONFIGS = 150         # random configs tried in the pre-screen
SCREEN_MIN_SHARPE = 0.5      # best pre-holdout Sharpe among them must reach this to continue


@dataclass
class Window:
    is_start: int
    is_end: int
    oos_end: int


def _month_ts(ts: int, months: int) -> int:
    d = datetime.fromtimestamp(ts, timezone.utc)
    y, m = divmod(d.month - 1 + months, 12)
    return int(d.replace(year=d.year + y, month=m + 1, day=1).timestamp())


def walk_forward_windows(times: np.ndarray, end_idx: int, timeframe: str = "H1") -> list[Window]:
    IS_MONTHS, OOS_MONTHS = WF_MONTHS.get(timeframe, WF_MONTHS["H1"])
    out = []
    t = int(times[0])
    while True:
        is_end_t = _month_ts(t, IS_MONTHS)
        oos_end_t = _month_ts(t, IS_MONTHS + OOS_MONTHS)
        is_end = int(np.searchsorted(times, is_end_t))
        oos_end = int(np.searchsorted(times, oos_end_t))
        if oos_end > end_idx or is_end >= end_idx:
            # final partial OOS window up to the holdout boundary if it's at least half-length
            if is_end < end_idx and (times[end_idx - 1] - times[is_end]) > OOS_MONTHS * 15 * 86400:
                out.append(Window(int(np.searchsorted(times, t)), is_end, end_idx))
            break
        out.append(Window(int(np.searchsorted(times, t)), is_end, oos_end))
        t = _month_ts(t, OOS_MONTHS)
    return out


def _score(trades: list[Trade], span_days: float) -> tuple[float, int]:
    if len(trades) < MIN_IS_TRADES:
        return -math.inf, len(trades)
    return stats.metrics(trades, span_days=span_days)["sharpe"], len(trades)


def _span(bars, a, b) -> float:
    return max((bars["time"][b - 1] - bars["time"][a]) / 86400, 1.0)


def costs_for(spec: dict, spread_mult: float = 1.0, slip: float = 0.0, floor: bool = True) -> Costs:
    """Research costs. floor=True charges at least the live spread (history understates it);
    floor=False reproduces the MT5 tester's own spread handling, for parity checks."""
    comm = config.settings().get("costs", {}).get("commission_price", {}).get(spec["name"], 0.0)
    return Costs(point=spec["point"], spread_mult=spread_mult, slippage_points=slip, commission_price=comm,
                 min_spread_points=float(spec.get("spread", 0)) if floor else 0.0)


def run(family: str, symbol: str, timeframe: str, bars: np.ndarray, spec: dict,
        con=None, mt5_confirm=None, progress=print) -> dict:
    """Run the full gauntlet. `mt5_confirm(params, from, to) -> dict` is optional."""
    fam = get_family(family)
    # Generated strategies share one multiple-testing pool per symbol/timeframe.
    trial_key = getattr(fam, "trial_key", family)
    g = config.gauntlet()
    con = con or db.connect()
    costs = costs_for(spec)
    stages: dict[str, dict] = {}

    times = bars["time"]
    hold_start_t = _month_ts(int(times[-1]), -config.settings()["research"]["holdout_months"])
    hold_idx = int(np.searchsorted(times, hold_start_t))
    windows = walk_forward_windows(times, hold_idx, timeframe)
    if not windows:
        return _finish(con, family, symbol, timeframe, {}, "fail",
                       {"data": {"pass": False, "reason": "not enough history for walk-forward"}})

    grid = fam.grid_params()

    def sigs(p):
        return fam.signals(bars, p)

    def bt(p, a, b, c=costs):
        d, sl, tp = sigs(p)
        return simulate(bars, d, sl, tp, p.InpMaxBars, c, a, b)

    a0, a1 = windows[0].is_start, hold_idx
    span_all = _span(bars, a0, a1)

    # ---- 0. pre-screen: skip the full walk-forward when no sampled config shows promise ----
    rng = np.random.default_rng(len(grid))
    sample = [grid[i] for i in rng.choice(len(grid), min(SCREEN_CONFIGS, len(grid)), replace=False)]
    screen_rows, best_screen = [], -math.inf
    for p in sample:
        tr = bt(p, a0, a1)
        best_screen = max(best_screen, _score(tr, span_all)[0])
        screen_rows.append((p.dict(), stats.trade_sharpe(np.array([t.r for t in tr])), len(tr)))
    stages["screen"] = {"pass": best_screen >= SCREEN_MIN_SHARPE, "best_sharpe": best_screen,
                        "configs": len(sample)}
    if not stages["screen"]["pass"]:
        db.log_trials(con, trial_key, symbol, timeframe, screen_rows)   # these evaluations count too
        return _finish(con, family, symbol, timeframe, {}, "fail", stages)
    progress(f"walk-forward: {len(windows)} windows x {len(grid)} configs")

    # ---- 1. walk-forward optimisation --------------------------------------------------
    # One pass over the grid: signals computed once per config, scored on every IS window
    # and on the whole pre-holdout span (used for plateau selection below).
    is_spans = [_span(bars, w.is_start, w.is_end) for w in windows]
    is_scores = np.full((len(grid), len(windows)), -math.inf)
    full_scores = {}
    trial_rows = []
    for gi, p in enumerate(grid):
        d, sl, tp = sigs(p)
        for wi, w in enumerate(windows):
            tr = simulate(bars, d, sl, tp, p.InpMaxBars, costs, w.is_start, w.is_end)
            is_scores[gi, wi] = _score(tr, is_spans[wi])[0]
        tr = simulate(bars, d, sl, tp, p.InpMaxBars, costs, a0, a1)
        full_scores[p] = _score(tr, span_all)[0]
        trial_rows.append((p.dict(), stats.trade_sharpe(np.array([t.r for t in tr])), len(tr)))
        if gi % 500 == 0:
            progress(f"  grid {gi}/{len(grid)}")

    oos_trades: list[Trade] = []
    chosen: list = []
    picked: list[tuple[Window, object]] = []      # (window, params) actually traded OOS
    is_sharpes, oos_sharpes = [], []
    for wi, w in enumerate(windows):
        gi = int(np.argmax(is_scores[:, wi]))
        best_s = is_scores[gi, wi]
        if not np.isfinite(best_s):
            continue
        best = grid[gi]
        chosen.append(best)
        picked.append((w, best))
        tr = bt(best, w.is_end, w.oos_end)
        oos_trades += tr
        is_sharpes.append(best_s)
        oos_sharpes.append(stats.metrics(tr, span_days=_span(bars, w.is_end, w.oos_end))["sharpe"] if tr else 0.0)
    db.log_trials(con, trial_key, symbol, timeframe, trial_rows)

    oos_span = _span(bars, windows[0].is_end, windows[-1].oos_end)
    m = stats.metrics(oos_trades, span_days=oos_span)
    wfe = (np.mean(oos_sharpes) / np.mean(is_sharpes)) if is_sharpes and np.mean(is_sharpes) > 0 else 0.0
    stages["walk_forward"] = {
        "pass": m["trades"] >= g["min_oos_trades"] and m["profit_factor"] >= g["min_profit_factor"]
                and m["sharpe"] >= g["min_sharpe_annual"] and wfe >= g["min_wfe"],
        "oos": m, "wfe": wfe, "windows": len(windows),
        "chosen_params": [c.dict() for c in chosen],
    }
    progress(f"walk-forward OOS: {m['trades']} trades, PF {m['profit_factor']:.2f}, Sharpe {m['sharpe']:.2f}, WFE {wfe:.2f}")

    # ---- 2. final params: plateau-aware selection on all pre-holdout data ---------------
    def plateau(p):
        nb = [full_scores.get(q, -math.inf) for q in fam.neighbours(p)]
        vals = [v for v in nb + [full_scores[p]] if np.isfinite(v)]
        return np.median(vals) if len(vals) == len(nb) + 1 else -math.inf
    final = max(grid, key=plateau)
    nb_vals = [full_scores.get(q, -math.inf) for q in fam.neighbours(final)]
    own = full_scores[final]
    nb_med = float(np.median(nb_vals)) if nb_vals else -math.inf
    degr = 1 - nb_med / own if own > 0 and np.isfinite(nb_med) else 1.0
    stages["neighbourhood"] = {"pass": own > 0 and degr <= g["neighbourhood"]["max_degradation"],
                               "sharpe": own, "neighbour_median": nb_med, "degradation": degr,
                               "final_params": final.dict()}

    # ---- 3. deflated Sharpe ------------------------------------------------------------
    n_trials, trial_srs = db.trial_stats(con, trial_key, symbol, timeframe)
    r_oos = np.array([t.r for t in oos_trades])
    dsr = stats.deflated_sharpe(r_oos, n_trials, trial_srs)
    stages["deflated_sharpe"] = {"pass": dsr["dsr"] >= g["dsr"]["min_prob"], **dsr}

    # ---- 4. sizing + Monte Carlo -------------------------------------------------------
    mc_cfg = g["montecarlo"]
    size = sizing.choose_risk(r_oos, g["sizing"], mc_cfg["dd95_max_pct"] / 100)
    risk = size["risk"]
    mc = montecarlo.simulate_drawdowns(r_oos, risk or g["sizing"]["min_risk_pct"] / 100, mc_cfg["runs"],
                                       mc_cfg["skip_prob"], mc_cfg["ruin_dd_pct"] / 100)
    eq_dd = stats.max_drawdown(stats.equity_curve(r_oos, risk)) if risk else 1.0
    stages["sizing_montecarlo"] = {
        "pass": risk > 0 and mc["dd_p95"] <= mc_cfg["dd95_max_pct"] / 100
                and mc["ruin_prob"] <= mc_cfg["max_ruin_prob"] and eq_dd <= g["max_drawdown_pct"] / 100,
        **size, "oos_max_dd": eq_dd, **mc}

    # ---- 5. cost stress (python) -------------------------------------------------------
    cs = g["cost_stress"]
    stressed = costs_for(spec, cs["spread_mult"], cs["extra_slippage_points"])
    st_trades = []
    for w, p in picked:
        st_trades += bt(p, w.is_end, w.oos_end, stressed)
    sm = stats.metrics(st_trades, span_days=oos_span)
    stages["cost_stress"] = {"pass": sm["profit_factor"] >= cs["min_profit_factor"], "stressed": sm}

    # ---- 6. benchmarks -----------------------------------------------------------------
    bcfg = g["benchmarks"]
    d, sl, tp = sigs(final)
    oa, ob = windows[0].is_end, windows[-1].oos_end
    rnd = benchmarks.random_entry_pvalue(bars, d, sl, tp, final.InpMaxBars, costs, oa, ob,
                                         m["expectancy_r"], runs=bcfg["random_entry_runs"])
    bh = benchmarks.buy_hold_sharpe(bars, oa, ob)
    stages["benchmarks"] = {"pass": rnd["p_value"] <= bcfg["max_p_value"]
                                    and (not bcfg["beat_buy_hold"] or m["sharpe"] > bh),
                            "random_entry": rnd, "buy_hold_sharpe": bh, "strategy_sharpe": m["sharpe"]}

    core = ["walk_forward", "neighbourhood", "deflated_sharpe", "sizing_montecarlo",
            "cost_stress", "benchmarks"]      # then the prop gate (7), before the holdout is spent
    all_pass = all(stages[s]["pass"] for s in core)

    # ---- 7. prop challenges (gate) -------------------------------------------------------
    # Uses the walk-forward OOS trades, never the tuned final params, so it isn't in-sample.
    # Each firm's trades are regenerated with its own costs (config/firmcosts.yaml) and each
    # program's weekend/news rules; a firm must also survive its own cost stress.
    oos = {"base": oos_trades}
    span = (int(times[windows[0].is_end]), int(times[windows[-1].oos_end - 1]))
    if all_pass:
        from . import firmcosts, propfirm

        def regen(c, blocked=None, flat=None):
            out = []
            for w, p in picked:
                d, sl, tp = sigs(p)
                out += simulate(bars, d, sl, tp, p.InpMaxBars, c, w.is_end, w.oos_end,
                                blocked=blocked, flat_at=flat)
            return out

        firm_rows = {}
        for prof in propfirm.profiles().values():
            v = propfirm.variant(prof)
            if v in oos or v in firm_rows:
                continue
            fc = firmcosts.costs(prof.firm, symbol, spec)
            if fc is None:
                firm_rows[v] = {"firm": prof.firm, "offered": False, "pass": False}
                continue
            blocked, flat = execution_rules(bars, symbol, spec, prof.weekend_flat_hour, prof.news_blackout_min)
            oos[v] = regen(fc, blocked, flat)
            stressed = regen(firmcosts.costs(prof.firm, symbol, spec, cs["spread_mult"], cs["extra_slippage_points"]),
                             blocked, flat)
            fm = stats.metrics(oos[v], span_days=oos_span)
            spf = stats.metrics(stressed, span_days=oos_span)["profit_factor"]
            firm_rows[v] = {"firm": prof.firm, "offered": True, "pass": spf >= cs["min_profit_factor"],
                            "profit_factor": fm["profit_factor"], "expectancy_r": fm["expectancy_r"],
                            "sharpe": fm["sharpe"], "stressed_profit_factor": spf}
        stages["firm_costs"] = {"pass": any(r["pass"] for r in firm_rows.values()), "variants": firm_rows}
        stages["prop"] = prop_gate(oos, oos_span, g["prop"],
                                   {v: r["pass"] for v, r in firm_rows.items()})
        all_pass = stages["prop"]["pass"]

    # ---- 8. holdout (once per candidate, only if everything else passed) ---------------
    cand = db.candidate_hash(family, symbol, timeframe, final.dict())
    if all_pass:
        prev = db.holdout_used(con, cand)
        if prev:
            hm = prev["result"]
            stages["holdout"] = {"pass": hm.get("pass", False), "reused": True, **hm}
        else:
            ht = bt(final, hold_idx, len(bars))
            hm = stats.metrics(ht, span_days=_span(bars, hold_idx, len(bars)))
            ok = hm["trades"] >= 10 and hm["expectancy_r"] > 0 and hm["profit_factor"] > 1.0
            db.mark_holdout(con, cand, {"pass": ok, **hm})
            stages["holdout"] = {"pass": ok, **hm}
    else:
        stages["holdout"] = {"pass": False, "skipped": "earlier stage failed; holdout preserved"}

    # ---- 9. MT5 confirmation ------------------------------------------------------------
    if all_pass and stages["holdout"]["pass"] and mt5_confirm:
        stages["mt5"] = mt5_confirm(final, times[a0], times[-1])
    elif all_pass and stages["holdout"]["pass"]:
        stages["mt5"] = {"pass": False, "pending": True}

    if not (all_pass and stages["holdout"]["pass"]):
        verdict = "fail"
    elif stages.get("mt5", {}).get("pending"):
        verdict = "pending_mt5"
    else:
        verdict = "pass" if stages["mt5"]["pass"] else "fail"
    return _finish(con, family, symbol, timeframe, final.dict(), verdict, stages, oos, span)


def execution_rules(bars, symbol: str, spec: dict, flat_hour: int, news_min: int):
    """(blocked, flat_at) bar masks for a prop firm's weekend and news rules, as QB_Host applies them."""
    from . import calendar
    from .engine import weekend_masks
    blocked = np.zeros(len(bars), dtype=bool)
    flat = None
    if flat_hour:
        blocked, flat = weekend_masks(bars["time"], flat_hour)
    if news_min:
        if not calendar.available(bars["time"]):
            raise RuntimeError("news calendar missing or stale: run `python scripts/research.py calendar`")
        blocked = blocked | calendar.news_mask(bars["time"], symbol, news_min, spec)
    return blocked, flat


def prop_gate(oos: dict[str, list[Trade]], span_days: float, cfg: dict,
              cost_ok: dict[str, bool] | None = None) -> dict:
    """Evaluate every program on its variant's OOS trades; pass if any program clears both
    min_pass_prob and min_lift (and its firm passed cost stress). Programs whose firm doesn't
    list the symbol are reported as not offered."""
    from . import propfirm
    progs = propfirm.profiles()
    names = list(progs) if cfg.get("programs", "all") == "all" else cfg["programs"]
    rows = []
    for n in names:
        prof = progs[n]
        v = propfirm.variant(prof)
        if v not in oos:
            rows.append({"profile": n, "pass": False, "offered": False, "pass_prob": 0.0, "lift": 0.0,
                         "variant": v})
            continue
        tr = oos[v]
        days = propfirm.trade_days(tr)
        active = min(len(days) / max(span_days * 5 / 7, 1), 1.0)
        e = propfirm.evaluate(days, active, prof, runs=cfg["runs"])
        stress_ok = (cost_ok or {}).get(v, True)
        ok = e["best"]["pass_prob"] >= cfg["min_pass_prob"] and e["lift"] >= cfg["min_lift"] and stress_ok
        rows.append({"profile": n, "pass": ok, "offered": True, "cost_stress_ok": stress_ok, "pass_prob": e["best"]["pass_prob"], "lift": e["lift"],
                     "baseline_pass_prob": e["baseline_pass_prob"], "risk_pct": e["best"]["risk_pct"],
                     "median_days": e["best"]["median_days_to_pass"],
                     "fail_breakdown": e["best"]["fail_breakdown"], "trades": len(tr),
                     "variant": v})
    rows.sort(key=lambda r: (r["pass"], r["pass_prob"]), reverse=True)
    return {"pass": any(r["pass"] for r in rows), "min_pass_prob": cfg["min_pass_prob"],
            "min_lift": cfg["min_lift"], "programs": rows}


def _finish(con, family, symbol, timeframe, params, verdict, stages, oos=None, span=None) -> dict:
    gid = db.log_gauntlet(con, family, symbol, timeframe, params, verdict, stages)
    for v, tr in (oos or {}).items():
        db.save_oos_trades(con, gid, v, span, tr)
    return {"id": gid, "family": family, "symbol": symbol, "timeframe": timeframe,
            "params": params, "verdict": verdict, "stages": stages}
