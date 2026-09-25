"""CFD-firm transfer test (P7): run a strategy under a static-drawdown firm's rules and CFD costs.

Currently FTMO 2-Step (config/firms/ftmo.yaml, verified 2026-09-25):
  - US100.cash: USD 1 per index point per lot, zero commission; one sizing unit = 1 lot.
  - Costs: half the measured Dukascopy median RTH spread + 1 NQ tick of slippage per fill
    (FTMO does not publish spreads; open question recorded in the firm file).
  - Fees are EUR; converted at the ECB reference rate (keyless API) and refunded with the
    first reward (2-Step), so an attempt's value = rewards - fee + fee x (reward received).
Parameters and sizes are re-selected per walk-forward fold on training data only. Members'
holdouts were opened under Apex costs on the same prices, so this run's holdout is
contaminated and its holdout gate fails (verdict capped at Contender).
"""

import json
import time
import uuid
from datetime import UTC, datetime
from pathlib import Path

import httpx
import matplotlib.pyplot as plt
import numpy as np
import polars as pl
import yaml

from propquant import paths
from propquant.data import store
from propquant.engine.backtest import Costs
from propquant.firms import sim_static
from propquant.gauntlet import challenge as ch
from propquant.gauntlet import config, random_entry, stats, verdict
from propquant.gauntlet.portfolio import Member, _member_runs
from propquant.reports import style
from propquant.reports.export import RUNS_DIR, _clean, _series
from propquant.trials import Registry
from propquant.vault import writer

LOT_GRID = (1, 2, 3, 4, 6, 8, 10, 15, 20, 30, 40, 60, 80, 100)
CFD_SYMBOL = {"NQ": "US100.cash", "ES": "US500.cash"}


def eur_usd() -> float:
    """Latest ECB EUR->USD reference rate (cached in data/ for a day)."""
    cache = paths.DATA_DIR / "ecb_eurusd.json"
    if cache.exists():
        c = json.loads(cache.read_text())
        if c["date"] == datetime.now(UTC).date().isoformat():
            return c["rate"]
    for attempt in range(6):  # flaky network: retry; never fall back to a guessed rate
        try:
            r = httpx.get("https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A",
                          params={"lastNObservations": 1, "format": "jsondata"},
                          timeout=60)  # fmt: skip
            r.raise_for_status()
            break
        except httpx.HTTPError:
            if attempt == 5:
                raise RuntimeError("ECB EUR/USD rate unavailable; not guessing one") from None
            time.sleep(10 * (attempt + 1))
    obs = r.json()["dataSets"][0]["series"]["0:0:0:0:0"]["observations"]
    rate = float(next(iter(obs.values()))[0])
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps({"date": datetime.now(UTC).date().isoformat(), "rate": rate}))
    return rate


def ftmo_2step(size: int = 50_000) -> dict:
    f = yaml.safe_load((paths.CONFIG_DIR / "firms" / "ftmo.yaml").read_text(encoding="utf-8"))
    pr = f["programmes"]["two_step"]
    ph = pr["phases"]
    phases = [ph["challenge"], ph["verification"]]
    return {
        "firm": "ftmo", "programme": "2-step", "size": size,
        "targets": np.array([size * p["profit_target_pct"] / 100 for p in phases]),
        "min_days": np.array([p["min_trading_days"] for p in phases], dtype=np.int64),
        "time_limits": np.array([p["time_limit_days"] or 0 for p in phases], dtype=np.int64),
        "daily_loss": size * phases[0]["daily_loss_pct"] / 100,
        "max_loss": size * phases[0]["max_loss_pct"] / 100,
        "split": pr["funded"]["profit_split"], "payout_days": 14,
        "fee_usd": f["fees_eur"]["two_step"][f"{size // 1000}K"] * eur_usd(),
        "refund_with_first_reward": True, "verified_on": str(f["verified_on"]),
        "usd_per_point_per_lot": f["instruments"]["US100.cash"]["usd_per_point_per_lot"],
    }  # fmt: skip


def blueberry_prime(size: int = 50_000) -> dict:
    """Blueberry Funded Prime (2-phase), config/firms/blueberry.yaml (verified 2026-09-25).

    Contract size for NAS100/SP500 is NOT published, so one sizing unit = USD 1 per index point
    (an assumption, recorded); results hold only if the account's lot step allows that
    granularity. The daily floor anchors on max(balance, equity) at the 17:00 New York reset;
    our strategies are flat by 15:55, so that equals the balance.
    """
    f = yaml.safe_load((paths.CONFIG_DIR / "firms" / "blueberry.yaml").read_text(encoding="utf-8"))
    pr = f["programmes"]["prime"]
    phases = [pr["phases"]["phase1"], pr["phases"]["phase2"]]
    return {
        "firm": "blueberry", "programme": "prime", "size": size,
        "targets": np.array([size * p["profit_target_pct"] / 100 for p in phases]),
        "min_days": np.array([p["min_active_days"] for p in phases], dtype=np.int64),
        "time_limits": np.array([p["time_limit_days"] or 0 for p in phases], dtype=np.int64),
        "daily_loss": size * phases[0]["daily_loss_pct"] / 100,
        "max_loss": size * phases[0]["max_loss_pct"] / 100,
        "split": pr["funded"]["profit_split"],
        "payout_days": pr["funded"]["reward_cycle_days"],
        "cycle_active_days": pr["funded"]["active_days_per_cycle"],
        "min_day_profit": 0.005 * size,  # an active day needs >= 0.5% realised profit
        "fee_usd": float(f["fees_usd"]["prime"][f"{size // 1000}K"]),
        "refund_with_first_reward": False, "verified_on": str(f["verified_on"]),
        "usd_per_point_per_lot": 1.0,  # ASSUMPTION: see docstring
    }  # fmt: skip


FIRMS = {"ftmo": ftmo_2step, "blueberry": blueberry_prime}


def cfd_costs(symbol: str, usd_per_point: float) -> Costs:
    """Half the median measured regular-hours spread + 1 futures tick per fill; no commission."""
    b = pl.read_parquet(store.bars_path(symbol, "1m"), columns=["ts", "spread"])
    et = pl.col("ts").dt.convert_time_zone("America/New_York")
    m = et.dt.hour().cast(pl.Int32) * 60 + et.dt.minute().cast(pl.Int32)
    spread = float(b.filter((m >= 570) & (m < 960))["spread"].median())
    return Costs(tick=1.0, point_value=usd_per_point, slip_ticks=spread / 2 + 0.25,
                 commission_side=0.0)  # fmt: skip


def _mc(pnl: dict, sizes: np.ndarray, rules: dict, starts: np.ndarray) -> np.ndarray:
    return sim_static.run_many(
        pnl["d_close"], pnl["d_low"], pnl["sess_start"], pnl["sess_day"], starts,
        sizes.astype(np.int64), float(rules["size"]), rules["targets"], rules["min_days"],
        rules["time_limits"], rules["daily_loss"], rules["max_loss"], rules["split"],
        rules["payout_days"], 365, rules.get("min_day_profit", 0.0),
        rules.get("cycle_active_days", 0),
    )  # fmt: skip


def _value(out: np.ndarray, rules: dict) -> np.ndarray:
    got = out[:, 2] >= 1
    refund = rules["fee_usd"] * got if rules["refund_with_first_reward"] else 0.0
    return out[:, 3] - rules["fee_usd"] + refund


def _summary(out: np.ndarray, rules: dict, boot: dict) -> dict:
    passed = out[:, 0] == sim_static.PASS
    paid = passed & (out[:, 2] >= 1)
    v = _value(out, rules)
    bs = stats.block_bootstrap_means(v, boot["n"], boot["block_sessions"], boot["seed"])
    used = out[passed, 1]
    return {
        "starts": len(out), "eval_pass": float(passed.mean()),
        "eval_fail": float((out[:, 0] == sim_static.FAIL).mean()),
        "eval_expired": float((out[:, 0] == sim_static.EXPIRED).mean()),
        "median_sessions_to_pass": float(np.median(used)) if len(used) else float("inf"),
        "p90_sessions_to_pass": float(np.percentile(used, 90)) if len(used) else float("inf"),
        "first_payout_given_pass": float(paid.sum() / passed.sum()) if passed.any() else 0.0,
        "end_to_end_payout": float(paid.mean()), "ev_per_attempt": float(v.mean()),
        "ev_p05": float(np.percentile(bs, 5)), "ev_p95": float(np.percentile(bs, 95)),
    }  # fmt: skip


def _pnl_from(x: dict, choose) -> dict:
    """Per-bar OOS arrays for a member, using `choose(fold)` params within each test year."""
    md = x["md_dev"]
    d_close, d_low = np.zeros(md.n), np.zeros(md.n)
    for f in x["folds"]:
        r = x["results"][json.dumps(choose(f), sort_keys=True)]
        in_f = (md.sess_day[md.sess] >= f[1]) & (md.sess_day[md.sess] <= f[2])
        d_close[in_f], d_low[in_f] = r.d_close[in_f], r.d_low[in_f]
    return {"d_close": d_close, "d_low": d_low, "sess_start": md.sess_start,
            "sess_day": md.sess_day}  # fmt: skip


def run(name: str, symbol: str = "NQ", log=print, firm: str = "ftmo") -> dict:
    cfg = config.load()
    rules = FIRMS[firm]()
    plan = f"{firm}_{rules['programme']}".replace("-", "")
    costs = cfd_costs(symbol, rules["usd_per_point_per_lot"])
    key = f"{firm}:{name}" + ("" if symbol == "NQ" else f"@{symbol}")
    reg = Registry()
    run_id = uuid.uuid4().hex[:10]
    x = _member_runs(Member(name, symbol), cfg, reg, run_id, log, costs=costs, key_suffix=":cfd")
    md = x["md_dev"]
    runway = cfg["challenge_mc"]["min_runway_sessions"]
    first_oos = int(np.searchsorted(md.sess_day, x["folds"][0][1]))
    # per-fold size (lots) chosen on training sessions only: max reach-payout with EV > 0
    sizes = np.ones(len(md.sess_day), dtype=np.int64)
    fold_rows = []
    for y, d0, d1, p in x["folds"]:
        a = int(np.searchsorted(md.sess_day, d0))
        r = x["results"][json.dumps(p, sort_keys=True)]
        full = {"d_close": r.d_close, "d_low": r.d_low, "d_high": r.d_high,
                "sess_start": md.sess_start, "sess_day": md.sess_day}  # fmt: skip
        train = ch.slice_pnl(full, 0, a)
        st = ch.start_sessions(a, runway)
        best, key_best = 1, (-1.0, -np.inf)
        for lots in LOT_GRID:
            out = _mc(train, np.full(a, lots), rules, st)
            v, e2e = (
                float(_value(out, rules).mean()),
                float(((out[:, 0] == 1) & (out[:, 2] >= 1)).mean()),
            )
            if v > 0 and (e2e, v) > key_best:
                best, key_best = lots, (e2e, v)
        b = int(np.searchsorted(md.sess_day, d1, side="right"))
        sizes[a:b] = best
        fold_rows.append({"test_year": y, "params": p, "train_sharpe": None,
                          "sizes": {plan: best}, "policies": {}})  # fmt: skip
        log(f"  fold {y}: params {p} lots {best}")
    pnl = _pnl_from(x, lambda f: f[3])
    oos = {"d_close": pnl["d_close"][md.sess_start[first_oos]:],
           "d_low": pnl["d_low"][md.sess_start[first_oos]:],
           "sess_start": md.sess_start[first_oos:] - md.sess_start[first_oos],
           "sess_day": md.sess_day[first_oos:]}  # fmt: skip
    starts = ch.start_sessions(len(oos["sess_day"]), runway)
    out = _mc(oos, sizes[first_oos:], rules, starts)
    summ = _summary(out, rules, cfg["challenge_mc"]["bootstrap"])
    daily = np.add.reduceat(oos["d_close"], oos["sess_start"][:-1])  # USD per lot per session
    # statistics
    trades = []
    for _y, d0, d1, p in x["folds"]:
        t = x["results"][json.dumps(p, sort_keys=True)].trades
        ed = md.sess_day[md.sess[t[:, 0].astype(np.int64)]]
        trades.append(t[(ed >= d0) & (ed <= d1)])
    t = np.concatenate(trades)
    re_cfg = cfg["random_entry"]
    cost_rt = 2 * costs.slip_ticks * costs.tick * costs.point_value
    re_runs = random_entry.benchmark(md, t, costs.point_value, cost_rt, re_cfg["runs"],
                                     re_cfg["seed"], 970)  # fmt: skip
    re_pct = random_entry.percentile(float(t[:, 5].sum()), re_runs)
    n_trials = reg.n_trials()
    sc = reg.con.execute("SELECT score FROM trials WHERE scope='dev'").fetchnumpy()["score"]
    reg.release()
    dsr = stats.dsr(daily, n_trials, float(np.var(sc)))
    cs = verdict.checks(cfg["gates"], oos_trades=len(t), dsr=dsr, re_pct=re_pct, ch=summ,
                        holdout_ok=False)  # fmt: skip
    v, failed = verdict.decide(cs, cfg["contender"], summ, cfg.get("champion"))
    # evidence: equity + outcome chart
    style.apply()
    att = writer.attachments_dir()
    fig, ax = plt.subplots(figsize=(12, 3.6))
    days = [np.datetime64("1970-01-01") + int(d) for d in oos["sess_day"]]
    ax.plot(days, np.cumsum(daily), color=style.SERIES[0])
    ax.axhline(0, color=style.NEUTRAL, lw=0.8)
    ax.set_title(f"{key}: out-of-sample equity per lot (USD, CFD costs)")
    style.save(fig, att / f"{key.replace(':', '_')}-equity.png")
    rec = {
        "run_id": run_id, "created": datetime.now(UTC).isoformat(timespec="seconds"),
        "strategy": key, "family": x["cls"].family, "verdict": v, "failed": failed,
        "best_plan": plan, "commit": reg.commit, "data_hash": md.data_hash,
        "seed": re_cfg["seed"], "final_params": x["final"], "final_sizes": {},
        "final_policies": {}, "checks": [c.row() for c in cs],
        "oos_challenge": {plan: summ}, "holdout": None,
        "holdout_note": "CONTAMINATED: holdout already opened for these prices under Apex",
        "stats": {"psr": stats.psr(daily), "dsr": dsr, "n_trials": n_trials,
                  "sr_variance": float(np.var(sc)), "re_percentile": re_pct,
                  "oos_total": float(t[:, 5].sum()), "oos_trades": len(t),
                  "oos_sharpe_ann": stats.annualised_sharpe(daily)},
        "grid": [], "folds": fold_rows, "oos_equity": _series(oos["sess_day"], daily),
        "holdout_equity": None, "random_entry_hist": np.histogram(re_runs, 30)[0].tolist(),
        "random_entry_edges": np.histogram(re_runs, 30)[1].tolist(),
        "charts": [f"{key.replace(':', '_')}-equity.png"],
        "firm_rules": {k: (vv.tolist() if isinstance(vv, np.ndarray) else vv)
                       for k, vv in rules.items()},
        "cfd_costs": {"slip_per_fill_points": costs.slip_ticks, "usd_per_point_per_lot":
                      costs.point_value},
    }  # fmt: skip
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    Path(RUNS_DIR / f"{run_id}.json").write_text(json.dumps(_clean(rec), indent=1), "utf-8")
    reg.log_run(run_id, key, v, {"verdict": v, "plan": plan,
                                 "e2e": summ["end_to_end_payout"], "eval_pass": summ["eval_pass"],
                                 "ev": summ["ev_per_attempt"], "dsr": dsr, "re_pct": re_pct,
                                 "oos_trades": len(t)}, md.data_hash, re_cfg["seed"])  # fmt: skip
    rows = [c.row() for c in cs]
    metrics = writer.md_table([{"metric": k, "value": vv} for k, vv in summ.items()])
    writer.write_note(
        f"{'Graveyard' if v == 'graveyard' else 'Strategies'}/{key.replace(':', '_')}.md",
        f"---\ntype: strategy\nstrategy: {key}\nfirm: {firm}\nverdict: {v}\nrun_id: {run_id}\n---\n"
        f"# {key}: **{v.upper()}** ({firm} {rules['programme']} 50K, CFD costs)\n\n"
        f"{writer.md_table(rows)}\n\n{metrics}\n\n"
        f"Fee ${rules['fee_usd']:,.0f} (list price; refunded with first reward: "
        f"{rules['refund_with_first_reward']}). "
        f"Costs: {costs.slip_ticks:.2f} pts per fill, no commission. Holdout contaminated.\n\n"
        f"![[{key.replace(':', '_')}-equity.png]]\n",
    )  # fmt: skip
    return rec
