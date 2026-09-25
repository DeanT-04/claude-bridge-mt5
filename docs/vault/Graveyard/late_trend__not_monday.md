---
type: strategy
strategy: late_trend__not_monday
family: late_trend
verdict: graveyard
plan: eod
run_id: 25305e4a47
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# late_trend__not_monday: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'decide': 780, 'k': 0.3, 'sl_atr': 0.25}; base sizes (micros)
{'eod': 3, 'intraday': 3}; sizing policy (alpha, beta, mu) {'eod': (1.0, 1.0, 5.332437253947177), 'intraday': (1.0, 1.0, 5.332437253947177)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 522 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.1917 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9950 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -253.7 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.1015 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2016 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.5033 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 6.5000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 17.1 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2016 | 0.0753 |
| eval_fail | 0.1573 | 0.5719 |
| eval_expired | 0.6411 | 0.3528 |
| median_sessions_to_pass | 6.5000 | 7.0000 |
| p90_sessions_to_pass | 17.1 | 17.9 |
| first_payout_given_pass | 0.5033 | 0.4821 |
| end_to_end_payout | 0.1015 | 0.0363 |
| mean_payouts_given_pass | 1.7700 | 0.9107 |
| ev_per_attempt | 112.8 | -138.4 |
| ev_p05 | -253.7 | -208.7 |
| ev_p95 | 553.8 | -45.1 |
| max_best_day_share | 1.3691 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 135.3 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 522; total P&L per micro 7,782 USD
- Annualised Sharpe (daily, per micro): 0.95
- PSR (vs 0): 0.995; **Deflated Sharpe: 0.192** over 305 recorded trials
  (Sharpe variance across trials 7.59e-04)
- Random-entry percentile: 0.995

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'decide': 840, 'k': 0.8, 'sl_atr': 0.25} | 0.0707 | 5 | 5 | (0.5, 1.0, 1.85) | (0.5, 1.0, 1.85) |
| 2020 | {'decide': 840, 'k': 0.8, 'sl_atr': 0.25} | 0.0492 | 6 | 6 | (0.5, 1.0, 1.18) | (0.5, 1.0, 1.18) |
| 2021 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | 0.0311 | 3 | 15 | (0.0, 1.0, 1.25) | (0.0, 1.0, 1.25) |
| 2022 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0467 | 6 | 6 | (2.0, 1.0, 2.66) | (2.0, 1.0, 2.66) |
| 2023 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0788 | 6 | 3 | (2.0, 1.0, 5.97) | (1.0, 1.0, 5.97) |
| 2024 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0798 | 5 | 3 | (2.0, 1.0, 6.08) | (1.0, 1.0, 6.08) |
| 2025 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0714 | 5 | 3 | (2.0, 1.0, 5.55) | (1.0, 1.0, 5.55) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1667 | 0.0741 |
| end_to_end_payout | 0.0556 | 0.0185 |
| ev_per_attempt | -515.2 | -233.2 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 3.00 USD

## Evidence
![[late_trend__not_monday-equity.png]]
![[late_trend__not_monday-fan.png]]
![[late_trend__not_monday-random.png]]
![[late_trend__not_monday-drawdown.png]]
![[late_trend__not_monday-monthly.png]]
![[late_trend__not_monday-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run late_trend__not_monday`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
