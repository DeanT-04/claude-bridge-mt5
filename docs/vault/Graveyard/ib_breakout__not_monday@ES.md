---
type: strategy
strategy: ib_breakout__not_monday@ES
family: initial_balance
verdict: graveyard
plan: eod
run_id: ab3b2b4268
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# ib_breakout__not_monday@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5}; base sizes (micros)
{'eod': 6, 'intraday': 6}; sizing policy (alpha, beta, mu) {'eod': (2.0, 1.0, 1.5612636497269878), 'intraday': (2.0, 1.0, 1.5612636497269878)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1218 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0007 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9920 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -546.0 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0276 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2493 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1105 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 4.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 12.0 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2493 | 0.1163 |
| eval_fail | 0.4933 | 0.6142 |
| eval_expired | 0.2574 | 0.2695 |
| median_sessions_to_pass | 4.0000 | 4.0000 |
| p90_sessions_to_pass | 12.0 | 13.8 |
| first_payout_given_pass | 0.1105 | 0.1734 |
| end_to_end_payout | 0.0276 | 0.0202 |
| mean_payouts_given_pass | 0.2776 | 0.2890 |
| ev_per_attempt | -465.1 | -202.9 |
| ev_p05 | -546.0 | -240.0 |
| ev_p95 | -357.7 | -153.5 |
| max_best_day_share | 1.4599 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 212.6 | 186.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 1,218; total P&L per micro 3,568 USD
- Annualised Sharpe (daily, per micro): 0.41
- PSR (vs 0): 0.853; **Deflated Sharpe: 0.001** over 821 recorded trials
  (Sharpe variance across trials 1.05e-03)
- Random-entry percentile: 0.992

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0047 | 8 | 8 | (0.0, 1.0, 0.19) | (0.0, 1.0, 0.19) |
| 2020 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | -0.0045 | 15 | 15 | (0.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2021 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | -0.0042 | 15 | 15 | (0.0, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2022 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | -0.0110 | 15 | 15 | (0.0, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2023 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0255 | 6 | 10 | (2.0, 1.0, 1.84) | (2.0, 0.0, 1.84) |
| 2024 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0224 | 6 | 5 | (2.0, 1.0, 1.62) | (0.5, 0.5, 1.62) |
| 2025 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0281 | 6 | 6 | (2.0, 1.0, 2.09) | (2.0, 1.0, 2.09) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1333 | 0.0593 |
| end_to_end_payout | 0.0037 | 0.0000 |
| ev_per_attempt | -563.0 | -252.5 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 0.89 USD

## Evidence
![[ib_breakout__not_monday@ES-equity.png]]
![[ib_breakout__not_monday@ES-fan.png]]
![[ib_breakout__not_monday@ES-random.png]]
![[ib_breakout__not_monday@ES-drawdown.png]]
![[ib_breakout__not_monday@ES-monthly.png]]
![[ib_breakout__not_monday@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ib_breakout__not_monday@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
