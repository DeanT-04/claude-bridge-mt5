# Prop Quant Lab — Full Build Plan

## Context
The MT5 project was archived (branch `archive/mt5-bridge`) and `main` was wiped. We're starting over as a **pure-Python research pipeline** that sources trading ideas on its own, turns them into strategies, and puts them through strict gauntlets. The goal is strategies that pass prop-firm challenges **and** reach payouts, with **real, reproducible, visual evidence**. There's no deployment and no live trading.

Constraints already agreed:
- Python with **uv** (uv 0.12.1 and Python 3.12.4 are installed).
- **No API keys and no spend**, while keeping quality high.
- Laptop only: Ryzen 7 3700U (4 cores, 8 threads), 14 GB RAM.
- Firms: **Apex first (CME futures)**, then FTMO and Blueberry Funded (CFDs).
- Sources: YouTube (discovered autonomously), research papers, oxfordstrat.com, quantifiedstrategies.com.
- Ideas are turned into strategies **by Claude in-session**, not through the API.
- The Obsidian vault at `C:\Users\Deano\Documents\prop-quant-vault` is the knowledge base, mirrored to `docs/vault/`.
- **BIG RULE: no faking anything.**

## Success targets
Everything is measured out-of-sample, across ≥ 1,000 challenge simulations that each start on a random date. Position size is tuned per strategy, in whole micro contracts, to maximise expected profit subject to these gates:

| Gate | Threshold |
|---|---|
| **End-to-end payout rate** (one purchased evaluation → at least one payout) | **≥ 60%** |
| Evaluation pass rate | ≥ 85% |
| First payout, once funded | ≥ 70% |
| Days to pass | median ≤ 15 trading days; 90th percentile ≤ 30 |
| Expected profit per attempt, after all fees | 5th-percentile bootstrap estimate > 0 |
| Statistics | Deflated Sharpe > 0.95; beats 95% of random-entry runs; holdout consistent |

Verdicts:
- **Elite**: passes every gate.
- **Contender**: fails only the speed gates or narrowly misses; kept for combining into portfolios.
- **Graveyard**: everything else, with the reason recorded.

## Stack
All installed with `uv add`:
- Data and speed: `polars`, `numpy`, `numba`, `pyarrow`, `duckdb`, `scipy`
- Config and CLI: `pydantic`, `pyyaml`, `typer`, `rich`
- Search and charts: `optuna`, `matplotlib`
- Fetching: `httpx`, `yfinance`, `yt-dlp`, `youtube-transcript-api`, `trafilatura`, `feedparser`, `pypdf`
- Dev: `pytest`, `hypothesis`, `pytest-xdist`, `ruff`

Tools we don't use: vectorbt and backtrader, because they can't model the order-dependent prop rules correctly and are heavy.

## Repo layout
The package is `propquant`, with a `src/` layout:
```
pyproject.toml, uv.lock, README.md, .gitignore (data/, cache/, .venv/)
config/instruments.yaml        CME specs: tick size, point value, sessions, proxy symbol
config/firms/apex.yaml         every rule, with source_url and verified_on date
src/propquant/
  cli.py                       typer: data | research | gauntlet | report | vault
  instruments.py
  data/      dukascopy.py  yfin.py  bars.py  store.py  tracking.py  calendar.py
  engine/    core.py (numba bar loop)  orders.py  costs.py  sizing.py
  firms/     base.py  apex.py  (later ftmo.py, blueberry.py)
  strategies/ base.py (StrategySpec: pydantic)  registry.py  families/*.py
  gauntlet/  stages.py  walkforward.py  random_entry.py  stats.py (PSR/DSR/bootstrap)
             challenge_mc.py  holdout.py  verdict.py
  reports/   charts.py  report.py
  research/  youtube.py  papers.py  sites.py  inbox.py
  vault/     writer.py  sync.py
  trials.py                    DuckDB trial registry: every attempt counted
tests/  unit/ property/ known_answer/ lookahead/ firms/
data/   (gitignored) parquet: raw/, bars/, yf_forward/
```

## Phases
Each phase ends with passing tests, a README update, and a commit plus push.

### P0: Scaffold
- `uv init --package`: pyproject, ruff config, pytest config, CI-style `uv run pytest` script.
- Create the vault skeleton:
  - `Home.md` dashboard
  - folders: `Ideas/`, `Sources/`, `Strategies/`, `Graveyard/`, `Lessons/`, `Firms/`, `Reports/`, `attachments/`
  - note templates
- `vault sync` mirrors the vault one-way into `docs/vault/`.
- **Exit:** `uv run pytest` is green, and the vault opens in Obsidian (you add it through "Open folder as vault").

### P1: Data layer (free, keyless, measured)
- **Dukascopy** minute candles. Each daily `BID_candles_min_1.bi5` / `ASK_...` file is fetched with httpx, decompressed, and unpacked with numpy.
  - Instruments: USATECH.IDX (NQ proxy), USA500.IDX (ES proxy); later XAU, oil and FX.
  - Range: 2012 to today.
  - Polite rate limit, resumable, content-hashed, stored as Parquet.
  - Bid and ask are both stored, so we get a real spread.
- **Bars**: exchange-time (ET) sessions using the CME calendar (the 17:00–18:00 break, holidays). Build 1m bars and resample to 5m, 15m and 1h. Data-quality checks cover gaps, outliers and flat bars.
- **yfinance** real futures (NQ=F, ES=F): the maximum available 1h (about 2 years) and 5m (60 days) history.
- **Tracking report**, comparing the proxy with real futures:
  - return correlation
  - how often bar highs and lows match
  - range ratio
  - session-open gap behaviour

  The output is an evidence PNG plus a note, `Lessons/Proxy-fidelity.md`. If fidelity is poor for a timeframe, we don't use that timeframe.
- **Forward collector**: `propquant data collect-forward` appends new yfinance bars. Scheduling it daily in Windows Task Scheduler needs your approval at that point.
- **Exit:** 14 years of NQ/ES proxy 1m bars on disk, and the tracking report is written to the vault.

### P2: Firm rules (Apex), verified
- Read Apex's live help pages and record every rule in `apex.yaml` and `Firms/Apex.md`, each with its URL and the date checked. Rules to capture:
  - account sizes, profit target, trailing drawdown type (intraday or end-of-day) and where it locks
  - daily loss limit (if any), contract limits, allowed trading hours and the close-by time
  - evaluation fee or subscription, activation fee, consistency rule
  - minimum trading days, payout rules and caps, safety net
- Build `firms/apex.py` as a numba-compatible state machine covering both stages: evaluation, then funded account (PA) and payouts.
- **Tests**: a hand-built scenario for each rule, showing it triggers exactly at the boundary and not one tick before. Hypothesis property tests check invariants, e.g. the drawdown threshold never moves down.
- **Exit:** a test covers every rule in the YAML.

### P3: Backtest engine
- A numba `@njit` bar loop. It supports market, stop and limit orders, bracket stop-loss and take-profit, and a forced flat time.
- **Pessimistic intrabar fills**: if a stop and a target are both hit in one bar, the stop fills first. Stops get slippage in ticks; limits fill only when price trades through them.
- Costs: Apex/Rithmic commission per side, plus tick slippage by session (wider at the open and around news).
- Prop rules are checked on every bar using intrabar worst-case equity, so a breach happens on the bar where it would really happen.
- Parameter sets run in parallel with `numba.prange` or a 6-worker process pool.
- **Anti-cheating tests**:
  - Lookahead: mutating bars after time *t* never changes signals or fills at or before *t*.
  - Known-answer: synthetic series with hand-computed P&L.
  - Every result is reproducible from the data hash, git commit and seed.
- Speed benchmark: a target of ≥ 200 full 14-year 1m backtests per minute.
- **Exit:** every engine test passes and the benchmark result is recorded.

### P4: Gauntlet, challenge Monte Carlo, visual reports
**Data split**:
- Walk-forward over 2012 to 2025-03.
- **Locked holdout: 2025-03-25 → 2026-09-25**. `holdout.py` logs every time it's opened, and each strategy gets one look.
- **True forward**: yfinance data collected from now on.

**Stages**, cheapest first, so most candidates die early:
1. sanity checks (enough trades, costs survived)
2. random-entry benchmark: 1,000 runs with the same trade count, holding times and sizing
3. anchored walk-forward (optimise with optuna inside each fold; score the next fold)
4. Probabilistic and Deflated Sharpe, using the **total trial count from `trials.py`**
5. size sweep plus challenge Monte Carlo
6. holdout

**Challenge Monte Carlo**:
- Pick a random start date in out-of-sample data and run the evaluation. If it passes, continue into the funded stage on the data that follows, until the first payout or a breach.
- Result distributions: pass rate, days to pass, payout rate, expected profit after fees.
- Start dates overlap, so the effective sample size is reported. A stationary block bootstrap of daily P&L is used as a cross-check.

**Report**: PNGs saved to the vault's `attachments/`. There's one note per strategy, plus `Home.md` with the leaderboard table. Charts:
- equity curve with in-sample, out-of-sample and holdout periods shaded
- where the strategy ranks among the random-entry runs
- a fan chart of Monte Carlo challenge paths with the target and drawdown lines
- a drawdown chart against the trailing threshold
- monthly returns heatmap
- sensitivity to parameter changes

**Exit**:
- A deliberately **no-edge control strategy** gets a **Graveyard** verdict, with a pass rate of about 45%, as theory predicts. This proves the gauntlet isn't rigged to pass things.
- A synthetic series with a planted edge gets detected.

### P5: Research ingestion (autonomous, keyless)
- **YouTube**:
  - search with `yt-dlp` using a query bank (e.g. "NQ opening range breakout backtest", "futures VWAP strategy rules") and dedupe
  - rank by views, likes and channel
  - fetch transcripts with `youtube-transcript-api`
  - stay polite: rate limits and a daily cap
- **Papers**: arXiv API (q-fin.TR, q-fin.ST), OpenAlex and Semantic Scholar keyless endpoints. Download open-access PDFs and extract text with pypdf.
- **Sites**: oxfordstrat.com and quantifiedstrategies.com. Check robots.txt first, crawl politely, and extract article text with trafilatura.
- Everything lands in an inbox (DuckDB plus text cache) with its source metadata, and gets a `Sources/` note containing **our own summary**, not copied text.
- **Exit:** the inbox fills from a single command with no URLs supplied.

### P6: Strategy factory (in-session)
- Loop:
  1. Claude reads the inbox and vault lessons.
  2. Claude writes a pre-registered `Ideas/` note: hypothesis, the market mechanism behind it, exact rules, and the parameter ranges fixed up front.
  3. Claude writes a `StrategySpec` plus family code.
  4. The gauntlet runs.
  5. The verdict note is written and lessons are updated.
- Starter families on NQ/ES:
  - opening-range breakout
  - VWAP reversion
  - overnight gap fill or continuation
  - trend day and initial-balance extension
  - volatility-regime filters
- Claude's own ideas are added once the basics are measured.
- Parameter ranges are kept small, and every trial is counted, to protect against overfitting.
- **Exit:** the first batch of at least 20 families has verdicts and visuals in the vault.

### P7: Portfolios, then the CFD firms
- Combine uncorrelated Contenders, and run the portfolio through the gauntlet as a single strategy.
- Add FTMO and Blueberry Funded:
  - verified rule YAML files and state machines
  - Dukascopy data for their instruments
  - their real spreads and commissions

## Rules enforced in code
- No number reaches a report unless it was produced by a run recorded in `trials.py`, with its data hash, commit and seed.
- The holdout can't be opened without writing a log entry.
- Firm rules without a `source_url` and `verified_on` date fail validation.
- Graveyard notes are mandatory, so failures teach future strategy design.

## Verification (end to end)
1. Environment and tests: `uv sync`, then `uv run pytest -n 6`. All green, covering unit, property, known-answer, lookahead and firm-rule tests.
2. Data: `uv run propquant data fetch --symbol NQ --from 2012`, then `uv run propquant data tracking`. Inspect the tracking PNG.
3. Controls:
   - `uv run propquant gauntlet run control_random` gets a Graveyard verdict, with a pass rate near the theoretical figure.
   - `uv run propquant gauntlet run control_planted_edge` is detected.
4. Real strategy: `uv run propquant gauntlet run orb_nq`. Open its vault note, check the charts, and re-run with the same seed to confirm identical numbers.
5. Backup: `uv run propquant vault sync`. `docs/vault/` matches the vault; commit and push.

## Deferred
- Rename the local folder `mql5-bridge` to `prop-quant-lab`, and move the memory directory along with it.
- Rename the GitHub repo to `prop-quant-lab`. `gh` isn't logged in, so you do it on the web or run `gh auth login`.
