# Prop Quant Lab (`propquant`)

A pure-Python research pipeline for prop-firm trading strategies. It collects trading ideas on its own (YouTube transcripts, research papers, strategy sites), turns them into precise strategies, and puts each one through a strict gauntlet. The aim is strategies that **pass prop challenges and reach payouts**, backed by reproducible, visual evidence. It does research only: nothing is deployed and nothing trades live.

- Firms: **Apex Trader Funding** (CME futures) first, then FTMO and Blueberry Funded (CFDs).
- Free and keyless: no API keys and no paid data.
- Knowledge base: an Obsidian vault (`~/Documents/prop-quant-vault`), mirrored to [`docs/vault/`](docs/vault/).
- Full roadmap: [`docs/PLAN.md`](docs/PLAN.md).

The previous MT5 project is archived on the `archive/mt5-bridge` branch.

## Status
| Phase | Scope | State |
|---|---|---|
| P0 | Scaffold, vault skeleton and sync | ✅ done |
| P1 | Data: Dukascopy proxy bars, yfinance futures, tracking report | ✅ NQ done; ES downloading |
| P2 | Apex rules, verified and tested | ✅ done |
| P3 | numba backtest engine plus anti-cheating tests | ✅ done |
| P4 | Gauntlet, challenge Monte Carlo, visual reports | ✅ done |
| P5 | Autonomous research ingestion | next |
| P6 | Strategy factory | — |
| P7 | Portfolios, then FTMO and Blueberry | — |

## Promotion gates
All gates are measured out-of-sample, across at least 1,000 challenge simulations that each start on a random date. The headline gate is an **end-to-end payout rate of at least 60%**: one purchased evaluation leading to at least one payout. The other gates: evaluation pass rate ≥ 85%, first payout once funded ≥ 70%, median days to pass ≤ 15, expected profit after fees above zero even at the 5th percentile, Deflated Sharpe > 0.95, beating 95% of random-entry runs, and a holdout result that doesn't contradict the rest. The details are in `docs/PLAN.md`.

## Findings so far
- **Free data works.** Dukascopy's keyless chart feed has 1-minute NASDAQ-100 and S&P 500 CFD bid/ask bars from 2012-01-19. It trades 18:00–16:15 ET, so it has no bars 16:15–17:00 ET. Yahoo supplies real CME futures bars for comparison: 1m for 8 days, 5m for 60 days, 1h for about 2 years.
- **The proxy tracks real NQ futures almost perfectly.**
  - Bar return correlation: 0.992 (1m), 0.998 (5m), 1.000 (1h).
  - High and low excursions from the open: correlation ≥ 0.98.
  - The high-before-low order inside a bar matches 98.7% of the time.
  - Before 2016 the data has weekend quotes and gaps, so **research starts on 2016-01-01**. That's 10.7 years and 3.4M one-minute bars.
  - Evidence is in `docs/vault/Reports/Proxy-fidelity-NQ.md`.
- **Engine:**
  - A numba bar loop with pessimistic fills: the stop wins when stop and target are both hit in a bar, gaps fill at the open, limit orders must trade through, and targets aren't credited on the entry bar.
  - Known-answer tests, plus property-based **lookahead tests**: changing any future bar never changes past results.
  - Speed on this laptop: about 290 full 10.7-year 1m backtests per minute, and about 60,000 challenge simulations per second.
- **The gauntlet has been checked in both directions.**
  - A random-entry control goes to the Graveyard: it beats only 47% of random-timing runs and has a Deflated Sharpe of 0.
  - On synthetic data with a planted edge, the edge is found (DSR 1.00, beats 100% of random entries). The same strategy with no planted edge is rejected.
  - The holdout can only be opened once per configuration.
- **Calibration against Apex's rules** (see the vault lesson *85 percent pass needs an extreme edge*):
  - An 85% evaluation pass rate needs an annualised Sharpe of about 8 or more, because the 30-day window is the rule that binds.
  - Expected profit per attempt turns positive at a Sharpe of about 2.
- **Apex's rules are verified** from Internet Archive captures of Apex's own help pages (the live site blocks bots). Both plan types, EOD and Intraday trailing, are encoded in `config/firms/apex.yaml`. Each rule cites its source, and every unresolved question is listed in that file. 50K list prices: EOD evaluation $550 plus $139 activation; Intraday evaluation $249 plus $59 activation.
- **The challenge simulator** (`propquant.firms.sim`) runs the evaluation, then the funded account, then payouts. It covers trailing type and lock level, the daily loss limit, the 30-day access window, PA scaling tiers, the 5 qualifying days, 50% consistency, the safety net and the payout caps. Where a bar is ambiguous it assumes the worst case, and each rule has a boundary test.

## Setup
Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run pytest
uv run propquant vault init     # create the vault skeleton (never overwrites)
uv run propquant vault sync     # mirror the vault into docs/vault
uv run propquant data fetch --symbol NQ     # Dukascopy bid+ask 1m, 2012 -> now (resumable)
uv run propquant data build --symbol NQ     # mid bars 1m/5m/15m/1h + data-quality note
uv run propquant data collect --symbol NQ   # real futures bars from Yahoo (run daily)
uv run propquant data tracking --symbol NQ  # proxy-vs-futures fidelity report + charts
uv run propquant firms note apex            # write verified firm rules into the vault
uv run propquant gauntlet run control_random  # full gauntlet + evidence note in the vault
```

Environment overrides: `PROPQUANT_VAULT` (vault path), `PROPQUANT_DATA` (data directory; default `data/`, gitignored).
