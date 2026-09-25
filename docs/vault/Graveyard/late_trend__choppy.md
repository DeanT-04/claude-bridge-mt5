---
type: strategy
strategy: late_trend__choppy
family: late_trend
verdict: graveyard
plan: eod
run_id: 620e2fbbf2
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# late_trend__choppy: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'decide': 780, 'k': 0.3, 'sl_atr': 0.25}; base sizes (micros)
{'eod': 10, 'intraday': 4}; sizing policy (alpha, beta, mu) {'eod': (2.0, 1.0, 3.755488124275973), 'intraday': (1.0, 1.0, 3.755488124275973)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 335 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.1806 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9880 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -451.4 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0706 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2681 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2632 | >= 0.7 | commercial | FAIL |
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
| eval_pass | 0.2681 | 0.1102 |
| eval_fail | 0.3031 | 0.5706 |
| eval_expired | 0.4288 | 0.3192 |
| median_sessions_to_pass | 7.0000 | 6.0000 |
| p90_sessions_to_pass | 16.0 | 15.7 |
| first_payout_given_pass | 0.2632 | 0.3720 |
| end_to_end_payout | 0.0706 | 0.0410 |
| mean_payouts_given_pass | 0.7268 | 1.0000 |
| ev_per_attempt | -237.8 | -70.5 |
| ev_p05 | -451.4 | -184.9 |
| ev_p95 | 20.4 | 63.7 |
| max_best_day_share | 1.3084 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 82.7 | 148.8 |
| censored_pa | 0 | 20 |

## Statistics
- OOS trades: 335; total P&L per micro 5,472 USD
- Annualised Sharpe (daily, per micro): 0.89
- PSR (vs 0): 0.992; **Deflated Sharpe: 0.181** over 421 recorded trials
  (Sharpe variance across trials 6.69e-04)
- Random-entry percentile: 0.988

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'decide': 840, 'k': 0.5, 'sl_atr': 0.25} | 0.0299 | 15 | 30 | (0.0, 1.0, 0.62) | (0.0, 0.5, 0.62) |
| 2020 | {'decide': 840, 'k': 0.8, 'sl_atr': 0.5} | 0.0035 | 25 | 60 | (0.0, 1.0, 0.05) | (0.5, 0.0, 0.05) |
| 2021 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | 0.0410 | 15 | 10 | (2.0, 1.0, 1.24) | (2.0, 1.0, 1.24) |
| 2022 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0458 | 8 | 5 | (0.5, 1.0, 2.09) | (0.0, 1.0, 2.09) |
| 2023 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0776 | 10 | 4 | (2.0, 1.0, 4.47) | (2.0, 1.0, 4.47) |
| 2024 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0718 | 10 | 4 | (2.0, 1.0, 4.11) | (2.0, 1.0, 4.11) |
| 2025 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0610 | 10 | 4 | (2.0, 1.0, 3.57) | (2.0, 1.0, 3.57) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0593 | 0.0296 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -558.2 | -250.7 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -8.99 USD

## Evidence
![[late_trend__choppy-equity.png]]
![[late_trend__choppy-fan.png]]
![[late_trend__choppy-random.png]]
![[late_trend__choppy-drawdown.png]]
![[late_trend__choppy-monthly.png]]
![[late_trend__choppy-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run late_trend__choppy`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
