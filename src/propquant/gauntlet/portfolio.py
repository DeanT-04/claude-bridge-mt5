"""Portfolio gauntlet: several strategies (any instruments) traded together as one account.

Honesty rules specific to portfolios:
  * Members' parameters are re-selected per walk-forward fold with exactly the single-strategy
    rule (best training Sharpe with enough trades), never from out-of-sample results.
  * Members are combined per SESSION (instruments have different bar clocks). Each member's
    worst intraday equity point is summed with the others' (as if simultaneous) and likewise
    the best points: pessimistic for both drawdown limits and trailing thresholds.
  * Apex's contract limit is shared: one "unit" = 1 micro of every member.
  * If any member's holdout was already opened, the portfolio's holdout is CONTAMINATED and
    its holdout gate fails. Clean confirmation then has to come from forward data.
"""

import json
import uuid
from dataclasses import dataclass
from datetime import date, timedelta

import numpy as np

from propquant.engine.backtest import Costs, MarketData
from propquant.firms import sim
from propquant.firms.base import challenge
from propquant.gauntlet import challenge as ch
from propquant.gauntlet import config, random_entry, stats, verdict
from propquant.gauntlet.run import MIN_TRAIN_TRADES, Fold, GauntletResult, _folds, param_grid
from propquant.strategies.base import get
from propquant.trials import Registry
from propquant.vault import ideas


@dataclass
class Member:
    name: str
    symbol: str

    @property
    def key(self) -> str:
        return self.name if self.symbol == "NQ" else f"{self.name}@{self.symbol}"


def session_path(d_close, d_low, d_high, sess_start) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Per-session (close, worst, best) equity change, from per-bar arrays."""
    k = len(sess_start) - 1
    c, lo, hi = np.zeros(k), np.zeros(k), np.zeros(k)
    for s in range(k):
        a, b = sess_start[s], sess_start[s + 1]
        before = np.concatenate([[0.0], np.cumsum(d_close[a:b])[:-1]])
        c[s] = d_close[a:b].sum()
        lo[s] = min(0.0, (before + d_low[a:b]).min()) if b > a else 0.0
        hi[s] = max(0.0, (before + d_high[a:b]).max()) if b > a else 0.0
    return c, lo, hi


def _member_runs(m: Member, cfg: dict, reg: Registry, run_id: str, log) -> dict:
    """Sweep the member's grid on dev data, pick params per fold (training only), and return
    per-session paths for each chosen config plus the member's final (all-dev) choice."""
    cls = get(m.name)
    md = MarketData.load(m.symbol, cls.timeframe)
    first = int(np.searchsorted(md.sess_day, config.day_number(cfg["research_start"])))
    last_day = config.day_number(cfg["holdout_end"] + timedelta(days=1))
    end = int(np.searchsorted(md.sess_day, last_day))
    md = md.slice_sessions(first, end)
    dev_end = int(np.searchsorted(md.sess_day, config.day_number(cfg["holdout_start"])))
    md_dev = md.slice_sessions(0, dev_end)
    costs = Costs.micro(m.symbol, slip_ticks=cfg["costs"]["slip_ticks"])
    spec = challenge(cfg["firm"]["name"], "eod", cfg["firm"]["size"])
    costs.commission_side = spec.commission_micro_rt / 2
    grid = param_grid(cls)
    daily, counts, results = [], [], {}
    for p in grid:
        r = cls(**p).backtest(md_dev, costs)
        d = r.daily_pnl()
        cnt = np.zeros(len(md_dev.sess_day))
        np.add.at(cnt, md_dev.sess[r.trades[:, 0].astype(np.int64)], 1)
        daily.append(d)
        counts.append(cnt)
        results[json.dumps(p, sort_keys=True)] = r
    reg.add_trials(run_id, m.key, cls.family,
                   [(p, "dev", stats.sharpe(d)) for p, d in zip(grid, daily, strict=True)],
                   md_dev.data_hash)  # fmt: skip
    folds = []
    for y, a, b in _folds(md_dev, cfg):
        sc = [stats.sharpe(d[:a]) if c[:a].sum() >= MIN_TRAIN_TRADES else -np.inf
              for d, c in zip(daily, counts, strict=True)]  # fmt: skip
        k = int(np.argmax(sc))
        folds.append((y, md_dev.sess_day[a], md_dev.sess_day[b - 1], grid[k]))
    dev_sc = [stats.sharpe(d) if c.sum() >= MIN_TRAIN_TRADES else -np.inf
              for d, c in zip(daily, counts, strict=True)]  # fmt: skip
    final = grid[int(np.argmax(dev_sc))]
    paths = {}
    for key, r in results.items():
        paths[key] = session_path(r.d_close, r.d_low, r.d_high, md_dev.sess_start)
    log(f"  member {m.key}: folds {[f[3] for f in folds]}")
    return {"cls": cls, "md": md, "md_dev": md_dev, "dev_end": dev_end, "costs": costs,
            "days": md_dev.sess_day, "folds": folds, "final": final, "paths": paths,
            "results": results}  # fmt: skip


def run(label: str, members: list[Member], cfg: dict | None = None, log=print) -> GauntletResult:
    cfg = cfg or config.load()
    idea_hash = ideas.require(label, "NQ" if all(m.symbol == "NQ" for m in members) else "ES")
    reg = Registry()
    run_id = uuid.uuid4().hex[:10]
    plans = {p: challenge(cfg["firm"]["name"], p, cfg["firm"]["size"])
             for p in cfg["firm"]["plans"]}  # fmt: skip
    per_unit = len(members)
    plans_unit = {  # one unit = 1 micro of each member: limits shrink accordingly
        p: s.model_copy(update={
            "eval_max_micros": s.eval_max_micros // per_unit,
            "tier_max_micros": [max(1, t // per_unit) for t in s.tier_max_micros],
        }) for p, s in plans.items()
    }  # fmt: skip
    runway = cfg["challenge_mc"]["min_runway_sessions"]
    sz = cfg.get("sizing_policy", {"alpha": [0.0], "beta": [0.0]})
    sizing = (tuple(sz["alpha"]), tuple(sz["beta"]))

    mem = [_member_runs(m, cfg, reg, run_id, log) for m in members]
    days = mem[0]["days"]
    for x in mem[1:]:
        days = np.intersect1d(days, x["days"])
    n = len(days)

    def combined(choose) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Sum members' per-session paths on the common days; `choose(member, s)` gives the
        params key used by that member on session s."""
        c, lo, hi = np.zeros(n), np.zeros(n), np.zeros(n)
        for x in mem:
            idx = np.searchsorted(x["days"], days)
            for s in range(n):
                pc, pl, ph = x["paths"][choose(x, days[s])]
                c[s] += pc[idx[s]]
                lo[s] += pl[idx[s]]
                hi[s] += ph[idx[s]]
        return c, lo, hi

    def fold_key(x, day):
        for _y, d0, d1, p in x["folds"]:
            if d0 <= day <= d1:
                return json.dumps(p, sort_keys=True)
        return json.dumps(x["folds"][0][3], sort_keys=True)  # pre-OOS (training) days

    def as_pnl(c, lo, hi, a=0, b=None):
        b = n if b is None else b
        return {"d_close": c[a:b].copy(), "d_low": lo[a:b].copy(), "d_high": hi[a:b].copy(),
                "sess_start": np.arange(b - a + 1, dtype=np.int64),
                "sess_day": days[a:b].copy()}  # fmt: skip

    # walk-forward: fold boundaries in portfolio session index
    years = [f[0] for f in mem[0]["folds"]]
    folds: list[Fold] = []
    for y in years:
        a = int(np.searchsorted(days, config.day_number(date(y, 1, 1))))
        b = int(np.searchsorted(days, config.day_number(date(y + 1, 1, 1))))
        b = min(b, n)
        if a >= b:
            continue
        params = {x_m.key: next(f[3] for f in x["folds"] if f[0] == y)
                  for x_m, x in zip(members, mem, strict=True)}  # fmt: skip
        f = Fold(y, (0, a), (a, b), params, float("nan"))
        # training arrays use THIS fold's member choices on the training sessions
        fk = {id(x): json.dumps(params[m_.key], sort_keys=True)
              for m_, x in zip(members, mem, strict=True)}  # fmt: skip
        tc, tl, th = combined(lambda x, _d, fk=fk: fk[id(x)])
        train = as_pnl(tc, tl, th, 0, a)
        f.train_sharpe = stats.sharpe(tc[:a])
        for plan, spec in plans_unit.items():
            f.sizes[plan], f.policies[plan] = ch.choose_sizing(train, spec, runway,
                                                               cfg["max_size_micros"] // per_unit,
                                                               *sizing)  # fmt: skip
        folds.append(f)
        log(f"  fold {y}: sizes {f.sizes}")
    oc, ol, oh = combined(fold_key)
    a0, b0 = folds[0].test_sessions[0], folds[-1].test_sessions[1]
    oos = as_pnl(oc, ol, oh, a0, b0)
    oos_daily = oc[a0:b0]
    oos_ch, mc_out, pol_rows = {}, {}, {}
    for plan, spec in plans_unit.items():
        sizes = np.concatenate([np.full(f.test_sessions[1] - f.test_sessions[0], f.sizes[plan])
                                for f in folds])  # fmt: skip
        pol_rows[plan] = np.concatenate([np.tile(f.policies[plan],
                                                 (f.test_sessions[1] - f.test_sessions[0], 1))
                                         for f in folds])  # fmt: skip
        starts = ch.start_sessions(b0 - a0, runway)
        out = sim.run_many(oos, starts, sizes, spec, pol_rows[plan])
        oos_ch[plan], mc_out[plan] = (
            ch.summarise(out, spec, cfg["challenge_mc"]["bootstrap"]).as_dict(),
            out,
        )
    best_plan = max(oos_ch, key=lambda p: (oos_ch[p]["end_to_end_payout"],
                                           oos_ch[p]["ev_per_attempt"]))  # fmt: skip

    # random entry: sum of members' random runs (same run index), vs the portfolio's total
    re_cfg = cfg["random_entry"]
    re_total, oos_total, all_trades = np.zeros(re_cfg["runs"]), 0.0, []
    for x in mem:
        c = x["costs"]
        trades = []
        for _y, d0, d1, p in x["folds"]:
            t = x["results"][json.dumps(p, sort_keys=True)].trades
            ed = x["md_dev"].sess_day[x["md_dev"].sess[t[:, 0].astype(np.int64)]]
            trades.append(t[(ed >= d0) & (ed <= d1)])
        t = np.concatenate(trades) if trades else np.zeros((0, 7))
        all_trades.append(t)
        oos_total += float(t[:, 5].sum())
        cost_rt = 2 * c.commission_side + 2 * c.slip_ticks * c.tick * c.point_value
        re_total += random_entry.benchmark(x["md_dev"], t, c.point_value, cost_rt, re_cfg["runs"],
                                           re_cfg["seed"], 970)  # fmt: skip
    re_pct = random_entry.percentile(oos_total, re_total)
    n_trials = reg.n_trials()
    sc = reg.con.execute("SELECT score FROM trials WHERE scope='dev'").fetchnumpy()["score"]
    reg.release()
    sr_var = float(np.var(sc)) if len(sc) > 1 else 0.0
    dsr = stats.dsr(oos_daily, n_trials, sr_var)

    # holdout: contaminated if any member's final config was already opened
    used = [m.key for m, x in zip(members, mem, strict=True) if reg.holdout_uses(m.key, x["final"])]
    note = (f"CONTAMINATED: member holdouts already opened ({', '.join(used)}); needs forward data"
            if used else "not run (portfolio holdout requires untouched members)")  # fmt: skip
    cs = verdict.checks(cfg["gates"], oos_trades=int(sum(len(t) for t in all_trades)), dsr=dsr,
                        re_pct=re_pct, ch=oos_ch[best_plan], holdout_ok=False)  # fmt: skip
    v, failed = verdict.decide(cs, cfg["contender"], oos_ch[best_plan], cfg.get("champion"))
    res = GauntletResult(
        strategy=label, family="portfolio", run_id=run_id, data_hash="+".join(
            x["md_dev"].data_hash for x in mem), commit=reg.commit, seed=re_cfg["seed"],
        grid=[], grid_dev_sharpe=[],
        grid_metrics=[{"params": {"member": m.key, "final": x["final"]}, "dev_sharpe_ann": None,
                       "trades": len(t), "net_pnl": float(t[:, 5].sum()), "win_rate": None}
                      for m, x, t in zip(members, mem, all_trades, strict=True)],
        folds=folds, oos_days=days[a0:b0], oos_daily=oos_daily,
        oos_trades=np.concatenate(all_trades), oos_challenge=oos_ch, best_plan=best_plan,
        re_runs=re_total, re_percentile=re_pct, oos_total=oos_total, psr=stats.psr(oos_daily),
        dsr=dsr, n_trials=n_trials, sr_variance=sr_var,
        final_params={m.key: x["final"] for m, x in zip(members, mem, strict=True)},
        final_sizes={}, final_policies={}, policy_rows=pol_rows, holdout=None,
        holdout_days=None, holdout_daily=None, holdout_note=note, checks=cs, verdict=v,
        failed=failed, mc_paths={"out": mc_out[best_plan], "pnl": oos},
    )  # fmt: skip
    reg.log_run(run_id, label, v, res.summary() | {"idea_hash": idea_hash,
                                                   "members": [m.key for m in members]},
                res.data_hash, re_cfg["seed"])  # fmt: skip
    return res
