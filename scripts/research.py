"""Research CLI.

python scripts/research.py scan [--equities]
python scripts/research.py enqueue --families all --symbols small|researchable|core|EURUSD,XAUUSD --tf H1,M30
python scripts/research.py run [--procs 3] [--no-mt5]
python scripts/research.py status
python scripts/research.py survivors
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from bridge import config  # noqa: E402
from research import jobqueue, universe  # noqa: E402
from research.strategies import FAMILIES  # noqa: E402


def resolve_symbols(spec: str) -> list[str]:
    if spec == "small":
        return [r["symbol"] for r in universe.load(small_account_only=True)]
    if spec == "researchable":
        return [r["symbol"] for r in universe.load()]
    if spec == "core":
        return list(config.settings()["research"]["core_symbols"])
    return [s.strip() for s in spec.split(",") if s.strip()]


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan"); s.add_argument("--equities", action="store_true")
    e = sub.add_parser("enqueue")
    e.add_argument("--families", default="all")
    e.add_argument("--symbols", default="small")
    e.add_argument("--tf", default="H1")
    e.add_argument("--redo", action="store_true")
    r = sub.add_parser("run"); r.add_argument("--procs", type=int, default=3); r.add_argument("--no-mt5", action="store_true")
    sub.add_parser("status"); sub.add_parser("survivors"); sub.add_parser("confirm")
    a = ap.parse_args()

    if a.cmd == "scan":
        rows = universe.scan(include_equities=a.equities)
        ok = [x for x in rows if x["researchable"]]
        print(json.dumps({"scanned": len(rows), "researchable": len(ok),
                          "small_account": sum(x["small_account"] for x in ok)}, indent=1))
    elif a.cmd == "enqueue":
        fams = list(FAMILIES) if a.families == "all" else a.families.split(",")
        syms = resolve_symbols(a.symbols)
        n = jobqueue.enqueue(fams, syms, a.tf.split(","), redo=a.redo)
        print(f"enqueued {n} jobs ({len(fams)} families x {len(syms)} symbols x {a.tf})")
    elif a.cmd == "run":
        print(json.dumps(jobqueue.run(a.procs, not a.no_mt5), indent=1, default=str))
    elif a.cmd == "confirm":
        print(json.dumps(jobqueue.confirm_pending(), indent=1))
    elif a.cmd == "status":
        print(json.dumps(jobqueue.status(), indent=1))
    elif a.cmd == "survivors":
        print(json.dumps(jobqueue.survivors(), indent=1, default=str))


if __name__ == "__main__":
    main()
