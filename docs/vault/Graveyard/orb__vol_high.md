---
type: strategy
strategy: orb__vol_high
family: opening_range
verdict: graveyard
plan: eod
run_id: 6451139f76
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# orb__vol_high: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'or_min': 30, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660}; base sizes (micros)
{'eod': 2, 'intraday': 2}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 3.7242889542209197), 'intraday': (0.0, 0.5, 3.7242889542209197)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 825 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0038 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9150 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -437.7 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0578 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1526 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.3789 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 2.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 11.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.1526 | 0.0632 |
| eval_fail | 0.4194 | 0.3918 |
| eval_expired | 0.4281 | 0.5450 |
| median_sessions_to_pass | 2.0000 | 2.0000 |
| p90_sessions_to_pass | 11.0 | 18.0 |
| first_payout_given_pass | 0.3789 | 0.3723 |
| end_to_end_payout | 0.0578 | 0.0235 |
| mean_payouts_given_pass | 1.0308 | 0.6915 |
| ev_per_attempt | -296.1 | -180.8 |
| ev_p05 | -437.7 | -234.2 |
| ev_p95 | -123.5 | -105.5 |
| max_best_day_share | 1.4554 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 114.5 | 70.9 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 825; total P&L per micro 5,591 USD
- Annualised Sharpe (daily, per micro): 0.39
- PSR (vs 0): 0.840; **Deflated Sharpe: 0.004** over 685 recorded trials
  (Sharpe variance across trials 8.08e-04)
- Random-entry percentile: 0.915

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | -0.0033 | 1 | 60 | (0.0, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2020 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0114 | 12 | 4 | (0.0, 1.0, 0.68) | (0.0, 1.0, 0.68) |
| 2021 | {'or_min': 30, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0129 | 3 | 4 | (0.0, 1.0, 0.98) | (2.0, 0.5, 0.98) |
| 2022 | {'or_min': 30, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0133 | 4 | 4 | (0.0, 1.0, 1.1) | (0.0, 0.5, 1.1) |
| 2023 | {'or_min': 30, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0256 | 3 | 2 | (0.0, 1.0, 2.74) | (0.0, 0.0, 2.74) |
| 2024 | {'or_min': 30, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0267 | 3 | 2 | (0.0, 1.0, 2.73) | (0.0, 0.0, 2.73) |
| 2025 | {'or_min': 30, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0384 | 2 | 2 | (0.0, 1.0, 4.23) | (0.0, 0.5, 4.23) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1296 | 0.0370 |
| end_to_end_payout | 0.0111 | 0.0000 |
| ev_per_attempt | -553.3 | -251.2 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -15.71 USD

## Evidence
![[orb__vol_high-equity.png]]
![[orb__vol_high-fan.png]]
![[orb__vol_high-random.png]]
![[orb__vol_high-drawdown.png]]
![[orb__vol_high-monthly.png]]
![[orb__vol_high-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run orb__vol_high`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
