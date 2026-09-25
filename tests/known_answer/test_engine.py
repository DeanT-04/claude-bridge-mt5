"""Hand-computed fills and P&L. Point value 2 (MNQ), tick 0.25, 1 tick slip, $0.51/side."""

import numpy as np
import pytest

from propquant.engine import core
from propquant.engine.backtest import Costs, MarketData, Orders, run

COSTS = Costs(tick=0.25, point_value=2.0, slip_ticks=1, commission_side=0.51)
SLIP = 0.25


def md_from(bars: list[tuple[float, float, float, float]], minutes=None, sess=None) -> MarketData:
    a = np.array(bars, dtype=np.float64)
    n = len(a)
    minutes = np.asarray(minutes if minutes is not None else 600 + np.arange(n), np.int64)
    sess = np.asarray(sess if sess is not None else np.zeros(n), np.int64)
    starts = np.flatnonzero(np.diff(sess, prepend=-1) != 0)
    return MarketData(
        symbol="T",
        ts=np.arange(n),
        open=a[:, 0].copy(),
        high=a[:, 1].copy(),
        low=a[:, 2].copy(),
        close=a[:, 3].copy(),
        volume=np.ones(n),
        minute=minutes,
        sess=sess,
        sess_start=np.append(starts, n).astype(np.int64),
        sess_day=np.arange(len(starts), dtype=np.int64),
    )


def buy(o: Orders, i: int, kind=core.MARKET, px=np.nan, sl=np.nan, tp=np.nan, d=1) -> Orders:
    o.order_type[i], o.order_dir[i], o.order_px[i] = kind, d, px
    o.sl_pts[i], o.tp_pts[i] = sl, tp
    return o


FLAT = [(100, 101, 99, 100)] * 3


def test_market_entry_target_exit_pnl() -> None:
    bars = [(100, 101, 99, 100), (100, 101, 99, 100.5), (100.5, 106, 100, 105), *FLAT]
    md = md_from(bars)
    r = run(md, buy(Orders.empty(md.n), 0, tp=5), COSTS)
    t = r.trades_frame().row(0, named=True)
    assert t["entry_px"] == 100 + SLIP and t["exit_px"] == pytest.approx(105.25)
    assert t["reason"] == core.EXIT_TP
    assert t["pnl"] == pytest.approx((105.25 - 100.25) * 2 - 1.02)
    assert r.d_close.sum() == pytest.approx(t["pnl"])  # bar P&L reconciles to trade P&L


def test_stop_wins_when_both_hit_in_one_bar() -> None:
    bars = [(100, 101, 99, 100), (100, 100.5, 99.5, 100), (100, 110, 90, 100), *FLAT]
    md = md_from(bars)
    t = run(md, buy(Orders.empty(md.n), 0, sl=5, tp=5), COSTS).trades_frame().row(0, named=True)
    assert t["reason"] == core.EXIT_SL
    assert t["exit_px"] == pytest.approx(100.25 - 5 - SLIP)


def test_stop_gap_through_fills_at_open() -> None:
    bars = [(100, 101, 99, 100), (100, 100.5, 99.5, 100), (90, 91, 89, 90), *FLAT]
    md = md_from(bars)
    t = run(md, buy(Orders.empty(md.n), 0, sl=5), COSTS).trades_frame().row(0, named=True)
    assert t["exit_px"] == pytest.approx(90 - SLIP)


def test_buy_stop_entry_and_gap() -> None:
    bars = [(100, 101, 99, 100), (100, 102, 99.5, 101), *FLAT]
    md = md_from(bars)
    o = buy(Orders.empty(md.n), 0, kind=core.STOP, px=101.5)
    assert run(md, o, COSTS).trades_frame()["entry_px"][0] == 101.5 + SLIP
    bars = [(100, 101, 99, 100), (103, 104, 102, 103), *FLAT]  # gaps above the stop
    md = md_from(bars)
    o = buy(Orders.empty(md.n), 0, kind=core.STOP, px=101.5)
    assert run(md, o, COSTS).trades_frame()["entry_px"][0] == 103 + SLIP


def test_limit_needs_trade_through() -> None:
    bars = [(100, 101, 99, 100), (100, 100.5, 99.0, 100), *FLAT]  # low == limit: no fill
    md = md_from(bars)
    o = buy(Orders.empty(md.n), 0, kind=core.LIMIT, px=99.0)
    assert run(md, o, COSTS).trades.shape[0] == 0
    bars[1] = (100, 100.5, 98.75, 100)
    md = md_from(bars)
    assert run(md, o, COSTS).trades_frame()["entry_px"][0] == 99.0


def test_target_not_credited_on_entry_bar() -> None:
    bars = [(100, 101, 99, 100), (100, 110, 99.9, 100), (100, 100.1, 99.9, 100), *FLAT]
    md = md_from(bars)
    t = run(md, buy(Orders.empty(md.n), 0, tp=5), COSTS).trades_frame().row(0, named=True)
    assert t["reason"] == core.EXIT_FLAT  # the +10 spike on the entry bar is not credited


def test_exit_signal_fills_next_open() -> None:
    bars = [(100, 101, 99, 100), (100, 101, 99, 100), (100, 101, 99, 101), (102, 103, 101, 102),
            *FLAT]  # fmt: skip
    md = md_from(bars)
    o = buy(Orders.empty(md.n), 0)
    o.exit_sig[2] = True
    t = run(md, o, COSTS).trades_frame().row(0, named=True)
    assert t["exit_i"] == 3 and t["exit_px"] == 102 - SLIP and t["reason"] == core.EXIT_SIGNAL


def test_forced_flat_before_cutoff_and_no_new_entries_after() -> None:
    bars = [(100, 101, 99, 100)] * 6
    md = md_from(bars, minutes=[965, 966, 967, 968, 969, 970])
    o = buy(Orders.empty(md.n), 0)
    t = run(md, o, COSTS, flat_minute=970).trades_frame().row(0, named=True)
    assert t["exit_i"] == 4 and t["reason"] == core.EXIT_FLAT
    o2 = buy(Orders.empty(md.n), 4)
    assert run(md, o2, COSTS, flat_minute=970).trades.shape[0] == 0


def test_no_carry_over_between_sessions() -> None:
    bars = [(100, 101, 99, 100)] * 6
    md = md_from(bars, minutes=[600, 601, 602, 600, 601, 602], sess=[0, 0, 0, 1, 1, 1])
    o = buy(Orders.empty(md.n), 1)
    tr = run(md, o, COSTS).trades_frame()
    assert tr["exit_i"][0] == 2  # closed at the session's last bar
    o = buy(Orders.empty(md.n), 2)  # decided on the last bar -> must not fill next session
    assert run(md, o, COSTS).trades.shape[0] == 0


def test_bar_extremes_bound_close_and_sim_invariants() -> None:
    rng = np.random.default_rng(0)
    close = 100 + np.cumsum(rng.normal(0, 0.5, 400))
    open_ = np.r_[100, close[:-1]]
    hi = np.maximum(open_, close) + rng.uniform(0, 0.5, 400)
    lo = np.minimum(open_, close) - rng.uniform(0, 0.5, 400)
    md = md_from(list(zip(open_, hi, lo, close, strict=True)))
    o = Orders.empty(md.n)
    for i in range(0, 390, 7):
        buy(o, i, sl=2, tp=3, d=1 if i % 2 else -1)
    r = run(md, o, COSTS)
    assert (r.d_low <= np.minimum(r.d_close, 0) + 1e-12).all()
    assert (r.d_high >= np.maximum(r.d_close, 0) - 1e-12).all()
    assert r.d_close.sum() == pytest.approx(r.trades[:, 5].sum())


def test_oco_bracket_takes_the_side_that_triggers() -> None:
    bars = [(100, 101, 99, 100), (100, 100.5, 97, 97.5), *FLAT]
    md = md_from(bars)
    o = Orders.empty(md.n)
    o.order_type[0], o.order_dir[0], o.order_px[0], o.order_px2[0] = core.STOP, 0, 102, 98
    t = run(md, o, COSTS).trades_frame().row(0, named=True)
    assert t["dir"] == -1 and t["entry_px"] == 98 - SLIP


def test_oco_both_touched_picks_side_nearer_open_then_checks_stop() -> None:
    # open 101.5: buy stop 102 is 0.5 away, sell stop 98 is 3.5 away -> long first,
    # then the low of 97 hits the long's 3-point stop in the same bar
    bars = [(100, 101, 99, 100), (101.5, 103, 97, 99), *FLAT]
    md = md_from(bars)
    o = Orders.empty(md.n)
    o.order_type[0], o.order_dir[0], o.order_px[0], o.order_px2[0] = core.STOP, 0, 102, 98
    o.sl_pts[0] = 3
    t = run(md, o, COSTS).trades_frame().row(0, named=True)
    assert t["dir"] == 1 and t["reason"] == core.EXIT_SL


def test_evening_positions_are_inside_the_session() -> None:
    # session opens 18:00: enter 18:01, exit on a signal at 03:00, flat time 16:10 not hit
    minutes = [1080, 1081, 1082, 1439, 0, 180, 181, 600]
    bars = [(100, 101, 99, 100)] * 3 + [(100, 105, 99, 104)] + [(104, 105, 103, 104)] * 4
    md = md_from(bars, minutes=minutes)
    o = buy(Orders.empty(md.n), 0)
    o.exit_sig[5] = True
    t = run(md, o, COSTS).trades_frame().row(0, named=True)
    assert t["entry_i"] == 1 and t["exit_i"] == 6 and t["reason"] == core.EXIT_SIGNAL
