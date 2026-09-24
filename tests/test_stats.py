import numpy as np
import pytest

from research import montecarlo, sizing, stats


def test_psr_higher_for_better_edge():
    rng = np.random.default_rng(1)
    good = rng.normal(0.3, 1, 400)
    flat = rng.normal(0.0, 1, 400)
    assert stats.probabilistic_sharpe(good) > 0.99
    assert stats.probabilistic_sharpe(flat) < 0.9


def test_dsr_hurdle_grows_with_trials():
    assert stats.expected_max_sharpe(1000, 0.01) > stats.expected_max_sharpe(10, 0.01) > 0
    r = np.random.default_rng(2).normal(0.1, 1, 300)
    assert stats.deflated_sharpe(r, 5000)["dsr"] < stats.deflated_sharpe(r, 2)["dsr"]


def test_kelly_even_money():
    # win +1 with p=0.6, lose -1: Kelly = 2p-1 = 0.2
    r = np.array([1.0] * 60 + [-1.0] * 40)
    assert sizing.kelly_fraction(r) == pytest.approx(0.2, abs=1e-3)
    assert sizing.kelly_fraction(-r) == 0.0


def test_montecarlo_ruin_increases_with_risk():
    r = np.random.default_rng(3).normal(0.1, 1.2, 300)
    lo = montecarlo.simulate_drawdowns(r, 0.01, runs=500)
    hi = montecarlo.simulate_drawdowns(r, 0.10, runs=500)
    assert hi["dd_p95"] > lo["dd_p95"] and hi["ruin_prob"] >= lo["ruin_prob"]


def test_min_lot_risk_pct():
    spec = {"tick_size": 0.01, "tick_value": 1.0, "volume_min": 0.01}
    # 5.00 price stop = 500 ticks * $1 * 0.01 lot = $5 loss on $100 -> 5%
    assert sizing.min_lot_risk_pct(spec, 5.0, 100.0) == pytest.approx(5.0)


def test_max_drawdown():
    assert stats.max_drawdown(np.array([1.1, 0.88, 1.2])) == pytest.approx(0.2)
