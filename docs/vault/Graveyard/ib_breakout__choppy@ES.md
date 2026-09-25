---
type: strategy
strategy: ib_breakout__choppy@ES
family: initial_balance
verdict: graveyard
plan: eod
run_id: b5ea0aab04
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# ib_breakout__choppy@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 1.0}; base sizes (micros)
{'eod': 20, 'intraday': 6}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.5, 1.1747543049139035), 'intraday': (0.0, 1.0, 1.1747543049139035)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 271 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0120 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9910 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -540.4 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0363 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1438 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2523 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 9.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 18.7 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- Holdout consistent
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1438 | 0.1317 |
| eval_fail | 0.3690 | 0.5840 |
| eval_expired | 0.4872 | 0.2843 |
| median_sessions_to_pass | 9.0000 | 8.0000 |
| p90_sessions_to_pass | 18.7 | 18.0 |
| first_payout_given_pass | 0.2523 | 0.1071 |
| end_to_end_payout | 0.0363 | 0.0141 |
| mean_payouts_given_pass | 0.6542 | 0.2296 |
| ev_per_attempt | -430.1 | -205.0 |
| ev_p05 | -540.4 | -254.4 |
| ev_p95 | -282.8 | -131.7 |
| max_best_day_share | 1.2774 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 74.4 | 148.8 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 271; total P&L per micro 1,997 USD
- Annualised Sharpe (daily, per micro): 0.61
- PSR (vs 0): 0.946; **Deflated Sharpe: 0.012** over 753 recorded trials
  (Sharpe variance across trials 8.60e-04)
- Random-entry percentile: 0.991

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 1.0} | 0.0198 | 40 | 20 | (0.5, 0.5, 0.31) | (0.5, 1.0, 0.31) |
| 2020 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 1.0, 'sl_frac': 1.0} | 0.0218 | 30 | 50 | (1.0, 1.0, 0.27) | (0.5, 0.5, 0.27) |
| 2021 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 1.0, 'sl_frac': 1.0} | 0.0318 | 6 | 50 | (0.0, 1.0, 0.66) | (0.5, 0.5, 0.66) |
| 2022 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 1.0} | 0.0274 | 10 | 15 | (0.5, 0.5, 0.73) | (0.5, 0.5, 0.73) |
| 2023 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 1.0, 'sl_frac': 1.0} | 0.0325 | 10 | 10 | (0.5, 1.0, 0.78) | (0.5, 0.5, 0.78) |
| 2024 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 1.0, 'sl_frac': 1.0} | 0.0348 | 15 | 8 | (0.0, 1.0, 0.82) | (0.5, 1.0, 0.82) |
| 2025 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 1.0} | 0.0335 | 20 | 8 | (0.0, 0.5, 1.01) | (0.0, 1.0, 1.01) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1704 | 0.1148 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -573.7 | -255.8 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -1.49 USD

## Evidence
![[ib_breakout__choppy@ES-equity.png]]
![[ib_breakout__choppy@ES-fan.png]]
![[ib_breakout__choppy@ES-random.png]]
![[ib_breakout__choppy@ES-drawdown.png]]
![[ib_breakout__choppy@ES-monthly.png]]
![[ib_breakout__choppy@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ib_breakout__choppy@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
