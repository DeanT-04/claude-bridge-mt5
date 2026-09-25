---
type: strategy
strategy: ib_breakout__not_monday
family: initial_balance
verdict: graveyard
plan: eod
run_id: 66aad24a9c
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# ib_breakout__not_monday: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'ib_min': 30, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 1.0}; base sizes (micros)
{'eod': 2, 'intraday': 1}; sizing policy (alpha, beta, mu) {'eod': (0.5, 1.0, 7.931023099537989), 'intraday': (0.0, 1.0, 7.931023099537989)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 710 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0032 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.8770 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -556.4 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0302 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1512 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2000 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 7.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 17.0 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- Beats random entry (percentile)
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1512 | 0.1109 |
| eval_fail | 0.5907 | 0.7560 |
| eval_expired | 0.2581 | 0.1331 |
| median_sessions_to_pass | 7.0000 | 7.0000 |
| p90_sessions_to_pass | 17.0 | 18.0 |
| first_payout_given_pass | 0.2000 | 0.1152 |
| end_to_end_payout | 0.0302 | 0.0128 |
| mean_payouts_given_pass | 0.2222 | 0.1455 |
| ev_per_attempt | -534.8 | -235.9 |
| ev_p05 | -556.4 | -250.9 |
| ev_p95 | -507.8 | -216.5 |
| max_best_day_share | 1.3178 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 135.3 | 248.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 710; total P&L per micro 3,487 USD
- Annualised Sharpe (daily, per micro): 0.30
- PSR (vs 0): 0.776; **Deflated Sharpe: 0.003** over 185 recorded trials
  (Sharpe variance across trials 9.75e-04)
- Random-entry percentile: 0.877

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0120 | 25 | 30 | (0.5, 1.0, 0.24) | (0.5, 0.5, 0.24) |
| 2020 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0236 | 25 | 30 | (0.5, 1.0, 0.53) | (0.5, 0.5, 0.53) |
| 2021 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 1.0} | 0.0070 | 25 | 20 | (0.5, 1.0, 0.31) | (0.0, 0.5, 0.31) |
| 2022 | {'ib_min': 60, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 1.0} | 0.0161 | 10 | 10 | (2.0, 1.0, 0.77) | (2.0, 0.5, 0.77) |
| 2023 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0434 | 2 | 2 | (1.0, 1.0, 5.1) | (1.0, 1.0, 5.1) |
| 2024 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0420 | 2 | 2 | (1.0, 1.0, 5.04) | (0.5, 1.0, 5.04) |
| 2025 | {'ib_min': 30, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 1.0} | 0.0531 | 2 | 1 | (0.5, 1.0, 8.05) | (0.0, 1.0, 8.05) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2630 | 0.1852 |
| end_to_end_payout | 0.1333 | 0.0481 |
| ev_per_attempt | -376.8 | -233.9 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 3.51 USD

## Evidence
![[ib_breakout__not_monday-equity.png]]
![[ib_breakout__not_monday-fan.png]]
![[ib_breakout__not_monday-random.png]]
![[ib_breakout__not_monday-drawdown.png]]
![[ib_breakout__not_monday-monthly.png]]
![[ib_breakout__not_monday-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ib_breakout__not_monday`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
