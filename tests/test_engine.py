import numpy as np
import pytest

from research.engine import Costs, atr_sma, simulate
from research.strategies import donchian

DT = [("time", "<i8"), ("open", "<f8"), ("high", "<f8"), ("low", "<f8"), ("close", "<f8"),
      ("tick_volume", "<u8"), ("spread", "<i4"), ("real_volume", "<u8")]
C0 = Costs(point=0.01)


def mk(rows, spread=0):
    b = np.zeros(len(rows), dtype=DT)
    for i, (o, h, l, c) in enumerate(rows):
        b[i] = (i * 3600, o, h, l, c, 0, spread, 0)
    return b


def sig(n, at, d, sl, tp):
    direction = np.zeros(n, np.int8); direction[at] = d
    s = np.zeros(n); s[at] = sl
    t = np.zeros(n); t[at] = tp
    return direction, s, t


def test_long_hits_tp():
    b = mk([(100, 101, 99, 100), (100, 103, 99.5, 102), (102, 107, 101, 106), (106, 106, 105, 105)])
    tr = simulate(b, *sig(4, 1, 1, 2.0, 5.0), max_bars=10, costs=C0)
    assert len(tr) == 1 and tr[0].reason == "tp" and tr[0].exit == 105 and tr[0].r == pytest.approx(2.5)


def test_sl_priority_when_both_in_bar():
    b = mk([(100, 100, 100, 100), (100, 106, 97, 100)])
    tr = simulate(b, *sig(2, 1, 1, 2.0, 5.0), max_bars=10, costs=C0)
    assert tr[0].reason == "sl" and tr[0].r == pytest.approx(-1.0)


def test_gap_through_stop_fills_at_open():
    b = mk([(100, 100, 100, 100), (100, 100.5, 99.5, 100), (96, 97, 95, 96)])
    tr = simulate(b, *sig(3, 1, 1, 2.0, 5.0), max_bars=10, costs=C0)
    assert tr[0].exit == 96 and tr[0].r == pytest.approx(-2.0)


def test_time_exit_and_reentry_same_bar():
    rows = [(100, 100.5, 99.5, 100)] * 6
    b = mk(rows)
    d = np.zeros(6, np.int8); d[1] = 1; d[3] = -1
    s = np.full(6, 5.0); t = np.full(6, 5.0)
    tr = simulate(b, d, s, t, max_bars=2, costs=C0)
    assert [x.reason for x in tr] == ["time", "time"]
    assert tr[0].exit_i == 3 and tr[1].entry_i == 3 and tr[1].direction == -1 and tr[1].exit_i == 5
    # a position still open at the end of data is not recorded
    assert len(simulate(b, d, s, t, max_bars=3, costs=C0)) == 1


def test_short_uses_ask_with_spread():
    # spread 100 points * 0.01 = 1.0 price
    b = mk([(100, 100, 100, 100), (100, 100.5, 99.5, 100), (100, 100, 96, 97)], spread=100)
    tr = simulate(b, *sig(3, 1, -1, 2.0, 3.0), max_bars=10, costs=C0)
    # short fills at bid 100; ask low in bar 2 = 97 <= tp 97 -> tp at 97
    assert tr[0].entry == 100 and tr[0].exit == 97 and tr[0].reason == "tp"


def test_spread_floor_applies_when_history_spread_is_zero():
    b = mk([(100, 100, 100, 100), (100, 100.5, 99.5, 100), (100, 110, 100, 105)], spread=0)
    raw = simulate(b, *sig(3, 1, 1, 2.0, 5.0), max_bars=10, costs=C0)
    floored = simulate(b, *sig(3, 1, 1, 2.0, 5.0), max_bars=10, costs=Costs(point=0.01, min_spread_points=50))
    assert raw[0].entry == 100 and floored[0].entry == pytest.approx(100.5)


def test_atr_is_sma_of_true_range():
    b = mk([(10, 12, 9, 11), (11, 13, 10, 12), (12, 12, 8, 9)])
    a = atr_sma(b, 2)
    assert np.isnan(a[0]) and a[1] == pytest.approx((3 + 3) / 2) and a[2] == pytest.approx((3 + 4) / 2)


def test_donchian_channel_matches_naive():
    rng = np.random.default_rng(0)
    c = 100 + np.cumsum(rng.normal(0, 1, 400))
    rows = [(c[i - 1] if i else c[0], max(c[i], c[i - 1] if i else c[0]) + 0.5,
             min(c[i], c[i - 1] if i else c[0]) - 0.5, c[i]) for i in range(400)]
    b = mk(rows)
    p = donchian.Params(InpChannel=10, InpSessionStart=0, InpSessionEnd=24)
    d, sl, _ = donchian.signals(b, p)
    atr = atr_sma(b, p.InpAtrPeriod)
    for i in range(p.InpChannel + 1, 400):
        upper = b["high"][i - p.InpChannel - 1:i - 1].max()
        lower = b["low"][i - p.InpChannel - 1:i - 1].min()
        exp = 1 if b["close"][i - 1] > upper else (-1 if b["close"][i - 1] < lower else 0)
        if not np.isfinite(atr[i - 1]):
            exp = 0
        assert d[i] == exp, i


# ---- prop execution rules ---------------------------------------------------------------
FRI = 86400 + 7 * 86400 * 2800             # a Friday 00:00 (1970-01-02 was a Friday; + whole weeks)


def test_weekend_masks_block_window_and_flatten_last_bar():
    from datetime import datetime, timezone
    from research.engine import weekend_masks
    fri = FRI
    assert datetime.fromtimestamp(fri, timezone.utc).weekday() == 4
    t = np.array([fri + h * 3600 for h in (19, 20, 21, 22, 23)] + [fri + 3 * 86400])  # ... Monday 00:00
    blocked, flat = weekend_masks(t, 22)
    assert blocked.tolist() == [False, False, False, True, True, False]
    assert flat.tolist() == [False, False, True, False, False, False]
    # market closing before the cutoff: the last Friday bar still flattens
    t2 = np.array([fri + 19 * 3600, fri + 20 * 3600, fri + 3 * 86400])
    b2, f2 = weekend_masks(t2, 22)
    assert f2.tolist() == [False, True, False] and not b2.any()


def test_flat_at_closes_position_at_bar_close():
    b = mk([(100, 100, 100, 100), (100, 101, 99.5, 100.5), (100.5, 101, 100, 100.8), (100.8, 110, 100, 109)])
    flat = np.array([False, False, True, False])
    tr = simulate(b, *sig(4, 1, 1, 2.0, 5.0), max_bars=10, costs=C0, flat_at=flat)
    assert len(tr) == 1 and tr[0].reason == "flat" and tr[0].exit == 100.8 and tr[0].exit_i == 2


def test_blocked_bar_skips_entry():
    b = mk([(100, 100, 100, 100), (100, 103, 99.5, 102), (102, 107, 101, 106)])
    blocked = np.array([False, True, False])
    assert simulate(b, *sig(3, 1, 1, 2.0, 5.0), max_bars=10, costs=C0, blocked=blocked) == []
