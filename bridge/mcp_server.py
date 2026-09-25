"""MCP server exposing the BlackBull MT5 research bridge to Claude.

Run: python -m bridge.mcp_server   (registered in .mcp.json)
No tool places orders directly. Trading happens only through QB_Host reading a portfolio
config, and a config changes only via apply_deployment (user-approved) or kill_switch (stop).
"""
from __future__ import annotations

import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp.server.mcpserver import MCPServer  # noqa: E402
from mcp.types import ToolAnnotations  # noqa: E402

from bridge import compiler, config, mt5_client, tester  # noqa: E402
from registry import db  # noqa: E402

mcp = MCPServer("mt5-bridge")


@mcp.tool()
def account_info() -> dict:
    """Connected BlackBull account: server, demo flag, currency, leverage, balance, equity."""
    return mt5_client.account_info()


@mcp.tool()
def list_symbols(group: str | None = None, name_contains: str | None = None, limit: int = 200) -> dict:
    """Broker symbols with contract specs. group: Forex, Metals, Indices, Cryptos, Commodities,
    Equities, Futures, Crypto Perpetuals."""
    syms = mt5_client.list_symbols(group)
    if name_contains:
        syms = [s for s in syms if name_contains.lower() in s["name"].lower()]
    return {"total": len(syms), "symbols": syms[:limit]}


@mcp.tool()
def symbol_spec(symbol: str) -> dict:
    """Full contract spec for one symbol (spread, tick value, min lot, swaps...)."""
    return mt5_client.symbol_spec(symbol)


@mcp.tool()
def get_bars(symbol: str, timeframe: str, start: str, end: str, tail: int = 20) -> dict:
    """OHLC bars (server time). Returns count, range and the last `tail` bars. Dates: YYYY-MM-DD."""
    b = mt5_client.get_bars(symbol, timeframe, datetime.fromisoformat(start), datetime.fromisoformat(end))
    rows = [{"time": datetime.utcfromtimestamp(int(r["time"])).isoformat(), "open": float(r["open"]),
             "high": float(r["high"]), "low": float(r["low"]), "close": float(r["close"]),
             "spread": int(r["spread"])} for r in b[-tail:]] if len(b) else []
    return {"count": int(len(b)),
            "first": datetime.utcfromtimestamp(int(b["time"][0])).isoformat() if len(b) else None,
            "last": rows[-1]["time"] if rows else None, "tail": rows}


@mcp.tool()
def compile_expert(name: str) -> dict:
    """Sync repo mql5/ sources into the tester copy and compile Experts/QB/<name>.mq5."""
    return compiler.compile_expert(name)


def _job(expert, symbol, timeframe, date_from, date_to, params, model, optimisation="none",
         criterion="custom", forward_date=None, spread=None) -> tester.Job:
    ps = {}
    for k, v in (params or {}).items():
        ps[k] = tester.Param(v["value"], v.get("start"), v.get("step"), v.get("stop")) \
            if isinstance(v, dict) else tester.Param(v)
    return tester.Job(expert, symbol, timeframe, date.fromisoformat(date_from), date.fromisoformat(date_to),
                      params=ps, model=model, optimisation=optimisation, criterion=criterion,
                      forward_date=date.fromisoformat(forward_date) if forward_date else None, spread=spread)


@mcp.tool()
def run_backtest(expert: str, symbol: str, timeframe: str, date_from: str, date_to: str,
                 params: dict | None = None, model: str = "ohlc_m1", spread: int | None = None) -> dict:
    """Single MT5 Strategy Tester run on the portable tester copy (deposit/currency/leverage
    from settings.yaml). expert like 'QB\\QB_Donchian.ex5'. model: ohlc_m1 | real_ticks |
    every_tick | open_prices. Returns report summary and trade count (trades stored in registry)."""
    res = tester.run(_job(expert, symbol, timeframe, date_from, date_to, params, model, spread=spread))
    if res.ok:
        con = db.connect()
        db.log_run(con, "mt5", expert, symbol, timeframe, params or {}, res.summary, res.trades, res.job.tag)
    return {"ok": res.ok, "error": res.error, "seconds": round(res.seconds, 1), "tag": res.job.tag,
            "summary": res.summary, "trades": len(res.trades)}


@mcp.tool()
def run_optimization(expert: str, symbol: str, timeframe: str, date_from: str, date_to: str,
                     params: dict, mode: str = "genetic", criterion: str = "custom",
                     forward_date: str | None = None, model: str = "ohlc_m1", top: int = 20) -> dict:
    """MT5 optimisation. params: {name: value} fixed or {name: {value,start,step,stop}} optimised.
    Returns the top passes (and forward-segment passes when forward_date is set)."""
    res = tester.run(_job(expert, symbol, timeframe, date_from, date_to, params, model,
                          optimisation=mode, criterion=criterion, forward_date=forward_date))
    key = "Result"
    passes = sorted(res.passes, key=lambda r: r.get(key, 0) if isinstance(r.get(key), float) else 0,
                    reverse=True)
    return {"ok": res.ok, "error": res.error, "seconds": round(res.seconds, 1),
            "passes": len(res.passes), "top": passes[:top], "forward_top": res.forward_passes[:top]}


@mcp.tool()
def run_gauntlet(family: str, symbol: str, timeframe: str, mt5: bool = False) -> dict:
    """Full validation gauntlet (walk-forward, plateau, DSR, Monte Carlo sizing, cost stress,
    random-entry + buy-and-hold benchmarks, £100 feasibility, one-shot holdout, optional MT5
    parity/stress). Can take several minutes."""
    from research import data, gauntlet
    bars = data.bars(symbol, timeframe)
    spec = mt5_client.symbol_spec(symbol)
    acct = mt5_client.account_info()["currency"]
    rate = gauntlet.acct_to_target_rate(mt5_client.symbol_spec, acct, config.settings()["account"]["currency"])
    confirm = None
    if mt5:
        from research import mt5_confirm
        confirm = mt5_confirm.make(family, symbol, timeframe, bars, spec)
    res = gauntlet.run(family, symbol, timeframe, bars, spec, rate, mt5_confirm=confirm,
                       progress=lambda *_: None)
    return _brief(res)


def _brief(res: dict) -> dict:
    s = res["stages"]
    return {"id": res["id"], "verdict": res["verdict"], "params": res["params"],
            "stages": {k: {kk: vv for kk, vv in v.items() if kk not in ("chosen_params",)}
                       for k, v in s.items()}}


@mcp.tool()
def universe(small_account_only: bool = False, limit: int = 100) -> dict:
    """Researchable symbols from the last scan, cheapest first (cost_atr = spread / H1 ATR,
    minlot_risk_pct = % of the £100 target lost by the minimum lot at a 1.5×ATR stop)."""
    from research import universe as uni
    rows = uni.load(small_account_only=small_account_only)
    return {"total": len(rows), "symbols": rows[:limit]}


@mcp.tool()
def scan_universe(include_equities: bool = False) -> dict:
    """Rescan every broker symbol and refresh the researchable / small-account lists (slow)."""
    from research import universe as uni
    rows = uni.scan(include_equities=include_equities, progress=lambda *_: None)
    ok = [r for r in rows if r["researchable"]]
    return {"scanned": len(rows), "researchable": len(ok), "small_account": sum(r["small_account"] for r in ok)}


@mcp.tool()
def enqueue_research(families: list[str], symbols: list[str], timeframes: list[str], redo: bool = False) -> dict:
    """Queue gauntlet jobs. families: names or ['all']. symbols: names or ['small'|'researchable'|'core']."""
    from research import jobqueue
    from research.strategies import FAMILIES
    from research import universe as uni
    fams = list(FAMILIES) if families == ["all"] else families
    if symbols in (["small"], ["researchable"]):
        syms = [r["symbol"] for r in uni.load(small_account_only=symbols == ["small"])]
    elif symbols == ["core"]:
        syms = list(config.settings()["research"]["core_symbols"])
    else:
        syms = symbols
    return {"enqueued": jobqueue.enqueue(fams, syms, timeframes, redo=redo)}


@mcp.tool()
def enqueue_ml(symbols: list[str], timeframes: list[str], models: list[str] | None = None,
               label_k: float = 1.5, label_bars: int = 24) -> dict:
    """Register ML strategies (walk-forward logreg/gbm on 12 features, exported to ONNX) and queue
    their gauntlets. symbols: names or ['small'|'researchable'|'core']."""
    from research import jobqueue, ml
    from research import universe as uni
    if symbols in (["small"], ["researchable"]):
        symbols = [r["symbol"] for r in uni.load(small_account_only=symbols == ["small"])]
    elif symbols == ["core"]:
        symbols = list(config.settings()["research"]["core_symbols"])
    n, fams = 0, []
    for s in symbols:
        for tf in timeframes:
            for mdl in models or ["logreg", "gbm"]:
                f = ml.register(s, tf, mdl, label_k, label_bars)
                fams.append(f)
                n += jobqueue.enqueue([f], [s], [tf])
    return {"families": fams, "enqueued": n}


@mcp.tool()
def start_research(processes: int = 3, mt5_confirm: bool = True) -> dict:
    """Start the queue worker in the background (Python gauntlets in parallel, then MT5
    confirmation of survivors). Output goes to runtime/reports/research_worker.log."""
    import subprocess
    log = config.reports_dir() / "research_worker.log"
    args = [sys.executable, str(config.ROOT / "scripts" / "research.py"), "run", "--procs", str(processes)]
    if not mt5_confirm:
        args.append("--no-mt5")
    with open(log, "a") as fh:
        p = subprocess.Popen(args, cwd=config.ROOT, stdout=fh, stderr=subprocess.STDOUT,
                             creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    return {"pid": p.pid, "log": str(log)}


@mcp.tool()
def research_status() -> dict:
    """Queue counts and verdict tallies."""
    from research import jobqueue
    return jobqueue.status()


@mcp.tool()
def research_survivors() -> list[dict]:
    """Strategies that passed the gauntlet (or await MT5 confirmation), with OOS metrics and sizing."""
    from research import jobqueue
    return jobqueue.survivors()


# ------------------------------------------------------------------ deployment (M3)
@mcp.tool()
def install_host(target: str = "demo") -> dict:
    """Sync the QB sources into the demo or live terminal and compile QB_Host there. Afterwards
    the user attaches QB_Host to any chart once (InpConfig=portfolio_<target>.cfg) and enables
    Algo Trading. ML sleeves also need their .onnx files, which live in the shared Common folder."""
    from bridge import preflight
    return compiler.compile_expert("QB_Host", preflight.terminal_mql5(target))


@mcp.tool()
def live_preflight() -> dict:
    """Read-only live-readiness report: live_enabled, separate live terminal reachable and on a
    REAL account in the target currency/leverage, QB_Host compiled + running + not halted, risk
    limits sane, every sleeve validated, and each sleeve's min lot fits its risk at the real
    balance. Run before approving any live proposal."""
    from bridge import preflight
    return preflight.live_preflight()


@mcp.tool()
def portfolio_allocation(gauntlet_ids: list[int], budget_pct: float | None = None) -> dict:
    """Correlation, inverse-vol risk allocation and combined Monte Carlo for a set of gauntlet
    results (last 3 years). budget_pct defaults to deployment.max_open_risk_pct."""
    from research import portfolio
    con = db.connect()
    sleeves = []
    for gid in gauntlet_ids:
        g = db.gauntlet(con, gid)
        risk = (g["stages"].get("sizing_montecarlo", {}).get("risk") or 0) * 100 \
            or config.settings()["deployment"]["unvalidated_risk_pct"]
        sleeves.append({**g, "risk_pct": risk})
    lim = config.settings()["deployment"]
    return portfolio.build(sleeves, budget_pct or lim["max_open_risk_pct"],
                           config.gauntlet()["montecarlo"]["dd95_max_pct"] / 100)


@mcp.tool()
def propose_deployment(add_gauntlet_ids: list[int] | None = None, remove_sleeve_ids: list[int] | None = None,
                       target: str = "demo", allow_unvalidated: bool = False, enabled: bool = True,
                       limits: dict | None = None, reset_halt: bool = False, note: str = "",
                       balance_scale: float | None = None) -> dict:
    """Draft a new QB_Host config. Changes NOTHING on the terminal. Returns the full config, a
    diff against the running one, and proposal_id + sha256. Show the user the diff and wait for
    their explicit approval in chat before calling apply_deployment. allow_unvalidated lets a
    sleeve that failed the gauntlet forward-test on demo only (small fixed risk).
    balance_scale: None on demo = size as the £100 target account; 1.0 = the demo's own equity."""
    from bridge import deploy
    from research import gauntlet
    scale = balance_scale
    if target == "demo" and scale is None:
        acct = mt5_client.account_info()
        rate = 1 / gauntlet.acct_to_target_rate(mt5_client.symbol_spec, acct["currency"],
                                                config.settings()["account"]["currency"])
        scale = deploy.demo_balance_scale(acct, rate)
    return deploy.propose(target, add_gauntlet_ids, remove_sleeve_ids, allow_unvalidated, enabled,
                          limits, scale, reset_halt, note)


@mcp.tool(annotations=ToolAnnotations(destructiveHint=True, idempotentHint=False))
def apply_deployment(proposal_id: int, sha256: str) -> dict:
    """Write an approved proposal to the terminal; QB_Host picks it up within a second and starts
    trading it. ONLY call after the user has explicitly approved this exact proposal in chat."""
    from bridge import deploy
    return deploy.apply(proposal_id, sha256)


@mcp.tool()
def kill_switch(target: str = "demo", reason: str = "") -> dict:
    """Immediately disable a portfolio: QB_Host closes every QB position and stops trading.
    Safe to call at any time; re-enabling requires a new approved proposal."""
    from bridge import deploy
    return deploy.kill(target, reason)


@mcp.tool()
def deployment_status(target: str = "demo") -> dict:
    """Running config (sleeves, limits, version) plus QB_Host's live status file (equity,
    drawdown state, halts, open sleeves, errors)."""
    from dataclasses import asdict
    from bridge import deploy
    return {"portfolio": asdict(deploy.current(target)), "host": deploy.host_status(target)}


@mcp.tool()
def forward_test_report(target: str = "demo") -> dict:
    """Per-sleeve forward-test results from the terminal's deal history: trades, R, profit,
    drift test vs backtest, and whether each sleeve is ready for live."""
    from bridge import monitor
    return monitor.forward_report(target)


@mcp.tool()
def promote_to_live(sleeve_ids: list[int], force: bool = False) -> dict:
    """Draft a LIVE config from demo sleeves that passed the gauntlet and their forward test.
    Refused unless account.live_enabled is true. Like any proposal it changes nothing until
    the user approves and apply_deployment is called."""
    from bridge import monitor
    return monitor.promote_to_live(sleeve_ids, force)


@mcp.tool()
def list_gauntlets(limit: int = 20) -> list[dict]:
    """Most recent gauntlet verdicts from the registry."""
    return db.recent_gauntlets(db.connect(), limit)


@mcp.tool()
def get_gauntlet(gauntlet_id: int) -> dict | None:
    """Full stage-by-stage detail of one gauntlet run."""
    return db.gauntlet(db.connect(), gauntlet_id)


if __name__ == "__main__":
    mcp.run()
