---
type: strategy
strategy: late_trend__trending
family: late_trend
verdict: graveyard
plan: eod
run_id: 26a56bc321
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# late_trend__trending: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'decide': 780, 'k': 0.3, 'sl_atr': 0.25}; base sizes (micros)
{'eod': 5, 'intraday': 6}; sizing policy (alpha, beta, mu) {'eod': (2.0, 0.5, 2.8705867703799433), 'intraday': (1.0, 0.5, 2.8705867703799433)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 343 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0211 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9390 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -552.0 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0316 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1700 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1858 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 8.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 17.0 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- Beats random entry (percentile)
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1700 | 0.0632 |
| eval_fail | 0.5450 | 0.7816 |
| eval_expired | 0.2849 | 0.1552 |
| median_sessions_to_pass | 8.0000 | 6.0000 |
| p90_sessions_to_pass | 17.0 | 14.7 |
| first_payout_given_pass | 0.1858 | 0.0638 |
| end_to_end_payout | 0.0316 | 0.0040 |
| mean_payouts_given_pass | 0.3584 | 0.0638 |
| ev_per_attempt | -486.3 | -248.5 |
| ev_p05 | -552.0 | -252.6 |
| ev_p95 | -392.1 | -243.0 |
| max_best_day_share | 1.2962 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 114.5 | 212.6 |
| censored_pa | 27 | 0 |

## Statistics
- OOS trades: 343; total P&L per micro 3,332 USD
- Annualised Sharpe (daily, per micro): 0.49
- PSR (vs 0): 0.906; **Deflated Sharpe: 0.021** over 453 recorded trials
  (Sharpe variance across trials 6.68e-04)
- Random-entry percentile: 0.939

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | 0.0739 | 20 | 15 | (0.5, 1.0, 1.87) | (0.0, 1.0, 1.87) |
| 2020 | {'decide': 840, 'k': 0.8, 'sl_atr': 0.25} | 0.0634 | 20 | 10 | (0.5, 1.0, 1.33) | (0.0, 0.5, 1.33) |
| 2021 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | 0.0274 | 20 | 15 | (0.5, 1.0, 0.88) | (0.0, 1.0, 0.88) |
| 2022 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0345 | 10 | 6 | (0.0, 1.0, 1.46) | (0.0, 1.0, 1.46) |
| 2023 | {'decide': 840, 'k': 0.3, 'sl_atr': 0.5} | 0.0506 | 10 | 8 | (0.5, 0.0, 2.96) | (1.0, 0.5, 2.96) |
| 2024 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0475 | 5 | 6 | (2.0, 0.5, 2.78) | (1.0, 0.5, 2.78) |
| 2025 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0444 | 5 | 6 | (2.0, 0.5, 2.66) | (1.0, 0.5, 2.66) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1963 | 0.1407 |
| end_to_end_payout | 0.1148 | 0.1074 |
| ev_per_attempt | -420.8 | -106.8 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 9.90 USD

## Evidence
![[late_trend__trending-equity.png]]
![[late_trend__trending-fan.png]]
![[late_trend__trending-random.png]]
![[late_trend__trending-drawdown.png]]
![[late_trend__trending-monthly.png]]
![[late_trend__trending-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run late_trend__trending`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
