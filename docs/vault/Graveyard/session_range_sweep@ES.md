---
type: strategy
strategy: session_range_sweep@ES
family: liquidity_sweep
verdict: graveyard
plan: eod
run_id: 0c069dcbeb
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# session_range_sweep@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'range': 'h8', 'target': 'mid'}; base sizes (micros)
{'eod': 30, 'intraday': 40}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1173 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9570 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -566.4 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0175 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1344 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1300 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 5.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 15.0 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1344 | 0.0726 |
| eval_fail | 0.3851 | 0.7661 |
| eval_expired | 0.4805 | 0.1613 |
| median_sessions_to_pass | 5.0000 | 4.0000 |
| p90_sessions_to_pass | 15.0 | 9.0000 |
| first_payout_given_pass | 0.1300 | 0.1019 |
| end_to_end_payout | 0.0175 | 0.0074 |
| mean_payouts_given_pass | 0.1450 | 0.1204 |
| ev_per_attempt | -542.9 | -241.1 |
| ev_p05 | -566.4 | -251.4 |
| ev_p95 | -513.4 | -228.5 |
| max_best_day_share | 1.2975 | 1.2757 |
| starts | 1488 | 1488 |
| effective_n | 74.4 | 297.6 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 1,173; total P&L per micro -2,269 USD
- Annualised Sharpe (daily, per micro): -0.77
- PSR (vs 0): 0.036; **Deflated Sharpe: 0.000** over 1333 recorded trials
  (Sharpe variance across trials 1.28e-03)
- Random-entry percentile: 0.957

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'range': 'premarket', 'target': 'mid'} | -0.1093 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'range': 'premarket', 'target': 'mid'} | -0.1183 | 60 | 60 | (2.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'range': 'premarket', 'target': 'mid'} | -0.0548 | 60 | 60 | (2.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'range': 'premarket', 'target': 'mid'} | -0.0454 | 25 | 20 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'range': 'h8', 'target': 'mid'} | -0.0395 | 30 | 40 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2024 | {'range': 'h8', 'target': 'mid'} | -0.0478 | 30 | 40 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'range': 'h8', 'target': 'mid'} | -0.0521 | 30 | 40 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1667 | 0.0296 |
| end_to_end_payout | 0.0667 | 0.0000 |
| ev_per_attempt | -503.6 | -250.7 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 0.38 USD

## Evidence
![[session_range_sweep@ES-equity.png]]
![[session_range_sweep@ES-fan.png]]
![[session_range_sweep@ES-random.png]]
![[session_range_sweep@ES-drawdown.png]]
![[session_range_sweep@ES-monthly.png]]
![[session_range_sweep@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run session_range_sweep@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
