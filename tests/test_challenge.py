import numpy as np
import pytest

from registry import db
from research import challenge, gauntlet, propfirm
from research.engine import Trade

DAY = 86400
T0 = 1_600_000_000 // DAY * DAY


def trades(seed, mu, n_days=700, corr_with=None):
    """Two trades on most weekdays; R ~ N(mu, 1)."""
    rng = np.random.default_rng(seed)
    out = []
    for d in range(n_days):
        if d % 7 >= 5 or rng.random() < 0.3:
            continue
        for k in range(2):
            r = rng.normal(mu, 1.0) if corr_with is None else corr_with[len(out)].r
            x = T0 + d * DAY + 3600 * (10 + k)
            out.append(Trade(0, 0, x - 1800, x, 1, 0.0, r, 1.0, "tp"))
    return out


@pytest.fixture
def con(tmp_path, monkeypatch):
    c = db.connect(tmp_path / "r.sqlite")
    monkeypatch.setattr(db, "connect", lambda *_: c)
    return c


def add(con, name, tr, verdict="pass", prop=None):
    gid = db.log_gauntlet(con, name, "EURUSD", "H1", {}, verdict, {"prop": prop or {}})
    for v in ("base", "wf22_nb5", "wf0_nb2"):
        db.save_oos_trades(con, gid, v, (T0, T0 + 700 * DAY), tr)
    return gid


def test_oos_trades_roundtrip(con):
    tr = trades(1, 0.1, 30)
    gid = add(con, "a", tr)
    o = db.oos_trades(con, gid)
    assert o["span"] == (T0, T0 + 700 * DAY) and len(o["trades"]) == len(tr)
    assert o["trades"][0][2] == pytest.approx(tr[0].r, abs=1e-5)
    assert db.oos_trades(con, gid, "nope") is None


def test_variant_names():
    p = propfirm.profiles()
    assert propfirm.variant(p["ftmo_2step"]) == "base"
    assert propfirm.variant(p["fundingpips_2step"]) == "wf22_nb5"


def test_lift_separates_edge_from_luck():
    rng = np.random.default_rng(3)
    edge = [rng.normal(0.15, 1.0, 2) for _ in range(400)]
    prof = propfirm.profiles()["ftmo_2step"]
    e = propfirm.evaluate(edge, 0.7, prof, runs=500)
    assert e["lift"] > 0.3 and e["baseline_pass_prob"] < 0.45
    luck = propfirm.evaluate(propfirm.demeaned(edge), 0.7, prof, runs=500)
    assert abs(luck["lift"]) < 0.08


def test_prop_gate_needs_probability_and_lift():
    cfg = {"programs": ["ftmo_2step"], "runs": 400, "min_pass_prob": 0.6, "min_lift": 0.2}
    good = gauntlet.prop_gate({"base": trades(2, 0.2)}, 700, cfg)
    bad = gauntlet.prop_gate({"base": trades(2, -0.05)}, 700, cfg)
    assert good["pass"] and good["programs"][0]["lift"] >= 0.2
    assert not bad["pass"]


def test_combiner_skips_correlated_and_improves_pass_prob(con):
    a = trades(4, 0.06)
    ids = [add(con, "a", a), add(con, "b", trades(5, 0.06)), add(con, "a_clone", trades(4, 0.06))]
    res = challenge.combine(["ftmo_2step"], ids, search_runs=300, final_runs=600, progress=lambda *_: None)
    names = {m["name"].split()[0] for m in res[0]["members"]}
    assert "a_clone" not in names or "a" not in names          # a perfect clone is never paired
    single = challenge.evaluate(challenge.load_sleeves(con, [ids[0]]), "ftmo_2step", 600)
    assert res[0]["best"]["pass_prob"] >= single["best"]["pass_prob"] - 0.03
    lb = challenge.leaderboard("ftmo_2step", 50000, con=con)
    assert lb and lb[0]["kind"] == "portfolio" and lb[0]["fee"] == 345


def test_risk_grid_respects_open_risk_cap():
    g = challenge.risk_grid([1.0, 1.0, 1.0])                  # max_open_risk_pct 3 over three sleeves
    assert max(g) <= 1.0 and 1.0 in g


def test_leaderboard_expands_sizes(con):
    prop = {"programs": [{"profile": "ftmo_2step", "pass_prob": 0.7, "lift": 0.4, "risk_pct": 1.0,
                          "median_days": 40}]}
    add(con, "a", trades(6, 0.1, 20), prop=prop)
    add(con, "b", trades(6, 0.1, 20), verdict="fail", prop=prop)
    rows = challenge.leaderboard(con=con, portfolios=False)
    assert [r["size"] for r in rows] == [10000, 25000, 50000, 100000, 200000]
    assert rows[2]["cost_per_pass"] == pytest.approx(345 / 0.7)
