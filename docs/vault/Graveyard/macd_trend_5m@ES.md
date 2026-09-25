---
type: strategy
strategy: macd_trend_5m@ES
family: macd_trend
verdict: graveyard
plan: eod
run_id: d7102c4f8f
data_hash: 2caacdca76e5ba37[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# macd_trend_5m@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'align': True, 'sl_atr': 2.0, 'tp_atr': 2.0}; base sizes (micros)
{'eod': 20, 'intraday': 12}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 2955 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9940 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -544.6 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0316 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1499 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2108 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 3.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 8.0000 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- Holdout consistent
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1499 | 0.0591 |
| eval_fail | 0.5148 | 0.8763 |
| eval_expired | 0.3353 | 0.0645 |
| median_sessions_to_pass | 3.0000 | 2.0000 |
| p90_sessions_to_pass | 8.0000 | 10.0 |
| first_payout_given_pass | 0.2108 | 0.0909 |
| end_to_end_payout | 0.0316 | 0.0054 |
| mean_payouts_given_pass | 0.2735 | 0.1023 |
| ev_per_attempt | -511.1 | -244.0 |
| ev_p05 | -544.6 | -249.8 |
| ev_p95 | -468.6 | -237.2 |
| max_best_day_share | 1.3323 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 248.0 | 744.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 2,955; total P&L per micro -3,044 USD
- Annualised Sharpe (daily, per micro): -0.40
- PSR (vs 0): 0.155; **Deflated Sharpe: 0.000** over 1267 recorded trials
  (Sharpe variance across trials 1.19e-03)
- Random-entry percentile: 0.994

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'align': True, 'sl_atr': 2.0, 'tp_atr': 2.0} | -0.1292 | 1 | 60 | (0.0, 0.0, 0.0) | (2.0, 0.0, 0.0) |
| 2020 | {'align': True, 'sl_atr': 2.0, 'tp_atr': 2.0} | -0.1323 | 1 | 40 | (0.0, 0.0, 0.0) | (2.0, 0.0, 0.0) |
| 2021 | {'align': True, 'sl_atr': 2.0, 'tp_atr': 2.0} | -0.0686 | 50 | 40 | (1.0, 0.0, 0.0) | (2.0, 0.0, 0.0) |
| 2022 | {'align': True, 'sl_atr': 2.0, 'tp_atr': 2.0} | -0.0560 | 50 | 40 | (0.0, 0.0, 0.0) | (2.0, 0.0, 0.0) |
| 2023 | {'align': True, 'sl_atr': 2.0, 'tp_atr': 2.0} | -0.0349 | 20 | 12 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2024 | {'align': True, 'sl_atr': 2.0, 'tp_atr': 2.0} | -0.0410 | 20 | 12 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'align': True, 'sl_atr': 2.0, 'tp_atr': 2.0} | -0.0503 | 20 | 12 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2037 | 0.0815 |
| end_to_end_payout | 0.0259 | 0.0185 |
| ev_per_attempt | -539.4 | -226.0 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -3.01 USD

## Evidence
![[macd_trend_5m@ES-equity.png]]
![[macd_trend_5m@ES-fan.png]]
![[macd_trend_5m@ES-random.png]]
![[macd_trend_5m@ES-drawdown.png]]
![[macd_trend_5m@ES-monthly.png]]
![[macd_trend_5m@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run macd_trend_5m@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
