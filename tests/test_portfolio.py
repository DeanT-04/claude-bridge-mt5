import numpy as np
import pytest

from bridge.monitor import drift
from research.portfolio import allocate


def test_allocate_inverse_vol_respects_caps_and_budget():
    rng = np.random.default_rng(0)
    mat = np.column_stack([rng.normal(0.05, 1.0, 1000), rng.normal(0.05, 2.0, 1000)])
    res = allocate(mat, max_risks=np.array([0.05, 0.05]), budget=0.03, dd95_max=0.9)
    r = res["risks"]
    assert r.sum() == pytest.approx(0.03) and r[0] == pytest.approx(2 * r[1], rel=0.05)
    capped = allocate(mat, max_risks=np.array([0.005, 0.05]), budget=0.03, dd95_max=0.9)["risks"]
    assert capped[0] == pytest.approx(0.005)


def test_allocate_shrinks_to_drawdown_cap():
    rng = np.random.default_rng(1)
    mat = rng.normal(0.0, 1.0, (800, 3))
    res = allocate(mat, max_risks=np.full(3, 0.2), budget=0.6, dd95_max=0.2)
    assert res["dd95"] <= 0.2 and res["risks"].sum() < 0.6


def test_drift_flags_worse_live_results():
    rng = np.random.default_rng(2)
    ref = rng.normal(0.3, 1.0, 400)
    assert drift(rng.normal(-0.6, 1.0, 60), ref)["drifting"]
    assert not drift(rng.normal(0.3, 1.0, 60), ref)["drifting"]
    assert drift(np.array([1.0, -1.0]), ref) == {"enough_data": False}
