---
type: strategy
strategy: macd_trend_15m
family: macd_trend
verdict: graveyard
plan: eod
run_id: a2fecb5973
data_hash: d223130e354eb243[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# macd_trend_15m: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'align': True, 'sl_atr': 2.0, 'tp_atr': 2.0}; base sizes (micros)
{'eod': 6, 'intraday': 3}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 1.7858276497022472), 'intraday': (0.0, 1.0, 1.7858276497022472)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1251 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0026 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.8140 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -570.8 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0175 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2527 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0691 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 3.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 8.5000 | <= 30 | speed | PASS |

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
| eval_pass | 0.2527 | 0.0981 |
| eval_fail | 0.6445 | 0.8481 |
| eval_expired | 0.1028 | 0.0538 |
| median_sessions_to_pass | 3.0000 | 6.0000 |
| p90_sessions_to_pass | 8.5000 | 16.0 |
| first_payout_given_pass | 0.0691 | 0.0822 |
| end_to_end_payout | 0.0175 | 0.0081 |
| mean_payouts_given_pass | 0.0931 | 0.0959 |
| ev_per_attempt | -554.0 | -245.9 |
| ev_p05 | -570.8 | -252.4 |
| ev_p95 | -533.4 | -237.6 |
| max_best_day_share | 1.3284 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 372.0 | 372.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 1,251; total P&L per micro 2,018 USD
- Annualised Sharpe (daily, per micro): 0.17
- PSR (vs 0): 0.664; **Deflated Sharpe: 0.003** over 521 recorded trials
  (Sharpe variance across trials 6.84e-04)
- Random-entry percentile: 0.814

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'align': True, 'sl_atr': 1.0, 'tp_atr': 4.0} | 0.0442 | 25 | 10 | (2.0, 1.0, 1.96) | (1.0, 1.0, 1.96) |
| 2020 | {'align': True, 'sl_atr': 1.0, 'tp_atr': 4.0} | 0.0248 | 10 | 5 | (1.0, 1.0, 1.06) | (0.0, 1.0, 1.06) |
| 2021 | {'align': True, 'sl_atr': 1.0, 'tp_atr': 4.0} | 0.0207 | 12 | 5 | (1.0, 1.0, 1.22) | (0.0, 1.0, 1.22) |
| 2022 | {'align': True, 'sl_atr': 2.0, 'tp_atr': 4.0} | 0.0333 | 10 | 10 | (0.5, 1.0, 2.74) | (0.5, 1.0, 2.74) |
| 2023 | {'align': True, 'sl_atr': 2.0, 'tp_atr': 4.0} | 0.0204 | 4 | 2 | (0.0, 1.0, 2.05) | (0.0, 1.0, 2.05) |
| 2024 | {'align': True, 'sl_atr': 2.0, 'tp_atr': 4.0} | 0.0271 | 4 | 2 | (0.0, 1.0, 2.76) | (0.0, 1.0, 2.76) |
| 2025 | {'align': True, 'sl_atr': 2.0, 'tp_atr': 4.0} | 0.0240 | 4 | 2 | (0.0, 1.0, 2.55) | (0.0, 1.0, 2.55) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.3259 | 0.0667 |
| end_to_end_payout | 0.0111 | 0.0111 |
| ev_per_attempt | -579.7 | -236.1 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -5.56 USD

## Evidence
![[macd_trend_15m-equity.png]]
![[macd_trend_15m-fan.png]]
![[macd_trend_15m-random.png]]
![[macd_trend_15m-drawdown.png]]
![[macd_trend_15m-monthly.png]]
![[macd_trend_15m-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run macd_trend_15m`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
