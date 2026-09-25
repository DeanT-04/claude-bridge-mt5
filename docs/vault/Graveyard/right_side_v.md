---
type: strategy
strategy: right_side_v
family: capitulation_reversal
verdict: graveyard
plan: eod
run_id: 070ee2231d
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# right_side_v: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'m': 0.7, 'f': 1.0, 'hold': 90}; base sizes (micros)
{'eod': 10, 'intraday': 60}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 441 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.4090 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -579.6 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0128 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2305 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0554 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 7.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 17.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.2305 | 0.0316 |
| eval_fail | 0.6478 | 0.9684 |
| eval_expired | 0.1216 | 0.0000 |
| median_sessions_to_pass | 7.0000 | 3.0000 |
| p90_sessions_to_pass | 17.0 | 8.4000 |
| first_payout_given_pass | 0.0554 | 0.0000 |
| end_to_end_payout | 0.0128 | 0.0000 |
| mean_payouts_given_pass | 0.0554 | 0.0000 |
| ev_per_attempt | -565.0 | -250.9 |
| ev_p05 | -579.6 | -252.1 |
| ev_p95 | -547.1 | -249.8 |
| max_best_day_share | 1.3139 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 165.3 | 496.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 441; total P&L per micro -1,297 USD
- Annualised Sharpe (daily, per micro): -0.19
- PSR (vs 0): 0.319; **Deflated Sharpe: 0.000** over 1029 recorded trials
  (Sharpe variance across trials 1.08e-03)
- Random-entry percentile: 0.409

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'m': 0.7, 'f': 1.0, 'hold': 90} | 0.0007 | 25 | 40 | (0.5, 1.0, 0.02) | (0.5, 1.0, 0.02) |
| 2020 | {'m': 0.7, 'f': 1.0, 'hold': 90} | 0.0160 | 15 | 40 | (0.0, 1.0, 0.39) | (0.5, 1.0, 0.39) |
| 2021 | {'m': 0.7, 'f': 1.0, 'hold': 90} | 0.0099 | 15 | 60 | (0.0, 1.0, 0.4) | (0.5, 0.5, 0.4) |
| 2022 | {'m': 0.7, 'f': 1.0, 'hold': 90} | -0.0226 | 30 | 60 | (1.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'m': 0.7, 'f': 1.0, 'hold': 90} | -0.0043 | 10 | 60 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2024 | {'m': 0.7, 'f': 1.0, 'hold': 90} | -0.0008 | 10 | 60 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'m': 0.7, 'f': 1.0, 'hold': 90} | -0.0033 | 10 | 60 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1000 | 0.0000 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -563.9 | -249.0 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -2.61 USD

## Evidence
![[right_side_v-equity.png]]
![[right_side_v-fan.png]]
![[right_side_v-random.png]]
![[right_side_v-drawdown.png]]
![[right_side_v-monthly.png]]
![[right_side_v-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run right_side_v`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
