# claude-bridge-mt5

Claude ↔ BlackBull Markets MT5 bridge for a full quant workflow: screen → optimise →
validate (gauntlet) → confirm in the MT5 Strategy Tester → (M3) approval-gated demo deployment.

## Layout
- `bridge/` – MT5 access (`mt5_client`), MetaEditor compile, Strategy Tester automation, MCP server
- `research/` – fast Python engine, strategy twins, gauntlet, Monte Carlo, sizing, benchmarks
- `mql5/` – QB framework (`Include/QB`) and EAs (`Experts/QB`); synced into terminals on compile
- `registry/` – SQLite schema/API (trials, runs, gauntlet verdicts, holdout usage)
- `config/` – `settings.yaml` (paths, target account), `gauntlet.yaml` (pass thresholds)
- `runtime/` – gitignored: tester copy, reports, cache, registry db

## Setup
```
pip install -r requirements.txt
python scripts/setup_tester.py          # portable tester copy in runtime/tester
runtime\tester\terminal64.exe /portable # once: log into the BlackBull demo, then close
```

## Use
- MCP server (`.mcp.json`): `python -m bridge.mcp_server`
- CLI: `python scripts/run_gauntlet.py donchian XAUUSD H1 [--mt5]`
- Tests: `python -m pytest`

## Conventions
- Backtests model the target live account: £100 GBP, 1:100 (`settings.yaml`).
- Each strategy exists as an MQL5 EA and a Python twin; MT5 parity must hold before a pass.
- Research is in R-multiples; sizing is chosen afterwards (fractional Kelly capped by Monte Carlo DD).
- No bridge tool places orders.
