---
type: strategy
strategy: ib_breakout__vix_high@ES
family: initial_balance
verdict: graveyard
plan: intraday
run_id: 8de2129576
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# ib_breakout__vix_high@ES: **GRAVEYARD**

Best plan: **Apex intraday 50K**. Final params {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5}; base sizes (micros)
{'eod': 6, 'intraday': 8}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.5, 2.5016867912641687), 'intraday': (0.0, 0.0, 2.5016867912641687)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 407 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.6140 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -242.7 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0215 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0927 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2319 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 8.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 18.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.0961 | 0.0927 |
| eval_fail | 0.2702 | 0.3763 |
| eval_expired | 0.6337 | 0.5309 |
| median_sessions_to_pass | 5.0000 | 8.0000 |
| p90_sessions_to_pass | 17.8 | 18.0 |
| first_payout_given_pass | 0.2168 | 0.2319 |
| end_to_end_payout | 0.0208 | 0.0215 |
| mean_payouts_given_pass | 0.3217 | 0.3551 |
| ev_per_attempt | -522.2 | -195.3 |
| ev_p05 | -552.9 | -242.7 |
| ev_p95 | -476.6 | -134.9 |
| max_best_day_share | 1.2587 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 70.9 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 407; total P&L per micro -903 USD
- Annualised Sharpe (daily, per micro): -0.15
- PSR (vs 0): 0.350; **Deflated Sharpe: 0.000** over 877 recorded trials
  (Sharpe variance across trials 1.05e-03)
- Random-entry percentile: 0.614

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 1.0, 'sl_frac': 0.5} | 0.0317 | 8 | 12 | (0.0, 0.5, 0.84) | (0.0, 1.0, 0.84) |
| 2020 | {'ib_min': 30, 'narrow': inf, 'tp_mult': 1.0, 'sl_frac': 1.0} | 0.0337 | 10 | 15 | (2.0, 1.0, 0.88) | (2.0, 0.5, 0.88) |
| 2021 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 1.0, 'sl_frac': 0.5} | 0.0320 | 40 | 8 | (0.5, 0.5, 0.59) | (0.5, 1.0, 0.59) |
| 2022 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 1.0, 'sl_frac': 1.0} | 0.0223 | 15 | 15 | (0.0, 1.0, 0.5) | (0.0, 0.5, 0.5) |
| 2023 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0416 | 5 | 8 | (0.0, 0.5, 3.04) | (0.0, 0.0, 3.04) |
| 2024 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0355 | 5 | 8 | (0.0, 0.5, 2.48) | (0.0, 0.0, 2.48) |
| 2025 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0357 | 5 | 8 | (0.0, 0.5, 2.41) | (0.0, 0.0, 2.41) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1444 | 0.0481 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -570.1 | -251.8 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 2.37 USD

## Evidence
![[ib_breakout__vix_high@ES-equity.png]]
![[ib_breakout__vix_high@ES-fan.png]]
![[ib_breakout__vix_high@ES-random.png]]
![[ib_breakout__vix_high@ES-drawdown.png]]
![[ib_breakout__vix_high@ES-monthly.png]]
![[ib_breakout__vix_high@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ib_breakout__vix_high@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
