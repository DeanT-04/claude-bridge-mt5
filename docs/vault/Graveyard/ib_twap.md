---
type: strategy
strategy: ib_twap
family: initial_balance
verdict: graveyard
plan: eod
run_id: 738d00eda5
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# ib_twap: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'sl_frac': 0.5, 'tp_mult': 2.0}; base sizes (micros)
{'eod': 2, 'intraday': 2}; sizing policy (alpha, beta, mu) {'eod': (0.5, 1.0, 6.150191516169623), 'intraday': (0.5, 1.0, 6.150191516169623)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1215 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.1904 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9980 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -558.8 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0390 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2231 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1747 | >= 0.7 | commercial | FAIL |
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
| eval_pass | 0.2231 | 0.0927 |
| eval_fail | 0.6290 | 0.7661 |
| eval_expired | 0.1478 | 0.1411 |
| median_sessions_to_pass | 4.0000 | 2.0000 |
| p90_sessions_to_pass | 12.0 | 8.0000 |
| first_payout_given_pass | 0.1747 | 0.2246 |
| end_to_end_payout | 0.0390 | 0.0208 |
| mean_payouts_given_pass | 0.1867 | 0.4348 |
| ev_per_attempt | -538.1 | -184.7 |
| ev_p05 | -558.8 | -231.8 |
| ev_p95 | -514.0 | -130.3 |
| max_best_day_share | 1.3317 | 1.4017 |
| starts | 1488 | 1488 |
| effective_n | 297.6 | 744.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 1,215; total P&L per micro 13,987 USD
- Annualised Sharpe (daily, per micro): 0.90
- PSR (vs 0): 0.991; **Deflated Sharpe: 0.190** over 285 recorded trials
  (Sharpe variance across trials 7.24e-04)
- Random-entry percentile: 0.998

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'sl_frac': 0.5, 'tp_mult': 2.0} | 0.0164 | 20 | 25 | (2.0, 1.0, 0.85) | (0.5, 0.0, 0.85) |
| 2020 | {'sl_frac': 0.5, 'tp_mult': 2.0} | 0.0277 | 20 | 20 | (1.0, 0.5, 1.45) | (0.0, 0.0, 1.45) |
| 2021 | {'sl_frac': 0.5, 'tp_mult': 2.0} | 0.0300 | 20 | 25 | (2.0, 1.0, 2.44) | (0.5, 0.0, 2.44) |
| 2022 | {'sl_frac': 0.5, 'tp_mult': 2.0} | 0.0404 | 25 | 25 | (2.0, 1.0, 3.71) | (0.5, 0.0, 3.71) |
| 2023 | {'sl_frac': 0.5, 'tp_mult': 2.0} | 0.0644 | 2 | 2 | (0.0, 1.0, 7.73) | (2.0, 1.0, 7.73) |
| 2024 | {'sl_frac': 0.5, 'tp_mult': 2.0} | 0.0600 | 2 | 2 | (1.0, 1.0, 7.24) | (0.5, 1.0, 7.24) |
| 2025 | {'sl_frac': 0.5, 'tp_mult': 2.0} | 0.0574 | 2 | 2 | (0.5, 1.0, 7.35) | (0.5, 1.0, 7.35) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2593 | 0.1333 |
| end_to_end_payout | 0.0037 | 0.0037 |
| ev_per_attempt | -584.0 | -251.3 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 6.18 USD

## Evidence
![[ib_twap-equity.png]]
![[ib_twap-fan.png]]
![[ib_twap-random.png]]
![[ib_twap-drawdown.png]]
![[ib_twap-monthly.png]]
![[ib_twap-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ib_twap`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
