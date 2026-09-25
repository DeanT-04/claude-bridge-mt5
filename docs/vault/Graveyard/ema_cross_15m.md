---
type: strategy
strategy: ema_cross_15m
family: ema_cross
verdict: graveyard
plan: eod
run_id: 2fecce6428
data_hash: d223130e354eb243[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# ema_cross_15m: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'pair': (50, 200), 'sl_atr': 2.0, 'tp_atr': 4.0}; base sizes (micros)
{'eod': 4, 'intraday': 5}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 2.4377949113390676), 'intraday': (2.0, 1.0, 2.4377949113390676)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 623 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0001 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.5340 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -511.9 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0659 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2137 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.3082 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 5.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 17.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.2137 | 0.0457 |
| eval_fail | 0.6526 | 0.8273 |
| eval_expired | 0.1337 | 0.1270 |
| median_sessions_to_pass | 5.0000 | 5.0000 |
| p90_sessions_to_pass | 17.0 | 11.3 |
| first_payout_given_pass | 0.3082 | 0.0147 |
| end_to_end_payout | 0.0659 | 0.0007 |
| mean_payouts_given_pass | 0.4214 | 0.0441 |
| ev_per_attempt | -456.7 | -247.7 |
| ev_p05 | -511.9 | -252.6 |
| ev_p95 | -391.3 | -239.8 |
| max_best_day_share | 1.3322 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 212.6 | 496.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 623; total P&L per micro -906 USD
- Annualised Sharpe (daily, per micro): -0.10
- PSR (vs 0): 0.397; **Deflated Sharpe: 0.000** over 141 recorded trials
  (Sharpe variance across trials 1.02e-03)
- Random-entry percentile: 0.534

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'pair': (20, 50), 'sl_atr': 1.0, 'tp_atr': 2.0} | 0.0377 | 12 | 12 | (0.0, 1.0, 0.91) | (0.0, 1.0, 0.91) |
| 2020 | {'pair': (20, 50), 'sl_atr': 1.0, 'tp_atr': 2.0} | 0.0065 | 12 | 12 | (0.0, 1.0, 0.16) | (0.0, 1.0, 0.16) |
| 2021 | {'pair': (20, 50), 'sl_atr': 1.0, 'tp_atr': 2.0} | 0.0152 | 12 | 12 | (0.0, 1.0, 0.62) | (0.0, 1.0, 0.62) |
| 2022 | {'pair': (20, 50), 'sl_atr': 2.0, 'tp_atr': 4.0} | 0.0042 | 15 | 10 | (0.0, 0.0, 0.3) | (0.0, 0.0, 0.3) |
| 2023 | {'pair': (50, 200), 'sl_atr': 2.0, 'tp_atr': 4.0} | 0.0411 | 4 | 5 | (0.0, 1.0, 2.11) | (2.0, 1.0, 2.11) |
| 2024 | {'pair': (50, 200), 'sl_atr': 2.0, 'tp_atr': 4.0} | 0.0472 | 4 | 5 | (0.0, 1.0, 2.46) | (2.0, 1.0, 2.46) |
| 2025 | {'pair': (50, 200), 'sl_atr': 2.0, 'tp_atr': 4.0} | 0.0362 | 4 | 5 | (0.0, 1.0, 1.96) | (2.0, 1.0, 1.96) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2519 | 0.0407 |
| end_to_end_payout | 0.1074 | 0.0407 |
| ev_per_attempt | -423.9 | -190.3 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 2.34 USD

## Evidence
![[ema_cross_15m-equity.png]]
![[ema_cross_15m-fan.png]]
![[ema_cross_15m-random.png]]
![[ema_cross_15m-drawdown.png]]
![[ema_cross_15m-monthly.png]]
![[ema_cross_15m-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ema_cross_15m`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
