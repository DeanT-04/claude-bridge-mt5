---
type: strategy
strategy: twap_reversion
family: twap_reversion
verdict: graveyard
plan: eod
run_id: 85730dec33
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# twap_reversion: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'k': 0.5, 'sl_mult': 0.5, 'start': 600}; base sizes (micros)
{'eod': 3, 'intraday': 4}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1029 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.5730 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -557.8 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0067 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0524 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1282 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 4.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 18.3 | <= 30 | speed | PASS |

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
| eval_pass | 0.0524 | 0.0625 |
| eval_fail | 0.3065 | 0.6855 |
| eval_expired | 0.6411 | 0.2520 |
| median_sessions_to_pass | 4.0000 | 9.0000 |
| p90_sessions_to_pass | 18.3 | 19.0 |
| first_payout_given_pass | 0.1282 | 0.0000 |
| end_to_end_payout | 0.0067 | 0.0000 |
| mean_payouts_given_pass | 0.1282 | 0.0000 |
| ev_per_attempt | -549.5 | -252.7 |
| ev_p05 | -557.8 | -254.2 |
| ev_p95 | -540.4 | -251.2 |
| max_best_day_share | 1.2934 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 135.3 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 1,029; total P&L per micro -1,554 USD
- Annualised Sharpe (daily, per micro): -0.16
- PSR (vs 0): 0.347; **Deflated Sharpe: 0.000** over 673 recorded trials
  (Sharpe variance across trials 8.15e-04)
- Random-entry percentile: 0.573

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'k': 0.3, 'sl_mult': 0.5, 'start': 600} | -0.0798 | 50 | 40 | (2.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2020 | {'k': 0.5, 'sl_mult': 0.5, 'start': 600} | -0.0622 | 60 | 30 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'k': 0.5, 'sl_mult': 0.5, 'start': 600} | -0.0046 | 3 | 4 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'k': 0.5, 'sl_mult': 0.5, 'start': 600} | -0.0320 | 3 | 4 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'k': 0.5, 'sl_mult': 0.5, 'start': 600} | -0.0349 | 3 | 4 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2024 | {'k': 0.5, 'sl_mult': 0.5, 'start': 600} | -0.0295 | 3 | 4 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'k': 0.5, 'sl_mult': 0.5, 'start': 600} | -0.0192 | 3 | 4 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0222 | 0.0926 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -553.1 | -254.5 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -0.28 USD

## Evidence
![[twap_reversion-equity.png]]
![[twap_reversion-fan.png]]
![[twap_reversion-random.png]]
![[twap_reversion-drawdown.png]]
![[twap_reversion-monthly.png]]
![[twap_reversion-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run twap_reversion`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
