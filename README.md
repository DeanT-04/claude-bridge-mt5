# claude-bridge-mt5

A Claude ↔ MetaTrader 5 bridge and research pipeline for **passing prop-firm challenges**:
discover symbols → generate and validate strategies (walk-forward gauntlet) → rank them against
every firm's challenge rules → confirm in the MT5 Strategy Tester → forward-test on demo → run the
challenge with an EA that enforces the firm's rules itself.

Market data comes from BlackBull Markets MT5 (a proxy for each firm's feed). Scope today: 1-step
and 2-step evaluations at FTMO, FundedNext, FundingPips, The5ers and FXIFY, in every account size
they offer. The roadmap is in [docs/PLAN.md](docs/PLAN.md).

## Prop programs modelled
`config/propfirms.yaml`. Every rule and fee was re-verified on the firms' own pages on 2026-09-25
(P2). **Re-verify on the firm's site before buying.**

| Program key | Firm | Targets | Daily loss | Max loss | Other rules | Sizes (fee) |
|---|---|---|---|---|---|---|
| `ftmo_2step` | FTMO | 10% → 5% | 5% of initial (balance) | 10% static | 4 min days | 10K–200K (€89–€1,080) |
| `ftmo_1step` | FTMO | 10% | 3% of initial (balance) | 10% trailing end-of-day balance | best day ≤ 50% | 10K–200K (€79–€999) |
| `fundednext_stellar_2step` | FundedNext | 8% → 5% | 5% of initial | 10% static | 5 min days; **EAs ≤ 25K, paid add-on** | 6K–200K ($49.99–$1,049.99) |
| `fundednext_stellar_1step` | FundedNext | 10% | 3% of initial | 6% static | 2 min days; **EAs ≤ 25K, paid add-on** | 6K–200K |
| `fundingpips_2step` | FundingPips | 8% → 5% | 5% of the day's higher bal/eq | 10% static | 3 min days | 5K–100K ($36–$522) |
| `fundingpips_1step_flex` | FundingPips | 12% | 3% of the day's higher bal/eq | 12% static | none | 5K–100K |
| `the5ers_highstakes_2step` | The5ers | 10% → 5% | 5% of the day's higher bal/eq | 10% static | 3 profitable days ≥ 0.5%, news ±2 min | 2.5K–25K ($19–$176) |
| `the5ers_highstakes_2step_large` | The5ers | 10% → 5% | 4% | 8% static | same | 50K, 100K ($249, $405) |
| `the5ers_classic_2step` | The5ers | 8% → 5% | 5% | 10% static | same | 2.5K–25K ($22–$195) |
| `the5ers_classic_2step_large` | The5ers | 8% → 5% | 4% | 8% static | same | 50K, 100K ($279, $455) |
| `fxify_2phase` | FXIFY | 10% → 5% | 4% of initial | 10% trailing closed balance, locks at start | 5 min days; EA pre-approval | 5K–400K ($59–$2,950) |
| `fxify_2phase_classic` | FXIFY | 10% → 5% | 4% | 10% static | 4 min days; EA pre-approval | 5K–100K |
| `fxify_2phase_pro` | FXIFY | 8% → 4% | 4% | 8% static | 3 min days; EA pre-approval | 10K–250K ($129–$1,350) |
| `fxify_1phase` | FXIFY | 10% | 3% | 6% trailing closed balance, locks at start | 5 min days; EA pre-approval | 5K–400K |

`python scripts/research.py programs` lists every size and fee. Rules are percentage-based, so pass
probabilities hold for any size; the size sets the fee. Sizes where a firm bans EAs are listed but
never proposed, ranked or deployed (`ea_max_size`). All five firms were chosen by Trustpilot review
volume; FXIFY replaces The Funded Trader (2.9★). No firm restricts news trading or weekend holds
during evaluation, except The5ers' ±2-minute news window.

**Firm costs** (`config/firmcosts.yaml`, `research/firmcosts.py`). Each firm's commissions and
tradable symbols come from its own pages:

| Firm | FX | Metals | Oil | Indices | Crypto | Symbols listed |
|---|---|---|---|---|---|---|
| FTMO | $5/lot RT | 0.0014% RT | 0 | 0 | 0.065% RT | 85 (public JSON) |
| FundedNext | $5/side | 0.0016%/side | $5/side | 0 | 0.04%/side | 70 |
| FundingPips | $5/lot | $5/lot | 0 | 0 | 0.04% | 41 |
| The5ers | $4/lot RT | $4 (assumed) | spread only | spread only | spread only | not public |
| FXIFY (Raw) | $6/lot RT | $6 | unknown | unknown | unknown | not public |

Spreads are BlackBull's bar spreads × a per-symbol ratio. The ratio comes from snapshots of the
firm's **published live spread table** (FTMO, FundedNext), paired with BlackBull's live spread at the
same moment (`config/spread_snapshots.jsonl`). Firms without a public table use the raw-spread
firms' median per asset class. For symbols the firms don't list publicly, only symbols that two of
the public lists share are used. Round-trip cost vs BlackBull (points; `research.py costs SYMBOL`):
EURUSD 7–11 vs 11, XAUUSD 50–59 vs 22, NAS100 12–21 vs 12, BTCUSD 975–8,983 vs 1,300.

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
python scripts/research.py costs XAUUSD        # per-firm spreads and commissions for a symbol
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
8. **Firm costs and prop gate:** the walk-forward out-of-sample trades are regenerated for each
   firm, with its spreads, commissions and each program's weekend/news rules. A firm must keep a
   profit factor ≥ 1.1 under its own cost stress (1.5× spread plus slippage). Firms that don't
   list the symbol are skipped. Every program is then simulated at its P(pass)-maximising risk. At
   least one program must reach P(pass) ≥ 0.6 **and** beat the same trades with their edge removed
   (de-meaned R) by ≥ 0.2. Luck alone passes 20–33% of challenges. The OOS trades are stored per
   firm variant (`oos_trades` table) for the leaderboard and combiner.
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
- daily limits as a % of the initial balance or of the day's own baseline (FundingPips, The5ers)
- trailing floors on equity, closed balance or the end-of-day balance high (FTMO 1-Step)
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
  basis, daily reference, static/trailing mode, trailing basis and lock
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
`.mcp.json` → `python -m bridge.mcp_server`. 34 tools:
- **data:** `account_info`, `list_symbols`, `symbol_spec`, `get_bars`, `universe`, `scan_universe`
- **tester:** `compile_expert`, `run_backtest`, `run_optimization`
- **research:** `run_gauntlet`, `enqueue_research`, `enqueue_ml`, `start_research`,
  `research_status`, `research_survivors`, `list_gauntlets`, `get_gauntlet`
- **prop:** `prop_profiles`, `prop_simulate`, `prop_rank`, `prop_leaderboard`, `prop_combine`,
  `firm_costs`, `record_spread_snapshot`, `export_calendar`, `prop_preflight`
- **deployment:** `install_host`, `portfolio_allocation`, `propose_deployment`, `apply_deployment`,
  `kill_switch`, `deployment_status`, `forward_test_report`, `promote`

No tool places orders directly.

## Tests
`python -m pytest`: 81 tests (engine and prop execution rules, indicators, families, genetic
operators, stats, tester ini/parsing, deployment, prop simulator and firm rule semantics, firm
costs, gate, leaderboard, combiner, calendar, queue).

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
- **Firm costs differ by asset class.** Raw-spread firms are cheaper than BlackBull's spread-only
  account on FX, but gold costs about twice as much at every firm. Crypto commissions (% of
  notional) make BTC 4–7× dearer at FTMO and FundedNext.
- **Firm rules found in P2.** FundedNext allows EAs only on accounts up to 25K, with a paid add-on.
  FundingPips' news and weekend limits apply only to funded accounts, and its daily limit is a %
  of the day's baseline. FTMO 1-Step trails the end-of-day balance, not equity. The5ers' 50K and
  100K High Stakes accounts have 4%/8% limits. FXIFY needs 5 minimum trading days.
- **P(pass) without edge.** A zero-edge strategy at its best risk passes 20–33% of these
  challenges. That is why the gate also requires lift over the de-meaned baseline.
- **Weekend flat vs early market close.** When a market closes before the flat hour, QB_Host gets
  no tick inside the window and holds over the weekend. The engine flattens at the last bar's
  close, so P4 must make the host do the same.
- **Built-in MCP.** MT5 build 6182 runs its own MCP server (127.0.0.1:22345/22346), not yet explored.
