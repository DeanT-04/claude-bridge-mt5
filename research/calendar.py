"""High-impact economic calendar history, for backtesting prop-firm news blackouts.

The Python MetaTrader5 API has no calendar and the Strategy Tester can't read it, so the
QB_ExportCalendar script dumps it once from the (connected) tester copy to
Common\\Files\\QB\\calendar_high.csv. Times are trade-server time, like bar times, and QB_Host
blocks entries within +/- N minutes of any high-impact event for the symbol's base or profit
currency; news_mask() reproduces that per bar.
"""
from __future__ import annotations

import subprocess
from functools import lru_cache

import numpy as np

from bridge import compiler, config

# Index CFDs carry no currency in their name; map them to the economy whose news moves them.
INDEX_CCY = {"NAS": "USD", "SPX": "USD", "US30": "USD", "US500": "USD", "US2000": "USD", "USTEC": "USD",
             "DJ": "USD", "GER": "EUR", "DE40": "EUR", "FRA": "EUR", "EU50": "EUR", "ESP": "EUR",
             "UK100": "GBP", "JPN": "JPY", "JP225": "JPY", "AUS": "AUD", "HK": "HKD", "CHINA": "CNY"}
CURRENCIES = {"USD", "EUR", "GBP", "JPY", "AUD", "NZD", "CAD", "CHF", "CNY", "HKD", "SGD", "SEK",
              "NOK", "MXN", "ZAR", "TRY", "PLN"}


def path():
    return config.common_files() / "QB" / "calendar_high.csv"


def export(timeout: int = 300) -> dict:
    """Run QB_ExportCalendar on the tester copy (it logs in with its saved demo account, writes the
    CSV and shuts down). The tester copy must not be running a test at the time."""
    comp = compiler.compile_expert("QB_ExportCalendar", kind="Scripts")
    if not comp["ok"]:
        return {"ok": False, "error": "compile failed", "compile": comp}
    ini = config.reports_dir() / "export_calendar.ini"      # the script's InpFrom default covers history_start
    ini.write_text("\r\n".join(["[StartUp]", "Script=QB\\QB_ExportCalendar", "Symbol=EURUSD", "Period=H1",
                                "ShutdownTerminal=1", ""]), encoding="utf-16")
    before = path().stat().st_mtime if path().exists() else 0
    tdir = config.tester_dir()
    try:
        subprocess.run([str(tdir / "terminal64.exe"), "/portable", f"/config:{ini}"], timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"timeout after {timeout}s"}
    if not path().exists() or path().stat().st_mtime <= before:
        return {"ok": False, "error": "no calendar written (not connected? see the tester copy's logs)"}
    load.cache_clear()
    ev = load()
    return {"ok": True, "events": len(ev["time"]), "file": str(path()),
            "from": int(ev["time"].min()), "to": int(ev["time"].max())}


@lru_cache
def load() -> dict[str, np.ndarray]:
    """{'time': int64 server times, 'currency': str array}; empty if never exported."""
    if not path().exists():
        return {"time": np.zeros(0, dtype=np.int64), "currency": np.zeros(0, dtype="<U3")}
    rows = [ln.split(",")[:2] for ln in path().read_text(encoding="latin-1").splitlines()[1:] if ln]
    t = np.array([int(r[0]) for r in rows], dtype=np.int64)
    c = np.array([r[1] for r in rows], dtype="<U3")
    o = np.argsort(t, kind="stable")
    return {"time": t[o], "currency": c[o]}


def available(times: np.ndarray | None = None) -> bool:
    """True when a calendar exists (and, given bar times, covers their span)."""
    ev = load()["time"]
    if not len(ev):
        return False
    return times is None or (ev[0] <= times[0] + 30 * 86400 and ev[-1] >= times[-1] - 7 * 86400)


def currencies(symbol: str, spec: dict | None = None) -> set[str]:
    """Currencies whose high-impact news QB_Host checks for a symbol (its base and profit
    currency), with a name-based fallback for index CFDs and older cached specs."""
    spec = spec or {}
    out = {c for c in (spec.get("currency_base"), spec.get("currency_profit")) if c in CURRENCIES}
    s = symbol.upper()
    for k, v in INDEX_CCY.items():
        if s.startswith(k):
            out.add(v)
    if len(s) >= 6:
        out |= {x for x in (s[:3], s[3:6]) if x in CURRENCIES}
    return out


def news_mask(times: np.ndarray, symbol: str, minutes: int, spec: dict | None = None) -> np.ndarray:
    """blocked[i] = a high-impact event for the symbol's currencies lies within +/- `minutes` of
    bar i's open (QB_Host decides entries at the bar open)."""
    ev = load()
    ccys = currencies(symbol, spec)
    et = ev["time"][np.isin(ev["currency"], list(ccys))] if ccys else np.zeros(0, dtype=np.int64)
    t = times.astype(np.int64)
    if not len(et) or minutes <= 0:
        return np.zeros(len(t), dtype=bool)
    w = minutes * 60
    lo = np.searchsorted(et, t - w, side="left")
    hi = np.searchsorted(et, t + w, side="right")
    return hi > lo
