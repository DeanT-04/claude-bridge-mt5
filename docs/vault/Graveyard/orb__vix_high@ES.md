---
type: strategy
strategy: orb__vix_high@ES
family: opening_range
verdict: graveyard
plan: eod
run_id: 27afbb8b31
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: 790a14f
seed: 11
---
# orb__vix_high@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660}; base sizes (micros)
{'eod': 3, 'intraday': 4}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 1.5075503989919992), 'intraday': (0.0, 0.5, 1.5075503989919992)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 640 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.6470 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -540.9 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0343 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1136 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.3018 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 3.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 15.2 | <= 30 | speed | PASS |

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
| eval_pass | 0.1136 | 0.0692 |
| eval_fail | 0.4200 | 0.4523 |
| eval_expired | 0.4664 | 0.4785 |
| median_sessions_to_pass | 3.0000 | 3.0000 |
| p90_sessions_to_pass | 15.2 | 18.0 |
| first_payout_given_pass | 0.3018 | 0.0583 |
| end_to_end_payout | 0.0343 | 0.0040 |
| mean_payouts_given_pass | 0.3609 | 0.0971 |
| ev_per_attempt | -511.1 | -242.1 |
| ev_p05 | -540.9 | -252.1 |
| ev_p95 | -474.3 | -228.7 |
| max_best_day_share | 1.2895 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 87.5 | 78.3 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 640; total P&L per micro -1,265 USD
- Annualised Sharpe (daily, per micro): -0.20
- PSR (vs 0): 0.311; **Deflated Sharpe: 0.000** over 1425 recorded trials
  (Sharpe variance across trials 1.34e-03)
- Random-entry percentile: 0.647

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0216 | 20 | 12 | (2.0, 0.5, 0.49) | (0.0, 1.0, 0.49) |
| 2020 | {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0295 | 50 | 25 | (0.0, 0.0, 0.62) | (2.0, 0.5, 0.62) |
| 2021 | {'or_min': 30, 'sl_frac': 0.5, 'tp_mult': 1.0, 'last_entry': 660} | 0.0090 | 30 | 8 | (1.0, 0.0, 0.37) | (0.0, 0.0, 0.37) |
| 2022 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0035 | 10 | 6 | (0.5, 1.0, 0.14) | (0.0, 1.0, 0.14) |
| 2023 | {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0249 | 10 | 5 | (0.0, 1.0, 1.86) | (0.0, 1.0, 1.86) |
| 2024 | {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0181 | 4 | 4 | (0.0, 1.0, 1.29) | (0.0, 0.5, 1.29) |
| 2025 | {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0178 | 4 | 4 | (0.0, 1.0, 1.22) | (0.0, 0.5, 1.22) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0556 | 0.0259 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -557.7 | -250.5 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -2.85 USD

## Evidence
![[orb__vix_high@ES-equity.png]]
![[orb__vix_high@ES-fan.png]]
![[orb__vix_high@ES-random.png]]
![[orb__vix_high@ES-drawdown.png]]
![[orb__vix_high@ES-monthly.png]]
![[orb__vix_high@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run orb__vix_high@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
