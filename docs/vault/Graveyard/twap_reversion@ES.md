---
type: strategy
strategy: twap_reversion@ES
family: twap_reversion
verdict: graveyard
plan: eod
run_id: 682caf4fd4
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: 790a14f
seed: 11
---
# twap_reversion@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'k': 0.5, 'sl_mult': 0.5, 'start': 600}; base sizes (micros)
{'eod': 10, 'intraday': 12}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 842 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.7160 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -562.4 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0047 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0833 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0565 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 7.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 15.0 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- Beats random entry (percentile)
- EV per attempt, 5th pct (USD)
- Holdout consistent
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0833 | 0.0235 |
| eval_fail | 0.5215 | 0.7681 |
| eval_expired | 0.3952 | 0.2083 |
| median_sessions_to_pass | 7.0000 | 4.0000 |
| p90_sessions_to_pass | 15.0 | 7.6000 |
| first_payout_given_pass | 0.0565 | 0.0571 |
| end_to_end_payout | 0.0047 | 0.0013 |
| mean_payouts_given_pass | 0.0565 | 0.0571 |
| ev_per_attempt | -554.5 | -248.4 |
| ev_p05 | -562.4 | -250.9 |
| ev_p95 | -545.2 | -245.0 |
| max_best_day_share | 1.2107 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 93.0 | 248.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 842; total P&L per micro -1,614 USD
- Annualised Sharpe (daily, per micro): -0.27
- PSR (vs 0): 0.248; **Deflated Sharpe: 0.000** over 1445 recorded trials
  (Sharpe variance across trials 1.37e-03)
- Random-entry percentile: 0.716

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'k': 0.5, 'sl_mult': 0.5, 'start': 630} | -0.0590 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'k': 0.5, 'sl_mult': 0.5, 'start': 630} | -0.0490 | 60 | 40 | (2.0, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2021 | {'k': 0.5, 'sl_mult': 0.5, 'start': 630} | -0.0005 | 60 | 40 | (2.0, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2022 | {'k': 0.5, 'sl_mult': 0.5, 'start': 630} | -0.0134 | 60 | 40 | (2.0, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2023 | {'k': 0.5, 'sl_mult': 0.5, 'start': 630} | -0.0063 | 10 | 10 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2024 | {'k': 0.5, 'sl_mult': 0.5, 'start': 630} | -0.0161 | 10 | 10 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'k': 0.5, 'sl_mult': 0.5, 'start': 600} | -0.0231 | 10 | 12 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2778 | 0.1778 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -588.6 | -259.5 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -0.85 USD

## Evidence
![[twap_reversion@ES-equity.png]]
![[twap_reversion@ES-fan.png]]
![[twap_reversion@ES-random.png]]
![[twap_reversion@ES-drawdown.png]]
![[twap_reversion@ES-monthly.png]]
![[twap_reversion@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run twap_reversion@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
