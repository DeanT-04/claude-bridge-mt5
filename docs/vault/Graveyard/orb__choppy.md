---
type: strategy
strategy: orb__choppy
family: opening_range
verdict: graveyard
plan: eod
run_id: 4a97c6f8d0
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# orb__choppy: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'or_min': 30, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660}; base sizes (micros)
{'eod': 3, 'intraday': 2}; sizing policy (alpha, beta, mu) {'eod': (1.0, 1.0, 6.716477530449392), 'intraday': (1.0, 1.0, 6.716477530449392)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 743 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0497 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9880 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -425.6 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.1062 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1989 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.5338 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 5.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 16.0 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- Holdout consistent
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1989 | 0.1163 |
| eval_fail | 0.5894 | 0.7675 |
| eval_expired | 0.2117 | 0.1163 |
| median_sessions_to_pass | 5.0000 | 5.0000 |
| p90_sessions_to_pass | 16.0 | 16.0 |
| first_payout_given_pass | 0.5338 | 0.4104 |
| end_to_end_payout | 0.1062 | 0.0477 |
| mean_payouts_given_pass | 0.9541 | 0.7168 |
| ev_per_attempt | -323.3 | -118.6 |
| ev_p05 | -425.6 | -214.7 |
| ev_p95 | -196.2 | 9.1862 |
| max_best_day_share | 1.3259 | 1.2109 |
| starts | 1488 | 1488 |
| effective_n | 212.6 | 372.0 |
| censored_pa | 13 | 0 |

## Statistics
- OOS trades: 743; total P&L per micro 7,706 USD
- Annualised Sharpe (daily, per micro): 0.68
- PSR (vs 0): 0.964; **Deflated Sharpe: 0.050** over 589 recorded trials
  (Sharpe variance across trials 7.05e-04)
- Random-entry percentile: 0.988

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0415 | 15 | 20 | (0.0, 1.0, 1.48) | (0.0, 0.5, 1.48) |
| 2020 | {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0374 | 20 | 8 | (0.0, 1.0, 1.73) | (0.0, 1.0, 1.73) |
| 2021 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0336 | 15 | 20 | (0.0, 1.0, 1.82) | (0.0, 0.5, 1.82) |
| 2022 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0498 | 25 | 25 | (1.0, 1.0, 3.3) | (1.0, 0.0, 3.3) |
| 2023 | {'or_min': 30, 'sl_frac': 0.5, 'tp_mult': 1.0, 'last_entry': 660} | 0.0529 | 2 | 2 | (0.5, 1.0, 3.92) | (0.5, 1.0, 3.92) |
| 2024 | {'or_min': 30, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0551 | 2 | 2 | (1.0, 1.0, 4.97) | (0.0, 1.0, 4.97) |
| 2025 | {'or_min': 30, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0645 | 3 | 3 | (1.0, 1.0, 6.2) | (1.0, 1.0, 6.2) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1889 | 0.0630 |
| end_to_end_payout | 0.0000 | 0.0037 |
| ev_per_attempt | -576.3 | -250.8 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -3.83 USD

## Evidence
![[orb__choppy-equity.png]]
![[orb__choppy-fan.png]]
![[orb__choppy-random.png]]
![[orb__choppy-drawdown.png]]
![[orb__choppy-monthly.png]]
![[orb__choppy-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run orb__choppy`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
