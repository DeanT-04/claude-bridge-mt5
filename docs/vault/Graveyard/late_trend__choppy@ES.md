---
type: strategy
strategy: late_trend__choppy@ES
family: late_trend
verdict: graveyard
plan: intraday
run_id: f3be12faeb
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# late_trend__choppy@ES: **GRAVEYARD**

Best plan: **Apex intraday 50K**. Final params {'decide': 840, 'k': 0.3, 'sl_atr': 0.25}; base sizes (micros)
{'eod': 8, 'intraday': 6}; sizing policy (alpha, beta, mu) {'eod': (1.0, 1.0, 0.43519228461588505), 'intraday': (0.5, 1.0, 0.43519228461588505)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 319 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.6910 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -251.3 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0121 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0524 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2308 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 7.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 18.3 | <= 30 | speed | PASS |

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
| eval_pass | 0.1082 | 0.0524 |
| eval_fail | 0.1405 | 0.3696 |
| eval_expired | 0.7513 | 0.5780 |
| median_sessions_to_pass | 8.0000 | 7.0000 |
| p90_sessions_to_pass | 19.0 | 18.3 |
| first_payout_given_pass | 0.0311 | 0.2308 |
| end_to_end_payout | 0.0034 | 0.0121 |
| mean_payouts_given_pass | 0.0314 | 0.2308 |
| ev_per_attempt | -560.0 | -233.9 |
| ev_p05 | -568.2 | -251.3 |
| ev_p95 | -550.8 | -205.6 |
| max_best_day_share | 1.2858 | 1.1835 |
| starts | 1488 | 1488 |
| effective_n | 67.6 | 70.9 |
| censored_pa | 2 | 0 |

## Statistics
- OOS trades: 319; total P&L per micro -349 USD
- Annualised Sharpe (daily, per micro): -0.09
- PSR (vs 0): 0.410; **Deflated Sharpe: 0.000** over 997 recorded trials
  (Sharpe variance across trials 1.08e-03)
- Random-entry percentile: 0.691

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.5} | -0.0373 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'decide': 780, 'k': 0.8, 'sl_atr': 0.5} | -0.0176 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | -0.0042 | 20 | 12 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | -0.0155 | 20 | 12 | (2.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'decide': 840, 'k': 0.3, 'sl_atr': 0.25} | 0.0125 | 8 | 6 | (1.0, 1.0, 0.43) | (0.5, 1.0, 0.43) |
| 2024 | {'decide': 840, 'k': 0.3, 'sl_atr': 0.25} | 0.0144 | 8 | 6 | (1.0, 1.0, 0.48) | (0.5, 1.0, 0.48) |
| 2025 | {'decide': 840, 'k': 0.3, 'sl_atr': 0.25} | 0.0102 | 8 | 6 | (1.0, 1.0, 0.34) | (0.5, 1.0, 0.34) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0296 | 0.0222 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -554.1 | -250.3 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -4.29 USD

## Evidence
![[late_trend__choppy@ES-equity.png]]
![[late_trend__choppy@ES-fan.png]]
![[late_trend__choppy@ES-random.png]]
![[late_trend__choppy@ES-drawdown.png]]
![[late_trend__choppy@ES-monthly.png]]
![[late_trend__choppy@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run late_trend__choppy@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
