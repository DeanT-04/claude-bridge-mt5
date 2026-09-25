---
type: strategy
strategy: ib_twap@ES
family: initial_balance
verdict: graveyard
plan: eod
run_id: f01e229265
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# ib_twap@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'sl_frac': 0.5, 'tp_mult': 2.0}; base sizes (micros)
{'eod': 2, 'intraday': 2}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 1.7173787274254266), 'intraday': (0.0, 1.0, 1.7173787274254266)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1241 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0011 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9970 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -542.5 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0349 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1727 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2023 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 10.0 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 19.0 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1727 | 0.1163 |
| eval_fail | 0.3757 | 0.6774 |
| eval_expired | 0.4516 | 0.2063 |
| median_sessions_to_pass | 10.0 | 11.0 |
| p90_sessions_to_pass | 19.0 | 19.0 |
| first_payout_given_pass | 0.2023 | 0.1908 |
| end_to_end_payout | 0.0349 | 0.0222 |
| mean_payouts_given_pass | 0.4358 | 0.3873 |
| ev_per_attempt | -459.2 | -173.9 |
| ev_p05 | -542.5 | -244.3 |
| ev_p95 | -354.6 | -92.8 |
| max_best_day_share | 1.1773 | 1.1170 |
| starts | 1488 | 1488 |
| effective_n | 78.3 | 156.6 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 1,241; total P&L per micro 4,624 USD
- Annualised Sharpe (daily, per micro): 0.52
- PSR (vs 0): 0.910; **Deflated Sharpe: 0.001** over 997 recorded trials
  (Sharpe variance across trials 1.08e-03)
- Random-entry percentile: 0.997

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'sl_frac': 0.5, 'tp_mult': 2.0} | -0.0168 | 8 | 60 | (0.5, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2020 | {'sl_frac': 0.5, 'tp_mult': 2.0} | -0.0215 | 8 | 60 | (0.5, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2021 | {'sl_frac': 0.5, 'tp_mult': 2.0} | -0.0026 | 8 | 10 | (0.5, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2022 | {'sl_frac': 0.5, 'tp_mult': 2.0} | -0.0020 | 8 | 5 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'sl_frac': 0.5, 'tp_mult': 2.0} | 0.0267 | 8 | 2 | (0.0, 0.0, 1.97) | (0.0, 1.0, 1.97) |
| 2024 | {'sl_frac': 0.5, 'tp_mult': 2.0} | 0.0252 | 8 | 3 | (0.0, 0.0, 1.85) | (0.0, 0.5, 1.85) |
| 2025 | {'sl_frac': 0.5, 'tp_mult': 2.0} | 0.0297 | 2 | 2 | (0.0, 1.0, 2.24) | (0.0, 1.0, 2.24) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2148 | 0.1815 |
| end_to_end_payout | 0.0407 | 0.0185 |
| ev_per_attempt | -556.2 | -249.3 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 3.50 USD

## Evidence
![[ib_twap@ES-equity.png]]
![[ib_twap@ES-fan.png]]
![[ib_twap@ES-random.png]]
![[ib_twap@ES-drawdown.png]]
![[ib_twap@ES-monthly.png]]
![[ib_twap@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ib_twap@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
