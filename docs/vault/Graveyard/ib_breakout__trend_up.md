---
type: strategy
strategy: ib_breakout__trend_up
family: initial_balance
verdict: graveyard
plan: eod
run_id: 7d7e766a5b
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# ib_breakout__trend_up: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'ib_min': 30, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 1.0}; base sizes (micros)
{'eod': 2, 'intraday': 2}; sizing policy (alpha, beta, mu) {'eod': (0.5, 1.0, 4.433168836623236), 'intraday': (1.0, 1.0, 4.433168836623236)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 825 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0116 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9340 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -493.8 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0719 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1882 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.3821 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 4.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 13.1 | <= 30 | speed | PASS |

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
| eval_pass | 0.1882 | 0.0840 |
| eval_fail | 0.4866 | 0.7332 |
| eval_expired | 0.3253 | 0.1828 |
| median_sessions_to_pass | 4.0000 | 4.0000 |
| p90_sessions_to_pass | 13.1 | 12.0 |
| first_payout_given_pass | 0.3821 | 0.2640 |
| end_to_end_payout | 0.0719 | 0.0222 |
| mean_payouts_given_pass | 0.5179 | 0.5040 |
| ev_per_attempt | -429.6 | -185.5 |
| ev_p05 | -493.8 | -224.5 |
| ev_p95 | -367.8 | -132.0 |
| max_best_day_share | 1.2719 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 124.0 | 212.6 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 825; total P&L per micro 4,097 USD
- Annualised Sharpe (daily, per micro): 0.39
- PSR (vs 0): 0.844; **Deflated Sharpe: 0.012** over 233 recorded trials
  (Sharpe variance across trials 8.20e-04)
- Random-entry percentile: 0.934

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'ib_min': 60, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 0.5} | -0.0008 | 20 | 40 | (0.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2020 | {'ib_min': 60, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0181 | 12 | 12 | (0.0, 0.5, 0.4) | (0.5, 1.0, 0.4) |
| 2021 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 1.0, 'sl_frac': 0.5} | 0.0004 | 10 | 4 | (2.0, 1.0, 0.02) | (1.0, 1.0, 0.02) |
| 2022 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 1.0, 'sl_frac': 0.5} | 0.0363 | 10 | 4 | (2.0, 1.0, 2.52) | (1.0, 1.0, 2.52) |
| 2023 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 1.0, 'sl_frac': 0.5} | 0.0372 | 10 | 2 | (2.0, 1.0, 2.7) | (0.0, 1.0, 2.7) |
| 2024 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0329 | 2 | 3 | (0.0, 1.0, 2.85) | (0.0, 0.5, 2.85) |
| 2025 | {'ib_min': 30, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 1.0} | 0.0416 | 2 | 2 | (0.5, 1.0, 4.79) | (1.0, 1.0, 4.79) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.3074 | 0.1259 |
| end_to_end_payout | 0.1037 | 0.0370 |
| ev_per_attempt | -467.5 | -202.0 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -3.21 USD

## Evidence
![[ib_breakout__trend_up-equity.png]]
![[ib_breakout__trend_up-fan.png]]
![[ib_breakout__trend_up-random.png]]
![[ib_breakout__trend_up-drawdown.png]]
![[ib_breakout__trend_up-monthly.png]]
![[ib_breakout__trend_up-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ib_breakout__trend_up`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
