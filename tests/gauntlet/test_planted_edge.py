"""The gauntlet must find a real edge and reject a fake one (same code path as production).

A synthetic market gets a known drift between 10:00 and 11:00 ET. A strategy that buys that
hour must pass the statistical gates; the identical strategy on a market WITHOUT the drift
must fail them.
"""

from datetime import date, timedelta

import numpy as np
import pytest

from propquant.engine import core
from propquant.engine.backtest import MarketData, Orders
from propquant.gauntlet import config
from propquant.gauntlet import run as grun
from propquant.strategies.base import Strategy
from propquant.trials import Registry

RTH = np.arange(9 * 60 + 30, 16 * 60, dtype=np.int64)  # 390 one-minute bars


class PlantedHour(Strategy):
    name = "test_planted_hour"
    family = "test"
    needs_idea_note = False
    defaults = {"entry_minute": 599, "hold": 60}
    param_space = {"entry_minute": [599, 629], "hold": [30, 60]}

    def orders(self, md: MarketData) -> Orders:
        o = Orders.empty(md.n)
        go = md.minute == self.params["entry_minute"]  # decided at this bar's close
        o.order_type[go] = core.MARKET
        o.order_dir[go] = 1
        out = md.minute == self.params["entry_minute"] + self.params["hold"]
        o.exit_sig[out] = True
        return o


def synthetic(drift_pts: float, seed: int) -> MarketData:
    rng = np.random.default_rng(seed)
    days = [date(2016, 1, 4) + timedelta(days=k) for k in range(0, 3920)]
    days = [d for d in days if d.weekday() < 5 and d <= date(2026, 9, 25)]
    n_s, m = len(days), len(RTH)
    steps = rng.normal(0, 1.0, (n_s, m))
    hour = (RTH >= 600) & (RTH < 660)
    steps[:, hour] += drift_pts / hour.sum()
    close = 15000 + np.cumsum(steps.ravel())
    open_ = np.r_[15000, close[:-1]]
    wick = np.abs(rng.normal(0, 0.5, close.size))
    sess = np.repeat(np.arange(n_s), m).astype(np.int64)
    return MarketData(
        symbol="NQ", ts=np.arange(close.size), open=open_,
        high=np.maximum(open_, close) + wick, low=np.minimum(open_, close) - wick, close=close,
        volume=np.ones(close.size), minute=np.tile(RTH, n_s), sess=sess,
        sess_start=np.append(np.arange(n_s) * m, n_s * m).astype(np.int64),
        sess_day=np.array([config.day_number(d) for d in days], dtype=np.int64),
        data_hash=f"synthetic-{drift_pts}-{seed}",
    )  # fmt: skip


@pytest.fixture
def reg(tmp_path):
    r = Registry(tmp_path / "trials.duckdb")
    yield r
    r.close()


def _stat_gates(res) -> dict[str, bool]:
    return {c.name: c.passed for c in res.checks if c.kind == "stat"}


@pytest.mark.slow
def test_planted_edge_is_detected(reg) -> None:
    res = grun.run("test_planted_hour", md_full=synthetic(4.0, 1), registry=reg,
                   progress=lambda *_: None)  # fmt: skip
    g = _stat_gates(res)
    assert g["Deflated Sharpe"] and g["Beats random entry (percentile)"], res.checks
    assert res.final_params["entry_minute"] == 599  # the hour with the drift
    assert res.oos_challenge[res.best_plan]["eval_pass"] > 0.5


@pytest.mark.slow
def test_no_edge_is_rejected(reg) -> None:
    res = grun.run("test_planted_hour", md_full=synthetic(0.0, 2), registry=reg,
                   progress=lambda *_: None)  # fmt: skip
    g = _stat_gates(res)
    assert not g["Deflated Sharpe"]
    assert res.verdict == "graveyard"


def test_holdout_is_opened_once_per_config(reg) -> None:
    md = synthetic(4.0, 3)
    a = grun.run("test_planted_hour", md_full=md, registry=reg, progress=lambda *_: None)
    b = grun.run("test_planted_hour", md_full=md, registry=reg, progress=lambda *_: None)
    assert a.holdout is not None and b.holdout is None
    assert "already used" in b.holdout_note
    assert not dict((c.name, c.passed) for c in b.checks)["Holdout consistent"]


def test_run_identity_is_the_strategy_name(reg) -> None:
    res = grun.run("test_planted_hour", md_full=synthetic(4.0, 4), registry=reg,
                   progress=lambda *_: None)  # fmt: skip
    assert res.strategy == "test_planted_hour"
    who = {r[0] for r in reg.con.execute("SELECT strategy FROM holdout_access").fetchall()}
    runs = {r[0] for r in reg.con.execute("SELECT strategy FROM runs").fetchall()}
    assert who == runs == {"test_planted_hour"}
