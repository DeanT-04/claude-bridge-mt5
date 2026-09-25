---
type: strategy
strategy: orb__not_monday
family: opening_range
verdict: graveyard
plan: eod
run_id: 7dabc4840c
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# orb__not_monday: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660}; base sizes (micros)
{'eod': 2, 'intraday': 1}; sizing policy (alpha, beta, mu) {'eod': (1.0, 1.0, 8.234860142797126), 'intraday': (0.0, 1.0, 8.234860142797126)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1259 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.1397 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9990 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -301.7 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0853 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2399 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.3557 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 2.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 9.0000 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2399 | 0.1512 |
| eval_fail | 0.5497 | 0.8353 |
| eval_expired | 0.2103 | 0.0134 |
| median_sessions_to_pass | 2.0000 | 3.0000 |
| p90_sessions_to_pass | 9.0000 | 13.6 |
| first_payout_given_pass | 0.3557 | 0.3911 |
| end_to_end_payout | 0.0853 | 0.0591 |
| mean_payouts_given_pass | 1.2269 | 1.1396 |
| ev_per_attempt | -45.4 | -18.5 |
| ev_p05 | -301.7 | -143.0 |
| ev_p95 | 256.6 | 130.6 |
| max_best_day_share | 1.3223 | 1.2540 |
| starts | 1488 | 1488 |
| effective_n | 372.0 | 744.0 |
| censored_pa | 0 | 3 |

## Statistics
- OOS trades: 1,259; total P&L per micro 13,461 USD
- Annualised Sharpe (daily, per micro): 0.86
- PSR (vs 0): 0.987; **Deflated Sharpe: 0.140** over 501 recorded trials
  (Sharpe variance across trials 6.91e-04)
- Random-entry percentile: 0.999

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | -0.0095 | 1 | 60 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0070 | 6 | 5 | (0.0, 1.0, 0.44) | (0.0, 1.0, 0.44) |
| 2021 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | -0.0075 | 50 | 20 | (2.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2022 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0181 | 4 | 5 | (0.0, 1.0, 1.47) | (0.0, 0.5, 1.47) |
| 2023 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0374 | 6 | 5 | (0.5, 1.0, 3.89) | (0.0, 0.5, 3.89) |
| 2024 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0393 | 2 | 1 | (0.5, 1.0, 5.6) | (0.0, 1.0, 5.6) |
| 2025 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0560 | 2 | 1 | (1.0, 1.0, 8.37) | (0.0, 1.0, 8.37) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2889 | 0.1889 |
| end_to_end_payout | 0.0963 | 0.0593 |
| ev_per_attempt | -512.6 | -217.9 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 2.14 USD

## Evidence
![[orb__not_monday-equity.png]]
![[orb__not_monday-fan.png]]
![[orb__not_monday-random.png]]
![[orb__not_monday-drawdown.png]]
![[orb__not_monday-monthly.png]]
![[orb__not_monday-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run orb__not_monday`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
