"""Sanity check: a one-member portfolio must reproduce that strategy's own OOS daily P&L.

Uses throwaway registries so no trials or holdout accesses are recorded.
"""

import tempfile
from pathlib import Path

import numpy as np

from propquant.gauntlet import portfolio
from propquant.gauntlet import run as grun
from propquant.trials import Registry

NAME = "late_trend"
with tempfile.TemporaryDirectory() as d:
    reg = Registry(Path(d) / "a.duckdb")
    single = grun.run(NAME, registry=reg, progress=lambda *_: None)
    reg.close()
    portfolio.Registry = lambda: Registry(Path(d) / "b.duckdb")  # isolate the portfolio run
    portfolio.ideas.require = lambda *a, **k: "check"
    port = portfolio.run("equivalence_check", [portfolio.Member(NAME, "NQ")], log=lambda *_: None)
a, b = single.oos_daily, port.oos_daily
print(
    f"days equal: {np.array_equal(single.oos_days, port.oos_days)}; sessions {len(a)} vs {len(b)}"
)
if len(a) == len(b):
    print(f"max |daily diff| = {np.max(np.abs(a - b)):.10f}")
print(f"single total {a.sum():.2f}  portfolio total {b.sum():.2f}")
