"""Machine-readable record of every gauntlet run (registry/runs/<run_id>.json).

The dashboard reads these; nothing in them is computed anywhere but the gauntlet itself.
"""

import json
from datetime import UTC, datetime

import numpy as np

from propquant.gauntlet.run import GauntletResult
from propquant.paths import REPO_ROOT

RUNS_DIR = REPO_ROOT / "registry" / "runs"
EPOCH = np.datetime64("1970-01-01")


def _clean(x):
    if isinstance(x, dict):
        return {str(k): _clean(v) for k, v in x.items()}
    if isinstance(x, list | tuple):
        return [_clean(v) for v in x]
    if isinstance(x, np.integer):
        return int(x)
    if isinstance(x, float | np.floating):
        return None if not np.isfinite(x) else round(float(x), 6)
    return x


def _series(days: np.ndarray, daily: np.ndarray, max_points: int = 600) -> dict:
    eq = np.cumsum(daily)
    step = max(1, len(eq) // max_points)
    idx = np.r_[np.arange(0, len(eq), step), len(eq) - 1] if len(eq) else np.zeros(0, int)
    return {"dates": [str(EPOCH + int(days[i])) for i in idx], "equity": eq[idx].tolist()}


def write(r: GauntletResult) -> str:
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    rec = {
        "run_id": r.run_id,
        "created": datetime.now(UTC).isoformat(timespec="seconds"),
        "strategy": r.strategy,
        "family": r.family,
        "verdict": r.verdict,
        "failed": r.failed,
        "best_plan": r.best_plan,
        "commit": r.commit,
        "data_hash": r.data_hash,
        "seed": r.seed,
        "final_params": r.final_params,
        "final_sizes": r.final_sizes,
        "final_policies": r.final_policies,
        "checks": [c.row() for c in r.checks],
        "oos_challenge": r.oos_challenge,
        "holdout": r.holdout,
        "holdout_note": r.holdout_note,
        "stats": {
            "psr": r.psr,
            "dsr": r.dsr,
            "n_trials": r.n_trials,
            "sr_variance": r.sr_variance,
            "re_percentile": r.re_percentile,
            "oos_total": r.oos_total,
            "oos_trades": len(r.oos_trades),
            "oos_sharpe_ann": float(
                np.mean(r.oos_daily) / (np.std(r.oos_daily) or 1) * np.sqrt(252)
            ),
        },
        "grid": r.grid_metrics,
        "folds": [
            {
                "test_year": f.test_year,
                "params": f.params,
                "train_sharpe": f.train_sharpe,
                "sizes": f.sizes,
                "policies": f.policies,
            }
            for f in r.folds
        ],
        "oos_equity": _series(r.oos_days, r.oos_daily),
        "holdout_equity": (
            _series(r.holdout_days, r.holdout_daily) if r.holdout_daily is not None else None
        ),
        "random_entry_hist": np.histogram(r.re_runs, bins=30)[0].tolist(),
        "random_entry_edges": np.histogram(r.re_runs, bins=30)[1].tolist(),
        "charts": [
            f"{r.strategy}-{k}.png"
            for k in ("equity", "fan", "random", "drawdown", "monthly", "sensitivity")
            if k != "sensitivity" or r.grid
        ],
    }
    path = RUNS_DIR / f"{r.run_id}.json"
    path.write_text(json.dumps(_clean(rec), indent=1), encoding="utf-8")
    return str(path)
