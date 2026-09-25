"""Python vs MT5 trade parity for strategy families on a window.

python scripts/parity_check.py XAUUSD H1 2024-01-01 2024-07-01 [family ...]
"""
import argparse
import sys
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np  # noqa: E402

from bridge import compiler, tester  # noqa: E402
from research import data  # noqa: E402
from research.engine import Costs  # noqa: E402
from research.mt5_confirm import BAR_SECONDS, parity  # noqa: E402
from research.strategies import FAMILIES, get_family  # noqa: E402


def check(fam_name, symbol, tf, d0, d1, point, params=None) -> dict:
    fam = get_family(fam_name)
    p = params or fam.Params()
    inputs = {k: tester.Param(v) for k, v in p.dict().items()}
    inputs["InpRiskPct"] = tester.Param(1.0)
    res = tester.run(tester.Job(fam.EXPERT, symbol, tf, d0, d1, params=inputs))
    if not res.ok:
        return {"family": fam_name, "error": res.error}
    b = data.bars(symbol, tf)
    ts = lambda d: datetime(d.year, d.month, d.day, tzinfo=timezone.utc).timestamp()
    a, z = np.searchsorted(b["time"], ts(d0)), np.searchsorted(b["time"], ts(d1))
    py = fam.backtest(b, p, Costs(point=point), int(a), int(z))
    return {"family": fam_name, **parity(py, res.trades, BAR_SECONDS[tf])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("symbol"); ap.add_argument("tf"); ap.add_argument("start"); ap.add_argument("end")
    ap.add_argument("families", nargs="*")
    ap.add_argument("--point", type=float, default=None)
    a = ap.parse_args()
    point = a.point
    if point is None:
        from bridge import mt5_client
        point = mt5_client.symbol_spec(a.symbol)["point"]
    compiler.compile_expert("QB_Rules")
    for f in a.families or list(FAMILIES):
        r = check(f, a.symbol, a.tf, date.fromisoformat(a.start), date.fromisoformat(a.end), point)
        print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()}, flush=True)


if __name__ == "__main__":
    main()
