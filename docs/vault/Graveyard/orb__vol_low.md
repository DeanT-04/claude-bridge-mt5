---
type: strategy
strategy: orb__vol_low
family: opening_range
verdict: graveyard
plan: intraday
run_id: e7d4b19634
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# orb__vol_low: **GRAVEYARD**

Best plan: **Apex intraday 50K**. Final params {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660}; base sizes (micros)
{'eod': 2, 'intraday': 2}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 3.829015539689188), 'intraday': (0.0, 1.0, 3.829015539689188)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 706 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0685 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9900 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -247.5 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0121 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0941 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1286 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 5.5000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 14.1 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1290 | 0.0941 |
| eval_fail | 0.4960 | 0.5833 |
| eval_expired | 0.3750 | 0.3226 |
| median_sessions_to_pass | 4.0000 | 5.5000 |
| p90_sessions_to_pass | 13.0 | 14.1 |
| first_payout_given_pass | 0.0729 | 0.1286 |
| end_to_end_payout | 0.0094 | 0.0121 |
| mean_payouts_given_pass | 0.1354 | 0.2650 |
| ev_per_attempt | -538.7 | -234.6 |
| ev_p05 | -562.8 | -247.5 |
| ev_p95 | -500.5 | -218.5 |
| max_best_day_share | 1.3320 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 135.3 | 212.6 |
| censored_pa | 0 | 23 |

## Statistics
- OOS trades: 706; total P&L per micro 6,982 USD
- Annualised Sharpe (daily, per micro): 0.74
- PSR (vs 0): 0.971; **Deflated Sharpe: 0.069** over 613 recorded trials
  (Sharpe variance across trials 7.17e-04)
- Random-entry percentile: 0.990

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0643 | 40 | 30 | (2.0, 1.0, 0.54) | (1.0, 1.0, 0.54) |
| 2020 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0512 | 15 | 15 | (0.5, 1.0, 0.81) | (0.5, 1.0, 0.81) |
| 2021 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0442 | 20 | 30 | (0.0, 0.5, 1.22) | (0.0, 0.5, 1.22) |
| 2022 | {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0583 | 25 | 25 | (0.5, 1.0, 3.18) | (0.0, 0.0, 3.18) |
| 2023 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0662 | 2 | 2 | (0.0, 1.0, 4.16) | (0.0, 1.0, 4.16) |
| 2024 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0482 | 20 | 2 | (0.0, 0.5, 3.58) | (0.0, 1.0, 3.58) |
| 2025 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0503 | 2 | 2 | (0.0, 1.0, 3.74) | (0.0, 1.0, 3.74) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2778 | 0.1296 |
| end_to_end_payout | 0.0778 | 0.0333 |
| ev_per_attempt | -488.2 | -211.8 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 4.54 USD

## Evidence
![[orb__vol_low-equity.png]]
![[orb__vol_low-fan.png]]
![[orb__vol_low-random.png]]
![[orb__vol_low-drawdown.png]]
![[orb__vol_low-monthly.png]]
![[orb__vol_low-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run orb__vol_low`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
