---
type: strategy
strategy: gap_fade
family: gap
verdict: graveyard
plan: eod
run_id: 560d2c5047
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 5455e7a-dirty
seed: 11
---
# gap_fade: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'g_min': 0.0025, 'g_max': 0.006, 'sl_mult': 1.0, 'exit_min': 660}; sizes (micros)
{'eod': 30, 'intraday': 20}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 663 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0145 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9430 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -557.4 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0430 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2829 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1520 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 6.0000 | <= 15 | speed | PASS |
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
| eval_pass | 0.2829 | 0.1452 |
| eval_fail | 0.6257 | 0.7829 |
| eval_expired | 0.0914 | 0.0719 |
| median_sessions_to_pass | 6.0000 | 7.0000 |
| p90_sessions_to_pass | 15.0 | 16.5 |
| first_payout_given_pass | 0.1520 | 0.1528 |
| end_to_end_payout | 0.0430 | 0.0222 |
| mean_payouts_given_pass | 0.2732 | 0.2407 |
| ev_per_attempt | -462.3 | -202.5 |
| ev_p05 | -557.4 | -251.3 |
| ev_p95 | -331.0 | -139.3 |
| max_best_day_share | 1.3319 | 1.3844 |
| starts | 1488 | 1488 |
| effective_n | 212.6 | 248.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 663; total P&L per micro 2,415 USD
- Annualised Sharpe (daily, per micro): 0.41
- PSR (vs 0): 0.855; **Deflated Sharpe: 0.014** over 45 recorded trials
  (Sharpe variance across trials 1.26e-03)
- Random-entry percentile: 0.943

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday |
|---|---|---|---|---|
| 2019 | {'g_min': 0.0025, 'g_max': 0.012, 'sl_mult': 0.5, 'exit_min': 660} | 0.0394 | 12 | 12 |
| 2020 | {'g_min': 0.0025, 'g_max': 0.012, 'sl_mult': 0.5, 'exit_min': 660} | 0.0158 | 15 | 12 |
| 2021 | {'g_min': 0.0025, 'g_max': 0.012, 'sl_mult': 0.5, 'exit_min': 660} | 0.0365 | 15 | 12 |
| 2022 | {'g_min': 0.0025, 'g_max': 0.006, 'sl_mult': 0.5, 'exit_min': 660} | 0.0376 | 30 | 20 |
| 2023 | {'g_min': 0.0025, 'g_max': 0.006, 'sl_mult': 0.5, 'exit_min': 660} | 0.0379 | 30 | 20 |
| 2024 | {'g_min': 0.0025, 'g_max': 0.006, 'sl_mult': 0.5, 'exit_min': 660} | 0.0217 | 30 | 20 |
| 2025 | {'g_min': 0.001, 'g_max': 0.006, 'sl_mult': 1.0, 'exit_min': 660} | 0.0260 | 30 | 25 |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1481 | 0.0259 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -570.6 | -250.5 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -4.39 USD

## Evidence
![[gap_fade-equity.png]]
![[gap_fade-fan.png]]
![[gap_fade-random.png]]
![[gap_fade-drawdown.png]]
![[gap_fade-monthly.png]]
![[gap_fade-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run gap_fade`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
