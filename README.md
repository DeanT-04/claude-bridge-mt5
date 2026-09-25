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
| P1 | Data: Dukascopy proxy bars, yfinance futures, tracking report | 🔄 code done; 2012→now download running |
| P2 | Apex rules, verified and tested | ✅ done |
| P3 | numba backtest engine plus anti-cheating tests | — |
| P4 | Gauntlet, challenge Monte Carlo, visual reports | — |
| P5 | Autonomous research ingestion | — |
| P6 | Strategy factory | — |
| P7 | Portfolios, then FTMO and Blueberry | — |

## Promotion gates
All gates are measured out-of-sample, across at least 1,000 challenge simulations that each start on a random date. The headline gate is an **end-to-end payout rate of at least 60%**: one purchased evaluation leading to at least one payout. The other gates: evaluation pass rate ≥ 85%, first payout once funded ≥ 70%, median days to pass ≤ 15, expected profit after fees above zero even at the 5th percentile, Deflated Sharpe > 0.95, beating 95% of random-entry runs, and a holdout result that doesn't contradict the rest. The details are in `docs/PLAN.md`.

## Findings so far
- **Free data works.** Dukascopy's keyless chart feed has 1-minute NASDAQ-100 and S&P 500 CFD bid/ask bars from 2012-01-19. It trades 18:00–16:15 ET, so it has no bars 16:15–17:00 ET. Yahoo supplies real CME futures bars for comparison: 1m for 8 days, 5m for 60 days, 1h for about 2 years.
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
```

Environment overrides: `PROPQUANT_VAULT` (vault path), `PROPQUANT_DATA` (data directory; default `data/`, gitignored).
