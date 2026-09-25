import numpy as np
import pytest

from bridge import config, deploy
from registry import db
from research import propfirm
from tests.test_deploy import PARAMS


def prof(**kw):
    base = dict(name="t", firm="T", program="t", phase_targets=(8,), max_daily_loss_pct=5,
                daily_loss_basis="max", max_total_dd_pct=10, max_dd_mode="static", min_trading_days=4,
                sizes=({"size": 50000, "fee": 300},))
    base.update(kw)
    return propfirm.Profile(**base)


def test_all_programs_load_with_size_ladders():
    p = propfirm.profiles()
    assert {"ftmo_2step", "ftmo_1step", "fundednext_stellar_2step", "fundednext_stellar_1step",
            "fundingpips_2step", "fundingpips_1step_flex", "the5ers_highstakes_2step",
            "the5ers_highstakes_2step_large", "the5ers_classic_2step", "the5ers_classic_2step_large",
            "fxify_2phase", "fxify_2phase_classic", "fxify_2phase_pro", "fxify_1phase"} == set(p)
    for prog in p.values():
        sizes = prog.size_options()
        assert sizes == sorted(sizes) and len(sizes) >= 2          # smallest -> largest
        assert prog.default_size() in prog.size_options(ea_only=True)
    assert p["ftmo_2step"].phase_targets == (10, 5) and p["ftmo_2step"].fee(50000) == 345
    assert p["fxify_2phase"].trailing_locks_at_initial and p["fxify_2phase"].min_trading_days == 5
    assert p["fundednext_stellar_2step"].size_options(ea_only=True) == [6000, 15000, 25000]
    assert p["fundingpips_2step"].news_blackout_min == 0 and p["fundingpips_2step"].daily_loss_ref == "baseline"
    assert p["ftmo_1step"].trailing_basis == "eod_balance" and p["ftmo_1step"].fee_currency == "EUR"


def test_baseline_daily_limit_scales_with_the_day_start():
    # +20% days and -4.5% days: after gains, a -4.5% day exceeds 5% of the INITIAL balance but
    # never 5% of the day's own starting balance
    days = [np.array([20.0]), np.array([-4.5])]
    kw = dict(phase_targets=(1000,), min_trading_days=0, max_total_dd_pct=90, max_days=40,
              daily_loss_basis="balance")
    init = propfirm.simulate(days, 1.0, prof(**kw), 0.01, runs=200)
    base = propfirm.simulate(days, 1.0, prof(daily_loss_ref="baseline", **kw), 0.01, runs=200)
    assert init["fail_breakdown"]["daily"] > 0.5 and base["fail_breakdown"]["daily"] == 0.0


def test_eod_trailing_ignores_intraday_peaks():
    # +8% then -9.5% within one day: an equity-trailing 10% floor (1.08 - 0.1) is hit,
    # an end-of-day-balance floor (still 0.9) is not
    day = [np.array([8.0, -9.5])]
    kw = dict(max_dd_mode="trailing", max_daily_loss_pct=50, min_trading_days=0, max_days=1)
    eq = propfirm.simulate(day, 1.0, prof(**kw), 0.01, runs=10)
    eod = propfirm.simulate(day, 1.0, prof(trailing_basis="eod_balance", **kw), 0.01, runs=10)
    assert eq["fail_breakdown"]["total"] == 1.0 and eod["fail_breakdown"]["total"] == 0.0


def test_sure_winner_passes_and_sure_loser_fails():
    win = [np.array([1.0, 1.0])] * 10
    lose = [np.array([-1.0, -1.0])] * 10
    assert propfirm.simulate(win, 1.0, prof(), 0.01, runs=200)["pass_prob"] == 1.0
    r = propfirm.simulate(lose, 1.0, prof(), 0.01, runs=200)
    assert r["fail_prob"] == 1.0 and r["fail_breakdown"]["total"] == 1.0


def test_two_phases_must_both_pass():
    win = [np.array([1.0, 1.0])] * 10
    r = propfirm.simulate(win, 1.0, prof(phase_targets=(8, 5)), 0.01, runs=100)
    assert r["pass_prob"] == 1.0 and r["phase_pass_prob"] == [1.0, 1.0]
    assert r["median_days_to_pass"] >= 8                            # >= 4 min days per phase


def test_min_trading_days_delays_pass():
    big = [np.array([10.0])] * 5                                    # target reached on day 1 at 1%
    r = propfirm.simulate(big, 1.0, prof(min_trading_days=4), 0.01, runs=100)
    assert r["pass_prob"] == 1.0 and r["median_days_to_pass"] == 4


def test_min_profitable_days():
    big = [np.array([10.0])] * 5
    r = propfirm.simulate(big, 1.0, prof(min_trading_days=0, min_profitable_days=3, profitable_day_pct=0.5),
                          0.01, runs=100)
    assert r["median_days_to_pass"] == 3


def test_best_day_rule_blocks_single_day_pass():
    one_big = [np.array([10.0])]                                    # +10% a day at 1% risk
    no_rule = propfirm.simulate(one_big, 1.0, prof(min_trading_days=0), 0.01, runs=50)
    assert no_rule["median_days_to_pass"] == 1
    # with a 50% best-day cap: day 1 = 100% of profits; day 2 (compounded, +11%) = 52%; day 3 fits
    rule = propfirm.simulate(one_big, 1.0, prof(min_trading_days=0, best_day_max_share=0.5), 0.01, runs=50)
    assert rule["pass_prob"] == 1.0 and rule["median_days_to_pass"] == 3


def test_daily_limit_breach_counted_separately():
    crash = [np.array([-3.0, -3.0])] * 3                            # -6% intraday at 1% > 5% daily
    r = propfirm.simulate(crash, 1.0, prof(max_total_dd_pct=50), 0.01, runs=100)
    assert r["fail_breakdown"]["daily"] == 1.0


def test_trailing_stricter_than_static_and_lock_relaxes_it():
    rng = np.random.default_rng(0)
    days = [rng.normal(0.1, 1.5, 3) for _ in range(300)]
    kw = dict(max_total_dd_pct=6)
    static = propfirm.simulate(days, 0.6, prof(**kw), 0.01, runs=800)["pass_prob"]
    trail = propfirm.simulate(days, 0.6, prof(max_dd_mode="trailing", **kw), 0.01, runs=800)["pass_prob"]
    locked = propfirm.simulate(days, 0.6, prof(max_dd_mode="trailing", trailing_locks_at_initial=True, **kw),
                               0.01, runs=800)["pass_prob"]
    assert trail <= locked <= static + 1e-9


def test_best_risk_reports_fee_and_cost_per_pass():
    rng = np.random.default_rng(1)
    days = [rng.normal(0.15, 1.0, 2) for _ in range(400)]
    res = propfirm.best_risk(days, 0.8, prof(), runs=400)
    assert 0 < res["best"]["risk_pct"] <= 3.0 and res["best"]["pass_prob"] > 0.3
    assert res["size"] == 50000 and res["fee"] == 300
    assert res["cost_per_pass"] == pytest.approx(300 / res["best"]["pass_prob"])


@pytest.fixture
def prop_env(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "common_files", lambda: tmp_path / "Common")
    monkeypatch.setitem(config.settings()["terminals"], "ftmo_x", {
        "install_dir": "x", "portable": True, "account_mode": "demo", "profile": "ftmo_1step", "size": 100000})
    con = db.connect(tmp_path / "r.sqlite")
    gid = db.log_gauntlet(con, "keltner", "SPX500", "H1", PARAMS, "pass", {"sizing_montecarlo": {"risk": 0.01}})
    return con, gid


def test_prop_target_needs_enabling_and_gets_its_program_and_size(prop_env, monkeypatch):
    con, gid = prop_env
    with pytest.raises(PermissionError):
        deploy.propose("ftmo_x", add_gauntlets=[gid], con=con)
    monkeypatch.setitem(config.settings()["account"], "enabled_targets", ["ftmo_x"])
    cfg = deploy.propose("ftmo_x", add_gauntlets=[gid], con=con)["config"]
    assert "account=demo" in cfg and "# prop profile: ftmo_1step" in cfg
    assert "prop_initial_balance=100000" in cfg and "max_dd_mode=trailing" in cfg
    assert "max_daily_loss_pct=2.4" in cfg and "max_total_dd_pct=8" in cfg     # 80% of 3% / 10%


def test_unoffered_size_is_refused(prop_env, monkeypatch):
    con, gid = prop_env
    monkeypatch.setitem(config.settings()["account"], "enabled_targets", ["ftmo_x"])
    with pytest.raises(ValueError):
        deploy.propose("ftmo_x", add_gauntlets=[gid], prop_size=75000, con=con)


def test_demo_can_rehearse_a_program(prop_env):
    con, gid = prop_env
    cfg = deploy.propose("demo", add_gauntlets=[gid], prop_profile="fundednext_stellar_2step",
                         prop_size=25000, con=con)["config"]
    assert "prop_initial_balance=25000" in cfg and "max_daily_loss_pct=4" in cfg
    with pytest.raises(ValueError, match="EAs"):                        # FundedNext: EAs only up to 25K
        deploy.propose("demo", add_gauntlets=[gid], prop_profile="fundednext_stellar_2step",
                       prop_size=50000, con=con)


def test_host_config_carries_firm_semantics(prop_env):
    con, gid = prop_env
    cfg = deploy.propose("demo", add_gauntlets=[gid], prop_profile="fxify_2phase", prop_size=50000,
                         con=con)["config"]
    assert "trailing_basis=balance" in cfg and "trailing_lock=1" in cfg and "daily_loss_ref=initial" in cfg
    cfg = deploy.propose("demo", add_gauntlets=[gid], prop_profile="fundingpips_2step", prop_size=50000,
                         con=con)["config"]
    assert "daily_loss_ref=baseline" in cfg and "news_blackout_min=0" in cfg
