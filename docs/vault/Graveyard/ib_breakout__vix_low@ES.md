---
type: strategy
strategy: ib_breakout__vix_low@ES
family: initial_balance
verdict: graveyard
plan: eod
run_id: 2e15272474
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# ib_breakout__vix_low@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'ib_min': 60, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 1.0}; base sizes (micros)
{'eod': 10, 'intraday': 6}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 0.16443196136078664), 'intraday': (0.0, 1.0, 0.16443196136078664)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 507 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.8480 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -565.0 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0222 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1794 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1236 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 7.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 18.4 | <= 30 | speed | PASS |

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
| eval_pass | 0.1794 | 0.0773 |
| eval_fail | 0.4294 | 0.6183 |
| eval_expired | 0.3911 | 0.3044 |
| median_sessions_to_pass | 7.0000 | 6.0000 |
| p90_sessions_to_pass | 18.4 | 18.0 |
| first_payout_given_pass | 0.1236 | 0.1304 |
| end_to_end_payout | 0.0222 | 0.0101 |
| mean_payouts_given_pass | 0.1423 | 0.1304 |
| ev_per_attempt | -536.6 | -238.4 |
| ev_p05 | -565.0 | -252.0 |
| ev_p95 | -512.9 | -219.8 |
| max_best_day_share | 1.3279 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 106.3 | 148.8 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 507; total P&L per micro -384 USD
- Annualised Sharpe (daily, per micro): -0.11
- PSR (vs 0): 0.388; **Deflated Sharpe: 0.000** over 937 recorded trials
  (Sharpe variance across trials 1.03e-03)
- Random-entry percentile: 0.848

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'ib_min': 60, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 1.0} | -0.0155 | 30 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | -0.0514 | 60 | 30 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 1.0, 'sl_frac': 0.5} | -0.0433 | 25 | 40 | (0.0, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2022 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 1.0, 'sl_frac': 0.5} | -0.0235 | 25 | 40 | (0.0, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2023 | {'ib_min': 60, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 1.0} | -0.0160 | 30 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2024 | {'ib_min': 60, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 1.0} | -0.0018 | 15 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'ib_min': 60, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0001 | 8 | 10 | (0.0, 1.0, 0.0) | (0.5, 0.5, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1556 | 0.0556 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -571.6 | -252.3 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -1.30 USD

## Evidence
![[ib_breakout__vix_low@ES-equity.png]]
![[ib_breakout__vix_low@ES-fan.png]]
![[ib_breakout__vix_low@ES-random.png]]
![[ib_breakout__vix_low@ES-drawdown.png]]
![[ib_breakout__vix_low@ES-monthly.png]]
![[ib_breakout__vix_low@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ib_breakout__vix_low@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
