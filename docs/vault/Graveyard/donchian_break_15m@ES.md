---
type: strategy
strategy: donchian_break_15m@ES
family: donchian_break
verdict: graveyard
plan: eod
run_id: 8c99f5791d
data_hash: c21e6fe846c4f1b4[1029:3800][0:2381]
commit: 15230e7-dirty
seed: 11
---
# donchian_break_15m@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'n': 55, 'sl_atr': 2.0, 'tp_atr': 4.0}; base sizes (micros)
{'eod': 8, 'intraday': 5}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1990 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9260 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -562.3 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0168 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1647 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1020 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 3.0000 | <= 15 | speed | PASS |
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
| eval_pass | 0.1647 | 0.0551 |
| eval_fail | 0.7379 | 0.8501 |
| eval_expired | 0.0974 | 0.0948 |
| median_sessions_to_pass | 3.0000 | 9.5000 |
| p90_sessions_to_pass | 15.6 | 18.0 |
| first_payout_given_pass | 0.1020 | 0.0000 |
| end_to_end_payout | 0.0168 | 0.0000 |
| mean_payouts_given_pass | 0.1020 | 0.0000 |
| ev_per_attempt | -547.7 | -252.3 |
| ev_p05 | -562.3 | -254.1 |
| ev_p95 | -531.4 | -250.8 |
| max_best_day_share | 1.3232 | 1.0455 |
| starts | 1488 | 1488 |
| effective_n | 248.0 | 248.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 1,990; total P&L per micro -1,725 USD
- Annualised Sharpe (daily, per micro): -0.19
- PSR (vs 0): 0.312; **Deflated Sharpe: 0.000** over 717 recorded trials
  (Sharpe variance across trials 8.08e-04)
- Random-entry percentile: 0.926

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'n': 55, 'sl_atr': 1.0, 'tp_atr': 4.0} | -0.0486 | 15 | 12 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'n': 55, 'sl_atr': 1.0, 'tp_atr': 4.0} | -0.0677 | 15 | 12 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'n': 55, 'sl_atr': 2.0, 'tp_atr': 2.0} | -0.0371 | 60 | 50 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'n': 55, 'sl_atr': 2.0, 'tp_atr': 2.0} | -0.0392 | 60 | 50 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'n': 55, 'sl_atr': 2.0, 'tp_atr': 2.0} | -0.0104 | 8 | 8 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2024 | {'n': 55, 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0102 | 8 | 5 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'n': 55, 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0093 | 8 | 5 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2037 | 0.0815 |
| end_to_end_payout | 0.0111 | 0.0000 |
| ev_per_attempt | -555.2 | -253.8 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -1.83 USD

## Evidence
![[donchian_break_15m@ES-equity.png]]
![[donchian_break_15m@ES-fan.png]]
![[donchian_break_15m@ES-random.png]]
![[donchian_break_15m@ES-drawdown.png]]
![[donchian_break_15m@ES-monthly.png]]
![[donchian_break_15m@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run donchian_break_15m@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
