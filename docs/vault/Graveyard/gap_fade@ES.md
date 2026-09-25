---
type: strategy
strategy: gap_fade@ES
family: gap
verdict: graveyard
plan: eod
run_id: f5a26ebea7
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: 790a14f
seed: 11
---
# gap_fade@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'g_min': 0.0025, 'g_max': 0.006, 'sl_mult': 0.5, 'exit_min': 720}; base sizes (micros)
{'eod': 60, 'intraday': 30}; sizing policy (alpha, beta, mu) {'eod': (2.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 625 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.8130 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -571.0 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0188 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2056 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0915 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 5.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 13.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.2056 | 0.1573 |
| eval_fail | 0.4973 | 0.7964 |
| eval_expired | 0.2970 | 0.0464 |
| median_sessions_to_pass | 5.0000 | 6.0000 |
| p90_sessions_to_pass | 13.0 | 13.0 |
| first_payout_given_pass | 0.0915 | 0.1111 |
| end_to_end_payout | 0.0188 | 0.0175 |
| mean_payouts_given_pass | 0.1375 | 0.1410 |
| ev_per_attempt | -538.0 | -222.6 |
| ev_p05 | -571.0 | -248.0 |
| ev_p95 | -489.4 | -192.0 |
| max_best_day_share | 1.3024 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 148.8 | 297.6 |
| censored_pa | 15 | 0 |

## Statistics
- OOS trades: 625; total P&L per micro -834 USD
- Annualised Sharpe (daily, per micro): -0.22
- PSR (vs 0): 0.291; **Deflated Sharpe: 0.000** over 1533 recorded trials
  (Sharpe variance across trials 1.51e-03)
- Random-entry percentile: 0.813

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'g_min': 0.0025, 'g_max': 0.012, 'sl_mult': 1.0, 'exit_min': 660} | -0.0214 | 40 | 15 | (2.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'g_min': 0.0025, 'g_max': 0.012, 'sl_mult': 1.0, 'exit_min': 660} | -0.0292 | 40 | 15 | (2.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'g_min': 0.0025, 'g_max': 0.006, 'sl_mult': 1.0, 'exit_min': 660} | 0.0087 | 40 | 30 | (0.0, 0.0, 0.21) | (0.5, 0.0, 0.21) |
| 2022 | {'g_min': 0.0025, 'g_max': 0.006, 'sl_mult': 0.5, 'exit_min': 660} | -0.0102 | 40 | 30 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'g_min': 0.0025, 'g_max': 0.006, 'sl_mult': 0.5, 'exit_min': 660} | -0.0088 | 40 | 30 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2024 | {'g_min': 0.0025, 'g_max': 0.006, 'sl_mult': 0.5, 'exit_min': 720} | -0.0126 | 60 | 30 | (2.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'g_min': 0.0025, 'g_max': 0.006, 'sl_mult': 0.5, 'exit_min': 720} | -0.0029 | 60 | 30 | (2.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1926 | 0.1074 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -576.8 | -255.3 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -2.18 USD

## Evidence
![[gap_fade@ES-equity.png]]
![[gap_fade@ES-fan.png]]
![[gap_fade@ES-random.png]]
![[gap_fade@ES-drawdown.png]]
![[gap_fade@ES-monthly.png]]
![[gap_fade@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run gap_fade@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
