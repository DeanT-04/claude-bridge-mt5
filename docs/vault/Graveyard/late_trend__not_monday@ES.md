---
type: strategy
strategy: late_trend__not_monday@ES
family: late_trend
verdict: graveyard
plan: eod
run_id: faa8dc0f0d
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# late_trend__not_monday@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'decide': 840, 'k': 0.5, 'sl_atr': 0.25}; base sizes (micros)
{'eod': 5, 'intraday': 5}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.5, 0.46983074425051286), 'intraday': (0.0, 1.0, 0.46983074425051286)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 520 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.8700 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -537.0 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0363 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1344 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2700 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 9.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 17.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.1344 | 0.0773 |
| eval_fail | 0.3965 | 0.4509 |
| eval_expired | 0.4691 | 0.4718 |
| median_sessions_to_pass | 9.0000 | 9.0000 |
| p90_sessions_to_pass | 17.0 | 17.6 |
| first_payout_given_pass | 0.2700 | 0.3565 |
| end_to_end_payout | 0.0363 | 0.0276 |
| mean_payouts_given_pass | 0.5300 | 0.6435 |
| ev_per_attempt | -459.5 | -165.9 |
| ev_p05 | -537.0 | -226.8 |
| ev_p95 | -352.9 | -82.9 |
| max_best_day_share | 1.1926 | 1.2359 |
| starts | 1488 | 1488 |
| effective_n | 74.4 | 78.3 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 520; total P&L per micro 808 USD
- Annualised Sharpe (daily, per micro): 0.14
- PSR (vs 0): 0.637; **Deflated Sharpe: 0.000** over 1035 recorded trials
  (Sharpe variance across trials 1.07e-03)
- Random-entry percentile: 0.870

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'decide': 840, 'k': 0.8, 'sl_atr': 0.5} | 0.0051 | 25 | 1 | (0.0, 0.5, 0.11) | (0.0, 0.0, 0.11) |
| 2020 | {'decide': 840, 'k': 0.8, 'sl_atr': 0.5} | -0.0094 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | -0.0045 | 12 | 10 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | -0.0006 | 20 | 10 | (1.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | 0.0227 | 3 | 3 | (0.0, 1.0, 1.19) | (0.0, 1.0, 1.19) |
| 2024 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | 0.0205 | 3 | 3 | (0.0, 1.0, 1.09) | (0.0, 1.0, 1.09) |
| 2025 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | 0.0121 | 3 | 3 | (0.0, 1.0, 0.65) | (0.0, 1.0, 0.65) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0963 | 0.0407 |
| end_to_end_payout | 0.0407 | 0.0000 |
| ev_per_attempt | -526.7 | -251.4 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -0.21 USD

## Evidence
![[late_trend__not_monday@ES-equity.png]]
![[late_trend__not_monday@ES-fan.png]]
![[late_trend__not_monday@ES-random.png]]
![[late_trend__not_monday@ES-drawdown.png]]
![[late_trend__not_monday@ES-monthly.png]]
![[late_trend__not_monday@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run late_trend__not_monday@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
