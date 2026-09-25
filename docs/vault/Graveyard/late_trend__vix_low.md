---
type: strategy
strategy: late_trend__vix_low
family: late_trend
verdict: graveyard
plan: intraday
run_id: a75287eb0a
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# late_trend__vix_low: **GRAVEYARD**

Best plan: **Apex intraday 50K**. Final params {'decide': 780, 'k': 0.5, 'sl_atr': 0.25}; base sizes (micros)
{'eod': 20, 'intraday': 25}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 1.1335548890945288), 'intraday': (0.0, 1.0, 1.1335548890945288)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 240 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0136 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.8610 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -251.1 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0000 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0202 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0000 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 3.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 6.1000 | <= 30 | speed | PASS |

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
| eval_pass | 0.0954 | 0.0202 |
| eval_fail | 0.3394 | 0.4913 |
| eval_expired | 0.5652 | 0.4886 |
| median_sessions_to_pass | 5.0000 | 3.0000 |
| p90_sessions_to_pass | 13.9 | 6.1000 |
| first_payout_given_pass | 0.0000 | 0.0000 |
| end_to_end_payout | 0.0000 | 0.0000 |
| mean_payouts_given_pass | 0.0000 | 0.0000 |
| ev_per_attempt | -563.3 | -250.2 |
| ev_p05 | -568.3 | -251.1 |
| ev_p95 | -558.0 | -249.4 |
| max_best_day_share | 1.3196 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 78.3 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 240; total P&L per micro 1,601 USD
- Annualised Sharpe (daily, per micro): 0.38
- PSR (vs 0): 0.838; **Deflated Sharpe: 0.014** over 409 recorded trials
  (Sharpe variance across trials 6.72e-04)
- Random-entry percentile: 0.861

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'decide': 840, 'k': 0.8, 'sl_atr': 0.25} | 0.0354 | 1 | 1 | (0.0, 0.0, 0.39) | (0.0, 0.0, 0.39) |
| 2020 | {'decide': 840, 'k': 0.8, 'sl_atr': 0.5} | 0.0335 | 20 | 20 | (0.0, 1.0, 0.48) | (0.0, 1.0, 0.48) |
| 2021 | {'decide': 840, 'k': 0.8, 'sl_atr': 0.5} | 0.0254 | 20 | 20 | (0.0, 1.0, 0.35) | (0.0, 1.0, 0.35) |
| 2022 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | 0.0243 | 20 | 25 | (0.0, 1.0, 0.59) | (0.0, 1.0, 0.59) |
| 2023 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | 0.0201 | 20 | 25 | (0.0, 1.0, 0.47) | (0.0, 1.0, 0.47) |
| 2024 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | 0.0302 | 20 | 30 | (0.0, 1.0, 0.89) | (0.5, 1.0, 0.89) |
| 2025 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | 0.0258 | 20 | 25 | (0.0, 1.0, 0.93) | (0.0, 1.0, 0.93) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0519 | 0.0000 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -557.2 | -249.0 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -6.19 USD

## Evidence
![[late_trend__vix_low-equity.png]]
![[late_trend__vix_low-fan.png]]
![[late_trend__vix_low-random.png]]
![[late_trend__vix_low-drawdown.png]]
![[late_trend__vix_low-monthly.png]]
![[late_trend__vix_low-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run late_trend__vix_low`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
