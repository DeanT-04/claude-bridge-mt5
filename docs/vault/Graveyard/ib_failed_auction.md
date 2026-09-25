---
type: strategy
strategy: ib_failed_auction
family: failed_auction
verdict: graveyard
plan: eod
run_id: e54a14afd0
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# ib_failed_auction: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'block': 5, 't': 0.5, 'double_sweep': True}; base sizes (micros)
{'eod': 25, 'intraday': 5}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1703 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.5490 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -555.4 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0242 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2345 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1032 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 3.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 8.0000 | <= 30 | speed | PASS |

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
| eval_pass | 0.2345 | 0.0995 |
| eval_fail | 0.7272 | 0.8878 |
| eval_expired | 0.0383 | 0.0128 |
| median_sessions_to_pass | 3.0000 | 4.0000 |
| p90_sessions_to_pass | 8.0000 | 10.0 |
| first_payout_given_pass | 0.1032 | 0.0405 |
| end_to_end_payout | 0.0242 | 0.0040 |
| mean_payouts_given_pass | 0.2264 | 0.0541 |
| ev_per_attempt | -492.5 | -246.0 |
| ev_p05 | -555.4 | -253.9 |
| ev_p95 | -413.0 | -234.9 |
| max_best_day_share | 1.3434 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 372.0 | 744.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 1,703; total P&L per micro -3,127 USD
- Annualised Sharpe (daily, per micro): -0.34
- PSR (vs 0): 0.194; **Deflated Sharpe: 0.000** over 877 recorded trials
  (Sharpe variance across trials 1.05e-03)
- Random-entry percentile: 0.549

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'block': 5, 't': 0.5, 'double_sweep': True} | 0.0176 | 25 | 20 | (1.0, 0.5, 0.48) | (0.5, 0.5, 0.48) |
| 2020 | {'block': 5, 't': 0.5, 'double_sweep': True} | -0.0086 | 40 | 20 | (0.5, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2021 | {'block': 5, 't': 0.5, 'double_sweep': False} | 0.0089 | 20 | 20 | (0.5, 1.0, 0.45) | (0.5, 1.0, 0.45) |
| 2022 | {'block': 5, 't': 0.5, 'double_sweep': False} | -0.0035 | 12 | 10 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'block': 5, 't': 0.5, 'double_sweep': True} | -0.0303 | 25 | 20 | (0.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2024 | {'block': 5, 't': 0.5, 'double_sweep': True} | -0.0232 | 25 | 20 | (0.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2025 | {'block': 5, 't': 0.5, 'double_sweep': True} | -0.0002 | 25 | 15 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2667 | 0.0222 |
| end_to_end_payout | 0.0074 | 0.0000 |
| ev_per_attempt | -576.0 | -250.3 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -7.39 USD

## Evidence
![[ib_failed_auction-equity.png]]
![[ib_failed_auction-fan.png]]
![[ib_failed_auction-random.png]]
![[ib_failed_auction-drawdown.png]]
![[ib_failed_auction-monthly.png]]
![[ib_failed_auction-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ib_failed_auction`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
