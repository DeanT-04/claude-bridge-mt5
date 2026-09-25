---
type: strategy
strategy: ema_cross_5m@ES
family: ema_cross
verdict: graveyard
plan: eod
run_id: 73c92f6025
data_hash: 2caacdca76e5ba37[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# ema_cross_5m@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'pair': (20, 50), 'sl_atr': 2.0, 'tp_atr': 4.0}; base sizes (micros)
{'eod': 15, 'intraday': 12}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.5, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1609 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.3920 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -566.0 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0168 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1539 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1092 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 6.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 14.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.1539 | 0.1035 |
| eval_fail | 0.7863 | 0.8582 |
| eval_expired | 0.0598 | 0.0383 |
| median_sessions_to_pass | 6.0000 | 5.0000 |
| p90_sessions_to_pass | 14.0 | 12.0 |
| first_payout_given_pass | 0.1092 | 0.0909 |
| end_to_end_payout | 0.0168 | 0.0094 |
| mean_payouts_given_pass | 0.2838 | 0.1688 |
| ev_per_attempt | -494.8 | -222.8 |
| ev_p05 | -566.0 | -251.0 |
| ev_p95 | -396.5 | -178.0 |
| max_best_day_share | 1.3306 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 212.6 | 297.6 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 1,609; total P&L per micro -6,539 USD
- Annualised Sharpe (daily, per micro): -0.84
- PSR (vs 0): 0.016; **Deflated Sharpe: 0.000** over 789 recorded trials
  (Sharpe variance across trials 1.06e-03)
- Random-entry percentile: 0.392

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'pair': (20, 50), 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0087 | 20 | 15 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'pair': (20, 50), 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0198 | 15 | 15 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'pair': (20, 50), 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0553 | 15 | 15 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'pair': (20, 50), 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0363 | 15 | 15 | (1.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'pair': (20, 50), 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0427 | 15 | 12 | (0.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2024 | {'pair': (50, 200), 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0422 | 25 | 20 | (0.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2025 | {'pair': (50, 200), 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0329 | 20 | 20 | (0.5, 0.0, 0.0) | (0.5, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1741 | 0.0852 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -574.2 | -254.0 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -2.95 USD

## Evidence
![[ema_cross_5m@ES-equity.png]]
![[ema_cross_5m@ES-fan.png]]
![[ema_cross_5m@ES-random.png]]
![[ema_cross_5m@ES-drawdown.png]]
![[ema_cross_5m@ES-monthly.png]]
![[ema_cross_5m@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ema_cross_5m@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
