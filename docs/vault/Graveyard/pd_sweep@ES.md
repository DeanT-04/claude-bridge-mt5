---
type: strategy
strategy: pd_sweep@ES
family: liquidity_sweep
verdict: graveyard
plan: eod
run_id: 5cc1658cbb
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: 790a14f
seed: 11
---
# pd_sweep@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'end': 720, 'buf': 0.1, 'tp_frac': 0.5}; base sizes (micros)
{'eod': 30, 'intraday': 10}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 872 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.1720 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -564.5 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0094 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1082 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0870 | >= 0.7 | commercial | FAIL |
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
| eval_pass | 0.1082 | 0.0168 |
| eval_fail | 0.3884 | 0.5417 |
| eval_expired | 0.5034 | 0.4415 |
| median_sessions_to_pass | 4.0000 | 4.0000 |
| p90_sessions_to_pass | 13.0 | 8.6000 |
| first_payout_given_pass | 0.0870 | 0.0000 |
| end_to_end_payout | 0.0094 | 0.0000 |
| mean_payouts_given_pass | 0.0870 | 0.0000 |
| ev_per_attempt | -550.9 | -250.0 |
| ev_p05 | -564.5 | -250.7 |
| ev_p95 | -531.9 | -249.4 |
| max_best_day_share | 1.3196 | 1.1901 |
| starts | 1488 | 1488 |
| effective_n | 74.4 | 90.2 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 872; total P&L per micro -5,068 USD
- Annualised Sharpe (daily, per micro): -1.00
- PSR (vs 0): 0.010; **Deflated Sharpe: 0.000** over 1465 recorded trials
  (Sharpe variance across trials 1.39e-03)
- Random-entry percentile: 0.172

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'end': 720, 'buf': 0.05, 'tp_frac': 1.0} | -0.1026 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'end': 720, 'buf': 0.05, 'tp_frac': 1.0} | -0.0734 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'end': 720, 'buf': 0.1, 'tp_frac': 0.5} | -0.0141 | 30 | 10 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'end': 720, 'buf': 0.1, 'tp_frac': 0.5} | -0.0244 | 30 | 10 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'end': 720, 'buf': 0.05, 'tp_frac': 1.0} | -0.0248 | 1 | 30 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2024 | {'end': 720, 'buf': 0.1, 'tp_frac': 0.5} | -0.0463 | 30 | 10 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'end': 720, 'buf': 0.1, 'tp_frac': 0.5} | -0.0481 | 30 | 10 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2630 | 0.1593 |
| end_to_end_payout | 0.0185 | 0.0000 |
| ev_per_attempt | -558.8 | -258.4 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 3.36 USD

## Evidence
![[pd_sweep@ES-equity.png]]
![[pd_sweep@ES-fan.png]]
![[pd_sweep@ES-random.png]]
![[pd_sweep@ES-drawdown.png]]
![[pd_sweep@ES-monthly.png]]
![[pd_sweep@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run pd_sweep@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
