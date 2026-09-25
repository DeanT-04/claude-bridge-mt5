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
    from settings.yaml). expert like 'QB\\QB_Rules.ex5'. model: ohlc_m1 | real_ticks |
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
    random-entry + buy-and-hold benchmarks, one-shot holdout, prop-challenge ranking of every
    firm program, optional MT5 parity/stress). Can take several minutes."""
    from research import data, gauntlet
    bars = data.bars(symbol, timeframe)
    spec = data.spec(symbol)
    confirm = None
    if mt5:
        from research import mt5_confirm
        confirm = mt5_confirm.make(family, symbol, timeframe, bars, spec)
    res = gauntlet.run(family, symbol, timeframe, bars, spec, mt5_confirm=confirm,
                       progress=lambda *_: None)
    return _brief(res)


def _brief(res: dict) -> dict:
    s = res["stages"]
    return {"id": res["id"], "verdict": res["verdict"], "params": res["params"],
            "stages": {k: {kk: vv for kk, vv in v.items() if kk not in ("chosen_params",)}
                       for k, v in s.items()}}


@mcp.tool()
def universe(limit: int = 100) -> dict:
    """Researchable symbols from the last scan, cheapest first (cost_atr = spread / H1 ATR,
    minlot_risk_pct = % of the research account lost by the minimum lot at a 1.5×ATR stop)."""
    from research import universe as uni
    rows = uni.load()
    return {"total": len(rows), "symbols": rows[:limit]}


@mcp.tool()
def scan_universe(include_equities: bool = False) -> dict:
    """Rescan every broker symbol and refresh the researchable list (about a minute)."""
    from research import universe as uni
    rows = uni.scan(include_equities=include_equities, progress=lambda *_: None)
    return {"scanned": len(rows), "researchable": sum(r["researchable"] for r in rows)}


def _symbols(symbols: list[str]) -> list[str]:
    """Resolve the ['researchable'] and ['core'] shortcuts."""
    from research import universe as uni
    if symbols == ["researchable"]:
        return [r["symbol"] for r in uni.load()]
    if symbols == ["core"]:
        return list(config.settings()["research"]["core_symbols"])
    return symbols


@mcp.tool()
def enqueue_research(families: list[str], symbols: list[str], timeframes: list[str], redo: bool = False) -> dict:
    """Queue gauntlet jobs. families: names, ['all'] or ['evolve'] (genetic search).
    symbols: names, ['researchable'] or ['core']."""
    from research import jobqueue
    from research.strategies import FAMILIES
    fams = list(FAMILIES) if families == ["all"] else families
    return {"enqueued": jobqueue.enqueue(fams, _symbols(symbols), timeframes, redo=redo)}


@mcp.tool()
def enqueue_ml(symbols: list[str], timeframes: list[str], models: list[str] | None = None,
               label_k: float = 1.5, label_bars: int = 24) -> dict:
    """Register ML strategies (walk-forward logreg/gbm on 12 features, exported to ONNX) and queue
    their gauntlets. symbols: names, ['researchable'] or ['core']."""
    from research import jobqueue, ml
    n, fams = 0, []
    for s in _symbols(symbols):
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


# ------------------------------------------------------------------ deployment
@mcp.tool()
def install_host(target: str = "demo") -> dict:
    """Sync the QB sources into a target terminal (demo or a prop account) and compile QB_Host
    there. Afterwards the user attaches QB_Host to any chart once (InpConfig=portfolio_<target>.cfg)
    and enables Algo Trading. ML sleeves also need their .onnx files (shared Common folder)."""
    from bridge import preflight
    return compiler.compile_expert("QB_Host", preflight.terminal_mql5(target))


@mcp.tool()
def prop_preflight(target: str) -> dict:
    """Read-only readiness report for a prop-account target: enabled by the user, program and
    size set, EA approval where the firm requires it, terminal reachable on the expected account
    type, balance = challenge size, QB_Host compiled/running/not halted, prop rules in the config,
    sleeves validated, min lots fit. Run before approving any prop proposal."""
    from bridge import preflight
    return preflight.preflight(target)


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
                       balance_scale: float | None = None, prop_profile: str | None = None,
                       prop_size: float | None = None) -> dict:
    """Draft a new QB_Host config. Changes NOTHING on the terminal. Returns the full config, a
    diff against the running one, and proposal_id + sha256. Show the user the diff and wait for
    their explicit approval in chat before calling apply_deployment. allow_unvalidated lets a
    sleeve that failed the gauntlet forward-test on demo only (small fixed risk).
    target: 'demo' or a prop target from settings.terminals (must be in enabled_targets); a prop
    target automatically gets its program's rules. prop_profile overrides (name from
    prop_profiles(); "" clears). On demo it rehearses a challenge's rules. Rules are tightened
    by prop_safety_buffer and enforced by QB_Host. prop_size: challenge account size (default:
    terminals.<target>.size). balance_scale: equity multiplier (default 1)."""
    from bridge import deploy
    return deploy.propose(target, add_gauntlet_ids, remove_sleeve_ids, allow_unvalidated, enabled,
                          limits, balance_scale, reset_halt, note, prop_profile=prop_profile,
                          prop_size=prop_size)


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
    drift test vs backtest, and whether each sleeve is ready for a prop account."""
    from bridge import monitor
    return monitor.forward_report(target)


@mcp.tool()
def promote(sleeve_ids: list[int], target: str, force: bool = False) -> dict:
    """Draft a prop-account config from demo sleeves that passed the gauntlet and their demo
    forward test, with the target's prop rules. Like any proposal it changes nothing until the
    user approves and apply_deployment is called."""
    from bridge import monitor
    return monitor.promote(sleeve_ids, target, force)


# ------------------------------------------------------------------ prop firms
@mcp.tool()
def prop_profiles() -> dict:
    """Every modelled prop program (config/propfirms.yaml): firm, rules, and all account sizes
    offered (smallest to largest) with fees, so the user can pick program + size."""
    from dataclasses import asdict
    from research import propfirm
    return {k: asdict(v) for k, v in propfirm.profiles().items()}


def _sleeves_for(gauntlet_ids: list[int]) -> list[dict]:
    con = db.connect()
    out = []
    for gid in gauntlet_ids:
        g = db.gauntlet(con, gid)
        risk = (g["stages"].get("sizing_montecarlo", {}).get("risk") or 0) * 100 or 1.0
        out.append({**g, "risk_pct": risk})
    return out


@mcp.tool()
def prop_simulate(gauntlet_ids: list[int], profile: str, size: float | None = None, years: float = 3.0) -> dict:
    """Monte Carlo one prop program for these strategies (their walk-forward OOS trades under the
    program's weekend/news rules, applied trade by trade, every phase): P(pass) vs risk per trade,
    the P(pass)-maximising risk, lift over the edge-removed baseline, and the fee and expected
    cost per pass for the chosen account size."""
    from research import propfirm
    prof = propfirm.profiles()[profile]
    days, active, _, source = propfirm.sleeve_days(_sleeves_for(gauntlet_ids), years, propfirm.variant(prof))
    res = propfirm.evaluate(days, active, prof, runs=2000, size=size)
    res.update({"trade_days": len(days), "active_share": round(active, 3), "source": source,
                "note": "risk_pct = risk per trade of the largest sleeve; others scale by their weights"})
    return res


@mcp.tool()
def prop_rank(gauntlet_ids: list[int], years: float = 3.0) -> list[dict]:
    """Rank EVERY modelled prop program for these strategies by P(pass) at its best risk, with
    lift over the edge-removed baseline, fee and cost per pass (at the research size)."""
    from research import propfirm
    sleeves = _sleeves_for(gauntlet_ids)
    cache, out = {}, []
    for name, prof in propfirm.profiles().items():
        v = propfirm.variant(prof)
        if v not in cache:
            cache[v] = propfirm.sleeve_days(sleeves, years, v)
        days, active, _, source = cache[v]
        out.append({**propfirm.evaluate(days, active, prof, runs=1000), "source": source})
    return sorted(out, key=lambda r: r["best"]["pass_prob"], reverse=True)


@mcp.tool()
def prop_leaderboard(program: str | None = None, size: float | None = None, min_pass_prob: float = 0.0,
                     include_portfolios: bool = True, limit: int = 50) -> list[dict]:
    """Challenge leaderboard: every surviving strategy (and combined portfolio) x program x
    account size, best P(pass) first, with lift over luck, the P(pass)-maximising risk, median
    days, fee and expected cost per pass. Filter by program key and/or size."""
    from research import challenge
    return challenge.leaderboard(program, size, min_pass_prob, portfolios=include_portfolios, limit=limit)


@mcp.tool()
def prop_combine(programs: list[str] | None = None, gauntlet_ids: list[int] | None = None,
                 max_sleeves: int = 5, max_corr: float = 0.5) -> list[dict]:
    """Build challenge portfolios: per program, greedily combine uncorrelated survivors (or the
    given gauntlets) while P(pass) improves, on their walk-forward OOS trades. Stored and shown
    in prop_leaderboard. Can take a few minutes with many survivors."""
    from research import challenge
    return challenge.combine(programs, gauntlet_ids, max_sleeves, max_corr, progress=lambda *_: None)


@mcp.tool()
def firm_costs(symbol: str) -> dict:
    """What trading a BlackBull symbol costs at each prop firm (config/firmcosts.yaml): whether the
    firm lists it, the spread ratio vs BlackBull and its source, commission, and total round-trip
    cost in BlackBull points (vs BlackBull's own spread)."""
    from research import data, firmcosts
    return firmcosts.describe(symbol, data.spec(symbol))


@mcp.tool()
def record_spread_snapshot(firm: str, spreads: dict[str, float]) -> dict:
    """Record a firm's PUBLISHED live spreads (firm symbol code -> spread in price units, e.g. read
    from ftmo.com/en/symbols or fundednext.com/symbols) against BlackBull's live spreads now.
    Snapshots set each firm's spread ratios in the gauntlet's firm-cost stage."""
    from research import firmcosts
    return firmcosts.record_snapshot(firm, spreads)


@mcp.tool()
def export_calendar() -> dict:
    """Refresh the high-impact news calendar history (used to backtest news blackouts) by running
    QB_ExportCalendar on the tester copy. Takes up to a minute; don't run during MT5 tests."""
    from research import calendar
    return calendar.export()


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
