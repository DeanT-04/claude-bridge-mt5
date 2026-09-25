"""Every Apex rule, exercised at its boundary with hand-built P&L paths (1 micro = $1 here)."""

import numpy as np
import pytest

from propquant.firms import sim
from propquant.firms.base import TRAIL_INTRADAY, challenge, load_firm

EOD = challenge("apex", "eod", "50K")
INTRA = challenge("apex", "intraday", "50K")
START = 50_000.0


def pnl(sessions: list[list[tuple[float, float, float]]], day_step: int = 1) -> dict:
    """sessions -> arrays. Each bar is (d_close, d_low, d_high) in $ per 'micro'."""
    rows = [bar for s in sessions for bar in s]
    d = np.array(rows, dtype=np.float64).reshape(-1, 3)
    starts = np.cumsum([0] + [len(s) for s in sessions]).astype(np.int64)
    return {
        "d_close": d[:, 0].copy(),
        "d_low": d[:, 1].copy(),
        "d_high": d[:, 2].copy(),
        "sess_start": starts,
        "sess_day": np.arange(len(sessions), dtype=np.int64) * day_step,
    }


def bar(close: float, low: float | None = None, high: float | None = None):
    return (
        close,
        min(0.0, close) if low is None else low,
        max(0.0, close) if high is None else high,
    )


def run_eval(p: dict, spec=EOD, size: int = 1, s0: int = 0):
    return sim.sim_eval(
        p["d_close"], p["d_low"], p["d_high"], p["sess_start"], p["sess_day"], s0, size,
        spec.balance, spec.target, spec.drawdown, spec.eval_dll, spec.eval_max_micros,
        spec.eval_trail, spec.eval_trail_cap, spec.access_days,
    )  # fmt: skip


def run_pa(p: dict, spec=EOD, size: int = 1, s1: int = 0):
    tf, tm, td = spec.tiers()
    return sim.sim_pa(
        p["d_close"], p["d_low"], p["d_high"], p["sess_start"], s1, size, spec.balance,
        spec.drawdown, spec.pa_trail, spec.pa_trail_cap, tf, tm, td, spec.min_daily_profit,
        spec.payout_min_days, spec.payout_consistency, spec.payout_min_amount,
        np.asarray(spec.payout_caps, dtype=np.float64), spec.safety_net,
    )  # fmt: skip


NO_DLL = EOD.model_copy(update={"eval_dll": 0.0})


# ---------- rule file ----------
def test_rule_file_is_verified_and_sourced() -> None:
    f = load_firm("apex")
    assert f.sources and str(f.verified_on) == "2026-09-25"
    assert EOD.target == 3000 and EOD.drawdown == 2000 and EOD.eval_dll == 1000
    assert EOD.eval_max_micros == 60 and INTRA.eval_dll == 0
    assert EOD.safety_net == 52_100 and EOD.pa_trail_cap == 50_100


def test_unspecified_size_is_rejected() -> None:
    with pytest.raises(KeyError):
        challenge("apex", "eod", "25K")  # 25K PA tiers are ambiguous at source -> excluded


# ---------- evaluation ----------
def test_pass_needs_target_at_session_close() -> None:
    assert run_eval(pnl([[bar(3000)]]))[0] == sim.PASS
    assert run_eval(pnl([[bar(2999.99)], [bar(0)]]))[0] == sim.NO_DATA


def test_intraday_touch_of_target_is_not_a_pass() -> None:
    assert run_eval(pnl([[bar(2500, high=3500)]]))[0] == sim.NO_DATA


def test_touching_eod_threshold_fails_one_cent_above_survives() -> None:
    assert run_eval(pnl([[bar(0, low=-2000)]]), NO_DLL)[0] == sim.FAIL
    assert run_eval(pnl([[bar(0, low=-1999.99)]]), NO_DLL)[0] == sim.NO_DATA


def test_eod_threshold_trails_the_close_not_the_intraday_high() -> None:
    # day 1 closes +800 after touching +1500 intraday -> threshold 48,800 (not 49,500)
    p = pnl([[bar(800, high=1500)], [bar(0, low=-1999.99)]])
    assert run_eval(p, NO_DLL)[0] == sim.NO_DATA
    p = pnl([[bar(800, high=1500)], [bar(0, low=-2000)]])
    assert run_eval(p, NO_DLL)[0] == sim.FAIL


def test_eod_threshold_never_moves_down() -> None:
    # +800 (thr 48,800), -500 (bal 50,300, thr stays), then a dip to 48,800 fails
    p = pnl([[bar(800)], [bar(-500)], [bar(0, low=-1500)]])
    assert run_eval(p, NO_DLL)[0] == sim.FAIL


def test_dll_pauses_the_day_without_failing() -> None:
    # -1,000 intraday hits the DLL: liquidated at 49,000; the rest of that session is ignored
    p = pnl([[bar(0, low=-1000), bar(-5000, low=-5000)], [bar(3000)], [bar(1000)]])
    out = run_eval(p)
    assert out[0] == sim.PASS and out[2] == 3  # 49,000 + 3,000 + 1,000 = 53,000


def test_dll_cannot_save_you_at_the_threshold() -> None:
    # day1 DLL -> 49,000. day2 DLL level 48,000 == threshold -> it's a breach, not a pause
    p = pnl([[bar(0, low=-1000)], [bar(0, low=-1000)]])
    assert run_eval(p)[0] == sim.FAIL


def test_intraday_trailing_follows_unrealised_peak() -> None:
    p = pnl([[bar(0, high=900), bar(0, low=-1100)]])
    assert run_eval(p, INTRA)[0] == sim.FAIL  # threshold moved to 48,900 on the open profit
    p = pnl([[bar(0, high=900), bar(0, low=-1099.99)]])
    assert run_eval(p, INTRA)[0] == sim.NO_DATA


def test_intraday_pessimistic_peak_before_trough_in_one_bar() -> None:
    assert run_eval(pnl([[bar(0, low=-1100, high=900)]]), INTRA)[0] == sim.FAIL


def test_intraday_trail_stops_at_target_balance() -> None:
    # peak 55,500 would put the threshold at 53,500, but it is capped at 53,000
    climb = [bar(1000)] * 5 + [bar(500)]  # in steps: each bar's low stays above the trail
    p = pnl([[*climb, bar(-2499, low=-2499.99)]])
    assert run_eval(p, INTRA)[0] == sim.PASS
    p = pnl([[*climb, bar(-2499, low=-2500)]])
    assert run_eval(p, INTRA)[0] == sim.FAIL


def test_access_period_is_30_calendar_days() -> None:
    p = pnl([[bar(10)] for _ in range(40)])
    out = run_eval(p)
    assert out[0] == sim.EXPIRED and out[2] == 30
    p = pnl([[bar(10)] for _ in range(40)], day_step=2)  # every other calendar day
    assert run_eval(p)[2] == 15


def test_eval_size_capped_at_max_contracts() -> None:
    # 100 micros requested, 60 allowed: +50/micro -> +3,000 exactly -> pass
    assert run_eval(pnl([[bar(50)]]), size=100)[0] == sim.PASS
    assert run_eval(pnl([[bar(49.99)]]), size=100)[0] == sim.NO_DATA


def test_largest_day_share_reported() -> None:
    out = run_eval(pnl([[bar(1000)], [bar(2000)]]))
    assert out[0] == sim.PASS and out[3] == pytest.approx(2000 / 3000)


# ---------- performance account ----------
def test_pa_tier_scaling_limits_size() -> None:
    # Level 1 = 2 contracts = 20 micros even though 40 are requested.
    out = run_pa(pnl([[bar(10)]]), size=40)
    assert out[5] == pytest.approx(50_200)
    # +100/micro on day 1 -> 52,000 (profit 2,000 >= 1,500 -> level 2 = 30 micros next day)
    out = run_pa(pnl([[bar(100)], [bar(-30)]]), size=40)
    assert out[5] == pytest.approx(52_000 - 900)


def test_pa_first_payout_amount_and_reset() -> None:
    p = pnl([[bar(600)] for _ in range(5)])
    out = run_pa(p)
    # 53,000 >= 52,600; amount = min(cap 1,500, 53,000 - 52,100) = 900
    assert out[0] == sim.NO_DATA and out[1] == 1 and out[2] == pytest.approx(900) and out[3] == 4


def test_pa_qualifying_day_needs_min_daily_profit() -> None:
    p = pnl([[bar(249.99)] for _ in range(20)])
    assert run_pa(p)[1] == 0
    p = pnl([[bar(250)] for _ in range(12)])
    assert run_pa(p)[1] == 1  # day 11: 52,750 >= 52,600 with 11 qualifying days


def test_pa_consistency_blocks_until_below_half() -> None:
    days = [2000, 250, 250, 250, 250]  # net 3,000, best 2,000 -> 67%: blocked
    p = pnl([[bar(x)] for x in days])
    assert run_pa(p)[1] == 0
    days += [250] * 5  # net 4,250 -> 47%: allowed
    assert run_pa(pnl([[bar(x)] for x in days]))[1] == 1


def test_pa_threshold_locks_at_start_plus_100() -> None:
    # EOD PA: close at 52,100 locks threshold at 50,100 even after 54,000. The DLL is removed
    # here so the threshold itself can be reached in one day.
    spec = EOD.model_copy(update={"tier_dll": [0.0] * len(EOD.tier_dll)})
    p = pnl([[bar(2100)], [bar(1900)], [bar(0, low=-3899.99)]])
    assert run_pa(p, spec)[0] == sim.NO_DATA
    p = pnl([[bar(2100)], [bar(1900)], [bar(0, low=-3900)]])
    assert run_pa(p, spec)[0] == sim.FAIL


def test_pa_dll_intervenes_before_distant_threshold() -> None:
    p = pnl([[bar(2100)], [bar(1900)], [bar(0, low=-3900)]])
    assert run_pa(p)[0] == sim.NO_DATA  # level-3 DLL ($2,000) cuts the day at 52,000


def test_pa_dll_by_tier() -> None:
    # level 1 DLL is $1,000: -1,500 intraday is cut at -1,000; the account survives
    p = pnl([[bar(0, low=-1500), bar(-800)], [bar(0)]])
    out = run_pa(p, size=1)
    assert out[0] == sim.NO_DATA


def test_pa_closes_after_six_payouts() -> None:
    p = pnl([[bar(700)] for _ in range(200)])
    out = run_pa(p)
    assert out[0] == sim.MAXED and out[1] == 6
    assert out[2] <= sum(EOD.payout_caps)


def test_run_many_end_to_end() -> None:
    p = pnl([[bar(700)] for _ in range(300)])
    res = sim.run_many(p, np.array([0, 10, 20]), 1, EOD)
    assert (res[:, 0] == sim.PASS).all() and (res[:, 3] == sim.MAXED).all()
    assert INTRA.eval_trail == TRAIL_INTRADAY
