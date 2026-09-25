import numpy as np

from propquant.gauntlet.portfolio import session_path


def test_session_path_close_worst_best() -> None:
    # session 1: +10, then a dip of -25 from there, close -5 ; session 2: flat
    d_close = np.array([10.0, -15.0, 0.0])
    d_low = np.array([0.0, -25.0, 0.0])
    d_high = np.array([12.0, 0.0, 0.0])
    c, lo, hi = session_path(d_close, d_low, d_high, np.array([0, 2, 3]))
    assert c.tolist() == [-5.0, 0.0]
    assert lo.tolist() == [-15.0, 0.0]  # 10 + (-25)
    assert hi.tolist() == [12.0, 0.0]


def test_session_path_matches_bar_sim_bounds() -> None:
    rng = np.random.default_rng(0)
    d_close = rng.normal(0, 5, 300)
    d_low = np.minimum(d_close, 0) - rng.uniform(0, 3, 300)
    d_high = np.maximum(d_close, 0) + rng.uniform(0, 3, 300)
    starts = np.arange(0, 301, 30)
    c, lo, hi = session_path(d_close, d_low, d_high, starts)
    assert np.allclose(c, np.add.reduceat(d_close, starts[:-1]))
    assert (lo <= np.minimum(c, 0) + 1e-12).all() and (hi >= np.maximum(c, 0) - 1e-12).all()
