---
type: strategy
strategy: ib_breakout__vol_low@ES
family: initial_balance
verdict: graveyard
plan: eod
run_id: a1d9c7a55c
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# ib_breakout__vol_low@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 1.0}; base sizes (micros)
{'eod': 30, 'intraday': 25}; sizing policy (alpha, beta, mu) {'eod': (2.0, 0.0, 0.518402981940385), 'intraday': (2.0, 0.0, 0.518402981940385)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 748 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9240 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -561.1 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0235 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1243 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1892 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 5.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 15.6 | <= 30 | speed | PASS |

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
| eval_pass | 0.1243 | 0.0551 |
| eval_fail | 0.3938 | 0.4677 |
| eval_expired | 0.4819 | 0.4772 |
| median_sessions_to_pass | 5.0000 | 6.5000 |
| p90_sessions_to_pass | 15.6 | 14.9 |
| first_payout_given_pass | 0.1892 | 0.2683 |
| end_to_end_payout | 0.0235 | 0.0148 |
| mean_payouts_given_pass | 0.1934 | 0.2716 |
| ev_per_attempt | -538.5 | -231.8 |
| ev_p05 | -561.1 | -250.9 |
| ev_p95 | -507.8 | -202.7 |
| max_best_day_share | 1.4583 | 1.1688 |
| starts | 1488 | 1488 |
| effective_n | 78.3 | 82.7 |
| censored_pa | 4 | 1 |

## Statistics
- OOS trades: 748; total P&L per micro 322 USD
- Annualised Sharpe (daily, per micro): 0.06
- PSR (vs 0): 0.560; **Deflated Sharpe: 0.000** over 961 recorded trials
  (Sharpe variance across trials 1.02e-03)
- Random-entry percentile: 0.924

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'ib_min': 30, 'narrow': inf, 'tp_mult': 1.0, 'sl_frac': 1.0} | -0.0185 | 60 | 30 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 1.0, 'sl_frac': 0.5} | -0.0552 | 60 | 60 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | -0.0271 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | -0.0096 | 12 | 8 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'ib_min': 30, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 1.0} | 0.0140 | 4 | 4 | (0.0, 1.0, 0.53) | (0.5, 1.0, 0.53) |
| 2024 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 1.0} | 0.0087 | 30 | 25 | (2.0, 0.0, 0.43) | (2.0, 0.0, 0.43) |
| 2025 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 1.0} | 0.0081 | 30 | 25 | (2.0, 0.0, 0.4) | (2.0, 0.0, 0.4) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1185 | 0.0778 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -566.5 | -253.6 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -4.83 USD

## Evidence
![[ib_breakout__vol_low@ES-equity.png]]
![[ib_breakout__vol_low@ES-fan.png]]
![[ib_breakout__vol_low@ES-random.png]]
![[ib_breakout__vol_low@ES-drawdown.png]]
![[ib_breakout__vol_low@ES-monthly.png]]
![[ib_breakout__vol_low@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ib_breakout__vol_low@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
