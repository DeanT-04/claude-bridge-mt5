---
type: strategy
strategy: orb__vol_expanding
family: opening_range
verdict: graveyard
plan: eod
run_id: 8244342c88
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# orb__vol_expanding: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660}; base sizes (micros)
{'eod': 8, 'intraday': 6}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 2.8393177236455025), 'intraday': (0.0, 0.5, 2.8393177236455025)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 757 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0155 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9480 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -521.9 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0477 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2016 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2367 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 3.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 13.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.2016 | 0.1048 |
| eval_fail | 0.7352 | 0.8253 |
| eval_expired | 0.0632 | 0.0699 |
| median_sessions_to_pass | 3.0000 | 5.0000 |
| p90_sessions_to_pass | 13.0 | 16.0 |
| first_payout_given_pass | 0.2367 | 0.1859 |
| end_to_end_payout | 0.0477 | 0.0195 |
| mean_payouts_given_pass | 0.3400 | 0.2500 |
| ev_per_attempt | -476.8 | -219.9 |
| ev_p05 | -521.9 | -239.4 |
| ev_p95 | -419.4 | -195.1 |
| max_best_day_share | 1.3289 | 1.2505 |
| starts | 1488 | 1488 |
| effective_n | 372.0 | 297.6 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 757; total P&L per micro 5,415 USD
- Annualised Sharpe (daily, per micro): 0.50
- PSR (vs 0): 0.903; **Deflated Sharpe: 0.015** over 637 recorded trials
  (Sharpe variance across trials 7.08e-04)
- Random-entry percentile: 0.948

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0133 | 20 | 15 | (0.0, 1.0, 0.35) | (0.0, 1.0, 0.35) |
| 2020 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0231 | 20 | 15 | (0.0, 0.5, 0.61) | (0.0, 1.0, 0.61) |
| 2021 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0072 | 20 | 20 | (0.0, 1.0, 0.41) | (0.0, 0.5, 0.41) |
| 2022 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0333 | 10 | 2 | (0.0, 1.0, 2.42) | (0.5, 1.0, 2.42) |
| 2023 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0258 | 8 | 5 | (0.0, 1.0, 2.21) | (0.0, 0.5, 2.21) |
| 2024 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0260 | 8 | 5 | (0.0, 1.0, 2.26) | (0.0, 0.5, 2.26) |
| 2025 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0272 | 8 | 6 | (0.0, 1.0, 2.45) | (0.0, 0.5, 2.45) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1852 | 0.0667 |
| end_to_end_payout | 0.0000 | 0.0037 |
| ev_per_attempt | -575.7 | -247.4 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 3.95 USD

## Evidence
![[orb__vol_expanding-equity.png]]
![[orb__vol_expanding-fan.png]]
![[orb__vol_expanding-random.png]]
![[orb__vol_expanding-drawdown.png]]
![[orb__vol_expanding-monthly.png]]
![[orb__vol_expanding-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run orb__vol_expanding`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
