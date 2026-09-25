"""Forward-test monitoring of QB_Host sleeves and promotion from demo to live."""
from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timedelta, timezone

import MetaTrader5 as mt5
import numpy as np
from scipy import stats as st

from registry import db

from . import config, deploy, mt5_client

MAGIC_SPAN = 100000


def sleeve_trades(days: int = 365) -> dict[int, list[dict]]:
    """Closed QB_Host positions from the connected terminal's history, keyed by sleeve id."""
    base = config.settings()["deployment"]["magic_base"]
    now = datetime.now(timezone.utc)
    out: dict[int, list[dict]] = {}
    with mt5_client.session():
        deals = mt5.history_deals_get(now - timedelta(days=days), now + timedelta(days=1)) or ()
        by_pos: dict[int, list] = {}
        for d in deals:
            if base <= d.magic < base + MAGIC_SPAN:
                by_pos.setdefault(d.position_id, []).append(d)
        for pid, ds in by_pos.items():
            ins = [d for d in ds if d.entry == mt5.DEAL_ENTRY_IN]
            outs = [d for d in ds if d.entry in (mt5.DEAL_ENTRY_OUT, mt5.DEAL_ENTRY_OUT_BY)]
            if not ins or not outs:
                continue                          # still open
            e = ins[0]
            orders = mt5.history_orders_get(position=pid) or ()
            sl = next((o.sl for o in orders if o.sl), 0.0)
            direction = 1 if e.type == mt5.DEAL_TYPE_BUY else -1
            vol = sum(o.volume for o in outs)
            exit_px = sum(o.price * o.volume for o in outs) / vol
            stop = abs(e.price - sl)
            out.setdefault(e.magic - base, []).append({
                "position_id": pid, "symbol": e.symbol, "direction": direction, "volume": e.volume,
                "open_time": datetime.fromtimestamp(e.time, timezone.utc).isoformat(),
                "close_time": datetime.fromtimestamp(outs[-1].time, timezone.utc).isoformat(),
                "entry": e.price, "exit": exit_px, "sl": sl,
                "r": direction * (exit_px - e.price) / stop if stop > 0 else None,
                "profit": sum(d.profit + d.commission + d.swap for d in ds),
            })
    for v in out.values():
        v.sort(key=lambda t: t["close_time"])
    return out


def backtest_r(sleeve: deploy.Sleeve, years: float = 3.0) -> np.ndarray:
    """R-multiples of the sleeve's rules on recent history (the forward test's reference)."""
    from research import data
    from research.gauntlet import costs_for
    from research.strategies import FAMILIES, get_family
    fam = get_family(sleeve.family)
    bars = data.bars(sleeve.symbol, sleeve.timeframe)
    start = int(np.searchsorted(bars["time"], bars["time"][-1] - years * 365.25 * 86400))
    p = fam.Params(**{k: v for k, v in sleeve.params.items() if k in fam.Params.__dataclass_fields__})
    trades = fam.backtest(bars, p, costs_for(data.spec(sleeve.symbol)), start)
    return np.array([t.r for t in trades])


def drift(live: np.ndarray, ref: np.ndarray) -> dict:
    """Is the live R distribution worse than the backtest? One-sided Welch t + KS."""
    if len(live) < 5 or len(ref) < 5:
        return {"enough_data": False}
    t, p2 = st.ttest_ind(live, ref, equal_var=False)
    p_worse = p2 / 2 if t < 0 else 1 - p2 / 2
    ks = st.ks_2samp(live, ref)
    return {"enough_data": True, "live_mean_r": float(live.mean()), "backtest_mean_r": float(ref.mean()),
            "p_worse": float(p_worse), "ks_p": float(ks.pvalue), "drifting": bool(p_worse < 0.05)}


def first_deployed(target: str, sleeve_id: int, con) -> datetime | None:
    for r in con.execute("SELECT sleeves, applied FROM deployments WHERE target=? AND applied IS NOT NULL "
                         "ORDER BY id", (target,)):
        sl = json.loads(r["sleeves"])["portfolio"]["sleeves"]
        if any(s["id"] == sleeve_id for s in sl):
            return datetime.fromisoformat(r["applied"]).replace(tzinfo=timezone.utc)
    return None


def forward_report(target: str = "demo", con=None) -> dict:
    con = con or db.connect()
    lim = config.settings()["deployment"]
    acct = mt5_client.account_info()
    if acct["is_demo"] != (target == "demo"):
        raise RuntimeError(f"the connected terminal is on a {'demo' if acct['is_demo'] else 'live'} account; "
                           f"a {target} report needs the {target} terminal")
    port = deploy.current(target, con)
    trades = sleeve_trades()
    now = datetime.now(timezone.utc)
    rows = []
    for s in port.sleeves:
        tr = trades.get(s.id, [])
        r = np.array([t["r"] for t in tr if t["r"] is not None])
        since = first_deployed(target, s.id, con)
        days = (now - since).days if since else 0
        wins, losses = r[r > 0].sum(), -r[r < 0].sum()
        d = drift(r, backtest_r(s)) if len(r) >= 5 else {"enough_data": False}
        ready = (s.validated and len(r) >= lim["promote_min_trades"] and days >= lim["promote_min_days"]
                 and r.mean() > 0 and not d.get("drifting", True))
        rows.append({"sleeve": asdict(s), "trades": len(r), "days_live": days,
                     "sum_r": float(r.sum()) if len(r) else 0.0,
                     "mean_r": float(r.mean()) if len(r) else None,
                     "profit_factor": float(wins / losses) if losses > 0 else None,
                     "profit": float(sum(t["profit"] for t in tr)), "drift": d, "ready_for_live": bool(ready)})
    return {"target": target, "version": port.version, "enabled": port.enabled,
            "host": deploy.host_status(target), "sleeves": rows}


def promote_to_live(sleeve_ids: list[int], force: bool = False, con=None) -> dict:
    """Propose a live config containing the chosen demo sleeves. Needs live_enabled, validated
    sleeves, and (unless force) a passing forward test. Still needs apply() approval after."""
    con = con or db.connect()
    report = forward_report("demo", con)
    chosen = [row for row in report["sleeves"] if row["sleeve"]["id"] in set(sleeve_ids)]
    missing = set(sleeve_ids) - {row["sleeve"]["id"] for row in chosen}
    if missing:
        raise ValueError(f"no demo sleeves {sorted(missing)}")
    for row in chosen:
        if not row["sleeve"]["validated"]:
            raise PermissionError(f"sleeve {row['sleeve']['id']} never passed the gauntlet")
        if not row["ready_for_live"] and not force:
            raise PermissionError(f"sleeve {row['sleeve']['id']} has not passed its forward test "
                                  f"({row['trades']} trades, {row['days_live']} days, drift {row['drift']})")
    sleeves = [deploy.Sleeve(**row["sleeve"]) for row in chosen]
    return deploy.propose("live", add_sleeves=sleeves, balance_scale=1.0,
                          note=f"promote demo sleeves {sorted(sleeve_ids)}" + (" (forced)" if force else ""),
                          con=con)
