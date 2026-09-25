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
| P1 | Data: Dukascopy proxy bars, yfinance futures, tracking report | next |
| P2 | Apex rules, verified and tested | — |
| P3 | numba backtest engine plus anti-cheating tests | — |
| P4 | Gauntlet, challenge Monte Carlo, visual reports | — |
| P5 | Autonomous research ingestion | — |
| P6 | Strategy factory | — |
| P7 | Portfolios, then FTMO and Blueberry | — |

## Promotion gates
All gates are measured out-of-sample, across at least 1,000 challenge simulations that each start on a random date. The headline gate is an **end-to-end payout rate of at least 60%**: one purchased evaluation leading to at least one payout. The other gates: evaluation pass rate ≥ 85%, first payout once funded ≥ 70%, median days to pass ≤ 15, expected profit after fees above zero even at the 5th percentile, Deflated Sharpe > 0.95, beating 95% of random-entry runs, and a holdout result that doesn't contradict the rest. The details are in `docs/PLAN.md`.

## Setup
Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run pytest
uv run propquant vault init     # create the vault skeleton (never overwrites)
uv run propquant vault sync     # mirror the vault into docs/vault
```

Environment overrides: `PROPQUANT_VAULT` (vault path), `PROPQUANT_DATA` (data directory; default `data/`, gitignored).
