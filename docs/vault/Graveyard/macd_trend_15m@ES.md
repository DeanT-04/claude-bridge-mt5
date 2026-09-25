---
type: strategy
strategy: macd_trend_15m@ES
family: macd_trend
verdict: graveyard
plan: eod
run_id: 93eff60bae
data_hash: c21e6fe846c4f1b4[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# macd_trend_15m@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'align': True, 'sl_atr': 2.0, 'tp_atr': 4.0}; base sizes (micros)
{'eod': 10, 'intraday': 8}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.5, 0.34518420797788835), 'intraday': (0.5, 1.0, 0.34518420797788835)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1190 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9560 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -561.0 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0242 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1949 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1241 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 7.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 16.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.1949 | 0.1129 |
| eval_fail | 0.6082 | 0.6566 |
| eval_expired | 0.1969 | 0.2305 |
| median_sessions_to_pass | 7.0000 | 10.0 |
| p90_sessions_to_pass | 16.0 | 18.0 |
| first_payout_given_pass | 0.1241 | 0.0952 |
| end_to_end_payout | 0.0242 | 0.0108 |
| mean_payouts_given_pass | 0.2034 | 0.0952 |
| ev_per_attempt | -514.3 | -244.1 |
| ev_p05 | -561.0 | -254.2 |
| ev_p95 | -458.1 | -231.4 |
| max_best_day_share | 1.3190 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 186.0 | 124.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 1,190; total P&L per micro 1,065 USD
- Annualised Sharpe (daily, per micro): 0.14
- PSR (vs 0): 0.635; **Deflated Sharpe: 0.000** over 1251 recorded trials
  (Sharpe variance across trials 1.14e-03)
- Random-entry percentile: 0.956

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'align': True, 'sl_atr': 1.0, 'tp_atr': 4.0} | -0.0116 | 10 | 8 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'align': True, 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0315 | 15 | 8 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'align': True, 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0248 | 15 | 8 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'align': True, 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0113 | 15 | 8 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'align': True, 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0039 | 20 | 8 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2024 | {'align': True, 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0017 | 20 | 8 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'align': True, 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0001 | 20 | 8 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2741 | 0.0667 |
| end_to_end_payout | 0.0074 | 0.0000 |
| ev_per_attempt | -551.1 | -252.9 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -6.48 USD

## Evidence
![[macd_trend_15m@ES-equity.png]]
![[macd_trend_15m@ES-fan.png]]
![[macd_trend_15m@ES-random.png]]
![[macd_trend_15m@ES-drawdown.png]]
![[macd_trend_15m@ES-monthly.png]]
![[macd_trend_15m@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run macd_trend_15m@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
