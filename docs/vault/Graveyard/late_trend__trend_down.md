---
type: strategy
strategy: late_trend__trend_down
family: late_trend
verdict: graveyard
plan: eod
run_id: b73b582a94
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# late_trend__trend_down: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'decide': 780, 'k': 0.3, 'sl_atr': 0.25}; base sizes (micros)
{'eod': 6, 'intraday': 3}; sizing policy (alpha, beta, mu) {'eod': (2.0, 1.0, 5.02691717569493), 'intraday': (1.0, 1.0, 5.02691717569493)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 258 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.2465 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 1.0000 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -421.7 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0605 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0941 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.6429 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 5.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 18.0 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0941 | 0.0242 |
| eval_fail | 0.1895 | 0.4133 |
| eval_expired | 0.7164 | 0.5625 |
| median_sessions_to_pass | 5.0000 | 2.5000 |
| p90_sessions_to_pass | 18.0 | 18.5 |
| first_payout_given_pass | 0.6429 | 0.2778 |
| end_to_end_payout | 0.0605 | 0.0067 |
| mean_payouts_given_pass | 2.6148 | 1.9545 |
| ev_per_attempt | -134.1 | -185.5 |
| ev_p05 | -421.7 | -239.3 |
| ev_p95 | 221.7 | -117.6 |
| max_best_day_share | 1.2011 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 70.9 |
| censored_pa | 18 | 14 |

## Statistics
- OOS trades: 258; total P&L per micro 7,990 USD
- Annualised Sharpe (daily, per micro): 0.99
- PSR (vs 0): 0.996; **Deflated Sharpe: 0.247** over 445 recorded trials
  (Sharpe variance across trials 6.76e-04)
- Random-entry percentile: 1.000

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'decide': 840, 'k': 0.3, 'sl_atr': 0.25} | 0.0632 | 10 | 6 | (0.0, 0.5, 1.97) | (0.0, 1.0, 1.97) |
| 2020 | {'decide': 840, 'k': 0.5, 'sl_atr': 0.25} | 0.0443 | 6 | 8 | (0.0, 1.0, 1.21) | (0.0, 0.5, 1.21) |
| 2021 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | 0.0395 | 6 | 4 | (0.0, 0.5, 1.73) | (0.0, 1.0, 1.73) |
| 2022 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | 0.0526 | 6 | 8 | (2.0, 1.0, 2.41) | (1.0, 1.0, 2.41) |
| 2023 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0891 | 6 | 3 | (2.0, 1.0, 5.8) | (1.0, 1.0, 5.8) |
| 2024 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0831 | 6 | 3 | (2.0, 1.0, 5.24) | (1.0, 1.0, 5.24) |
| 2025 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0723 | 6 | 3 | (2.0, 1.0, 4.5) | (1.0, 1.0, 4.5) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0852 | 0.0370 |
| end_to_end_payout | 0.0296 | 0.0296 |
| ev_per_attempt | -517.4 | -227.9 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 7.43 USD

## Evidence
![[late_trend__trend_down-equity.png]]
![[late_trend__trend_down-fan.png]]
![[late_trend__trend_down-random.png]]
![[late_trend__trend_down-drawdown.png]]
![[late_trend__trend_down-monthly.png]]
![[late_trend__trend_down-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run late_trend__trend_down`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
