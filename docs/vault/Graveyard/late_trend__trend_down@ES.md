---
type: strategy
strategy: late_trend__trend_down@ES
family: late_trend
verdict: graveyard
plan: eod
run_id: f94996dc8b
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# late_trend__trend_down@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'decide': 780, 'k': 0.3, 'sl_atr': 0.5}; base sizes (micros)
{'eod': 20, 'intraday': 25}; sizing policy (alpha, beta, mu) {'eod': (0.5, 0.0, 1.5445151346972958), 'intraday': (0.0, 0.0, 1.5445151346972958)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 251 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0014 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9620 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -527.1 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0430 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1203 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.3575 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 9.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 19.0 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1203 | 0.0329 |
| eval_fail | 0.2211 | 0.4765 |
| eval_expired | 0.6586 | 0.4906 |
| median_sessions_to_pass | 9.0000 | 2.0000 |
| p90_sessions_to_pass | 19.0 | 6.0000 |
| first_payout_given_pass | 0.3575 | 0.2857 |
| end_to_end_payout | 0.0430 | 0.0094 |
| mean_payouts_given_pass | 0.5922 | 0.4286 |
| ev_per_attempt | -463.6 | -225.7 |
| ev_p05 | -527.1 | -244.0 |
| ev_p95 | -382.4 | -202.9 |
| max_best_day_share | 1.3130 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 74.4 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 251; total P&L per micro 2,913 USD
- Annualised Sharpe (daily, per micro): 0.55
- PSR (vs 0): 0.922; **Deflated Sharpe: 0.001** over 1079 recorded trials
  (Sharpe variance across trials 1.06e-03)
- Random-entry percentile: 0.962

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | 0.0388 | 10 | 12 | (0.5, 1.0, 0.99) | (0.0, 0.5, 0.99) |
| 2020 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | 0.0283 | 10 | 6 | (0.0, 0.5, 0.67) | (0.0, 1.0, 0.67) |
| 2021 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | 0.0317 | 20 | 25 | (1.0, 0.0, 1.06) | (0.0, 0.0, 1.06) |
| 2022 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | 0.0198 | 10 | 25 | (0.0, 0.5, 0.62) | (0.0, 0.0, 0.62) |
| 2023 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | 0.0416 | 12 | 25 | (2.0, 0.0, 1.86) | (0.0, 0.0, 1.86) |
| 2024 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | 0.0416 | 20 | 25 | (0.5, 0.0, 1.83) | (0.0, 0.0, 1.83) |
| 2025 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | 0.0300 | 20 | 25 | (0.5, 0.0, 1.3) | (0.0, 0.0, 1.3) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0852 | 0.1000 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -561.8 | -254.9 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 7.13 USD

## Evidence
![[late_trend__trend_down@ES-equity.png]]
![[late_trend__trend_down@ES-fan.png]]
![[late_trend__trend_down@ES-random.png]]
![[late_trend__trend_down@ES-drawdown.png]]
![[late_trend__trend_down@ES-monthly.png]]
![[late_trend__trend_down@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run late_trend__trend_down@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
