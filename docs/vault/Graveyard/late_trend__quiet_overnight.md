---
type: strategy
strategy: late_trend__quiet_overnight
family: late_trend
verdict: graveyard
plan: eod
run_id: 2e9e4461d2
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# late_trend__quiet_overnight: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'decide': 780, 'k': 0.3, 'sl_atr': 0.25}; base sizes (micros)
{'eod': 8, 'intraday': 12}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 1.5265680282548124), 'intraday': (2.0, 1.0, 1.5265680282548124)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 115 | >= 200 | stat | FAIL |
| Deflated Sharpe | 0.0172 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.8710 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -559.1 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0148 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0739 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2000 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 12.0 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 20.0 | <= 30 | speed | PASS |

Failed gates:
- OOS trades
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
| eval_pass | 0.0739 | 0.0175 |
| eval_fail | 0.2392 | 0.6559 |
| eval_expired | 0.6868 | 0.3266 |
| median_sessions_to_pass | 12.0 | 5.5000 |
| p90_sessions_to_pass | 20.0 | 16.5 |
| first_payout_given_pass | 0.2000 | 0.0000 |
| end_to_end_payout | 0.0148 | 0.0000 |
| mean_payouts_given_pass | 0.2000 | 0.0000 |
| ev_per_attempt | -538.1 | -250.0 |
| ev_p05 | -559.1 | -251.1 |
| ev_p95 | -507.9 | -249.2 |
| max_best_day_share | 1.1719 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 124.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 115; total P&L per micro 1,652 USD
- Annualised Sharpe (daily, per micro): 0.42
- PSR (vs 0): 0.862; **Deflated Sharpe: 0.017** over 421 recorded trials
  (Sharpe variance across trials 6.69e-04)
- Random-entry percentile: 0.871

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | 0.0491 | 25 | 15 | (0.5, 0.5, 1.05) | (0.0, 1.0, 1.05) |
| 2020 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | 0.0355 | 25 | 15 | (0.5, 0.5, 0.67) | (0.0, 1.0, 0.67) |
| 2021 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | 0.0372 | 12 | 12 | (0.0, 1.0, 0.8) | (0.0, 1.0, 0.8) |
| 2022 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.5} | 0.0412 | 12 | 12 | (0.0, 1.0, 0.94) | (0.0, 1.0, 0.94) |
| 2023 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.5} | 0.0521 | 8 | 12 | (1.0, 1.0, 1.76) | (0.0, 1.0, 1.76) |
| 2024 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | 0.0431 | 12 | 15 | (0.0, 1.0, 1.29) | (0.0, 1.0, 1.29) |
| 2025 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0371 | 8 | 12 | (0.0, 1.0, 1.48) | (2.0, 1.0, 1.48) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1333 | 0.0926 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -568.5 | -254.5 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -2.06 USD

## Evidence
![[late_trend__quiet_overnight-equity.png]]
![[late_trend__quiet_overnight-fan.png]]
![[late_trend__quiet_overnight-random.png]]
![[late_trend__quiet_overnight-drawdown.png]]
![[late_trend__quiet_overnight-monthly.png]]
![[late_trend__quiet_overnight-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run late_trend__quiet_overnight`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
