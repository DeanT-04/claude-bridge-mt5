---
type: strategy
strategy: ib_breakout__trending
family: initial_balance
verdict: graveyard
plan: eod
run_id: 30bfaa1d4e
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# ib_breakout__trending: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 1.0, 'sl_frac': 1.0}; base sizes (micros)
{'eod': 20, 'intraday': 10}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.5, 0.8996833263334627), 'intraday': (0.0, 1.0, 0.8996833263334627)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 612 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0044 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.8500 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -554.3 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0296 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1620 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1826 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 3.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 12.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.1620 | 0.0551 |
| eval_fail | 0.6196 | 0.8192 |
| eval_expired | 0.2184 | 0.1257 |
| median_sessions_to_pass | 3.0000 | 6.0000 |
| p90_sessions_to_pass | 12.0 | 16.0 |
| first_payout_given_pass | 0.1826 | 0.0244 |
| end_to_end_payout | 0.0296 | 0.0013 |
| mean_payouts_given_pass | 0.2573 | 0.0732 |
| ev_per_attempt | -510.0 | -244.2 |
| ev_p05 | -554.3 | -253.2 |
| ev_p95 | -453.8 | -227.9 |
| max_best_day_share | 1.3296 | 1.0231 |
| starts | 1488 | 1488 |
| effective_n | 212.6 | 248.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 612; total P&L per micro 2,505 USD
- Annualised Sharpe (daily, per micro): 0.25
- PSR (vs 0): 0.737; **Deflated Sharpe: 0.004** over 249 recorded trials
  (Sharpe variance across trials 7.84e-04)
- Random-entry percentile: 0.850

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | -0.0383 | 50 | 60 | (2.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2020 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 0.5} | -0.0134 | 30 | 40 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 1.0, 'sl_frac': 1.0} | -0.0120 | 20 | 30 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0036 | 8 | 20 | (0.0, 1.0, 0.25) | (0.0, 1.0, 0.25) |
| 2023 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0277 | 10 | 2 | (0.0, 1.0, 2.59) | (0.5, 1.0, 2.59) |
| 2024 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0225 | 8 | 2 | (0.0, 1.0, 2.14) | (0.5, 1.0, 2.14) |
| 2025 | {'ib_min': 60, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0193 | 5 | 5 | (0.0, 1.0, 0.87) | (0.0, 0.5, 0.87) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0593 | 0.0148 |
| end_to_end_payout | 0.0111 | 0.0000 |
| ev_per_attempt | -541.6 | -249.9 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -0.26 USD

## Evidence
![[ib_breakout__trending-equity.png]]
![[ib_breakout__trending-fan.png]]
![[ib_breakout__trending-random.png]]
![[ib_breakout__trending-drawdown.png]]
![[ib_breakout__trending-monthly.png]]
![[ib_breakout__trending-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ib_breakout__trending`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
