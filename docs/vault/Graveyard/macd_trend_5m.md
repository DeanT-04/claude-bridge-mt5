---
type: strategy
strategy: macd_trend_5m
family: macd_trend
verdict: graveyard
plan: eod
run_id: d94c4a9bf7
data_hash: b6e54fe4873dca2a[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# macd_trend_5m: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'align': True, 'sl_atr': 1.0, 'tp_atr': 4.0}; base sizes (micros)
{'eod': 2, 'intraday': 3}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.5, 3.623663075424371), 'intraday': (1.0, 0.5, 3.623663075424371)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 3039 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0951 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9980 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -471.4 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0517 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1559 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.3319 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 8.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 19.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.1559 | 0.0766 |
| eval_fail | 0.4913 | 0.5894 |
| eval_expired | 0.3528 | 0.3340 |
| median_sessions_to_pass | 8.0000 | 12.0 |
| p90_sessions_to_pass | 19.0 | 20.7 |
| first_payout_given_pass | 0.3319 | 0.5789 |
| end_to_end_payout | 0.0517 | 0.0444 |
| mean_payouts_given_pass | 1.3190 | 2.8947 |
| ev_per_attempt | -171.3 | 109.3 |
| ev_p05 | -471.4 | -165.5 |
| ev_p95 | 201.3 | 446.4 |
| max_best_day_share | 1.3153 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 93.0 | 135.3 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 3,039; total P&L per micro 10,538 USD
- Annualised Sharpe (daily, per micro): 0.78
- PSR (vs 0): 0.978; **Deflated Sharpe: 0.095** over 553 recorded trials
  (Sharpe variance across trials 6.96e-04)
- Random-entry percentile: 0.998

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'align': True, 'sl_atr': 2.0, 'tp_atr': 2.0} | -0.0661 | 6 | 25 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'align': True, 'sl_atr': 1.0, 'tp_atr': 4.0} | -0.0661 | 25 | 60 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'align': True, 'sl_atr': 1.0, 'tp_atr': 4.0} | 0.0044 | 3 | 2 | (0.5, 1.0, 0.32) | (0.0, 1.0, 0.32) |
| 2022 | {'align': True, 'sl_atr': 1.0, 'tp_atr': 4.0} | -0.0168 | 3 | 2 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'align': True, 'sl_atr': 1.0, 'tp_atr': 4.0} | 0.0394 | 2 | 2 | (0.0, 0.5, 4.12) | (0.0, 0.0, 4.12) |
| 2024 | {'align': True, 'sl_atr': 1.0, 'tp_atr': 4.0} | 0.0322 | 2 | 2 | (0.0, 0.5, 3.39) | (0.0, 0.5, 3.39) |
| 2025 | {'align': True, 'sl_atr': 1.0, 'tp_atr': 4.0} | 0.0316 | 2 | 2 | (0.0, 0.5, 3.43) | (0.0, 0.0, 3.43) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0407 | 0.0852 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -555.7 | -254.0 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -4.21 USD

## Evidence
![[macd_trend_5m-equity.png]]
![[macd_trend_5m-fan.png]]
![[macd_trend_5m-random.png]]
![[macd_trend_5m-drawdown.png]]
![[macd_trend_5m-monthly.png]]
![[macd_trend_5m-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run macd_trend_5m`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
