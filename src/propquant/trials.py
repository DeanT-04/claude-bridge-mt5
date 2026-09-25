"""Trial registry: every configuration ever evaluated is counted here.

The Deflated Sharpe Ratio needs the true number of trials, so nothing is evaluated without
being recorded. Holdout access is logged in the same database. The file lives in
`registry/` and is committed, so the count survives a wipe of `data/`.
"""

import json
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path

import duckdb

from propquant.paths import REPO_ROOT

DB_PATH = REPO_ROOT / "registry" / "trials.duckdb"

SCHEMA = """
CREATE TABLE IF NOT EXISTS trials (
    ts TIMESTAMP, run_id VARCHAR, strategy VARCHAR, family VARCHAR, params VARCHAR,
    scope VARCHAR, score DOUBLE, commit VARCHAR, data_hash VARCHAR
);
CREATE TABLE IF NOT EXISTS holdout_access (
    ts TIMESTAMP, run_id VARCHAR, strategy VARCHAR, params VARCHAR, commit VARCHAR,
    forced BOOLEAN
);
CREATE TABLE IF NOT EXISTS runs (
    ts TIMESTAMP, run_id VARCHAR, strategy VARCHAR, verdict VARCHAR, summary VARCHAR,
    commit VARCHAR, data_hash VARCHAR, seed INTEGER
);
"""


def git_commit() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], cwd=REPO_ROOT, capture_output=True,
            text=True, check=True,
        )  # fmt: skip
        dirty = subprocess.run(
            ["git", "status", "--porcelain", "--", "src", "config"], cwd=REPO_ROOT,
            capture_output=True, text=True, check=True,
        ).stdout.strip()  # fmt: skip
        return out.stdout.strip() + ("-dirty" if dirty else "")
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


class Registry:
    """Connects on demand and releases the file after each write/read helper, so a long
    gauntlet run never holds the DuckDB lock while it backtests (other processes can read)."""

    def __init__(self, path: Path = DB_PATH) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        self._con: duckdb.DuckDBPyConnection | None = None
        self.commit = git_commit()
        self.con.execute(SCHEMA)
        self.release()

    @property
    def con(self) -> duckdb.DuckDBPyConnection:
        if self._con is None:
            for attempt in range(120):  # wait up to ~2 min for another process's write
                try:
                    self._con = duckdb.connect(str(self.path))
                    break
                except duckdb.IOException:
                    if attempt == 119:
                        raise
                    time.sleep(1)
        return self._con  # type: ignore[return-value]

    def release(self) -> None:
        if self._con is not None:
            self._con.close()
            self._con = None

    close = release

    def add_trials(
        self, run_id: str, strategy: str, family: str, rows: list[tuple[dict, str, float]],
        data_hash: str,
    ) -> None:  # fmt: skip
        now = datetime.now(UTC)
        self.con.executemany(
            "INSERT INTO trials VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (now, run_id, strategy, family, json.dumps(p, sort_keys=True), scope, score,
                 self.commit, data_hash)
                for p, scope, score in rows
            ],
        )  # fmt: skip
        self.release()

    def n_trials(self, family: str | None = None) -> int:
        """Distinct configurations ever evaluated (optionally within one family)."""
        q = "SELECT count(DISTINCT strategy || params) FROM trials"
        args: list = []
        if family:
            q += " WHERE family = ?"
            args.append(family)
        n = int(self.con.execute(q, args).fetchone()[0])  # type: ignore[index]
        self.release()
        return n

    def holdout_uses(self, strategy: str, params: dict) -> int:
        q = "SELECT count(*) FROM holdout_access WHERE strategy = ? AND params = ?"
        row = self.con.execute(q, [strategy, json.dumps(params, sort_keys=True)]).fetchone()
        self.release()
        return int(row[0])  # type: ignore[index]

    def log_holdout(self, run_id: str, strategy: str, params: dict, forced: bool) -> None:
        self.con.execute(
            "INSERT INTO holdout_access VALUES (?, ?, ?, ?, ?, ?)",
            [datetime.now(UTC), run_id, strategy, json.dumps(params, sort_keys=True),
             self.commit, forced],
        )  # fmt: skip
        self.release()

    def log_run(self, run_id: str, strategy: str, verdict: str, summary: dict, data_hash: str,
                seed: int) -> None:  # fmt: skip
        self.con.execute(
            "INSERT INTO runs VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [datetime.now(UTC), run_id, strategy, verdict, json.dumps(summary, default=float),
             self.commit, data_hash, seed],
        )  # fmt: skip
        self.release()
