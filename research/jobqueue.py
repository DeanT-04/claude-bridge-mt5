"""Research job queue: enqueue family x symbol x timeframe gauntlets, run them in parallel
Python workers, then MT5-confirm the survivors one at a time (single tester copy)."""
from __future__ import annotations

import json
import multiprocessing as mp
import traceback
from datetime import datetime, timezone

from bridge import config, mt5_client
from registry import db

from . import data, gauntlet
from .strategies import FAMILIES


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def enqueue(families: list[str], symbols: list[str], timeframes: list[str], redo: bool = False, con=None) -> int:
    """Add jobs; skips combos already queued/running, and done ones unless redo."""
    con = con or db.connect()
    unknown = set(families) - set(FAMILIES)
    if unknown:
        raise ValueError(f"unknown families {sorted(unknown)}")
    skip = ("queued", "running") if redo else ("queued", "running", "done")
    n = 0
    for f in families:
        for s in symbols:
            for tf in timeframes:
                q = "SELECT 1 FROM jobs WHERE family=? AND symbol=? AND timeframe=? AND status IN (%s)" \
                    % ",".join("?" * len(skip))
                if con.execute(q, (f, s, tf, *skip)).fetchone():
                    continue
                con.execute("INSERT INTO jobs(family, symbol, timeframe) VALUES (?,?,?)", (f, s, tf))
                n += 1
    con.commit()
    return n


def status(con=None) -> dict:
    con = con or db.connect()
    counts = {r["status"]: r["n"] for r in con.execute("SELECT status, COUNT(*) n FROM jobs GROUP BY status")}
    verdicts = {r["verdict"]: r["n"] for r in con.execute(
        "SELECT verdict, COUNT(*) n FROM jobs WHERE status='done' GROUP BY verdict")}
    return {"jobs": counts, "verdicts": verdicts}


def survivors(con=None) -> list[dict]:
    """Gauntlets that passed (or await MT5), newest first, with headline OOS metrics."""
    con = con or db.connect()
    rows = con.execute("SELECT id, family, symbol, timeframe, verdict, params, stages FROM gauntlets "
                       "WHERE verdict IN ('pass','pending_mt5') ORDER BY id DESC").fetchall()
    out = []
    for r in rows:
        st = json.loads(r["stages"])
        oos = st.get("walk_forward", {}).get("oos", {})
        out.append({"gauntlet_id": r["id"], "family": r["family"], "symbol": r["symbol"],
                    "timeframe": r["timeframe"], "verdict": r["verdict"], "params": json.loads(r["params"]),
                    "oos_sharpe": oos.get("sharpe"), "oos_pf": oos.get("profit_factor"),
                    "oos_trades": oos.get("trades"),
                    "risk": st.get("sizing_montecarlo", {}).get("risk"),
                    "small_account": st.get("small_account", {}).get("feasible")})
    return out


# ------------------------------------------------------------------ workers
def _prefetch(con) -> float:
    """Load bars/specs for every queued combo in this (MT5-connected) process."""
    rows = con.execute("SELECT DISTINCT symbol, timeframe FROM jobs WHERE status='queued'").fetchall()
    for r in rows:
        data.bars(r["symbol"], r["timeframe"])
        data.spec(r["symbol"])
    acct = mt5_client.account_info()["currency"]
    return gauntlet.acct_to_target_rate(data.spec, acct, config.settings()["account"]["currency"])


def _claim(con):
    return con.execute(
        "UPDATE jobs SET status='running', started=? WHERE id = "
        "(SELECT id FROM jobs WHERE status='queued' ORDER BY id LIMIT 1) RETURNING *", (_now(),)).fetchone()


def _worker(rate: float) -> int:
    con = db.connect()
    done = 0
    while True:
        job = _claim(con)
        con.commit()
        if job is None:
            return done
        try:
            bars = data.bars(job["symbol"], job["timeframe"])     # served from cache
            spec = data.spec(job["symbol"])
            res = gauntlet.run(job["family"], job["symbol"], job["timeframe"], bars, spec, rate,
                               con=con, progress=lambda *_: None)
            con.execute("UPDATE jobs SET status='done', gauntlet_id=?, verdict=?, finished=? WHERE id=?",
                        (res["id"], res["verdict"], _now(), job["id"]))
        except Exception:
            con.execute("UPDATE jobs SET status='error', error=?, finished=? WHERE id=?",
                        (traceback.format_exc()[-2000:], _now(), job["id"]))
        con.commit()
        done += 1


def run(processes: int = 3, mt5_confirm: bool = True, progress=print) -> dict:
    con = db.connect()
    con.execute("UPDATE jobs SET status='queued' WHERE status='running'")   # recover a crashed run
    con.commit()
    rate = _prefetch(con)
    progress(f"prefetched data; starting {processes} workers")
    with mp.get_context("spawn").Pool(processes) as pool:
        done = sum(pool.map(_worker, [rate] * processes))
    progress(f"python gauntlets done: {done} jobs")
    confirmed = confirm_pending(con, progress) if mt5_confirm else []
    return {**status(con), "mt5_confirmed": confirmed}


def confirm_pending(con=None, progress=print) -> list[dict]:
    """MT5 parity + cost stress for every pending_mt5 gauntlet; updates verdicts."""
    from . import mt5_confirm
    con = con or db.connect()
    rows = con.execute("SELECT id, family, symbol, timeframe, params, stages FROM gauntlets "
                       "WHERE verdict='pending_mt5'").fetchall()
    out = []
    for r in rows:
        fam = FAMILIES[r["family"]]
        params = fam.Params(**json.loads(r["params"]))
        bars = data.bars(r["symbol"], r["timeframe"])
        spec = data.spec(r["symbol"])
        progress(f"MT5 confirm {r['family']} {r['symbol']} {r['timeframe']}")
        res = mt5_confirm.make(r["family"], r["symbol"], r["timeframe"], bars, spec, con)(
            params, bars["time"][0], bars["time"][-1])
        stages = json.loads(r["stages"])
        stages["mt5"] = res
        verdict = "pass" if res.get("pass") else "fail"
        con.execute("UPDATE gauntlets SET verdict=?, stages=? WHERE id=?",
                    (verdict, json.dumps(stages, default=db._js), r["id"]))
        con.execute("UPDATE jobs SET verdict=? WHERE gauntlet_id=?", (verdict, r["id"]))
        con.commit()
        out.append({"gauntlet_id": r["id"], "verdict": verdict})
    return out
