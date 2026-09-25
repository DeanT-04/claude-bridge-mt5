---
type: strategy
strategy: wide_ib_rotation@ES
family: ib_rotation
verdict: graveyard
plan: intraday
run_id: a8c522c8ed
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: 790a14f
seed: 11
---
# wide_ib_rotation@ES: **GRAVEYARD**

Best plan: **Apex intraday 50K**. Final params {'q': 1.3, 's': 0.1, 'target': 'far25'}; base sizes (micros)
{'eod': 8, 'intraday': 10}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.5, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 611 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.2690 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -249.5 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0000 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0040 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0000 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 8.5000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 19.5 | <= 30 | speed | PASS |

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
| eval_pass | 0.0027 | 0.0040 |
| eval_fail | 0.0289 | 0.3239 |
| eval_expired | 0.9684 | 0.6720 |
| median_sessions_to_pass | 19.5 | 8.5000 |
| p90_sessions_to_pass | 20.7 | 19.5 |
| first_payout_given_pass | 0.0000 | 0.0000 |
| end_to_end_payout | 0.0000 | 0.0000 |
| mean_payouts_given_pass | 0.0000 | 0.0000 |
| ev_per_attempt | -550.4 | -249.2 |
| ev_p05 | -551.1 | -249.5 |
| ev_p95 | -550.0 | -249.0 |
| max_best_day_share | 0.5985 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 67.6 | 70.9 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 611; total P&L per micro -2,947 USD
- Annualised Sharpe (daily, per micro): -0.75
- PSR (vs 0): 0.039; **Deflated Sharpe: 0.000** over 1365 recorded trials
  (Sharpe variance across trials 1.32e-03)
- Random-entry percentile: 0.269

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'q': 1.6, 's': 0.2, 'target': 'far25'} | -0.0430 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'q': 1.6, 's': 0.1, 'target': 'far25'} | -0.0489 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'q': 1.6, 's': 0.2, 'target': 'far25'} | -0.0510 | 1 | 40 | (0.0, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2022 | {'q': 1.6, 's': 0.2, 'target': 'far25'} | -0.0516 | 1 | 40 | (0.0, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2023 | {'q': 1.3, 's': 0.1, 'target': 'far25'} | -0.0341 | 8 | 10 | (0.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2024 | {'q': 1.3, 's': 0.1, 'target': 'far25'} | -0.0353 | 8 | 10 | (0.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2025 | {'q': 1.3, 's': 0.1, 'target': 'far25'} | -0.0333 | 8 | 10 | (0.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1704 | 0.0815 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -573.7 | -253.8 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 1.63 USD

## Evidence
![[wide_ib_rotation@ES-equity.png]]
![[wide_ib_rotation@ES-fan.png]]
![[wide_ib_rotation@ES-random.png]]
![[wide_ib_rotation@ES-drawdown.png]]
![[wide_ib_rotation@ES-monthly.png]]
![[wide_ib_rotation@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run wide_ib_rotation@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
