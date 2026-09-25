---
type: strategy
strategy: orb__vix_low@ES
family: opening_range
verdict: graveyard
plan: eod
run_id: 34bc3ca4f3
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: 790a14f
seed: 11
---
# orb__vix_low@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660}; base sizes (micros)
{'eod': 30, 'intraday': 12}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 922 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.8420 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -569.9 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0074 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1452 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0509 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 3.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 6.0000 | <= 30 | speed | PASS |

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
| eval_pass | 0.1452 | 0.0921 |
| eval_fail | 0.5692 | 0.6223 |
| eval_expired | 0.2856 | 0.2856 |
| median_sessions_to_pass | 3.0000 | 4.0000 |
| p90_sessions_to_pass | 6.0000 | 8.0000 |
| first_payout_given_pass | 0.0509 | 0.0584 |
| end_to_end_payout | 0.0074 | 0.0054 |
| mean_payouts_given_pass | 0.0509 | 0.0584 |
| ev_per_attempt | -559.1 | -246.4 |
| ev_p05 | -569.9 | -254.6 |
| ev_p95 | -544.6 | -232.8 |
| max_best_day_share | 1.3138 | 1.0064 |
| starts | 1488 | 1488 |
| effective_n | 297.6 | 212.6 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 922; total P&L per micro -1,305 USD
- Annualised Sharpe (daily, per micro): -0.27
- PSR (vs 0): 0.248; **Deflated Sharpe: 0.000** over 1377 recorded trials
  (Sharpe variance across trials 1.34e-03)
- Random-entry percentile: 0.842

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0531 | 30 | 15 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0559 | 30 | 15 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0525 | 30 | 15 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0255 | 30 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0248 | 30 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2024 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0298 | 30 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0198 | 30 | 12 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2259 | 0.1630 |
| end_to_end_payout | 0.0222 | 0.0000 |
| ev_per_attempt | -548.1 | -258.6 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -2.77 USD

## Evidence
![[orb__vix_low@ES-equity.png]]
![[orb__vix_low@ES-fan.png]]
![[orb__vix_low@ES-random.png]]
![[orb__vix_low@ES-drawdown.png]]
![[orb__vix_low@ES-monthly.png]]
![[orb__vix_low@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run orb__vix_low@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
