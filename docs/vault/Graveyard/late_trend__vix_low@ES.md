---
type: strategy
strategy: late_trend__vix_low@ES
family: late_trend
verdict: graveyard
plan: intraday
run_id: bc5fdb1b7c
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# late_trend__vix_low@ES: **GRAVEYARD**

Best plan: **Apex intraday 50K**. Final params {'decide': 780, 'k': 0.8, 'sl_atr': 0.25}; base sizes (micros)
{'eod': 1, 'intraday': 1}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 118 | >= 200 | stat | FAIL |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.4490 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -249.0 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0000 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0000 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0000 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | inf | <= 15 | speed | FAIL |
| 90th pct sessions to pass | inf | <= 30 | speed | FAIL |

Failed gates:
- OOS trades
- Deflated Sharpe
- Beats random entry (percentile)
- EV per attempt, 5th pct (USD)
- Holdout consistent
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded
- Median sessions to pass
- 90th pct sessions to pass

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0000 | 0.0000 |
| eval_fail | 0.0000 | 0.0000 |
| eval_expired | 1.0000 | 1.0000 |
| median_sessions_to_pass | inf | inf |
| p90_sessions_to_pass | inf | inf |
| first_payout_given_pass | 0.0000 | 0.0000 |
| end_to_end_payout | 0.0000 | 0.0000 |
| mean_payouts_given_pass | 0.0000 | 0.0000 |
| ev_per_attempt | -550.0 | -249.0 |
| ev_p05 | -550.0 | -249.0 |
| ev_p95 | -550.0 | -249.0 |
| max_best_day_share | 0.0000 | 0.0000 |
| starts | 1488 | 1488 |
| effective_n | 67.6 | 67.6 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 118; total P&L per micro -480 USD
- Annualised Sharpe (daily, per micro): -0.28
- PSR (vs 0): 0.250; **Deflated Sharpe: 0.000** over 1195 recorded trials
  (Sharpe variance across trials 1.10e-03)
- Random-entry percentile: 0.449

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'decide': 780, 'k': 0.8, 'sl_atr': 0.25} | -0.0193 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'decide': 780, 'k': 0.8, 'sl_atr': 0.25} | -0.0083 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'decide': 780, 'k': 0.8, 'sl_atr': 0.25} | -0.0108 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'decide': 780, 'k': 0.8, 'sl_atr': 0.25} | -0.0153 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'decide': 780, 'k': 0.8, 'sl_atr': 0.25} | -0.0141 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2024 | {'decide': 780, 'k': 0.8, 'sl_atr': 0.25} | -0.0186 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'decide': 780, 'k': 0.8, 'sl_atr': 0.25} | -0.0181 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0000 | 0.0000 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -550.0 | -249.0 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -2.58 USD

## Evidence
![[late_trend__vix_low@ES-equity.png]]
![[late_trend__vix_low@ES-fan.png]]
![[late_trend__vix_low@ES-random.png]]
![[late_trend__vix_low@ES-drawdown.png]]
![[late_trend__vix_low@ES-monthly.png]]
![[late_trend__vix_low@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run late_trend__vix_low@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
