import pytest

from bridge import config, deploy
from registry import db

PARAMS = {"InpAtrPeriod": 14, "InpSlAtr": 2.0, "InpTpAtr": 3.0, "InpMaxBars": 24, "InpSessionStart": 0,
          "InpSessionEnd": 24, "InpKcPeriod": 20, "InpKcMult": 1.5, "InpFamily": 5}


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "common_files", lambda: tmp_path / "Common")
    con = db.connect(tmp_path / "r.sqlite")
    stages_pass = {"sizing_montecarlo": {"risk": 0.012}}
    g_pass = db.log_gauntlet(con, "keltner", "SPX500", "H1", PARAMS, "pass", stages_pass)
    g_fail = db.log_gauntlet(con, "keltner", "DOTUSD", "H1", PARAMS, "fail", {"walk_forward": {"pass": False}})
    return con, g_pass, g_fail


def test_propose_apply_writes_exact_config(env):
    con, g_pass, _ = env
    p = deploy.propose("demo", add_gauntlets=[g_pass], balance_scale=0.132, con=con)
    assert p["version"] == 1 and p["sleeves"][0]["risk_pct"] == pytest.approx(1.2)
    assert "sleeve=id:1;family:5;symbol:SPX500;tf:H1;risk:1.2" in p["config"]
    assert "account=demo" in p["config"] and "balance_scale=0.132" in p["config"]
    deploy.apply(p["proposal_id"], p["sha256"], con=con)
    assert deploy.config_path("demo").read_text() == p["config"]
    assert deploy.current("demo", con).version == 1


def test_apply_rejects_wrong_sha_and_stale_base(env):
    con, g_pass, _ = env
    p1 = deploy.propose("demo", add_gauntlets=[g_pass], con=con)
    with pytest.raises(ValueError):
        deploy.apply(p1["proposal_id"], "0" * 64, con=con)
    p2 = deploy.propose("demo", add_gauntlets=[g_pass], con=con)
    deploy.apply(p2["proposal_id"], p2["sha256"], con=con)
    with pytest.raises(ValueError):          # p1 was rejected when p2 applied
        deploy.apply(p1["proposal_id"], p1["sha256"], con=con)


def test_unvalidated_needs_flag_and_never_live(env, monkeypatch):
    con, _, g_fail = env
    with pytest.raises(ValueError):
        deploy.propose("demo", add_gauntlets=[g_fail], con=con)
    p = deploy.propose("demo", add_gauntlets=[g_fail], allow_unvalidated=True, con=con)
    assert p["unvalidated"] == [1] and p["sleeves"][0]["risk_pct"] == 0.5
    with pytest.raises(PermissionError):     # live disabled in settings
        deploy.propose("live", add_gauntlets=[g_fail], allow_unvalidated=True, con=con)
    monkeypatch.setitem(config.settings()["account"], "live_enabled", True)
    with pytest.raises(PermissionError):     # still refused: unvalidated on live
        deploy.propose("live", add_gauntlets=[g_fail], allow_unvalidated=True, con=con)


def test_readding_same_strategy_keeps_sleeve_id_and_remove_works(env):
    con, g_pass, _ = env
    p = deploy.propose("demo", add_gauntlets=[g_pass], con=con)
    deploy.apply(p["proposal_id"], p["sha256"], con=con)
    p2 = deploy.propose("demo", add_gauntlets=[g_pass], con=con)
    assert [s["id"] for s in p2["sleeves"]] == [1]
    p3 = deploy.propose("demo", remove_sleeves=[1], con=con)
    assert p3["sleeves"] == [] and "-sleeve=id:1" in p3["diff"]


def test_kill_disables_without_approval(env):
    con, g_pass, _ = env
    p = deploy.propose("demo", add_gauntlets=[g_pass], con=con)
    deploy.apply(p["proposal_id"], p["sha256"], con=con)
    k = deploy.kill("demo", "test", con=con)
    text = deploy.config_path("demo").read_text()
    assert "enabled=0" in text and f"version={k['version']}" in text and "sleeve=id:1" in text
    assert deploy.current("demo", con).enabled is False
