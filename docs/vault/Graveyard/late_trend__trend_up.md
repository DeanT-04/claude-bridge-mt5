---
type: strategy
strategy: late_trend__trend_up
family: late_trend
verdict: graveyard
plan: eod
run_id: ba2d1ba8a9
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# late_trend__trend_up: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'decide': 780, 'k': 0.5, 'sl_atr': 0.25}; base sizes (micros)
{'eod': 20, 'intraday': 20}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 1.4387325801560944), 'intraday': (0.0, 1.0, 1.4387325801560944)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 369 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0435 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9580 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -551.0 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0457 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2204 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2073 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 6.0000 | <= 15 | speed | PASS |
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
| eval_pass | 0.2204 | 0.0336 |
| eval_fail | 0.6263 | 0.8629 |
| eval_expired | 0.1532 | 0.1035 |
| median_sessions_to_pass | 6.0000 | 3.0000 |
| p90_sessions_to_pass | 16.0 | 7.0000 |
| first_payout_given_pass | 0.2073 | 0.0600 |
| end_to_end_payout | 0.0457 | 0.0020 |
| mean_payouts_given_pass | 0.2195 | 0.0600 |
| ev_per_attempt | -508.4 | -248.3 |
| ev_p05 | -551.0 | -251.4 |
| ev_p95 | -456.4 | -243.7 |
| max_best_day_share | 1.3196 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 186.0 | 372.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 369; total P&L per micro 2,958 USD
- Annualised Sharpe (daily, per micro): 0.56
- PSR (vs 0): 0.929; **Deflated Sharpe: 0.044** over 365 recorded trials
  (Sharpe variance across trials 6.63e-04)
- Random-entry percentile: 0.958

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | 0.0314 | 20 | 20 | (0.0, 1.0, 0.6) | (0.0, 1.0, 0.6) |
| 2020 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | 0.0210 | 20 | 20 | (0.0, 1.0, 0.43) | (0.0, 1.0, 0.43) |
| 2021 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | 0.0474 | 20 | 20 | (0.0, 1.0, 1.57) | (0.0, 1.0, 1.57) |
| 2022 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | 0.0393 | 20 | 20 | (0.0, 1.0, 1.41) | (0.0, 1.0, 1.41) |
| 2023 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | 0.0341 | 20 | 20 | (0.0, 1.0, 1.25) | (0.0, 1.0, 1.25) |
| 2024 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | 0.0357 | 20 | 20 | (0.0, 1.0, 1.38) | (0.0, 1.0, 1.38) |
| 2025 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | 0.0313 | 20 | 20 | (0.0, 1.0, 1.36) | (0.0, 1.0, 1.36) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0519 | 0.0000 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -557.2 | -249.0 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -4.14 USD

## Evidence
![[late_trend__trend_up-equity.png]]
![[late_trend__trend_up-fan.png]]
![[late_trend__trend_up-random.png]]
![[late_trend__trend_up-drawdown.png]]
![[late_trend__trend_up-monthly.png]]
![[late_trend__trend_up-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run late_trend__trend_up`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
