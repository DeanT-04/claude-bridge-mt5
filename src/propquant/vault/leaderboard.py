"""Rebuild the Home.md leaderboard from the trial registry (latest run per strategy)."""

import json
import re

from propquant import paths
from propquant.trials import Registry

START, END = "<!-- AUTO:leaderboard:start -->", "<!-- AUTO:leaderboard:end -->"
ORDER = {"champion": 0, "elite": 1, "contender": 2, "graveyard": 3}


def rows(reg: Registry) -> list[dict]:
    q = """
        SELECT strategy, verdict, summary, ts, run_id FROM runs
        QUALIFY row_number() OVER (PARTITION BY strategy ORDER BY ts DESC) = 1
    """
    out = []
    for strategy, v, summary, ts, run_id in reg.con.execute(q).fetchall():
        s = json.loads(summary)
        out.append({"strategy": strategy, "verdict": v, "ts": ts, "run_id": run_id, **s})
    out.sort(key=lambda r: (ORDER.get(r["verdict"], 9), -r.get("e2e", 0)))
    return out


def render(rs: list[dict]) -> str:
    if not rs:
        return "_No strategies tested yet._"
    lines = [
        "| # | Strategy | Tier | Plan | Reach payout | Eval pass | EV/attempt | DSR "
        "| Beats random |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(rs, 1):
        lines.append(
            f"| {i} | [[{r['strategy']}]] | {r['verdict']} | {r.get('plan', '')} "
            f"| {r.get('e2e', 0):.0%} | {r.get('eval_pass', 0):.0%} | ${r.get('ev', 0):,.0f} "
            f"| {r.get('dsr', 0):.2f} | {r.get('re_pct', 0):.0%} |"
        )
    lines.append(f"\n_{len(rs)} strategies. Ranked by tier, then by reach-payout rate._")
    return "\n".join(lines)


def update(reg: Registry | None = None) -> None:
    own = reg is None
    reg = reg or Registry()
    try:
        home = paths.vault_dir() / "Home.md"
        text = home.read_text(encoding="utf-8")
        block = f"{START}\n{render(rows(reg))}\n{END}"
        text = re.sub(re.escape(START) + ".*?" + re.escape(END), lambda _: block, text,
                      flags=re.S)  # fmt: skip
        home.write_text(text, encoding="utf-8")
    finally:
        if own:
            reg.close()
