import numpy as np
import pytest

from propquant.gauntlet import stats


def test_psr_known_normal_case() -> None:
    # iid normal, SR = 0.1 per period, 1000 periods: PSR(0) = Phi(0.1*sqrt(999)/sqrt(1+0.1^2/2))
    rng = np.random.default_rng(0)
    x = rng.normal(0, 1, 1000)
    x = (x - x.mean()) / x.std(ddof=1) * 1.0 + 0.1  # exact SR 0.1
    sr = stats.sharpe(x)
    assert sr == pytest.approx(0.1, abs=1e-9)
    assert 0.99 < stats.psr(x) < 1.0


def test_psr_zero_edge_is_about_half() -> None:
    rng = np.random.default_rng(1)
    vals = [stats.psr(rng.normal(0, 1, 500)) for _ in range(400)]
    assert 0.45 < np.mean(vals) < 0.55  # uniform under the null


def test_expected_max_sharpe_grows_with_trials() -> None:
    v = 0.01
    e = [stats.expected_max_sharpe(n, v) for n in (1, 10, 100, 1000)]
    assert e[0] == 0 and e[1] < e[2] < e[3]
    # matches brute force: best of 100 skill-less Sharpe estimates with variance v
    rng = np.random.default_rng(2)
    sim = rng.normal(0, np.sqrt(v), (20000, 100)).max(axis=1).mean()
    assert stats.expected_max_sharpe(100, v) == pytest.approx(sim, rel=0.05)


def test_dsr_penalises_many_trials() -> None:
    rng = np.random.default_rng(3)
    x = rng.normal(0.05, 1, 1000)
    assert stats.dsr(x, 1, 0.002) > stats.dsr(x, 1000, 0.002)


def test_block_bootstrap_centres_on_mean() -> None:
    x = np.arange(100, dtype=float)
    m = stats.block_bootstrap_means(x, 5000, 10, 0)
    assert m.mean() == pytest.approx(x.mean(), rel=0.03)
