"""SQLite registry: the source of truth for trials, runs and gauntlet verdicts."""
from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path

import numpy as np

from bridge import config

SCHEMA = Path(__file__).with_name("schema.sql")


def connect(path: Path | None = None) -> sqlite3.Connection:
    p = path or config.path(config.settings()["paths"]["registry_db"])
    p.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(p, timeout=60)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")      # several research workers write concurrently
    _migrate(con)
    con.executescript(SCHEMA.read_text())
    return con


def _migrate(con) -> None:
    """The universe table is a rebuildable cache; drop the pre-prop layout (small_account column)."""
    cols = [r[1] for r in con.execute("PRAGMA table_info(universe)")]
    if "small_account" in cols:
        con.execute("DROP TABLE universe")


def candidate_hash(family: str, symbol: str, timeframe: str, params: dict) -> str:
    blob = json.dumps([family, symbol, timeframe, params], sort_keys=True)
    return hashlib.sha1(blob.encode()).hexdigest()[:16]


def log_trials(con, family, symbol, timeframe, rows: list[tuple[dict, float, int]]) -> None:
    con.executemany(
        "INSERT INTO trials(family, symbol, timeframe, params, sr_trade, trades) VALUES (?,?,?,?,?,?)",
        [(family, symbol, timeframe, json.dumps(p, sort_keys=True), sr, n) for p, sr, n in rows])
    con.commit()


def trial_stats(con, family, symbol, timeframe) -> tuple[int, np.ndarray]:
    """(number of distinct configurations tried, their per-trade Sharpes)."""
    rows = con.execute(
        "SELECT params, AVG(sr_trade) AS sr FROM trials WHERE family=? AND symbol=? AND timeframe=? "
        "GROUP BY params", (family, symbol, timeframe)).fetchall()
    return len(rows), np.array([r["sr"] for r in rows if r["sr"] is not None], dtype=float)


def log_run(con, engine, family, symbol, timeframe, params, metrics, trades, tag=None) -> int:
    cur = con.execute(
        "INSERT INTO runs(engine, tag, family, symbol, timeframe, params, metrics, trades) "
        "VALUES (?,?,?,?,?,?,?,?)",
        (engine, tag, family, symbol, timeframe, json.dumps(params), json.dumps(metrics, default=str),
         json.dumps(trades, default=str)))
    con.commit()
    return cur.lastrowid


def log_gauntlet(con, family, symbol, timeframe, params, verdict, stages) -> int:
    cand = candidate_hash(family, symbol, timeframe, params)
    cur = con.execute(
        "INSERT INTO gauntlets(candidate, family, symbol, timeframe, params, verdict, stages) "
        "VALUES (?,?,?,?,?,?,?)",
        (cand, family, symbol, timeframe, json.dumps(params), verdict, json.dumps(stages, default=_js)))
    con.commit()
    return cur.lastrowid


def holdout_used(con, candidate: str) -> dict | None:
    r = con.execute("SELECT result, used FROM holdout_uses WHERE candidate=?", (candidate,)).fetchone()
    return None if r is None else {"result": json.loads(r["result"]), "used": r["used"]}


def mark_holdout(con, candidate: str, result: dict) -> None:
    con.execute("INSERT INTO holdout_uses(candidate, result) VALUES (?,?)",
                (candidate, json.dumps(result, default=_js)))
    con.commit()


def recent_gauntlets(con, limit: int = 20) -> list[dict]:
    rows = con.execute("SELECT id, candidate, family, symbol, timeframe, params, verdict, created "
                       "FROM gauntlets ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return [dict(r) for r in rows]


def gauntlet(con, gid: int) -> dict | None:
    r = con.execute("SELECT * FROM gauntlets WHERE id=?", (gid,)).fetchone()
    if r is None:
        return None
    d = dict(r)
    d["stages"] = json.loads(d["stages"])
    d["params"] = json.loads(d["params"])
    return d


def _js(o):
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.bool_):
        return bool(o)
    return str(o)


def save_genome(con, family: str, genome: dict, description: str, symbol: str, timeframe: str,
                fitness: float) -> None:
    con.execute("INSERT OR IGNORE INTO genomes(id, genome, description, symbol, timeframe, fitness) "
                "VALUES (?,?,?,?,?,?)", (family.removeprefix("gen_"), json.dumps(genome, sort_keys=True),
                                         description, symbol, timeframe, fitness))
    con.commit()


def get_genome(con, family: str) -> dict | None:
    r = con.execute("SELECT genome FROM genomes WHERE id=?", (family.removeprefix("gen_"),)).fetchone()
    return None if r is None else json.loads(r["genome"])


def save_ml_spec(con, family: str, spec: dict) -> None:
    con.execute("INSERT OR IGNORE INTO ml_models(id, spec) VALUES (?,?)", (family, json.dumps(spec, sort_keys=True)))
    con.commit()


def get_ml_spec(con, family: str) -> dict | None:
    r = con.execute("SELECT spec FROM ml_models WHERE id=?", (family,)).fetchone()
    return None if r is None else json.loads(r["spec"])
