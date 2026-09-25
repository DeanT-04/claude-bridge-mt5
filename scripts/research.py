"""Research CLI.

python scripts/research.py scan [--equities]                  # discover + filter broker symbols
python scripts/research.py enqueue --families all --symbols researchable --tf H1,M30
python scripts/research.py enqueue --families evolve --symbols core --tf H1   # genetic search
python scripts/research.py ml --symbols core --tf H1 --models logreg,gbm      # ML strategies
python scripts/research.py run [--procs 3] [--no-mt5]            # work the queue
python scripts/research.py status | survivors | confirm
python scripts/research.py gauntlet donchian XAUUSD H1 [--mt5]  # one gauntlet, printed
python scripts/research.py programs                               # prop programs + sizes/fees
python scripts/research.py leaderboard [--program ftmo_2step] [--size 50000] [--limit 30]
python scripts/research.py combine [--programs ftmo_2step,...] [--max-sleeves 5]
python scripts/research.py calendar                               # refresh the news calendar

--symbols takes researchable, core, or a comma list (EURUSD,XAUUSD).
"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from bridge import config  # noqa: E402
from research import jobqueue, universe  # noqa: E402
from research.strategies import FAMILIES, get_family  # noqa: E402


def resolve_symbols(spec: str) -> list[str]:
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
    e.add_argument("--symbols", default="researchable")
    e.add_argument("--tf", default="H1")
    e.add_argument("--redo", action="store_true")
    m = sub.add_parser("ml")
    m.add_argument("--symbols", default="core"); m.add_argument("--tf", default="H1")
    m.add_argument("--models", default="logreg,gbm")
    m.add_argument("--label-k", type=float, default=1.5); m.add_argument("--label-bars", type=int, default=24)
    r = sub.add_parser("run"); r.add_argument("--procs", type=int, default=3); r.add_argument("--no-mt5", action="store_true")
    g = sub.add_parser("gauntlet")
    g.add_argument("family"); g.add_argument("symbol"); g.add_argument("timeframe")
    g.add_argument("--mt5", action="store_true", help="confirm the finalist in the MT5 tester")
    lb = sub.add_parser("leaderboard")
    lb.add_argument("--program"); lb.add_argument("--size", type=float)
    lb.add_argument("--min-pass", type=float, default=0.0); lb.add_argument("--limit", type=int, default=30)
    cb = sub.add_parser("combine")
    cb.add_argument("--programs"); cb.add_argument("--ids")
    cb.add_argument("--max-sleeves", type=int, default=5); cb.add_argument("--max-corr", type=float, default=0.5)
    for name in ("status", "survivors", "confirm", "programs", "calendar"):
        sub.add_parser(name)
    a = ap.parse_args()

    if a.cmd == "scan":
        rows = universe.scan(include_equities=a.equities)
        print(json.dumps({"scanned": len(rows), "researchable": sum(x["researchable"] for x in rows)}, indent=1))
    elif a.cmd == "enqueue":
        fams = list(FAMILIES) if a.families == "all" else a.families.split(",")
        syms = resolve_symbols(a.symbols)
        n = jobqueue.enqueue(fams, syms, a.tf.split(","), redo=a.redo)
        print(f"enqueued {n} jobs ({len(fams)} families x {len(syms)} symbols x {a.tf})")
    elif a.cmd == "ml":
        from research import ml
        n = total = 0
        for sym in resolve_symbols(a.symbols):
            for tf in a.tf.split(","):
                for mdl in a.models.split(","):
                    fam = ml.register(sym, tf, mdl, a.label_k, a.label_bars)
                    spec = get_family(fam).spec          # each ML family is tied to one symbol/timeframe
                    n += jobqueue.enqueue([fam], [spec.symbol], [spec.timeframe])
                    total += 1
        print(f"registered {total} ML families, enqueued {n} gauntlets")
    elif a.cmd == "run":
        print(json.dumps(jobqueue.run(a.procs, not a.no_mt5), indent=1, default=str))
    elif a.cmd == "confirm":
        print(json.dumps(jobqueue.confirm_pending(), indent=1))
    elif a.cmd == "status":
        print(json.dumps(jobqueue.status(), indent=1))
    elif a.cmd == "survivors":
        print(json.dumps(jobqueue.survivors(), indent=1, default=str))
    elif a.cmd == "gauntlet":
        from research import data, gauntlet
        t0 = time.time()
        bars, spec = data.bars(a.symbol, a.timeframe), data.spec(a.symbol)
        confirm = None
        if a.mt5:
            from research import mt5_confirm
            confirm = mt5_confirm.make(a.family, a.symbol, a.timeframe, bars, spec)
        res = gauntlet.run(a.family, a.symbol, a.timeframe, bars, spec, mt5_confirm=confirm)
        out = config.reports_dir() / f"gauntlet_{res['id']}.json"
        out.write_text(json.dumps(res, indent=2, default=str))
        print(json.dumps({"id": res["id"], "verdict": res["verdict"], "params": res["params"],
                          "stages": {k: v.get("pass") for k, v in res["stages"].items()},
                          "seconds": round(time.time() - t0, 1), "file": str(out)}, indent=2))
    elif a.cmd == "leaderboard":
        from research import challenge
        rows = challenge.leaderboard(a.program, a.size, a.min_pass, limit=a.limit)
        for r in rows:
            cpp = f"{r['fee_currency']} {r['cost_per_pass']:,.0f}" if r["cost_per_pass"] else "fee n/a"
            print(f"{r['pass_prob']:5.2f} lift {r['lift'] or 0:+.2f}  {r['program']:26} {r['size'] / 1000:>5g}K "
                  f"risk {r['risk_pct']:.2f}%  {r['median_days'] or 0:>4.0f}d  {cpp:>12}  {r['kind'][:4]} {r['id']} {r['name']}")
        if not rows:
            print("no survivors with a prop stage yet")
    elif a.cmd == "combine":
        from research import challenge
        challenge.combine(a.programs.split(",") if a.programs else None,
                          [int(x) for x in a.ids.split(",")] if a.ids else None, a.max_sleeves, a.max_corr)
    elif a.cmd == "calendar":
        from research import calendar
        print(json.dumps(calendar.export(), indent=1))
    elif a.cmd == "programs":
        from research import propfirm
        for k, p in propfirm.profiles().items():
            sizes = ", ".join(f"{x['size'] / 1000:g}K" + (f" {p.fee_currency} {x['fee']:g}" if x.get("fee") else "")
                              for x in p.sizes)
            print(f"{k:26} {p.firm:11} {p.program:34} targets {list(p.phase_targets)} "
                  f"daily {p.max_daily_loss_pct}% max {p.max_total_dd_pct}% {p.max_dd_mode}\n{'':26} sizes: {sizes}")


if __name__ == "__main__":
    main()
