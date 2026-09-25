---
type: strategy
strategy: orb__trending@ES
family: opening_range
verdict: graveyard
plan: intraday
run_id: 220ae25dfd
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: 790a14f
seed: 11
---
# orb__trending@ES: **GRAVEYARD**

Best plan: **Apex intraday 50K**. Final params {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660}; base sizes (micros)
{'eod': 8, 'intraday': 40}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 820 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.4310 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -254.8 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0087 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1089 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0802 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 3.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 10.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.2003 | 0.1089 |
| eval_fail | 0.6949 | 0.8864 |
| eval_expired | 0.1048 | 0.0047 |
| median_sessions_to_pass | 5.0000 | 3.0000 |
| p90_sessions_to_pass | 14.3 | 10.0 |
| first_payout_given_pass | 0.0034 | 0.0802 |
| end_to_end_payout | 0.0007 | 0.0087 |
| mean_payouts_given_pass | 0.0034 | 0.1481 |
| ev_per_attempt | -577.3 | -227.5 |
| ev_p05 | -584.3 | -254.8 |
| ev_p95 | -571.3 | -180.8 |
| max_best_day_share | 1.3291 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 212.6 | 496.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 820; total P&L per micro -3,173 USD
- Annualised Sharpe (daily, per micro): -0.55
- PSR (vs 0): 0.081; **Deflated Sharpe: 0.000** over 1353 recorded trials
  (Sharpe variance across trials 1.30e-03)
- Random-entry percentile: 0.431

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0452 | 40 | 30 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0362 | 40 | 30 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0244 | 30 | 40 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0165 | 30 | 40 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0157 | 30 | 40 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2024 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0235 | 8 | 40 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0140 | 8 | 40 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0185 | 0.0296 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -552.6 | -250.7 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -3.83 USD

## Evidence
![[orb__trending@ES-equity.png]]
![[orb__trending@ES-fan.png]]
![[orb__trending@ES-random.png]]
![[orb__trending@ES-drawdown.png]]
![[orb__trending@ES-monthly.png]]
![[orb__trending@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run orb__trending@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
