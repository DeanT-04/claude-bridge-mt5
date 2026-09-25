"""Changing the future must never change the past.

Engine: mutate every price after bar t -> per-bar P&L up to t and trades closed by t are identical.
Strategies: every registered strategy's orders up to t are identical when bars after t change.
"""

import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from propquant.engine import core
from propquant.engine.backtest import Costs, MarketData, Orders, run
from propquant.strategies.base import REGISTRY, get

COSTS = Costs(tick=0.25, point_value=2.0)
SESSION_MINUTES = np.r_[np.arange(18 * 60, 24 * 60), np.arange(0, 16 * 60 + 15)]


def synthetic_md(seed: int, sessions: int = 3) -> MarketData:
    rng = np.random.default_rng(seed)
    minute = np.tile(SESSION_MINUTES, sessions).astype(np.int64)
    sess = np.repeat(np.arange(sessions), len(SESSION_MINUTES)).astype(np.int64)
    n = len(minute)
    close = 18000 + np.cumsum(rng.normal(0, 3, n))
    open_ = np.r_[18000, close[:-1]]
    hi = np.maximum(open_, close) + rng.uniform(0, 3, n)
    lo = np.minimum(open_, close) - rng.uniform(0, 3, n)
    starts = np.flatnonzero(np.diff(sess, prepend=-1) != 0)
    return MarketData("T", np.arange(n), open_, hi, lo, close, rng.uniform(1, 9, n), minute,
                      sess, np.append(starts, n), np.arange(sessions))  # fmt: skip


def mutate_after(md: MarketData, t: int, seed: int) -> MarketData:
    rng = np.random.default_rng(seed + 1000)
    m = MarketData(**{k: (v.copy() if isinstance(v, np.ndarray) else v)
                      for k, v in md.__dict__.items()})  # fmt: skip
    k = md.n - t - 1
    shock = rng.normal(0, 25, k)
    m.open[t + 1 :] += shock
    m.close[t + 1 :] += shock + rng.normal(0, 5, k)
    m.high[t + 1 :] = np.maximum(m.open[t + 1 :], m.close[t + 1 :]) + rng.uniform(0, 9, k)
    m.low[t + 1 :] = np.minimum(m.open[t + 1 :], m.close[t + 1 :]) - rng.uniform(0, 9, k)
    m.volume[t + 1 :] = rng.uniform(1, 9, k)
    return m


def random_orders(md: MarketData, seed: int) -> Orders:
    rng = np.random.default_rng(seed)
    o = Orders.empty(md.n)
    fire = rng.random(md.n) < 0.02
    kinds = rng.integers(1, 4, md.n)
    o.order_type[fire] = kinds[fire]
    o.order_dir[fire] = np.where(rng.random(md.n) < 0.5, 1, -1)[fire]
    off = rng.uniform(-6, 6, md.n)
    o.order_px[fire] = (md.close + off)[fire]
    oco = fire & (rng.random(md.n) < 0.3) & (o.order_type == core.STOP)
    o.order_dir[oco] = 0
    o.order_px[oco] = (md.close + 4)[oco]
    o.order_px2[oco] = (md.close - 4)[oco]
    o.sl_pts[fire] = rng.uniform(2, 30, md.n)[fire]
    o.tp_pts[fire] = rng.uniform(2, 30, md.n)[fire]
    o.exit_sig[:] = rng.random(md.n) < 0.01
    return o


@settings(max_examples=40, deadline=None)
@given(seed=st.integers(0, 10_000), frac=st.floats(0.05, 0.95))
def test_engine_has_no_lookahead(seed: int, frac: float) -> None:
    md = synthetic_md(seed)
    t = int(frac * (md.n - 2))
    orders = random_orders(md, seed)
    a = run(md, orders, COSTS)
    b = run(mutate_after(md, t, seed), orders, COSTS)
    np.testing.assert_array_equal(a.d_close[: t + 1], b.d_close[: t + 1])
    np.testing.assert_array_equal(a.d_low[: t + 1], b.d_low[: t + 1])
    np.testing.assert_array_equal(a.d_high[: t + 1], b.d_high[: t + 1])
    done_a = a.trades[a.trades[:, 1] <= t]
    done_b = b.trades[b.trades[:, 1] <= t]
    np.testing.assert_array_equal(done_a, done_b)


def test_order_kinds_are_exercised() -> None:
    reasons: set[int] = set()
    for seed in range(6):
        md = synthetic_md(seed)
        reasons |= set(run(md, random_orders(md, seed), COSTS).trades[:, 6].astype(int))
    assert {core.EXIT_SL, core.EXIT_TP, core.EXIT_SIGNAL, core.EXIT_FLAT} <= reasons


get("control_random")  # populate the registry (imports every family)


@pytest.mark.parametrize("name", sorted(REGISTRY))
@pytest.mark.parametrize("seed", [3, 17])
def test_strategy_orders_are_causal(name: str, seed: int) -> None:
    md = synthetic_md(seed, sessions=25)
    strat = REGISTRY[name]()
    a = strat.orders(md)
    assert (a.order_type != 0).any(), f"{name} placed no orders: causality test would be vacuous"
    for frac in (0.2, 0.5, 0.8):
        t = int(frac * md.n)
        b = strat.orders(mutate_after(md, t, seed))
        for f in (
            "order_type",
            "order_dir",
            "order_px",
            "order_px2",
            "sl_pts",
            "tp_pts",
            "exit_sig",
        ):
            np.testing.assert_array_equal(getattr(a, f)[: t + 1], getattr(b, f)[: t + 1], f)
