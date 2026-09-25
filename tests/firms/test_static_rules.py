"""Static-drawdown (CFD firm) rules at their boundaries. Illustrative FTMO-like numbers:
$100k, phase targets $10k / $5k, daily loss $5k, max loss $10k, 4 min days."""

import numpy as np

from propquant.firms import sim_static as S

START, DAILY, MAXL = 100_000.0, 5_000.0, 10_000.0


def pnl(days: list[list[tuple[float, float]]]):
    rows = [b for d in days for b in d]
    a = np.array(rows, dtype=np.float64).reshape(-1, 2)
    starts = np.cumsum([0] + [len(d) for d in days]).astype(np.int64)
    return a[:, 0].copy(), a[:, 1].copy(), starts, np.arange(len(days), dtype=np.int64)


def phase(days, target=10_000.0, min_days=4, limit=0, min_profit=0.0):
    dc, dl, ss, sd = pnl(days)
    size = np.ones(len(sd), dtype=np.int64)
    return S.sim_phase(
        dc, dl, ss, sd, 0, size, START, target, DAILY, MAXL, min_days, limit, min_profit
    )


def bar(c, lo=None):
    return (c, min(0.0, c) if lo is None else lo)


def test_target_needs_min_trading_days() -> None:
    assert phase([[bar(10_000)]])[0] == S.NO_DATA  # 1 day < 4 minimum
    days = [[bar(10_000)], [bar(1)], [bar(1)], [bar(1)]]
    assert phase(days)[0] == S.PASS


def test_daily_loss_touch_fails_one_cent_less_survives() -> None:
    assert phase([[bar(0, -5_000)]])[0] == S.FAIL
    assert phase([[bar(0, -4_999.99)]])[0] == S.NO_DATA


def test_daily_loss_resets_from_each_day_start_balance() -> None:
    # day 1 +3,000 -> day-2 floor is 103,000 - 5,000 = 98,000
    assert phase([[bar(3_000)], [bar(0, -4_999.99)]])[0] == S.NO_DATA
    assert phase([[bar(3_000)], [bar(0, -5_000)]])[0] == S.FAIL


def test_max_loss_is_static() -> None:
    # two -4,500 days: balance 91,000; a -1,000 dip on day 3 touches 90,000 -> fail
    days = [[bar(-4_500)], [bar(-4_500)], [bar(0, -1_000)]]
    assert phase(days)[0] == S.FAIL
    # profits never raise the static floor: +8,000 then -9,999.99 intraday over 2 days
    days = [[bar(4_000)], [bar(4_000)], [bar(-4_999)], [bar(-4_999)], [bar(0, -4_000)]]
    assert phase(days)[0] == S.NO_DATA  # 98,002 - 4,000 = 94,002 > both floors


def test_time_limit() -> None:
    assert phase([[bar(10)]] * 40, limit=30)[0] == S.EXPIRED


def test_two_phases_then_payouts() -> None:
    days = [[bar(2_600)]] * 200
    dc, dl, ss, sd = pnl(days)
    out = S.run_many(dc, dl, ss, sd, np.array([0]), np.ones(len(sd), dtype=np.int64), START,
                     np.array([10_000.0, 5_000.0]), np.array([4, 4], dtype=np.int64),
                     np.array([0, 0], dtype=np.int64), DAILY, MAXL, 0.8, 14, 365, 0.0,
                     0)  # fmt: skip
    assert out[0, 0] == S.PASS and out[0, 1] == 8  # 4 days each phase
    assert out[0, 2] >= 1 and out[0, 3] > 0


def test_active_days_need_minimum_profit() -> None:
    # Blueberry-style: only days with >= $500 realised count (0.5% of $100k)
    days = [[bar(10_000)], [bar(100)], [bar(100)], [bar(600)], [bar(600)]]
    assert phase(days, min_days=3, min_profit=500)[0] == S.PASS  # days 1, 4, 5 count
    assert phase(days[:4], min_days=3, min_profit=500)[0] == S.NO_DATA


def test_funded_payout_needs_active_days_per_cycle() -> None:
    days = [[bar(2_600)]] * 8 + [[bar(10)]] * 60  # passes, then tiny days only
    dc, dl, ss, sd = pnl(days)
    out = S.run_many(dc, dl, ss, sd, np.array([0]), np.ones(len(sd), dtype=np.int64), START,
                     np.array([10_000.0, 5_000.0]), np.array([4, 4], dtype=np.int64),
                     np.array([0, 0], dtype=np.int64), DAILY, MAXL, 0.8, 14, 365, 500.0,
                     3)  # fmt: skip
    assert out[0, 0] == S.PASS and out[0, 2] == 0  # no cycle ever has 3 days of >= $500
