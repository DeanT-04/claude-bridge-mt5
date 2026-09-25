"""Evidence charts + vault note for one gauntlet run. Every number comes from the result object."""

from datetime import date, timedelta

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm
from matplotlib.dates import AutoDateLocator, ConciseDateFormatter

from propquant.firms import sim
from propquant.firms.base import challenge
from propquant.gauntlet import config
from propquant.gauntlet.run import GauntletResult
from propquant.reports import style
from propquant.vault import writer

EPOCH = date(1970, 1, 1)
DIVERGING = ("#e34948", "#f0efec", "#2a78d6")  # red <- loss | neutral | gain -> blue


def _dates(days: np.ndarray) -> list[date]:
    return [EPOCH + timedelta(days=int(d)) for d in days]


def _date_axis(ax) -> None:
    loc = AutoDateLocator()
    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(ConciseDateFormatter(loc))


def equity(r: GauntletResult, path) -> None:
    fig, ax = plt.subplots(figsize=(12, 3.8))
    oos = np.cumsum(r.oos_daily)
    ax.plot(_dates(r.oos_days), oos, color=style.SERIES[0], label="walk-forward out-of-sample")
    if r.holdout_daily is not None:
        h = oos[-1] + np.cumsum(r.holdout_daily)
        ax.plot(_dates(r.holdout_days), h, color=style.SERIES[1], label="locked holdout")
        ax.axvspan(_dates(r.holdout_days[:1])[0], _dates(r.holdout_days[-1:])[0],
                   color=style.SERIES[1], alpha=0.06, lw=0)  # fmt: skip
    ax.axhline(0, color=style.NEUTRAL, lw=0.8)
    ax.set_title("Equity per micro contract, after costs (USD)")
    ax.legend(loc="upper left")
    _date_axis(ax)
    style.save(fig, path)


def random_entry(r: GauntletResult, path) -> None:
    fig, ax = plt.subplots(figsize=(6, 3.6))
    ax.hist(r.re_runs, bins=50, color=style.NEUTRAL, alpha=0.7, label="1,000 random-entry runs")
    ax.axvline(r.oos_total, color=style.SERIES[0], lw=2,
               label=f"strategy: beats {r.re_percentile:.1%}")  # fmt: skip
    ax.set_title("Out-of-sample P&L vs random timing (USD/micro)")
    ax.legend(loc="upper left")
    style.save(fig, path)


def fan(r: GauntletResult, path, n_paths: int = 120) -> None:
    cfg = config.load()
    spec = challenge(cfg["firm"]["name"], r.best_plan, cfg["firm"]["size"])
    if r.family == "portfolio":  # one unit = 1 micro of every member
        units = max(1, len(r.final_params))
        spec = spec.model_copy(update={"eval_max_micros": spec.eval_max_micros // units})
    out, pnl = r.mc_paths["out"], r.mc_paths["pnl"]
    sizes = np.concatenate([np.full(f.test_sessions[1] - f.test_sessions[0], f.sizes[r.best_plan])
                            for f in r.folds])  # fmt: skip
    idx = np.linspace(0, len(out) - 1, min(n_paths, len(out))).astype(int)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    colors = {sim.PASS: style.SERIES[0], sim.FAIL: style.CRITICAL, sim.EXPIRED: style.NEUTRAL}
    for j in idx:
        res, bal, _thr = sim.eval_path(
            pnl["d_close"], pnl["d_low"], pnl["d_high"], pnl["sess_start"], pnl["sess_day"],
            int(j), sizes, spec.balance, spec.target, spec.drawdown, spec.eval_dll,
            spec.eval_max_micros, spec.eval_trail, spec.eval_trail_cap, spec.access_days,
            r.policy_rows[r.best_plan],
        )  # fmt: skip
        ax.plot(bal, color=colors.get(res, style.NEUTRAL), alpha=0.35, lw=1)
    ax.axhline(spec.balance + spec.target, color=style.GOOD, ls="--", lw=1)
    ax.axhline(spec.balance - spec.drawdown, color=style.CRITICAL, ls="--", lw=1)
    ax.text(0.2, spec.balance + spec.target, " target", va="bottom", color=style.TEXT_2)
    ax.text(0.2, spec.balance - spec.drawdown, " starting threshold", va="top", color=style.TEXT_2)
    c = r.oos_challenge[r.best_plan]
    ax.set_title(
        f"{len(idx)} evaluation paths ({r.best_plan}): pass {c['eval_pass']:.0%} "
        f"(blue), fail {c['eval_fail']:.0%} (red), expired {c['eval_expired']:.0%}"
    )
    ax.set_xlabel("sessions since purchase")
    ax.set_ylabel("closing balance (USD)")
    style.save(fig, path)


def drawdown(r: GauntletResult, path) -> None:
    size = np.median([f.sizes[r.best_plan] for f in r.folds])
    eq = np.cumsum(r.oos_daily) * size
    dd = eq - np.maximum.accumulate(np.r_[0.0, eq])[1:]
    cfg = config.load()
    spec = challenge(cfg["firm"]["name"], r.best_plan, cfg["firm"]["size"])
    fig, ax = plt.subplots(figsize=(12, 3.2))
    ax.fill_between(_dates(r.oos_days), dd, 0, color=style.SERIES[0], alpha=0.35, lw=0)
    ax.axhline(-spec.drawdown, color=style.CRITICAL, ls="--", lw=1)
    ax.text(_dates(r.oos_days[:1])[0], -spec.drawdown, f" max drawdown ${spec.drawdown:,.0f}",
            va="bottom", color=style.TEXT_2)  # fmt: skip
    ax.set_title(f"Out-of-sample drawdown from peak at the median size ({size:g} micros)")
    _date_axis(ax)
    style.save(fig, path)


def monthly(r: GauntletResult, path) -> None:
    ds = _dates(r.oos_days)
    years = sorted({d.year for d in ds})
    grid = np.full((len(years), 12), np.nan)
    for d, v in zip(ds, r.oos_daily, strict=True):
        y, m = years.index(d.year), d.month - 1
        grid[y, m] = (0 if np.isnan(grid[y, m]) else grid[y, m]) + v
    lim = np.nanmax(np.abs(grid)) or 1.0
    from matplotlib.colors import LinearSegmentedColormap

    cmap = LinearSegmentedColormap.from_list("div", DIVERGING)
    fig, ax = plt.subplots(figsize=(9, 0.45 * len(years) + 1.2))
    ax.imshow(grid, cmap=cmap, norm=TwoSlopeNorm(0, -lim, lim), aspect="auto")
    ax.set_xticks(range(12), ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"])
    ax.set_yticks(range(len(years)), [str(y) for y in years])
    for (i, j), v in np.ndenumerate(grid):
        if not np.isnan(v):
            ax.text(j, i, f"{v:,.0f}", ha="center", va="center", fontsize=7, color=style.TEXT)
    ax.grid(False)
    ax.set_title("Monthly out-of-sample P&L per micro (USD)")
    style.save(fig, path)


def sensitivity(r: GauntletResult, path) -> None:
    if not r.grid:  # portfolios have no parameter grid of their own
        return
    sr = np.array(r.grid_dev_sharpe) * np.sqrt(252)
    order = np.argsort(sr)
    chosen = r.grid.index(r.final_params)
    fig, ax = plt.subplots(figsize=(8, 3.2))
    colors = [style.SERIES[1] if k == chosen else style.SERIES[0] for k in order]
    ax.bar(range(len(sr)), sr[order], color=colors, width=0.8)
    ax.axhline(0, color=style.NEUTRAL, lw=0.8)
    ax.set_title(f"Parameter sensitivity: annualised dev Sharpe of all {len(sr)} configs "
                 "(orange = final pick)")  # fmt: skip
    ax.set_xticks([])
    style.save(fig, path)


def write(r: GauntletResult) -> str:
    style.apply()
    slug = r.strategy
    att = writer.attachments_dir()
    charts = {
        "equity": equity, "random": random_entry, "fan": fan, "drawdown": drawdown,
        "monthly": monthly, "sensitivity": sensitivity,
    }  # fmt: skip
    for key, fn in charts.items():
        fn(r, att / f"{slug}-{key}.png")

    c = r.oos_challenge
    plans = list(c)
    ch_rows = [
        {"metric": k, **{p: c[p][k] for p in plans}}
        for k in ("eval_pass", "eval_fail", "eval_expired", "median_sessions_to_pass",
                  "p90_sessions_to_pass", "first_payout_given_pass", "end_to_end_payout",
                  "mean_payouts_given_pass", "ev_per_attempt", "ev_p05", "ev_p95",
                  "max_best_day_share", "starts", "effective_n", "censored_pa")
    ]  # fmt: skip
    fold_rows = [
        {"test year": f.test_year, "params": f.params, "train SR (daily)": f.train_sharpe,
         **{f"size {p}": f.sizes[p] for p in plans},
         **{f"policy {p}": tuple(round(x, 2) for x in f.policies[p]) for p in plans}}
        for f in r.folds
    ]  # fmt: skip
    hold = "not run"
    if r.holdout:
        hold = writer.md_table([
            {"metric": k, **{p: r.holdout[p][k] for p in plans}}
            for k in ("eval_pass", "end_to_end_payout", "ev_per_attempt", "starts")
        ])  # fmt: skip
        hold += f"\n\nHoldout daily mean P&L per micro: {np.mean(r.holdout_daily):.2f} USD"
    folder = {
        "champion": "Strategies",
        "elite": "Strategies",
        "contender": "Strategies",
        "graveyard": "Graveyard",
    }
    reasons = "\n".join(f"- {f}" for f in r.failed) or "- none"
    body = f"""---
type: strategy
strategy: {r.strategy}
family: {r.family}
verdict: {r.verdict}
plan: {r.best_plan}
run_id: {r.run_id}
data_hash: {r.data_hash}
commit: {r.commit}
seed: {r.seed}
---
# {r.strategy}: **{r.verdict.upper()}**

Best plan: **Apex {r.best_plan} 50K**. Final params {r.final_params}; base sizes (micros)
{r.final_sizes}; sizing policy (alpha, beta, mu) {r.final_policies}.

## Gates (out-of-sample unless noted)
{writer.md_table([ck.row() for ck in r.checks])}

Failed gates:
{reasons}

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
{writer.md_table(ch_rows)}

## Statistics
- OOS trades: {len(r.oos_trades):,}; total P&L per micro {r.oos_total:,.0f} USD
- Annualised Sharpe (daily, per micro): {
        np.mean(r.oos_daily) / (np.std(r.oos_daily) or 1) * np.sqrt(252):.2f}
- PSR (vs 0): {r.psr:.3f}; **Deflated Sharpe: {r.dsr:.3f}** over {r.n_trials} recorded trials
  (Sharpe variance across trials {r.sr_variance:.2e})
- Random-entry percentile: {r.re_percentile:.3f}

## Walk-forward folds (params and size picked on training years only)
{writer.md_table(fold_rows)}

## Holdout ({r.holdout_note})
{hold}

## Evidence
![[{slug}-equity.png]]
![[{slug}-fan.png]]
![[{slug}-random.png]]
![[{slug}-drawdown.png]]
![[{slug}-monthly.png]]
{"" if not r.grid else f"![[{slug}-sensitivity.png]]"}

Reproduce: `uv run propquant gauntlet run {r.strategy}`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
"""
    path = writer.write_note(f"{folder[r.verdict]}/{slug}.md", body)
    other = "Graveyard" if folder[r.verdict] == "Strategies" else "Strategies"
    stale = writer.attachments_dir().parent / other / f"{slug}.md"
    if stale.exists():
        stale.unlink()
    return str(path)
