"""Print the CFD-firm transfer results (robustness columns) from registry/runs/*.json."""

import json
from pathlib import Path

RUNS = Path(__file__).resolve().parents[1] / "registry" / "runs"
for f in sorted(RUNS.glob("*.json")):
    r = json.loads(f.read_text(encoding="utf-8"))
    if ":" not in r["strategy"]:
        continue
    c = r["oos_challenge"][r["best_plan"]]
    s = r["stats"]
    print(f"{r['strategy']:<30} {r['verdict']:<9} pass={c['eval_pass']:.2f} "
          f"e2e={c['end_to_end_payout']:.2f} ev={c['ev_per_attempt']:7.0f} "
          f"p05={c['ev_p05']:7.0f} med={c['median_sessions_to_pass']:.0f} "
          f"p90={c['p90_sessions_to_pass']:.0f} dsr={s['dsr']:.2f} re={s['re_percentile']:.2f} "
          f"sr={s['oos_sharpe_ann']:.2f}")  # fmt: skip
