"""Live-readiness checks. Every check must pass before a live proposal should be approved.

Nothing here changes anything; it only reports.
"""
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


def live_preflight(con=None) -> dict:
    con = con or db.connect()
    s = config.settings()
    checks = []
    checks.append(_check("live_enabled in settings", s["account"].get("live_enabled"),
                         "set account.live_enabled: true yourself when ready"))

    exe, _ = config.target_terminal("live")
    checks.append(_check("live terminal installed", exe.exists(), str(exe)))
    acct = None
    if exe.exists():
        try:
            acct = mt5_client.account_info("live")
        except Exception as e:                       # not running / not logged in
            checks.append(_check("live terminal reachable", False, str(e)))
    if acct:
        checks.append(_check("live terminal reachable", True, f"{acct['server']} {acct['currency']}"))
        checks.append(_check("account is a REAL account", not acct["is_demo"],
                             "the 'live' terminal is logged into a demo account" if acct["is_demo"] else ""))
        checks.append(_check("account currency matches target", acct["currency"] == s["account"]["currency"],
                             f"{acct['currency']} vs target {s['account']['currency']}"))
        checks.append(_check("leverage matches research assumption", acct["leverage"] == s["account"]["leverage"],
                             f"1:{acct['leverage']} vs 1:{s['account']['leverage']}"))

    host_ex5 = terminal_mql5("live") / "Experts" / "QB" / "QB_Host.ex5"
    checks.append(_check("QB_Host compiled in live terminal", host_ex5.exists(), "run install_host(target='live')"))

    status = deploy.host_status("live")
    age = host_status_age("live")
    checks.append(_check("QB_Host running on live (status < 60 s old)", age is not None and age < STATUS_MAX_AGE_SEC,
                         f"age {age:.0f}s" if age is not None else "no status file: attach QB_Host with "
                                                                    "InpConfig=portfolio_live.cfg"))
    if status:
        checks.append(_check("host sees a live account", status.get("account_mode") == "live",
                             status.get("account_mode", "")))
        checks.append(_check("algo trading allowed in terminal", status.get("algo_trading_allowed"), ""))
        checks.append(_check("host not halted", not status.get("halted"), status.get("error", "")))

    port = deploy.current("live", con)
    lim = config.settings()["deployment"]
    checks.append(_check("risk limits sane", 0 < port.max_daily_loss_pct <= 10 and 0 < port.max_total_dd_pct <= 50
                         and 0 < port.max_open_risk_pct <= 15,
                         f"daily {port.max_daily_loss_pct}% total {port.max_total_dd_pct}% open {port.max_open_risk_pct}%"))
    checks.append(_check("every live sleeve validated", all(sl.validated for sl in port.sleeves),
                         ", ".join(str(sl.id) for sl in port.sleeves if not sl.validated)))

    # Minimum-lot feasibility at the real live balance
    if acct:
        from research import data, sizing
        for sl in port.sleeves:
            spec = data.spec(sl.symbol)
            atr = _recent_atr(sl.symbol, sl.timeframe, sl.params.get("InpAtrPeriod", 14))
            stop = sl.params.get("InpSlAtr", 2.0) * atr
            pct = sizing.min_lot_risk_pct(spec, stop, acct["equity"])
            checks.append(_check(f"sleeve {sl.id} {sl.symbol} min lot fits its risk",
                                 pct <= sl.risk_pct + 1e-9,
                                 f"min lot risks {pct:.2f}% vs sleeve risk {sl.risk_pct:.2f}% "
                                 f"(trades would be skipped)" if pct > sl.risk_pct else f"{pct:.2f}%"))

    ok = all(c["ok"] for c in checks)
    return {"ready": ok, "checks": checks, "sleeves": len(port.sleeves), "live_version": port.version}


def _recent_atr(symbol: str, timeframe: str, period: int) -> float:
    from research import data
    from research.engine import atr_sma
    import numpy as np
    b = data.bars(symbol, timeframe)
    a = atr_sma(b[-500:], period)
    return float(np.nanmedian(a))
