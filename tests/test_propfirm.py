import numpy as np
import pytest

from bridge import config, deploy
from registry import db
from research import propfirm
from tests.test_deploy import PARAMS


def prof(**kw):
    base = dict(name="t", account_size=10000, profit_target_pct=8, max_daily_loss_pct=5, daily_loss_basis="max",
                max_total_dd_pct=10, max_dd_mode="static", min_trading_days=4, max_days=0,
                weekend_flat_hour=0, news_blackout_min=0)
    base.update(kw)
    return propfirm.Profile(**base)


def test_profiles_load():
    p = propfirm.profiles()
    assert {"two_step_standard", "one_step_trailing", "instant_funded"} <= set(p)
    assert p["one_step_trailing"].max_dd_mode == "trailing"


def test_sure_winner_passes_and_sure_loser_fails():
    win = [np.array([1.0, 1.0])] * 10
    lose = [np.array([-1.0, -1.0])] * 10
    assert propfirm.simulate(win, 1.0, prof(), 0.01, runs=200)["pass_prob"] == 1.0
    r = propfirm.simulate(lose, 1.0, prof(), 0.01, runs=200)
    assert r["fail_prob"] == 1.0 and r["fail_breakdown"]["total"] == 1.0


def test_min_trading_days_delays_pass():
    big = [np.array([10.0])] * 5                      # one trade reaches the target at 1% risk
    r = propfirm.simulate(big, 1.0, prof(min_trading_days=4), 0.01, runs=100)
    assert r["pass_prob"] == 1.0 and r["median_days_to_pass"] == 4


def test_daily_limit_breach_counted_separately():
    crash = [np.array([-3.0, -3.0])] * 3              # -6% intraday at 1% risk > 5% daily
    r = propfirm.simulate(crash, 1.0, prof(max_total_dd_pct=50), 0.01, runs=100)
    assert r["fail_breakdown"]["daily"] == 1.0


def test_trailing_dd_is_stricter_than_static():
    rng = np.random.default_rng(0)
    days = [rng.normal(0.1, 1.5, 3) for _ in range(300)]
    static = propfirm.simulate(days, 0.6, prof(max_total_dd_pct=6), 0.01, runs=800)["pass_prob"]
    trail = propfirm.simulate(days, 0.6, prof(max_total_dd_pct=6, max_dd_mode="trailing"), 0.01, runs=800)["pass_prob"]
    assert trail <= static


def test_best_risk_prefers_moderate_risk_for_edge():
    rng = np.random.default_rng(1)
    days = [rng.normal(0.15, 1.0, 2) for _ in range(400)]
    res = propfirm.best_risk(days, 0.8, prof(), runs=400)
    assert 0 < res["best"]["risk_pct"] <= 3.0 and res["best"]["pass_prob"] > 0.3


def test_prop_profile_tightens_limits_and_is_rendered(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "common_files", lambda: tmp_path / "Common")
    monkeypatch.setitem(config.settings()["terminals"], "prop_x", {"install_dir": "x", "portable": True,
                                                                   "account_mode": "demo"})
    con = db.connect(tmp_path / "r.sqlite")
    gid = db.log_gauntlet(con, "keltner", "SPX500", "H1", PARAMS, "pass", {"sizing_montecarlo": {"risk": 0.01}})
    with pytest.raises(PermissionError):              # not in enabled_targets yet
        deploy.propose("prop_x", add_gauntlets=[gid], prop_profile="one_step_trailing", con=con)
    monkeypatch.setitem(config.settings()["account"], "enabled_targets", ["prop_x"])
    p = deploy.propose("prop_x", add_gauntlets=[gid], prop_profile="one_step_trailing", con=con)
    cfg = p["config"]
    assert "account=demo" in cfg and "prop_initial_balance=10000" in cfg and "max_dd_mode=trailing" in cfg
    assert "max_daily_loss_pct=3.2" in cfg and "max_total_dd_pct=4.8" in cfg      # 80% of 4% / 6%
    assert "weekend_flat_hour=22" in cfg and "news_blackout_min=2" in cfg
