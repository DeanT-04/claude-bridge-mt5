---
type: strategy
strategy: ib_breakout__trending@ES
family: initial_balance
verdict: graveyard
plan: eod
run_id: cce6823cbd
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# ib_breakout__trending@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5}; base sizes (micros)
{'eod': 12, 'intraday': 12}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 0.5859502309953712), 'intraday': (0.0, 1.0, 0.5859502309953712)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 803 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0001 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9300 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -586.6 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0034 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2433 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0138 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 4.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 13.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.2433 | 0.0941 |
| eval_fail | 0.7151 | 0.8595 |
| eval_expired | 0.0417 | 0.0464 |
| median_sessions_to_pass | 4.0000 | 3.5000 |
| p90_sessions_to_pass | 13.0 | 12.0 |
| first_payout_given_pass | 0.0138 | 0.0143 |
| end_to_end_payout | 0.0034 | 0.0013 |
| mean_payouts_given_pass | 0.0138 | 0.0143 |
| ev_per_attempt | -578.8 | -252.5 |
| ev_p05 | -586.6 | -255.1 |
| ev_p95 | -568.2 | -249.7 |
| max_best_day_share | 1.5071 | 1.4663 |
| starts | 1488 | 1488 |
| effective_n | 297.6 | 496.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 803; total P&L per micro 925 USD
- Annualised Sharpe (daily, per micro): 0.13
- PSR (vs 0): 0.634; **Deflated Sharpe: 0.000** over 893 recorded trials
  (Sharpe variance across trials 1.03e-03)
- Random-entry percentile: 0.930

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0174 | 12 | 12 | (0.0, 1.0, 0.61) | (0.0, 1.0, 0.61) |
| 2020 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | -0.0010 | 20 | 15 | (0.5, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2021 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0011 | 12 | 12 | (0.0, 1.0, 0.05) | (0.0, 1.0, 0.05) |
| 2022 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0051 | 12 | 12 | (0.0, 1.0, 0.24) | (0.0, 1.0, 0.24) |
| 2023 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0158 | 12 | 12 | (0.0, 1.0, 0.9) | (0.0, 1.0, 0.9) |
| 2024 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0115 | 12 | 12 | (0.0, 1.0, 0.65) | (0.0, 1.0, 0.65) |
| 2025 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0132 | 12 | 12 | (0.0, 1.0, 0.75) | (0.0, 1.0, 0.75) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2259 | 0.0519 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -581.4 | -252.1 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 4.22 USD

## Evidence
![[ib_breakout__trending@ES-equity.png]]
![[ib_breakout__trending@ES-fan.png]]
![[ib_breakout__trending@ES-random.png]]
![[ib_breakout__trending@ES-drawdown.png]]
![[ib_breakout__trending@ES-monthly.png]]
![[ib_breakout__trending@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ib_breakout__trending@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
