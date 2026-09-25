---
type: strategy
strategy: ib_failed_auction@ES
family: failed_auction
verdict: graveyard
plan: eod
run_id: 971ae2f3dd
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# ib_failed_auction@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'block': 30, 't': 0.5, 'double_sweep': False}; base sizes (micros)
{'eod': 12, 'intraday': 12}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1368 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.2840 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -562.4 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0067 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0806 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0833 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 11.0 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 19.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.0806 | 0.0571 |
| eval_fail | 0.5000 | 0.8340 |
| eval_expired | 0.4194 | 0.1089 |
| median_sessions_to_pass | 11.0 | 11.0 |
| p90_sessions_to_pass | 19.0 | 17.6 |
| first_payout_given_pass | 0.0833 | 0.0235 |
| end_to_end_payout | 0.0067 | 0.0013 |
| mean_payouts_given_pass | 0.0833 | 0.0235 |
| ev_per_attempt | -554.9 | -251.5 |
| ev_p05 | -562.4 | -253.3 |
| ev_p95 | -545.4 | -249.9 |
| max_best_day_share | 1.0000 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 82.7 | 186.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 1,368; total P&L per micro -5,691 USD
- Annualised Sharpe (daily, per micro): -1.25
- PSR (vs 0): 0.001; **Deflated Sharpe: 0.000** over 1151 recorded trials
  (Sharpe variance across trials 1.09e-03)
- Random-entry percentile: 0.284

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'block': 5, 't': 0.5, 'double_sweep': True} | -0.0709 | 20 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'block': 5, 't': 0.5, 'double_sweep': True} | -0.0610 | 20 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'block': 30, 't': 0.5, 'double_sweep': False} | -0.0418 | 1 | 25 | (0.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2022 | {'block': 30, 't': 0.5, 'double_sweep': False} | -0.0550 | 15 | 12 | (0.5, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2023 | {'block': 30, 't': 0.25, 'double_sweep': False} | -0.0689 | 30 | 40 | (1.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2024 | {'block': 30, 't': 0.5, 'double_sweep': False} | -0.0632 | 15 | 12 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'block': 30, 't': 0.5, 'double_sweep': False} | -0.0621 | 12 | 12 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1111 | 0.0852 |
| end_to_end_payout | 0.0185 | 0.0185 |
| ev_per_attempt | -549.4 | -238.0 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -5.25 USD

## Evidence
![[ib_failed_auction@ES-equity.png]]
![[ib_failed_auction@ES-fan.png]]
![[ib_failed_auction@ES-random.png]]
![[ib_failed_auction@ES-drawdown.png]]
![[ib_failed_auction@ES-monthly.png]]
![[ib_failed_auction@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ib_failed_auction@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
