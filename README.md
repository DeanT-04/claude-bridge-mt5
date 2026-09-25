# claude-bridge-mt5

A Claude ↔ MetaTrader 5 bridge and research pipeline for **passing prop-firm challenges**:
discover symbols → generate and validate strategies (walk-forward gauntlet) → rank them against
every firm's challenge rules → confirm in the MT5 Strategy Tester → forward-test on demo → run the
challenge with an EA that enforces the firm's rules itself.

Market data comes from BlackBull Markets MT5 (a proxy for each firm's feed). Scope today: 1-step
and 2-step evaluations at FTMO, FundedNext, FundingPips, The5ers and FXIFY, in every account size
they offer. The roadmap is in [docs/PLAN.md](docs/PLAN.md).

## Prop programs modelled
`config/propfirms.yaml` (researched 2026-09-25; **re-verify on the firm's site before buying**):

| Program key | Firm | Targets | Daily loss | Max loss | Other rules | Sizes |
|---|---|---|---|---|---|---|
| `ftmo_2step` | FTMO | 10% → 5% | 5% (balance) | 10% static | 4 min days | 10K–200K |
| `ftmo_1step` | FTMO | 10% | 3% | 10% trailing | best day ≤ 50% | 10K–200K |
| `fundednext_stellar_2step` | FundedNext | 8% → 5% | 5% | 10% static | 5 min days | 6K–200K |
| `fundednext_stellar_1step` | FundedNext | 10% | 3% | 6% static | 2 min days | 6K–200K |
| `fundingpips_2step` | FundingPips | 8% → 5% | 5% (higher of bal/eq) | 10% static | 3 min days, news 5 min, Fri flat | 5K–100K |
| `fundingpips_1step_flex` | FundingPips | 12% | 3% | 12% static | news 5 min, Fri flat | 5K–100K |
| `the5ers_highstakes_2step` | The5ers | 10% → 5% | 5% | 10% static | 3 profitable days ≥ 0.5% | 2.5K–100K |
| `fxify_2phase` | FXIFY | 10% → 5% | 4% | 10% trailing, locks at start | EA approval required | 5K–400K |
| `fxify_1phase` | FXIFY | 10% | 3% | 6% trailing, locks at start | EA approval required | 5K–200K |

Every program lists all its sizes (smallest → largest) with fees where published
(`python scripts/research.py programs`). Rules are percentage-based, so pass probabilities hold for
any size; the size sets the fee and minimum-lot limits. Every firm allows EAs on MT5 with
conditions (in `ea_policy`). All five were chosen by Trustpilot review volume; FXIFY replaces The
Funded Trader (2.9★).

## How it fits together
```
Claude ──MCP──> bridge (Python)
  ├─ data/specs ─────────────> BlackBull terminal (research data, demo forward tests)
  ├─ Strategy Tester ────────> portable tester copy (runtime/tester)
  ├─ research: universe → families / genetic / ML → gauntlet (prop gate) → MT5 confirm
  ├─ challenge selection: leaderboard, challenge-portfolio combiner (walk-forward OOS trades)
  ├─ registry (SQLite): trials, gauntlets, genomes, ML specs, jobs, deployments
  └─ deployment: portfolio_<target>.cfg ──> QB_Host EA in each account's own terminal
```

## Layout
- `bridge/`: MT5 client, compiler, Strategy Tester runner, deployment (`deploy.py`), forward-test
  monitoring and promotion (`monitor.py`), prop preflight, MCP server
- `research/`: execution engine, MT5-exact indicators, strategy families (`strategies/`), gauntlet,
  genetic search, ML (`ml.py`), prop simulator (`propfirm.py`), leaderboard and combiner
  (`challenge.py`), news calendar (`calendar.py`), portfolio, universe, job queue
- `mql5/`: `Include/QB` (signals, risk, execution-with-retry, trade logger, tester score),
  `Experts/QB` (`QB_Rules` runs any strategy in the tester; `QB_Host` trades a portfolio live) and
  `Scripts/QB` (`QB_ExportCalendar` dumps the news calendar history)
- `registry/`: SQLite schema and API
- `config/`: `settings.yaml` (paths, account size, terminals), `gauntlet.yaml` (thresholds),
  `propfirms.yaml` (programs)
- `docs/`: `PLAN.md` (roadmap), `VPS.md` (running prop accounts on a VPS)
- `runtime/`: gitignored tester copy, prop terminals, cache, reports, registry db

## Setup
```
pip install -r requirements.txt
python scripts/setup_terminal.py tester        # portable Strategy Tester copy
runtime\tester\terminal64.exe /portable        # once: log into a BlackBull demo (save password)
python scripts/research.py scan                # symbol universe
python scripts/research.py calendar            # news calendar history (for news-blackout backtests)
```

## Research
```
python scripts/research.py enqueue --families all --symbols researchable --tf H1,M30
python scripts/research.py enqueue --families evolve --symbols core --tf H1     # genetic search
python scripts/research.py ml --symbols core --tf H1 --models logreg,gbm        # ML strategies
python scripts/research.py run --procs 3        # parallel gauntlets, then MT5 confirmation
python scripts/research.py status | survivors
python scripts/research.py gauntlet keltner SPX500 H1 [--mt5]
python scripts/research.py leaderboard [--program ftmo_2step] [--size 50000]
python scripts/research.py combine [--programs ftmo_2step] [--max-sleeves 5]   # challenge portfolios
python scripts/parity_check.py XAUUSD H1 2024-01-01 2024-07-01 [families]
```
`--symbols`: `researchable` (61 symbols: cost ≤ 15% of H1 ATR, ≥ 3 years of history), `core`
(`settings.research.core_symbols`) or a comma list.

**Strategy sources.**
- Seven rule families: `donchian`, `ema_pullback`, `rsi_reversion`, `bb_reversion`, `orb`,
  `keltner` and `hour_momentum`, with 98.5–100% trade parity against MT5.
- **Generated** `gen_<hash>` genomes: a trigger plus up to two filters, evolved on pre-holdout
  data (92.5–100% parity).
- **ML** `ml_<hash>`: 12 features, walk-forward logistic regression or gradient boosting,
  exported to ONNX and run inside MT5 (96.6% parity).

## The gauntlet
1. Pre-screen: 150 random configurations; the best must reach Sharpe 0.5.
2. Walk-forward: in-sample/out-of-sample months of 12/3 on M15, 18/4 on M30 and 24/6 on H1.
3. Stability: the chosen settings must sit on a plateau of their neighbours.
4. Deflated Sharpe, counting every configuration ever tried.
5. Sizing: fractional Kelly with a Monte Carlo drawdown check.
6. Cost stress: 1.5× spread plus slippage.
7. Benchmarks: beat random entries and buy-and-hold.
8. **Prop gate:** every program is simulated on the walk-forward out-of-sample trades at its
   P(pass)-maximising risk. Firms with weekend or news rules get the OOS trades regenerated under
   those rules first. At least one program must reach P(pass) ≥ 0.6 **and** beat the same trades
   with their edge removed (de-meaned R) by ≥ 0.2. Luck alone passes 20–33% of challenges. The
   OOS trades are stored per rule variant (`oos_trades` table) for the leaderboard and combiner.
9. One-shot 12-month holdout.
10. MT5 parity and cost stress in the real Strategy Tester.

Thresholds are in `config/gauntlet.yaml`.

**Prop simulator** (`research/propfirm.py`). It bootstraps real trade days, trade by trade, through
every phase, and models:
- the daily loss basis (balance, equity or the higher of the two)
- static drawdown, trailing drawdown, and trailing that locks at the starting balance
- minimum trading days and minimum profitable days
- the best-day rule
- time limits
- weekend flattening and news blackouts, in the execution engine (the trades themselves change)

It is vectorised over runs × risk levels, and every risk level sees the same bootstrapped days.
The weekend rule mirrors `QB_Host`: no entries from Friday's flat hour until Monday, and a position
is closed at the close of the last bar before the cutoff. The news rule blocks entries within ±N
minutes of a high-impact event for the symbol's base or profit currency. Its calendar history
comes from `QB_ExportCalendar` (Common\Files\QB\calendar_high.csv, server time).

**Challenge selection** (`research/challenge.py`):
- **Leaderboard:** each strategy or portfolio × program × account size, with P(pass), lift over
  luck, best risk, median days, fee and cost per pass.
- **Combiner:** for each program, start from the best survivor, then greedily add the sleeve
  that raises P(pass) most. Candidates whose daily OOS R correlates above 0.5 with a chosen
  sleeve are skipped. Weights are inverse-volatility, and risk is capped so all sleeves open at
  once stay within `max_open_risk_pct`.
- `portfolio_allocation`, `prop_simulate` and `prop_rank` also use the stored OOS trades. They
  fall back to the tuned params only for gauntlets from before P1.

## Running a challenge
Each prop account gets its **own portable terminal** (`terminals.<name>` in `settings.yaml` with
`profile`, `size` and `account_mode`), logged in by you. `QB_Host` trades every approved sleeve
from one chart and enforces, inside the EA:
- the config's account type must match the terminal's
- the firm's daily and total limits, tightened by `prop_safety_buffer` (0.8), with the firm's
  basis and static/trailing mode
- weekend flattening and a high-impact news blackout (MT5 calendar)
- an open-risk cap, a spread filter, and closing positions of removed sleeves
- orders rejected at session open ("Market closed") are retried within the same bar

Flow (MCP):
1. `install_host(target)` → attach `QB_Host` (`InpConfig=portfolio_<target>.cfg`), Algo Trading on.
2. Forward-test on `demo`: `propose_deployment(target='demo', prop_profile=..., prop_size=...)`
   rehearses a program's rules on the BlackBull demo (USD 10,000). Then `forward_test_report`.
3. Add the target to `account.enabled_targets` yourself → `prop_preflight(target)` all OK.
4. `promote(sleeve_ids, target)` → review the diff → **approve in chat** → `apply_deployment`
   (marked destructive, so Claude Code always asks you).
5. `deployment_status`; `kill_switch(target)` stops everything immediately.

Panic stop without Python or Claude:
`powershell -ExecutionPolicy Bypass -File scripts\kill_switch.ps1 <target>`.
Only gauntlet-validated sleeves may go to a prop account; unvalidated sleeves are demo-only.

## MCP server
`.mcp.json` → `python -m bridge.mcp_server`. 32 tools:
- **data:** `account_info`, `list_symbols`, `symbol_spec`, `get_bars`, `universe`, `scan_universe`
- **tester:** `compile_expert`, `run_backtest`, `run_optimization`
- **research:** `run_gauntlet`, `enqueue_research`, `enqueue_ml`, `start_research`,
  `research_status`, `research_survivors`, `list_gauntlets`, `get_gauntlet`
- **prop:** `prop_profiles`, `prop_simulate`, `prop_rank`, `prop_leaderboard`, `prop_combine`,
  `export_calendar`, `prop_preflight`
- **deployment:** `install_host`, `portfolio_allocation`, `propose_deployment`, `apply_deployment`,
  `kill_switch`, `deployment_status`, `forward_test_report`, `promote`

No tool places orders directly.

## Tests
`python -m pytest`: 72 tests (engine and prop execution rules, indicators, families, genetic
operators, stats, tester ini/parsing, deployment, prop simulator, gate, leaderboard, combiner,
calendar, queue).

## Findings and gotchas
- **History understates spreads.** BTCUSD records a spread of 0 on 57% of H1 bars; XAUUSD history
  shows 12 points against 22 live. Research charges max(history, live) spread, and parity checks
  keep the raw spreads.
- **Session-open rejections.** Orders at a session's first bar can be rejected ("Market closed" at
  01:00 server on XAUUSD). `Execution.mqh` retries within the bar.
- **Stale tester inputs.** The MT5 tester reuses the previous run's value for any input left out,
  so `tester.Job` writes every input (defaults parsed from the EA source).
- **Bar limit.** The terminal caps each history request at 100k bars, so `get_bars` pages through
  time. M15 history covers about 3–4 years.
- **Short tester history.** Tester M1 history is short (XAUUSD from 2022-12), so MT5 confirmation
  covers only the last 3 years.
- **First research batch (574 rule-family gauntlets on H1/M30): 0 passes.** The near-misses were
  trend-following on alt-coins, SPX500 and USDJPY. None survived the multiple-testing correction.
- **In-sample optimism.** Tuned-parameter backtests look much better than walk-forward OOS. Since
  P1, prop and portfolio tools use the stored OOS trades.
- **P(pass) without edge.** A zero-edge strategy at its best risk passes 20–33% of these
  challenges. That is why the gate also requires lift over the de-meaned baseline.
- **Weekend flat vs early market close.** When a market closes before the flat hour, QB_Host gets
  no tick inside the window and holds over the weekend. The engine flattens at the last bar's
  close, so P4 must make the host do the same.
- **Built-in MCP.** MT5 build 6182 runs its own MCP server (127.0.0.1:22345/22346), not yet explored.
