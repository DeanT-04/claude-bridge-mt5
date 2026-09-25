---
type: strategy
strategy: orb__trend_down
family: opening_range
verdict: graveyard
plan: intraday
run_id: b289a148e7
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# orb__trend_down: **GRAVEYARD**

Best plan: **Apex intraday 50K**. Final params {'or_min': 30, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660}; base sizes (micros)
{'eod': 3, 'intraday': 3}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.5, 3.461198236035286), 'intraday': (0.0, 0.0, 3.461198236035286)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 471 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0162 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9450 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -228.8 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0168 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0612 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2747 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 7.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 19.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.0921 | 0.0612 |
| eval_fail | 0.3407 | 0.4106 |
| eval_expired | 0.5672 | 0.5282 |
| median_sessions_to_pass | 7.0000 | 7.0000 |
| p90_sessions_to_pass | 18.4 | 19.0 |
| first_payout_given_pass | 0.1387 | 0.2747 |
| end_to_end_payout | 0.0128 | 0.0168 |
| mean_payouts_given_pass | 0.1825 | 0.8791 |
| ev_per_attempt | -537.6 | -141.9 |
| ev_p05 | -559.5 | -228.8 |
| ev_p95 | -509.7 | -16.3 |
| max_best_day_share | 1.3149 | 1.1709 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 74.4 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 471; total P&L per micro 5,906 USD
- Annualised Sharpe (daily, per micro): 0.50
- PSR (vs 0): 0.903; **Deflated Sharpe: 0.016** over 637 recorded trials
  (Sharpe variance across trials 7.08e-04)
- Random-entry percentile: 0.945

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0028 | 30 | 12 | (2.0, 1.0, 0.13) | (2.0, 1.0, 0.13) |
| 2020 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0290 | 30 | 30 | (2.0, 1.0, 1.4) | (2.0, 0.0, 1.4) |
| 2021 | {'or_min': 30, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0063 | 12 | 20 | (0.0, 1.0, 0.34) | (0.0, 0.5, 0.34) |
| 2022 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0032 | 20 | 12 | (0.5, 1.0, 0.16) | (0.0, 0.0, 0.16) |
| 2023 | {'or_min': 30, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0313 | 4 | 3 | (0.5, 0.0, 3.04) | (0.0, 0.0, 3.04) |
| 2024 | {'or_min': 30, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0329 | 4 | 3 | (0.5, 0.0, 3.16) | (0.0, 0.0, 3.16) |
| 2025 | {'or_min': 30, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0371 | 3 | 3 | (0.0, 0.5, 3.54) | (0.0, 0.0, 3.54) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1704 | 0.0185 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -573.7 | -250.1 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -3.10 USD

## Evidence
![[orb__trend_down-equity.png]]
![[orb__trend_down-fan.png]]
![[orb__trend_down-random.png]]
![[orb__trend_down-drawdown.png]]
![[orb__trend_down-monthly.png]]
![[orb__trend_down-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run orb__trend_down`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
