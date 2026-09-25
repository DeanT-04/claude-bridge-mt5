"""MT5 confirmation of a finalist: Python/MT5 trade parity, then MT5 cost stress."""
from __future__ import annotations

from datetime import datetime, timezone

import numpy as np

from bridge import compiler, config, tester
from registry import db

from . import stats
from .gauntlet import costs_for
from .strategies import FAMILIES, get_family

PARITY_MIN_MATCH = 0.85      # share of trades matched by entry bar + direction
PARITY_MAX_R_MAE = 0.15      # mean abs R difference on matched trades
# Parity/stress compare trade lists; they run at the research account size (settings, 50K).
# Tester M1 history on BlackBull is short (e.g. XAUUSD from 2022-12), so confirm on recent years only.
CONFIRM_YEARS = 3


def _date(ts) -> datetime:
    return datetime.fromtimestamp(int(ts), timezone.utc)


def mt5_r(trades: list[dict]) -> np.ndarray:
    out = []
    for t in trades:
        stop = abs(t["open_price"] - t["sl"])
        if stop > 0:
            out.append(t["direction"] * (t["close_price"] - t["open_price"]) / stop)
    return np.array(out)


def parity(py_trades, mt_trades, bar_seconds: int) -> dict:
    """Match by (entry bar, direction). MT5 fills a moment after the bar opens, so floor to the bar."""
    py = {(t.entry_time // bar_seconds, t.direction): t for t in py_trades}
    matched, diffs = 0, []
    for m in mt_trades:
        key = (int(m["open_time"].replace(tzinfo=timezone.utc).timestamp()) // bar_seconds, m["direction"])
        p = py.get(key)
        if p is None:
            continue
        matched += 1
        stop = abs(m["open_price"] - m["sl"])
        if stop > 0:
            diffs.append(abs(m["direction"] * (m["close_price"] - m["open_price"]) / stop - p.r))
    denom = max(len(py_trades), len(mt_trades), 1)
    share = matched / denom
    mae = float(np.mean(diffs)) if diffs else 1.0
    return {"pass": share >= PARITY_MIN_MATCH and mae <= PARITY_MAX_R_MAE, "match_share": share,
            "r_mae": mae, "py_trades": len(py_trades), "mt5_trades": len(mt_trades)}


BAR_SECONDS = {"M15": 900, "M30": 1800, "H1": 3600, "H4": 14400}


def make(family: str, symbol: str, timeframe: str, bars: np.ndarray, spec: dict, con=None):
    fam = get_family(family)
    g = config.gauntlet()

    def confirm(params, t_from, t_to) -> dict:
        comp = compiler.compile_expert(fam.EXPERT.split("\\")[-1].removesuffix(".ex5"))
        if not comp["ok"]:
            return {"pass": False, "stage": "compile", **comp}
        t_from = max(int(t_from), int(t_to) - CONFIRM_YEARS * 365 * 86400)
        d0, d1 = _date(t_from).date(), _date(t_to).date()
        inputs = {k: tester.Param(v) for k, v in params.dict().items()}
        inputs["InpRiskPct"] = tester.Param(1.0)

        base = tester.run(tester.Job(fam.EXPERT, symbol, timeframe, d0, d1, params=dict(inputs)))
        if not base.ok:
            return {"pass": False, "stage": "mt5_backtest", "error": base.error}
        a = int(np.searchsorted(bars["time"], t_from))
        z = int(np.searchsorted(bars["time"], int(t_to) + 86400))
        py = fam.backtest(bars, params, costs_for(spec, floor=False), a, z)   # mirror the tester
        par = parity(py, base.trades, BAR_SECONDS[timeframe])

        cs = g["cost_stress"]
        med_spread = max(int(np.median(bars["spread"][a:])), int(spec.get("spread", 0)))
        stressed = tester.run(tester.Job(fam.EXPERT, symbol, timeframe, d0, d1, params=dict(inputs),
                                         spread=int(round(med_spread * cs["spread_mult"]))
                                         + int(cs["extra_slippage_points"])))
        r = mt5_r(stressed.trades) if stressed.ok else np.zeros(0)
        pf = float(r[r > 0].sum() / -r[r < 0].sum()) if (r < 0).any() else 0.0

        c = con or db.connect()
        db.log_run(c, "mt5", family, symbol, timeframe, params.dict(), base.summary,
                   base.trades, tag=base.job.tag)
        return {"pass": par["pass"] and pf >= cs["min_profit_factor"],
                "parity": par, "mt5_summary": base.summary,
                "mt5_stress": {"profit_factor_r": pf, "trades": len(r), "summary": stressed.summary},
                "seconds": round(base.seconds + stressed.seconds, 1)}

    return confirm
