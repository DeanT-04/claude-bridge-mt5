---
type: strategy
strategy: orb__not_monday@ES
family: opening_range
verdict: graveyard
plan: eod
run_id: d016ccb98f
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# orb__not_monday@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660}; base sizes (micros)
{'eod': 10, 'intraday': 10}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1247 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.7520 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -563.0 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0262 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1781 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1472 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 5.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 15.6 | <= 30 | speed | PASS |

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
| eval_pass | 0.1781 | 0.1022 |
| eval_fail | 0.5853 | 0.8931 |
| eval_expired | 0.2366 | 0.0047 |
| median_sessions_to_pass | 5.0000 | 3.0000 |
| p90_sessions_to_pass | 15.6 | 12.0 |
| first_payout_given_pass | 0.1472 | 0.1118 |
| end_to_end_payout | 0.0262 | 0.0114 |
| mean_payouts_given_pass | 0.1736 | 0.1316 |
| ev_per_attempt | -540.4 | -242.0 |
| ev_p05 | -563.0 | -252.9 |
| ev_p95 | -511.5 | -226.9 |
| max_best_day_share | 1.3296 | 1.2412 |
| starts | 1488 | 1488 |
| effective_n | 186.0 | 496.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 1,247; total P&L per micro -2,803 USD
- Annualised Sharpe (daily, per micro): -0.38
- PSR (vs 0): 0.171; **Deflated Sharpe: 0.000** over 1291 recorded trials
  (Sharpe variance across trials 1.24e-03)
- Random-entry percentile: 0.752

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | -0.0372 | 60 | 60 | (0.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2020 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | -0.0187 | 60 | 10 | (2.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | -0.0341 | 60 | 15 | (2.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0128 | 8 | 60 | (0.5, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2023 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0000 | 5 | 5 | (0.0, 1.0, 0.0) | (0.0, 1.0, 0.0) |
| 2024 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0079 | 8 | 30 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0042 | 3 | 3 | (0.0, 1.0, 0.35) | (0.0, 1.0, 0.35) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2407 | 0.1222 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -583.5 | -256.2 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -3.03 USD

## Evidence
![[orb__not_monday@ES-equity.png]]
![[orb__not_monday@ES-fan.png]]
![[orb__not_monday@ES-random.png]]
![[orb__not_monday@ES-drawdown.png]]
![[orb__not_monday@ES-monthly.png]]
![[orb__not_monday@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run orb__not_monday@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
