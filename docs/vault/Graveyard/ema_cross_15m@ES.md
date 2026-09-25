---
type: strategy
strategy: ema_cross_15m@ES
family: ema_cross
verdict: graveyard
plan: intraday
run_id: 90f0f13a4e
data_hash: c21e6fe846c4f1b4[1029:3800][0:2381]
commit: 15230e7-dirty
seed: 11
---
# ema_cross_15m@ES: **GRAVEYARD**

Best plan: **Apex intraday 50K**. Final params {'pair': (50, 200), 'sl_atr': 1.0, 'tp_atr': 4.0}; base sizes (micros)
{'eod': 20, 'intraday': 10}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 0.7801457507820027), 'intraday': (0.0, 1.0, 0.7801457507820027)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 608 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.0470 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -254.7 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0000 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0659 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0000 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 8.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 16.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.1734 | 0.0659 |
| eval_fail | 0.6371 | 0.7782 |
| eval_expired | 0.1895 | 0.1559 |
| median_sessions_to_pass | 8.0000 | 8.0000 |
| p90_sessions_to_pass | 19.0 | 16.0 |
| first_payout_given_pass | 0.0000 | 0.0000 |
| end_to_end_payout | 0.0000 | 0.0000 |
| mean_payouts_given_pass | 0.0000 | 0.0000 |
| ev_per_attempt | -574.1 | -252.9 |
| ev_p05 | -581.8 | -254.7 |
| ev_p95 | -567.4 | -251.2 |
| max_best_day_share | 1.3248 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 135.3 | 212.6 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 608; total P&L per micro -5,791 USD
- Annualised Sharpe (daily, per micro): -1.08
- PSR (vs 0): 0.002; **Deflated Sharpe: 0.000** over 729 recorded trials
  (Sharpe variance across trials 8.21e-04)
- Random-entry percentile: 0.047

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'pair': (20, 50), 'sl_atr': 2.0, 'tp_atr': 2.0} | 0.0052 | 12 | 15 | (0.0, 0.5, 0.13) | (0.5, 1.0, 0.13) |
| 2020 | {'pair': (9, 21), 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0078 | 12 | 10 | (1.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2021 | {'pair': (50, 200), 'sl_atr': 1.0, 'tp_atr': 4.0} | 0.0145 | 20 | 10 | (0.0, 1.0, 0.35) | (0.0, 1.0, 0.35) |
| 2022 | {'pair': (20, 50), 'sl_atr': 2.0, 'tp_atr': 2.0} | 0.0186 | 12 | 20 | (0.0, 0.5, 0.69) | (0.0, 0.0, 0.69) |
| 2023 | {'pair': (50, 200), 'sl_atr': 1.0, 'tp_atr': 4.0} | 0.0414 | 20 | 10 | (0.0, 1.0, 1.14) | (0.0, 1.0, 1.14) |
| 2024 | {'pair': (50, 200), 'sl_atr': 1.0, 'tp_atr': 4.0} | 0.0402 | 20 | 6 | (0.0, 1.0, 1.1) | (0.0, 1.0, 1.1) |
| 2025 | {'pair': (50, 200), 'sl_atr': 1.0, 'tp_atr': 4.0} | 0.0347 | 20 | 10 | (0.0, 1.0, 0.95) | (0.0, 1.0, 0.95) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1519 | 0.0185 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -571.1 | -250.1 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 0.80 USD

## Evidence
![[ema_cross_15m@ES-equity.png]]
![[ema_cross_15m@ES-fan.png]]
![[ema_cross_15m@ES-random.png]]
![[ema_cross_15m@ES-drawdown.png]]
![[ema_cross_15m@ES-monthly.png]]
![[ema_cross_15m@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ema_cross_15m@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
