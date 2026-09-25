"""Readiness checks for a prop-account target. Read-only: reports, never changes anything.
Every check should pass before a proposal for that target is approved."""
from __future__ import annotations

from datetime import datetime, timezone

from registry import db

from . import config, deploy, mt5_client

STATUS_MAX_AGE_SEC = 60


def _check(name: str, ok: bool, detail: str = "") -> dict:
    return {"check": name, "ok": bool(ok), "detail": detail}


def terminal_mql5(target: str):
    """MQL5 folder of a target terminal (portable copies keep it inside the install)."""
    t = config.settings()["terminals"][target]
    if t.get("portable"):
        return config.path(t["install_dir"]) / "MQL5"
    return config.path(config.settings()["terminal"]["data_dir"]) / "MQL5"


def host_status_age(target: str) -> float | None:
    """Seconds since QB_Host last wrote its status file (file mtime; the status's own timestamp
    is broker server time, which isn't local time)."""
    p = deploy.status_path(target)
    return (datetime.now(timezone.utc).timestamp() - p.stat().st_mtime) if p.exists() else None


def preflight(target: str, con=None) -> dict:
    con = con or db.connect()
    s = config.settings()
    checks = []
    if target not in deploy.targets() or target == "demo":
        raise ValueError(f"preflight is for prop targets; configured: {deploy.targets()}")
    profile_name = deploy.target_profile(target)
    checks.append(_check("enabled by the user", target in (s["account"].get("enabled_targets") or []),
                         "add it to account.enabled_targets yourself when ready"))
    from research.propfirm import profiles
    prof = profiles().get(profile_name)
    checks.append(_check("prop profile configured", prof is not None,
                         profile_name or "set terminals.<target>.profile"))
    if prof and "approval" in prof.ea_policy.lower():
        approved = bool(s["terminals"][target].get("ea_approved"))
        checks.append(_check(f"{prof.firm}: EA approval obtained", approved,
                             f"{prof.ea_policy}. Get it in writing, then set terminals.{target}.ea_approved: true"))

    exe, _ = config.target_terminal(target)
    checks.append(_check("terminal installed", exe.exists(), str(exe)))
    acct = None
    if exe.exists():
        try:
            acct = mt5_client.account_info(target)
        except Exception as e:                       # not running / not logged in
            checks.append(_check("terminal reachable", False, str(e)))
    if acct:
        mode = deploy.account_mode(target)
        checks.append(_check("terminal reachable", True, f"{acct['server']} {acct['currency']}"))
        checks.append(_check("account type as expected", acct["is_demo"] == (mode == "demo"),
                             f"terminal is {'demo' if acct['is_demo'] else 'live'}, settings expect {mode}"))
        checks.append(_check("account currency matches research", acct["currency"] == s["account"]["currency"],
                             f"{acct['currency']} vs {s['account']['currency']}"))
        size = float(s["account"]["deposit"])
        checks.append(_check("balance is the challenge size", abs(acct["balance"] - size) / size < 0.2,
                             f"{acct['balance']:.0f} vs {size:.0f}"))

    host_ex5 = terminal_mql5(target) / "Experts" / "QB" / "QB_Host.ex5"
    checks.append(_check("QB_Host compiled in the terminal", host_ex5.exists(), f"run install_host(target='{target}')"))
    status = deploy.host_status(target)
    age = host_status_age(target)
    checks.append(_check("QB_Host running (status < 60 s old)", age is not None and age < STATUS_MAX_AGE_SEC,
                         f"age {age:.0f}s" if age is not None else
                         f"no status file: attach QB_Host with InpConfig=portfolio_{target}.cfg"))
    if status:
        checks.append(_check("algo trading allowed in terminal", status.get("algo_trading_allowed"), ""))
        checks.append(_check("host not halted", not status.get("halted"), status.get("error", "")))

    port = deploy.current(target, con)
    checks.append(_check("prop rules in the running config", bool(port.prop_profile) or not port.sleeves,
                         port.prop_profile or "config has no prop profile"))
    checks.append(_check("every sleeve validated", all(sl.validated for sl in port.sleeves),
                         ", ".join(str(sl.id) for sl in port.sleeves if not sl.validated)))
    if acct:
        from research import data, sizing
        for sl in port.sleeves:
            atr = _recent_atr(sl.symbol, sl.timeframe, sl.params.get("InpAtrPeriod", 14))
            pct = sizing.min_lot_risk_pct(data.spec(sl.symbol), sl.params.get("InpSlAtr", 2.0) * atr, acct["equity"])
            checks.append(_check(f"sleeve {sl.id} {sl.symbol}: min lot fits its risk", pct <= sl.risk_pct + 1e-9,
                                 f"min lot risks {pct:.3f}% vs sleeve risk {sl.risk_pct:.2f}%"))
    return {"target": target, "profile": profile_name, "ready": all(c["ok"] for c in checks), "checks": checks}


def _recent_atr(symbol: str, timeframe: str, period: int) -> float:
    import numpy as np
    from research import data
    from research.engine import atr_sma
    return float(np.nanmedian(atr_sma(data.bars(symbol, timeframe)[-500:], period)))
