"""The gauntlet: walk-forward selection -> OOS challenge Monte Carlo -> statistics -> holdout.

Data discipline:
  * The parameter sweep only ever sees data before the holdout (the market data is truncated).
  * Each walk-forward fold picks params AND position size on its training years only, then
    trades the next year untouched. The stitched test years are the out-of-sample record.
  * The holdout is run once per (strategy, params) and every access is logged.
"""

import itertools
import json
import uuid
from dataclasses import dataclass, field
from datetime import date, timedelta

import numpy as np

from propquant.engine import backtest
from propquant.engine.backtest import Costs, MarketData, Result
from propquant.firms import sim
from propquant.firms.base import ChallengeSpec, challenge
from propquant.gauntlet import challenge as ch
from propquant.gauntlet import config, random_entry, stats, verdict
from propquant.strategies.base import Strategy, get
from propquant.trials import Registry
from propquant.vault import ideas

MIN_TRAIN_TRADES = 50


@dataclass
class Fold:
    test_year: int
    train_sessions: tuple[int, int]
    test_sessions: tuple[int, int]
    params: dict
    train_sharpe: float
    sizes: dict[str, int] = field(default_factory=dict)
    policies: dict[str, tuple] = field(default_factory=dict)


@dataclass
class GauntletResult:
    strategy: str
    family: str
    run_id: str
    data_hash: str
    commit: str
    seed: int
    grid: list[dict]
    grid_dev_sharpe: list[float]
    grid_metrics: list[dict]
    folds: list[Fold]
    oos_days: np.ndarray  # session day numbers
    oos_daily: np.ndarray  # USD per micro per session
    oos_trades: np.ndarray
    oos_challenge: dict[str, dict]
    best_plan: str
    re_runs: np.ndarray
    re_percentile: float
    oos_total: float
    psr: float
    dsr: float
    n_trials: int
    sr_variance: float
    final_params: dict
    final_sizes: dict[str, int]
    final_policies: dict[str, tuple]
    policy_rows: dict[str, np.ndarray]  # OOS (alpha, beta, mu) per session, per plan
    holdout: dict | None
    holdout_days: np.ndarray | None
    holdout_daily: np.ndarray | None
    holdout_note: str
    checks: list[verdict.Check]
    verdict: str
    failed: list[str]
    mc_paths: dict = field(default_factory=dict)

    def summary(self) -> dict:
        c = self.oos_challenge[self.best_plan]
        return {
            "verdict": self.verdict,
            "plan": self.best_plan,
            "e2e": c["end_to_end_payout"],
            "eval_pass": c["eval_pass"],
            "ev": c["ev_per_attempt"],
            "dsr": self.dsr,
            "re_pct": self.re_percentile,
            "oos_trades": len(self.oos_trades),
        }


def param_grid(cls: type[Strategy]) -> list[dict]:
    keys = list(cls.param_space)
    if not keys:
        return [dict(cls.defaults)]
    combos = itertools.product(*(cls.param_space[k] for k in keys))
    return [{**cls.defaults, **dict(zip(keys, c, strict=True))} for c in combos]


def _sessions_from(md: MarketData, d: date) -> int:
    return int(np.searchsorted(md.sess_day, config.day_number(d)))


def _folds(md_dev: MarketData, cfg: dict) -> list[tuple[int, int, int]]:
    """(test_year, test_first_session, test_end_session) over the dev period."""
    n = len(md_dev.sess_day)
    out = []
    y = cfg["walk_forward"]["first_test_year"]
    while True:
        a = _sessions_from(md_dev, date(y, 1, 1))
        if a >= n:
            break
        b = min(_sessions_from(md_dev, date(y + 1, 1, 1)), n)
        out.append((y, a, b))
        y += 1
    return out


def _stitch(results: dict[str, Result], folds: list[Fold], md: MarketData, oos_first: int):
    """Per-bar OOS arrays (for sessions [oos_first, last fold end)) from each fold's choice."""
    oos_end = folds[-1].test_sessions[1]
    a0, b0 = md.sess_start[oos_first], md.sess_start[oos_end]
    d_close, d_low, d_high = (np.zeros(b0 - a0) for _ in range(3))
    trades = []
    for f in folds:
        r = results[json.dumps(f.params, sort_keys=True)]
        a, b = md.sess_start[f.test_sessions[0]], md.sess_start[f.test_sessions[1]]
        d_close[a - a0 : b - a0] = r.d_close[a:b]
        d_low[a - a0 : b - a0] = r.d_low[a:b]
        d_high[a - a0 : b - a0] = r.d_high[a:b]
        t = r.trades
        trades.append(t[(t[:, 0] >= a) & (t[:, 0] < b)])
    pnl = {
        "d_close": d_close,
        "d_low": d_low,
        "d_high": d_high,
        "sess_start": md.sess_start[oos_first : oos_end + 1] - a0,
        "sess_day": md.sess_day[oos_first:oos_end],
    }
    return pnl, np.concatenate(trades) if trades else np.zeros((0, 7))


def _mc(pnl: dict, sizes: np.ndarray, spec: ChallengeSpec, cfg: dict,
        policy=sim.NO_POLICY) -> tuple[dict, np.ndarray]:  # fmt: skip
    mc = cfg["challenge_mc"]
    starts = ch.start_sessions(len(pnl["sess_start"]) - 1, mc["min_runway_sessions"])
    out = sim.run_many(pnl, starts, sizes, spec, policy)
    return ch.summarise(out, spec, mc["bootstrap"]).as_dict(), out


def run(name: str, symbol: str = "NQ", md_full: MarketData | None = None, cfg: dict | None = None,
        registry: Registry | None = None, force_holdout: bool = False,
        progress=print) -> GauntletResult:  # fmt: skip
    cfg = cfg or config.load()
    cls = get(name)
    idea_hash = ""
    if cls.needs_idea_note:
        idea_hash = ideas.require(name, symbol)  # no pre-registered hypothesis -> no test
    skey = name if symbol == "NQ" else f"{name}@{symbol}"  # registry / vault identity
    own_registry = registry is None
    reg = registry or Registry()
    run_id = uuid.uuid4().hex[:10]
    seed = cfg["random_entry"]["seed"]
    try:
        if md_full is None:
            md_full = MarketData.load(symbol, cls.timeframe)
        first = _sessions_from(md_full, cfg["research_start"])
        end = _sessions_from(md_full, cfg["holdout_end"] + timedelta(days=1))
        md_full = md_full.slice_sessions(first, end)
        dev_end = _sessions_from(md_full, cfg["holdout_start"])
        md_dev = md_full.slice_sessions(0, dev_end)  # the sweep never sees the holdout
        costs = Costs.micro(symbol, slip_ticks=cfg["costs"]["slip_ticks"])
        plans = {p: challenge(cfg["firm"]["name"], p, cfg["firm"]["size"])
                 for p in cfg["firm"]["plans"]}  # fmt: skip
        costs.commission_side = next(iter(plans.values())).commission_micro_rt / 2
        runway = cfg["challenge_mc"]["min_runway_sessions"]
        max_micros = cfg["max_size_micros"]
        sz_cfg = cfg.get("sizing_policy", {"alpha": [0.0], "beta": [0.0]})
        sizing = (tuple(sz_cfg["alpha"]), tuple(sz_cfg["beta"]))

        # ---- 1. sweep the pre-registered grid on dev data (every point is a counted trial)
        grid = param_grid(cls)
        progress(f"{name}: sweeping {len(grid)} configs on {len(md_dev.sess_day)} dev sessions")
        daily, n_trades_by_sess, dev_sharpe, grid_metrics = [], [], [], []
        for p in grid:
            r = cls(**p).backtest(md_dev, costs)
            d = r.daily_pnl()
            daily.append(d)
            wins = r.trades[:, 5] > 0 if len(r.trades) else np.zeros(0, bool)
            grid_metrics.append({
                "params": p, "dev_sharpe_ann": stats.annualised_sharpe(d),
                "trades": len(r.trades), "net_pnl": float(r.trades[:, 5].sum()),
                "win_rate": float(wins.mean()) if len(wins) else 0.0,
            })  # fmt: skip
            cnt = np.zeros(len(md_dev.sess_day))
            np.add.at(cnt, md_dev.sess[r.trades[:, 0].astype(np.int64)], 1)
            n_trades_by_sess.append(cnt)
            dev_sharpe.append(stats.sharpe(d))
        reg.add_trials(run_id, skey, cls.family,
                       [(p, "dev", s) for p, s in zip(grid, dev_sharpe, strict=True)],
                       md_dev.data_hash)  # fmt: skip

        # ---- 2. walk-forward: choose params + size per fold on training data only
        folds: list[Fold] = []
        cache: dict[str, Result] = {}
        for y, a, b in _folds(md_dev, cfg):
            scores = [
                stats.sharpe(d[:a]) if c[:a].sum() >= MIN_TRAIN_TRADES else -np.inf
                for d, c in zip(daily, n_trades_by_sess, strict=True)
            ]
            k = int(np.argmax(scores))
            f = Fold(y, (0, a), (a, b), grid[k], float(scores[k]))
            key = json.dumps(grid[k], sort_keys=True)
            if key not in cache:
                cache[key] = cls(**grid[k]).backtest(md_dev, costs)
            train = ch.slice_pnl(cache[key].sim_input(), 0, a)
            for plan, spec in plans.items():
                f.sizes[plan], f.policies[plan] = ch.choose_sizing(
                    train, spec, runway, max_micros, *sizing
                )
            folds.append(f)
            progress(
                f"  fold {y}: params={grid[k]} train SR={scores[k]:.3f} sizes={f.sizes} "
                f"policies={ {p: tuple(round(x, 2) for x in v) for p, v in f.policies.items()} }"
            )
        oos_first = folds[0].test_sessions[0]
        oos_pnl, oos_trades = _stitch(cache, folds, md_dev, oos_first)
        oos_daily = np.add.reduceat(oos_pnl["d_close"], oos_pnl["sess_start"][:-1])

        # ---- 3. OOS challenge Monte Carlo per plan (sizes from each fold's training)
        oos_ch, mc_out, pol_rows = {}, {}, {}
        for plan, spec in plans.items():
            sizes = np.concatenate([np.full(f.test_sessions[1] - f.test_sessions[0],
                                            f.sizes[plan]) for f in folds])  # fmt: skip
            pol_rows[plan] = np.concatenate([
                np.tile(f.policies[plan], (f.test_sessions[1] - f.test_sessions[0], 1))
                for f in folds
            ])  # fmt: skip
            oos_ch[plan], mc_out[plan] = _mc(oos_pnl, sizes, spec, cfg, pol_rows[plan])
        # rank plans by the chance of completing every stage; EV breaks ties
        best_plan = max(oos_ch, key=lambda p: (oos_ch[p]["end_to_end_payout"],
                                               oos_ch[p]["ev_per_attempt"]))  # fmt: skip

        # ---- 4. statistics: random entry + deflated Sharpe
        re_cfg = cfg["random_entry"]
        cost_rt = 2 * costs.commission_side + 2 * costs.slip_ticks * costs.tick * costs.point_value
        re_runs = random_entry.benchmark(md_dev, oos_trades, costs.point_value, cost_rt,
                                         re_cfg["runs"], re_cfg["seed"],
                                         backtest.DEFAULT_FLAT_MINUTE)  # fmt: skip
        oos_total = float(oos_trades[:, 5].sum()) if len(oos_trades) else 0.0
        re_pct = random_entry.percentile(oos_total, re_runs)
        n_trials = reg.n_trials()
        scores = reg.con.execute("SELECT score FROM trials WHERE scope='dev'").fetchnumpy()
        reg.release()
        sr_var = float(np.var(scores["score"])) if len(scores["score"]) > 1 else 0.0
        dsr = stats.dsr(oos_daily, n_trials, sr_var)
        psr = stats.psr(oos_daily)

        # ---- 5. holdout (once per config)
        dev_scores = [
            s if c.sum() >= MIN_TRAIN_TRADES else -np.inf
            for s, c in zip(dev_sharpe, n_trades_by_sess, strict=True)
        ]
        final = grid[int(np.argmax(dev_scores))]
        key = json.dumps(final, sort_keys=True)
        if key not in cache:
            cache[key] = cls(**final).backtest(md_dev, costs)
        dev_pnl = cache[key].sim_input()
        final_sizing = {p: ch.choose_sizing(dev_pnl, s, runway, max_micros, *sizing)
                        for p, s in plans.items()}  # fmt: skip
        final_sizes = {p: v[0] for p, v in final_sizing.items()}
        final_policies = {p: v[1] for p, v in final_sizing.items()}
        holdout, h_days, h_daily, note = None, None, None, ""
        uses = reg.holdout_uses(skey, final)
        if uses and not force_holdout:
            note = f"holdout already used {uses}x for these params: not re-run"
        else:
            reg.log_holdout(run_id, skey, final, forced=bool(uses))
            full = cls(**final).backtest(md_full, costs)
            h_pnl = ch.slice_pnl(full.sim_input(), dev_end, len(md_full.sess_day))
            h_daily = np.add.reduceat(h_pnl["d_close"], h_pnl["sess_start"][:-1])
            h_days = h_pnl["sess_day"]
            holdout = {p: _mc(h_pnl, np.full(len(h_days), final_sizes[p]), s, cfg,
                              final_policies[p])[0]
                       for p, s in plans.items()}  # fmt: skip
            note = "first access" if not uses else f"FORCED re-access (used {uses}x before)"
        hg = cfg["gates"]["holdout"]
        holdout_ok = bool(
            holdout is not None
            and h_daily is not None
            and float(np.mean(h_daily)) > hg["min_daily_mean"]
            and holdout[best_plan]["eval_pass"]
            >= oos_ch[best_plan]["eval_pass"] - hg["min_pass_rate_drop"]
        )

        # ---- 6. verdict
        cs = verdict.checks(cfg["gates"], oos_trades=len(oos_trades), dsr=dsr, re_pct=re_pct,
                            ch=oos_ch[best_plan], holdout_ok=holdout_ok)  # fmt: skip
        v, failed = verdict.decide(cs, cfg["contender"], oos_ch[best_plan], cfg.get("champion"))
        res = GauntletResult(
            strategy=skey, family=cls.family, run_id=run_id, data_hash=md_dev.data_hash,
            commit=reg.commit, seed=seed, grid=grid, grid_dev_sharpe=dev_sharpe,
            grid_metrics=grid_metrics, folds=folds,
            oos_days=oos_pnl["sess_day"], oos_daily=oos_daily, oos_trades=oos_trades,
            oos_challenge=oos_ch, best_plan=best_plan, re_runs=re_runs, re_percentile=re_pct,
            oos_total=oos_total, psr=psr, dsr=dsr, n_trials=n_trials, sr_variance=sr_var,
            final_params=final, final_sizes=final_sizes, final_policies=final_policies,
            policy_rows=pol_rows, holdout=holdout, holdout_days=h_days,
            holdout_daily=h_daily, holdout_note=note, checks=cs, verdict=v, failed=failed,
            mc_paths={"out": mc_out[best_plan], "pnl": oos_pnl},
        )  # fmt: skip
        reg.log_run(run_id, skey, v, res.summary() | {"idea_hash": idea_hash}, md_dev.data_hash,
                    seed)  # fmt: skip
        return res
    finally:
        if own_registry:
            reg.close()
