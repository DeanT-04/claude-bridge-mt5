# claude-bridge-mt5

Claude ↔ BlackBull Markets MT5 bridge for a full quant workflow: screen → optimise →
validate (gauntlet) → confirm in the MT5 Strategy Tester → approval-gated demo deployment
→ (when ready) promote to live.

## Status
| Milestone | Scope | State |
|---|---|---|
| M1 | Bridge, tester automation, research engine, gauntlet, MT5 parity | ✅ done |
| M2 | Symbol auto-discovery + cost filter, 7 strategy families, research queue | 🔨 in progress |
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
- `research/`: fast Python engine, MT5-exact indicators, strategy twins, gauntlet, Monte Carlo,
  sizing, benchmarks, MT5 confirm, symbol universe (`universe.py`), job queue (`jobqueue.py`)
- `mql5/`: QB framework (`Include/QB`, including `Signals.mqh`) and EAs (`Experts/QB`:
  `QB_Rules` runs every rule family; `QB_Donchian` is the original standalone)
- `registry/`: SQLite schema/API (trials, runs, gauntlet verdicts, holdout usage, universe, jobs)
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
  `run_gauntlet`, `universe`, `scan_universe`, `enqueue_research`, `start_research`,
  `research_status`, `research_survivors`, `list_gauntlets`, `get_gauntlet`. None of them place orders.
- Research CLI:
  ```
  python scripts/research.py scan                     # discover + filter all broker symbols
  python scripts/research.py enqueue --families all --symbols small --tf H1,M30
  python scripts/research.py run --procs 3            # parallel gauntlets, then MT5 confirm
  python scripts/research.py status | survivors
  ```
  `--symbols` takes `small` (fits £100), `researchable`, `core` or a comma list.
- Single gauntlet: `python scripts/run_gauntlet.py <family> XAUUSD H1 [--mt5]`
- Parity check: `python scripts/parity_check.py XAUUSD H1 2024-01-01 2024-07-01 [families]`
- Tests: `python -m pytest`

## Strategy families
All share the same execution: entry at the bar open on a closed-bar signal, ATR stop and target,
time exit and a session filter.

| Family | Signal | Parity vs MT5 (XAUUSD H1, H1 2024) |
|---|---|---|
| `donchian` | close breaks the N-bar channel | 99.5% |
| `ema_pullback` | trend by fast/slow EMA; bar tags the fast EMA and closes back with the trend | 98.5% |
| `rsi_reversion` | RSI crosses back out of oversold/overbought | 98.7% |
| `bb_reversion` | close re-enters the Bollinger band | 99.3% |
| `orb` | close crosses today's opening range (server hours) | 99.3% |
| `keltner` | close crosses EMA ± k·ATR | 100% |
| `hour_momentum` | at a fixed hour, trade the direction of the last N bars | 100% |

## Symbol universe
`research/universe.py` scans every tradable non-equity symbol (equities optional) and records
history depth, `cost_atr` (median spread ÷ median H1 ATR) and `minlot_risk_pct` (the % of £100
lost by the minimum lot at a 1.5×ATR stop). **Researchable** means cost_atr ≤ 0.15 and ≥ 3 years
of history. **Small-account** additionally means the minimum lot fits the 5% risk cap.

## The gauntlet (gate to demo)
Pre-screen (150 random configs; the best must reach Sharpe 0.5, or the job stops early) →
walk-forward (in-sample/out-of-sample months: M15 12/3, M30 18/4, H1 24/6) → plateau/neighbourhood
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
- **Broker history understates spreads.** BTCUSD records a spread of 0 on 57% of H1 bars
  (live: 1300 pts), and XAUUSD history shows 12 pts against 22 live. Research therefore charges
  each bar max(history spread, live spread). Parity checks keep the raw spreads so they compare
  like with like against MT5's tester.
- Universe (2026-09-24): 197 non-equity symbols scanned, 56 researchable, 41 fit £100 (25 FX,
  8 crypto, 6 indices, Brent, WTI). Gold, silver, NAS100, US30, JPN225 and BTCUSD are researchable
  but larger/prop account only (min lot risks 6–20% of £100).
- First queue test (all 7 families on XAUUSD H1): all failed. Keltner came closest (OOS Sharpe 0.12).
- MT5 build 6182 starts its own built-in MCP server (127.0.0.1:22346); to be explored.
