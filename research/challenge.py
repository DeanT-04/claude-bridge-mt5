"""Prop-challenge selection: the leaderboard and the challenge-portfolio combiner.

Both work from each gauntlet's stored walk-forward OOS trades (registry.oos_trades), in the
execution variant a program needs (weekend/news rules), never from the tuned final params.

leaderboard(): strategy or portfolio x program x account size, with P(pass), the risk that
    maximises it, lift over the edge-removed baseline, median days, fee and cost per pass.
combine():     greedy forward selection of uncorrelated survivors per program, keeping a sleeve
    only if it raises P(pass); results are stored in registry.prop_portfolios.
"""
from __future__ import annotations

import json
import math

import numpy as np

from bridge import config
from registry import db

from . import propfirm

DAY = 86400
SURVIVOR_VERDICTS = ("pass", "pending_mt5")
MIN_OVERLAP_DAYS = 365          # sleeves must share at least a year of OOS history to combine


# ------------------------------------------------------------------ OOS trade sets
def load_sleeves(con, gauntlet_ids: list[int], variant: str = "base") -> list[dict]:
    """[{gauntlet_id, name, span, trades: [[entry, exit, r], ...]}] for gauntlets with stored OOS
    trades in that variant (others are skipped)."""
    out = []
    for gid in gauntlet_ids:
        o = db.oos_trades(con, gid, variant)
        if o is None:
            continue
        g = db.gauntlet(con, gid)
        out.append({"gauntlet_id": gid, "name": f"{g['family']} {g['symbol']} {g['timeframe']}",
                    "span": o["span"], "trades": o["trades"]})
    return out


def overlap(sleeves: list[dict]) -> tuple[int, int]:
    return max(s["span"][0] for s in sleeves), min(s["span"][1] for s in sleeves)


def daily_matrix(sleeves: list[dict], lo: int, hi: int) -> np.ndarray:
    """Calendar-day R sums [days x sleeves] over [lo, hi] (zero on days without exits)."""
    d0, d1 = lo // DAY, hi // DAY
    mat = np.zeros((d1 - d0 + 1, len(sleeves)))
    for j, s in enumerate(sleeves):
        for _, x, r in s["trades"]:
            if lo <= x <= hi:
                mat[x // DAY - d0, j] += r
    return mat


def combined_days(sleeves: list[dict], weights, lo: int, hi: int) -> tuple[list[np.ndarray], float]:
    """Trade days of the weighted combination over [lo, hi], trades in exit order within a day,
    plus the share of weekdays with a trade (for propfirm.simulate)."""
    per: dict[int, list[tuple[int, float]]] = {}
    for s, w in zip(sleeves, weights):
        for _, x, r in s["trades"]:
            if lo <= x <= hi:
                per.setdefault(x // DAY, []).append((x, r * w))
    days = [np.array([r for _, r in sorted(v)]) for _, v in sorted(per.items())]
    active = min(len(days) / max((hi - lo) / DAY * 5 / 7, 1), 1.0)
    return days, active


def inverse_vol_weights(mat: np.ndarray) -> np.ndarray:
    """Equal daily volatility per sleeve, scaled so the largest weight is 1 (its risk per trade
    is the portfolio's `risk_pct`)."""
    vol = mat.std(axis=0, ddof=1)
    w = np.where(vol > 0, 1 / np.where(vol > 0, vol, 1), 0.0)
    return w / w.max() if w.max() > 0 else np.ones(len(w))


def risk_grid(weights) -> tuple:
    """Risk levels for the largest sleeve such that the sum of all sleeves' risks (everything open
    at once) stays within deployment.max_open_risk_pct, so QB_Host never blocks an entry the
    simulation counted."""
    cap = config.settings()["deployment"]["max_open_risk_pct"] / float(np.sum(weights))
    grid = tuple(r for r in (0.1, 0.15, 0.25, 0.35, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0) if r <= cap + 1e-9)
    return grid or (round(cap, 3),)


def evaluate(sleeves: list[dict], program: str, runs: int = 1500) -> dict | None:
    """P(pass) of the inverse-vol combination on the sleeves' common OOS period."""
    lo, hi = overlap(sleeves)
    if (hi - lo) / DAY < MIN_OVERLAP_DAYS:
        return None
    mat = daily_matrix(sleeves, lo, hi)
    w = inverse_vol_weights(mat)
    days, active = combined_days(sleeves, w, lo, hi)
    if not days:
        return None
    res = propfirm.evaluate(days, active, propfirm.profiles()[program], runs=runs, grid_pct=risk_grid(w))
    res["weights"] = w.tolist()
    res["overlap_days"] = int((hi - lo) / DAY)
    res["correlation"] = np.round(np.corrcoef(mat.T), 3).tolist() if len(sleeves) > 1 else [[1.0]]
    return res


# ------------------------------------------------------------------ combiner
def survivor_ids(con) -> list[int]:
    q = "SELECT id FROM gauntlets WHERE verdict IN (%s) ORDER BY id" % ",".join("?" * len(SURVIVOR_VERDICTS))
    return [r["id"] for r in con.execute(q, SURVIVOR_VERDICTS)]


def combine(programs: list[str] | None = None, gauntlet_ids: list[int] | None = None, max_sleeves: int = 5,
            max_corr: float = 0.5, min_gain: float = 0.01, search_runs: int = 600, final_runs: int = 3000,
            con=None, progress=print) -> list[dict]:
    """For each program: start from the best single survivor, then repeatedly add the sleeve that
    raises P(pass) most (at least `min_gain`), skipping any whose daily OOS R correlates above
    `max_corr` with a chosen sleeve. The final set is re-simulated with `final_runs` and stored."""
    con = con or db.connect()
    ids = gauntlet_ids or survivor_ids(con)
    progs = propfirm.profiles()
    out = []
    for prog in programs or list(progs):
        pool = load_sleeves(con, ids, propfirm.variant(progs[prog]))
        if not pool:
            progress(f"{prog}: no candidates with stored OOS trades")
            continue
        scored = [(evaluate([s], prog, search_runs), s) for s in pool]
        scored = [(e, s) for e, s in scored if e]
        if not scored:
            continue
        best_e, first = max(scored, key=lambda x: x[0]["best"]["pass_prob"])
        chosen, cur = [first], best_e["best"]["pass_prob"]
        while len(chosen) < max_sleeves:
            step = None
            taken = {c["gauntlet_id"] for c in chosen}
            for s in pool:
                if s["gauntlet_id"] in taken or _too_correlated(chosen, s, max_corr):
                    continue
                e = evaluate(chosen + [s], prog, search_runs)
                if e and e["best"]["pass_prob"] >= cur + min_gain and (step is None or
                                                                      e["best"]["pass_prob"] > step[0]):
                    step = (e["best"]["pass_prob"], s)
            if step is None:
                break
            cur = step[0]
            chosen.append(step[1])
        final = evaluate(chosen, prog, final_runs)
        members = [{"gauntlet_id": s["gauntlet_id"], "name": s["name"], "weight": round(w, 4)}
                   for s, w in zip(chosen, final["weights"])]
        pid = db.save_prop_portfolio(con, prog, members, final["best"]["pass_prob"], _strip(final))
        progress(f"{prog}: {len(chosen)} sleeves, P(pass) {final['best']['pass_prob']:.2f} "
                 f"(lift {final['lift']:+.2f}) at {final['best']['risk_pct']:.2f}%")
        out.append({"portfolio_id": pid, "program": prog, "members": members, **_strip(final)})
    return out


def _too_correlated(chosen: list[dict], cand: dict, max_corr: float) -> bool:
    lo, hi = overlap(chosen + [cand])
    if hi <= lo:
        return True
    mat = daily_matrix(chosen + [cand], lo, hi)
    c = np.corrcoef(mat.T)[-1, :-1]
    return bool(np.any(np.nan_to_num(c) > max_corr))


def _strip(res: dict) -> dict:
    keep = ("best", "curve", "lift", "baseline_pass_prob", "weights", "overlap_days", "correlation")
    return {k: res[k] for k in keep if k in res}


# ------------------------------------------------------------------ leaderboard
def leaderboard(program: str | None = None, size: float | None = None, min_pass_prob: float = 0.0,
                verdicts: tuple = SURVIVOR_VERDICTS, portfolios: bool = True, limit: int = 50,
                con=None) -> list[dict]:
    """Every (strategy or portfolio) x program x account size, best first: P(pass) (rules are %,
    so it's the same for every size), lift, the P(pass)-maximising risk, median days, and the
    size's fee and expected cost per pass. Strategies use their gauntlet's prop stage."""
    con = con or db.connect()
    progs = propfirm.profiles()
    entries = []
    q = "SELECT id, family, symbol, timeframe, verdict, stages FROM gauntlets WHERE verdict IN (%s)" \
        % ",".join("?" * len(verdicts))
    for r in con.execute(q, verdicts):
        st = json.loads(r["stages"]).get("prop", {})
        for p in st.get("programs", []):
            entries.append({"kind": "strategy", "id": r["id"], "verdict": r["verdict"],
                            "name": f"{r['family']} {r['symbol']} {r['timeframe']}", "program": p["profile"],
                            "pass_prob": p["pass_prob"], "lift": p.get("lift"), "risk_pct": p["risk_pct"],
                            "median_days": p["median_days"]})
    if portfolios:
        latest = {}
        for pf in db.prop_portfolios(con):
            key = (pf["program"], tuple(sorted(m["gauntlet_id"] for m in pf["members"])))
            latest[key] = pf                                 # newest run of the same set wins
        for pf in latest.values():
            b = pf["result"]["best"]
            entries.append({"kind": "portfolio", "id": pf["id"], "verdict": None,
                            "name": " + ".join(m["name"] for m in pf["members"]), "program": pf["program"],
                            "pass_prob": b["pass_prob"], "lift": pf["result"].get("lift"),
                            "risk_pct": b["risk_pct"], "median_days": b.get("median_days_to_pass")})
    rows = []
    for e in entries:
        if (program and e["program"] != program) or e["pass_prob"] < min_pass_prob or e["program"] not in progs:
            continue
        prof = progs[e["program"]]
        for sz in ([size] if size else prof.size_options()):
            if float(sz) not in prof.size_options():
                continue
            fee = prof.fee(sz)
            rows.append({**e, "firm": prof.firm, "size": sz, "fee": fee, "fee_currency": prof.fee_currency,
                         "cost_per_pass": propfirm.cost_per_pass(prof, e["pass_prob"], sz)})
    rows.sort(key=lambda x: (-x["pass_prob"], x["cost_per_pass"] if x["cost_per_pass"] is not None else math.inf))
    return rows[:limit]
