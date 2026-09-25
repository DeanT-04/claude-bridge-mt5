---
type: strategy
strategy: orb__vix_low
family: opening_range
verdict: graveyard
plan: eod
run_id: 9a85e0e546
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# orb__vix_low: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660}; base sizes (micros)
{'eod': 2, 'intraday': 2}; sizing policy (alpha, beta, mu) {'eod': (0.5, 1.0, 4.509609827803395), 'intraday': (2.0, 1.0, 4.509609827803395)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 955 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0153 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9560 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -547.4 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0336 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1888 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1779 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 3.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 7.0000 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1888 | 0.1028 |
| eval_fail | 0.5013 | 0.6163 |
| eval_expired | 0.3098 | 0.2809 |
| median_sessions_to_pass | 3.0000 | 3.0000 |
| p90_sessions_to_pass | 7.0000 | 6.0000 |
| first_payout_given_pass | 0.1779 | 0.1961 |
| end_to_end_payout | 0.0336 | 0.0202 |
| mean_payouts_given_pass | 0.2527 | 0.2549 |
| ev_per_attempt | -521.6 | -220.8 |
| ev_p05 | -547.4 | -236.6 |
| ev_p95 | -489.8 | -201.7 |
| max_best_day_share | 1.2850 | 1.3221 |
| starts | 1488 | 1488 |
| effective_n | 248.0 | 372.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 955; total P&L per micro 5,082 USD
- Annualised Sharpe (daily, per micro): 0.45
- PSR (vs 0): 0.876; **Deflated Sharpe: 0.015** over 565 recorded trials
  (Sharpe variance across trials 6.99e-04)
- Random-entry percentile: 0.956

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0158 | 10 | 10 | (0.0, 1.0, 0.4) | (0.0, 1.0, 0.4) |
| 2020 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0116 | 40 | 8 | (2.0, 0.0, 0.33) | (0.0, 1.0, 0.33) |
| 2021 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0172 | 20 | 15 | (0.5, 0.0, 0.69) | (0.0, 0.0, 0.69) |
| 2022 | {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0522 | 4 | 3 | (0.0, 1.0, 3.38) | (0.0, 1.0, 3.38) |
| 2023 | {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0319 | 4 | 3 | (0.0, 1.0, 2.07) | (0.0, 1.0, 2.07) |
| 2024 | {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0289 | 4 | 3 | (0.0, 1.0, 2.27) | (0.0, 1.0, 2.27) |
| 2025 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0405 | 2 | 2 | (0.5, 1.0, 4.09) | (2.0, 1.0, 4.09) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2815 | 0.1074 |
| end_to_end_payout | 0.1222 | 0.0370 |
| ev_per_attempt | -342.6 | -179.5 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 1.25 USD

## Evidence
![[orb__vix_low-equity.png]]
![[orb__vix_low-fan.png]]
![[orb__vix_low-random.png]]
![[orb__vix_low-drawdown.png]]
![[orb__vix_low-monthly.png]]
![[orb__vix_low-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run orb__vix_low`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
