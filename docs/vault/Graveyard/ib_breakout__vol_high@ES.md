---
type: strategy
strategy: ib_breakout__vol_high@ES
family: initial_balance
verdict: graveyard
plan: eod
run_id: 0253c083dd
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# ib_breakout__vol_high@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5}; base sizes (micros)
{'eod': 6, 'intraday': 4}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 2.1119450860982583), 'intraday': (0.0, 0.5, 2.1119450860982583)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 668 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.4610 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -561.3 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0255 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2130 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1199 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 8.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 19.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.2130 | 0.0323 |
| eval_fail | 0.4019 | 0.6378 |
| eval_expired | 0.3851 | 0.3300 |
| median_sessions_to_pass | 8.0000 | 2.0000 |
| p90_sessions_to_pass | 19.0 | 17.3 |
| first_payout_given_pass | 0.1199 | 0.1042 |
| end_to_end_payout | 0.0255 | 0.0034 |
| mean_payouts_given_pass | 0.1893 | 0.1042 |
| ev_per_attempt | -521.3 | -247.8 |
| ev_p05 | -561.3 | -250.1 |
| ev_p95 | -465.3 | -244.9 |
| max_best_day_share | 1.3219 | 1.2884 |
| starts | 1488 | 1488 |
| effective_n | 106.3 | 186.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 668; total P&L per micro -2,623 USD
- Annualised Sharpe (daily, per micro): -0.36
- PSR (vs 0): 0.182; **Deflated Sharpe: 0.000** over 981 recorded trials
  (Sharpe variance across trials 1.08e-03)
- Random-entry percentile: 0.461

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0390 | 15 | 15 | (0.0, 1.0, 1.53) | (0.0, 1.0, 1.53) |
| 2020 | {'ib_min': 30, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 1.0} | 0.0243 | 12 | 12 | (0.0, 1.0, 1.03) | (0.0, 1.0, 1.03) |
| 2021 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0186 | 15 | 15 | (0.0, 1.0, 1.05) | (0.0, 1.0, 1.05) |
| 2022 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 1.0, 'sl_frac': 1.0} | 0.0105 | 8 | 6 | (1.0, 1.0, 0.25) | (0.0, 1.0, 0.25) |
| 2023 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0337 | 6 | 15 | (0.0, 0.5, 2.37) | (0.0, 1.0, 2.37) |
| 2024 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0274 | 6 | 15 | (0.0, 0.5, 1.82) | (0.0, 1.0, 1.82) |
| 2025 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0357 | 6 | 4 | (0.0, 0.5, 2.46) | (0.0, 0.5, 2.46) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2111 | 0.0667 |
| end_to_end_payout | 0.0111 | 0.0000 |
| ev_per_attempt | -562.7 | -252.9 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 4.52 USD

## Evidence
![[ib_breakout__vol_high@ES-equity.png]]
![[ib_breakout__vol_high@ES-fan.png]]
![[ib_breakout__vol_high@ES-random.png]]
![[ib_breakout__vol_high@ES-drawdown.png]]
![[ib_breakout__vol_high@ES-monthly.png]]
![[ib_breakout__vol_high@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ib_breakout__vol_high@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
