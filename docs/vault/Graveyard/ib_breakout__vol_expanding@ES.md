---
type: strategy
strategy: ib_breakout__vol_expanding@ES
family: initial_balance
verdict: graveyard
plan: eod
run_id: 5c3aa4130b
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# ib_breakout__vol_expanding@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5}; base sizes (micros)
{'eod': 8, 'intraday': 5}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 1.1319613607727712), 'intraday': (0.0, 1.0, 1.1319613607727712)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 430 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.3540 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -563.5 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0128 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1022 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1250 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 6.0000 | <= 15 | speed | PASS |
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
| eval_pass | 0.1022 | 0.0276 |
| eval_fail | 0.4597 | 0.5497 |
| eval_expired | 0.4382 | 0.4227 |
| median_sessions_to_pass | 6.0000 | 10.0 |
| p90_sessions_to_pass | 17.0 | 18.0 |
| first_payout_given_pass | 0.1250 | 0.2439 |
| end_to_end_payout | 0.0128 | 0.0067 |
| mean_payouts_given_pass | 0.1250 | 0.2439 |
| ev_per_attempt | -545.0 | -240.5 |
| ev_p05 | -563.5 | -250.4 |
| ev_p95 | -518.8 | -225.3 |
| max_best_day_share | 1.2505 | 1.2197 |
| starts | 1488 | 1488 |
| effective_n | 78.3 | 93.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 430; total P&L per micro -2,245 USD
- Annualised Sharpe (daily, per micro): -0.47
- PSR (vs 0): 0.123; **Deflated Sharpe: 0.000** over 921 recorded trials
  (Sharpe variance across trials 1.05e-03)
- Random-entry percentile: 0.354

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0287 | 8 | 8 | (0.0, 1.0, 1.06) | (0.0, 1.0, 1.06) |
| 2020 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 1.0, 'sl_frac': 0.5} | 0.0156 | 12 | 12 | (0.5, 1.0, 0.46) | (0.5, 1.0, 0.46) |
| 2021 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 1.0, 'sl_frac': 1.0} | 0.0085 | 15 | 1 | (1.0, 1.0, 0.1) | (0.0, 0.0, 0.1) |
| 2022 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 1.0, 'sl_frac': 1.0} | 0.0122 | 15 | 1 | (1.0, 1.0, 0.16) | (0.0, 0.0, 0.16) |
| 2023 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0183 | 8 | 8 | (0.0, 1.0, 1.1) | (0.0, 0.5, 1.1) |
| 2024 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 1.0, 'sl_frac': 1.0} | 0.0113 | 12 | 12 | (0.0, 1.0, 0.18) | (0.0, 1.0, 0.18) |
| 2025 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0201 | 8 | 5 | (0.0, 1.0, 1.24) | (0.0, 1.0, 1.24) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2333 | 0.1185 |
| end_to_end_payout | 0.0407 | 0.0000 |
| ev_per_attempt | -541.4 | -256.0 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 3.75 USD

## Evidence
![[ib_breakout__vol_expanding@ES-equity.png]]
![[ib_breakout__vol_expanding@ES-fan.png]]
![[ib_breakout__vol_expanding@ES-random.png]]
![[ib_breakout__vol_expanding@ES-drawdown.png]]
![[ib_breakout__vol_expanding@ES-monthly.png]]
![[ib_breakout__vol_expanding@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ib_breakout__vol_expanding@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
