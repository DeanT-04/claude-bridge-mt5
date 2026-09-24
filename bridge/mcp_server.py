"""MCP server exposing the BlackBull MT5 research bridge to Claude.

Run: python -m bridge.mcp_server   (registered in .mcp.json)
No tool here can place orders or change a live deployment; that arrives in M3 behind
explicit user approval.
"""
from __future__ import annotations

import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp.server.mcpserver import MCPServer  # noqa: E402

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
def list_gauntlets(limit: int = 20) -> list[dict]:
    """Most recent gauntlet verdicts from the registry."""
    return db.recent_gauntlets(db.connect(), limit)


@mcp.tool()
def get_gauntlet(gauntlet_id: int) -> dict | None:
    """Full stage-by-stage detail of one gauntlet run."""
    return db.gauntlet(db.connect(), gauntlet_id)


if __name__ == "__main__":
    mcp.run()
