"""CLI: python scripts/run_gauntlet.py donchian XAUUSD H1 [--mt5]"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from bridge import config, mt5_client  # noqa: E402
from research import data, gauntlet  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("family")
    ap.add_argument("symbol")
    ap.add_argument("timeframe")
    ap.add_argument("--mt5", action="store_true", help="confirm finalist in the MT5 tester")
    a = ap.parse_args()

    t0 = time.time()
    bars = data.bars(a.symbol, a.timeframe)
    spec = mt5_client.symbol_spec(a.symbol)
    acct = mt5_client.account_info()["currency"]
    rate = gauntlet.acct_to_target_rate(mt5_client.symbol_spec, acct, config.settings()["account"]["currency"])
    confirm = None
    if a.mt5:
        from research import mt5_confirm
        confirm = mt5_confirm.make(a.family, a.symbol, a.timeframe, bars, spec)
    res = gauntlet.run(a.family, a.symbol, a.timeframe, bars, spec, rate, mt5_confirm=confirm)
    res["seconds"] = round(time.time() - t0, 1)
    out = config.reports_dir() / f"gauntlet_{res['id']}.json"
    out.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps({"id": res["id"], "verdict": res["verdict"], "params": res["params"],
                      "stages": {k: v.get("pass") for k, v in res["stages"].items()},
                      "seconds": res["seconds"], "file": str(out)}, indent=2))


if __name__ == "__main__":
    main()
