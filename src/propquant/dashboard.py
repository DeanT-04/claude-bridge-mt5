"""Build dashboard/data.js from the registry (runs, trials, catalogue). Open dashboard/index.html.

The page is static: data is embedded as a JS assignment so it also works from file:// with no
server. Everything shown comes from registry/runs/*.json and the trial registry.
"""

import json
from datetime import UTC, datetime

from propquant.catalogue import catalogue
from propquant.paths import REPO_ROOT
from propquant.reports.export import RUNS_DIR
from propquant.strategies.base import REGISTRY
from propquant.trials import Registry

OUT = REPO_ROOT / "dashboard" / "data.js"
TIERS = {"champion": 0, "elite": 1, "contender": 2, "graveyard": 3}


def build() -> str:
    cat = catalogue()  # also registers every strategy family (needed for REGISTRY below)
    runs = {}
    for f in sorted(RUNS_DIR.glob("*.json")):
        r = json.loads(f.read_text(encoding="utf-8"))
        runs[r["run_id"]] = r
    reg = Registry()
    try:
        n_trials = reg.n_trials()
        holdouts = reg.con.execute("SELECT count(*) FROM holdout_access").fetchone()[0]
        legacy = reg.con.execute(
            "SELECT run_id, strategy, verdict, summary, ts FROM runs ORDER BY ts"
        ).fetchall()
    finally:
        reg.close()

    # strategies: latest run per key, plus the full run history
    strategies: dict[str, dict] = {}
    for run_id, key, verdict, summary, ts in legacy:
        s = strategies.setdefault(key, {"key": key, "history": []})
        s["history"].append({"run_id": run_id, "verdict": verdict, "ts": str(ts)[:19],
                             "detail": run_id in runs, **json.loads(summary)})  # fmt: skip
    for s in strategies.values():
        latest = s["history"][-1]
        rec = runs.get(latest["run_id"], {})
        name, _, sym = s["key"].partition("@")
        cls = REGISTRY.get(name)
        s.update({
            "name": name, "symbol": sym or "NQ",
            "family": rec.get("family") or (cls.family if cls else ""),
            "verdict": latest["verdict"], "plan": latest.get("plan", ""),
            "e2e": latest.get("e2e", 0), "eval_pass": latest.get("eval_pass", 0),
            "ev": latest.get("ev", 0), "dsr": latest.get("dsr", 0),
            "re_pct": latest.get("re_pct", 0), "oos_trades": latest.get("oos_trades", 0),
            "latest_run": latest["run_id"], "runs": len(s["history"]),
        })  # fmt: skip
    ordered = sorted(strategies.values(),
                     key=lambda s: (TIERS.get(s["verdict"], 9), -s["e2e"]))  # fmt: skip
    tested = sum(1 for c in cat if c["key"] in strategies)
    data = {
        "generated": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S"),
        "summary": {
            "strategies": len(ordered), "runs": len(legacy), "trials": n_trials,
            "holdout_accesses": holdouts, "catalogue_total": len(cat),
            "catalogue_tested": tested,
            "tiers": {t: sum(1 for s in ordered if s["verdict"] == t) for t in TIERS},
        },
        "catalogue": [{**c, "tested": c["key"] in strategies} for c in cat],
        "strategies": ordered,
        "runs": runs,
    }  # fmt: skip
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("window.PQ = " + json.dumps(data, separators=(",", ":")) + ";\n",
                   encoding="utf-8")  # fmt: skip
    return str(OUT)
