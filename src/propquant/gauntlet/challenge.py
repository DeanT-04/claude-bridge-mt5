"""Challenge Monte Carlo summaries and position sizing from simulator output."""

from dataclasses import dataclass

import numpy as np

from propquant.firms import sim
from propquant.firms.base import ChallengeSpec
from propquant.gauntlet.stats import block_bootstrap_means

SIZE_GRID = (1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 30, 40, 50, 60)


def slice_pnl(pnl: dict, first: int, last: int) -> dict:
    """Sessions [first, last) of a sim input dict."""
    a, b = pnl["sess_start"][first], pnl["sess_start"][last]
    return {
        "d_close": pnl["d_close"][a:b],
        "d_low": pnl["d_low"][a:b],
        "d_high": pnl["d_high"][a:b],
        "sess_start": pnl["sess_start"][first : last + 1] - a,
        "sess_day": pnl["sess_day"][first:last],
    }


def start_sessions(n_sessions: int, runway: int) -> np.ndarray:
    return np.arange(0, max(0, n_sessions - runway), dtype=np.int64)


def attempt_value(out: np.ndarray, spec: ChallengeSpec) -> np.ndarray:
    """Net USD per purchased evaluation: payouts - eval fee - activation fee if passed."""
    passed = out[:, 0] == sim.PASS
    return out[:, 5] - spec.eval_fee - passed * spec.activation_fee


@dataclass
class ChallengeStats:
    plan: str
    starts: int
    effective_n: float
    eval_pass: float
    eval_fail: float
    eval_expired: float
    median_sessions_to_pass: float
    p90_sessions_to_pass: float
    first_payout_given_pass: float
    end_to_end_payout: float
    mean_payouts_given_pass: float
    ev_per_attempt: float
    ev_p05: float
    ev_p95: float
    max_best_day_share: float
    censored_pa: int

    def as_dict(self) -> dict:
        return self.__dict__.copy()


def summarise(out: np.ndarray, spec: ChallengeSpec, boot: dict) -> ChallengeStats:
    n = len(out)
    passed = out[:, 0] == sim.PASS
    paid_any = passed & (out[:, 4] >= 1)
    # PA that ended for lack of data before any payout or breach: unknown outcome
    censored = passed & (out[:, 3] == sim.NO_DATA) & (out[:, 4] == 0)
    known = passed & ~censored
    v = attempt_value(out, spec)
    bs = block_bootstrap_means(v, boot["n"], boot["block_sessions"], boot["seed"])
    used = out[passed, 1]
    med_len = float(np.median(out[:, 1])) if n else 1.0
    return ChallengeStats(
        plan=spec.plan,
        starts=n,
        effective_n=n / max(med_len, 1.0),
        eval_pass=float(passed.mean()) if n else 0.0,
        eval_fail=float((out[:, 0] == sim.FAIL).mean()) if n else 0.0,
        eval_expired=float((out[:, 0] == sim.EXPIRED).mean()) if n else 0.0,
        median_sessions_to_pass=float(np.median(used)) if len(used) else np.inf,
        p90_sessions_to_pass=float(np.percentile(used, 90)) if len(used) else np.inf,
        # censored PAs count as failures here (pessimistic) and are reported
        first_payout_given_pass=float(paid_any.sum() / passed.sum()) if passed.any() else 0.0,
        end_to_end_payout=float(paid_any.mean()) if n else 0.0,
        mean_payouts_given_pass=float(out[known, 4].mean()) if known.any() else 0.0,
        ev_per_attempt=float(v.mean()) if n else 0.0,
        ev_p05=float(np.percentile(bs, 5)),
        ev_p95=float(np.percentile(bs, 95)),
        max_best_day_share=float(out[passed, 2].max()) if passed.any() else 0.0,
        censored_pa=int(censored.sum()),
    )


def choose_size(pnl: dict, spec: ChallengeSpec, runway: int, max_micros: int,
                gates: dict | None = None) -> tuple[int, float]:  # fmt: skip
    """Size (micros) chosen on THIS data (training only).

    Goal: the highest chance of completing every stage (end-to-end payout rate) among sizes
    with positive expected profit per attempt; expected profit breaks ties. If no size is
    profitable, the least-bad size by expected profit. ``gates`` is kept for callers but the
    objective no longer depends on it.
    """
    starts = start_sessions(len(pnl["sess_start"]) - 1, runway)
    if len(starts) == 0:
        return 1, 0.0
    best, best_key, fallback, fallback_v = None, (-np.inf, -np.inf), 1, -np.inf
    for size in SIZE_GRID:
        if size > max_micros:
            break
        out = sim.run_many(pnl, starts, size, spec)
        v = float(attempt_value(out, spec).mean())
        e2e = float(((out[:, 0] == sim.PASS) & (out[:, 4] >= 1)).mean())
        if v > fallback_v:
            fallback, fallback_v = size, v
        if v > 0 and (e2e, v) > best_key:
            best, best_key = size, (e2e, v)
    return (best, best_key[1]) if best is not None else (fallback, fallback_v)


def _meets(out: np.ndarray, g: dict) -> bool:
    passed = out[:, 0] == sim.PASS
    if not passed.any():
        return False
    paid = passed & (out[:, 4] >= 1)
    used = out[passed, 1]
    return bool(
        passed.mean() >= g["eval_pass"]
        and paid.mean() >= g["end_to_end_payout"]
        and paid.sum() / passed.sum() >= g["first_payout_given_pass"]
        and np.median(used) <= g["median_sessions_to_pass"]
        and np.percentile(used, 90) <= g["p90_sessions_to_pass"]
    )
