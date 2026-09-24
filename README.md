# claude-bridge-mt5

Claude ↔ BlackBull Markets MT5 bridge for a full quant workflow: screen → optimise →
validate (gauntlet) → confirm in the MT5 Strategy Tester → approval-gated demo deployment
→ (when ready) promote to live.

## Status
| Milestone | Scope | State |
|---|---|---|
| M1 | Bridge, tester automation, research engine, gauntlet, MT5 parity | ✅ done |
| M2 | Symbol auto-discovery + cost filter, 6–10 strategy templates, overnight queue | next |
| M3 | Portfolio host EA, approval-gated demo deployment, monitoring, `promote_to_live` | planned |
| M4 | Generated / genetic strategies (grammar → Python + MQL5) | planned |
| M5 | ML strategies (ONNX) | planned |
| M6 | Live readiness + VPS migration | planned |
| M7 | Prop-firm rule profiles | planned |

## Accounts
- **Demo only for now.** Main terminal and tester copy are each logged into a BlackBull demo
  account (main: USD 1000, 1:100).
- Backtests model the **target** account: £100 GBP at 1:100 (`config/settings.yaml`).
- No live account yet. `promote_to_live` (M3) moves approved strategies to live once the user
  has logged into a live account and set `live_enabled: true`. Nothing trades live before then.

## Layout
- `bridge/`: MT5 access (`mt5_client`), MetaEditor compile, Strategy Tester automation, MCP server
- `research/`: fast Python engine, strategy twins, gauntlet, Monte Carlo, sizing, benchmarks, MT5 confirm
- `mql5/`: QB framework (`Include/QB`) and EAs (`Experts/QB`), synced into terminals on compile
- `registry/`: SQLite schema/API (trials, runs, gauntlet verdicts, holdout usage)
- `config/`: `settings.yaml` (paths, target account), `gauntlet.yaml` (pass thresholds)
- `runtime/`: gitignored tester copy, reports, cache and registry db

## Setup
```
pip install -r requirements.txt
python scripts/setup_tester.py          # portable tester copy in runtime/tester
runtime\tester\terminal64.exe /portable # once: log into a BlackBull demo (save password), then close
```

## Use
- MCP server (`.mcp.json`): `python -m bridge.mcp_server`. Tools: `account_info`, `list_symbols`,
  `symbol_spec`, `get_bars`, `compile_expert`, `run_backtest`, `run_optimization`,
  `run_gauntlet`, `list_gauntlets`, `get_gauntlet`. None of them place orders.
- CLI: `python scripts/run_gauntlet.py donchian XAUUSD H1 [--mt5]`
- Tests: `python -m pytest`

## The gauntlet (gate to demo)
Walk-forward (24-month in-sample, 6-month out-of-sample windows) → plateau/neighbourhood
stability → Deflated Sharpe over every configuration ever tried → fractional-Kelly sizing capped
by Monte Carlo drawdown → cost stress (1.5× spread + slippage) → random-entry and buy-and-hold
benchmarks → £100 min-lot feasibility → one-shot 12-month holdout → MT5 parity and cost stress.
Thresholds are in `config/gauntlet.yaml`.

## Conventions
- Each strategy exists as an MQL5 EA and a Python twin, and MT5 parity must hold before a pass.
  (Donchian: 99.5% of trades matched over 3 years, mean R error 0.004.)
- Research is done in R-multiples. Sizing is chosen afterwards.
- The EA refuses a trade whose minimum lot would exceed its risk cap, rather than over-risking.

## Findings / gotchas
- The terminal caps each history request at "Max bars in chart" (100k), so `get_bars` pages
  through time. M15 history is limited to about 3–4 years.
- The tester can't test in GBP here: it needs e.g. `XAUGBP` history, which starts 2026-03.
  Tests run in USD with a deposit equal to £100 at the current rate.
- Tester M1 history is short (XAUUSD from 2022-12), so MT5 confirmation covers only the last 3 years.
- String EA inputs must be written as plain `name=value` in `[TesterInputs]`; the range syntax corrupts them.
- At £100, gold's minimum lot at an ATR stop risks about 10% per trade, so wide-stop gold setups
  only suit a larger or prop account.
- First candidate (Donchian breakout, XAUUSD H1) **failed**. It looked good in-sample
  (Sharpe ≈ 1.0) but had a walk-forward out-of-sample Sharpe of −0.34 and a random-entry p-value of 0.60.
- MT5 build 6182 starts its own built-in MCP server (127.0.0.1:22346); to be explored.
