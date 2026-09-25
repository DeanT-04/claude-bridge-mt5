---
type: strategy
strategy: intraday_momentum@ES
family: intraday_momentum
verdict: graveyard
plan: eod
run_id: 82866f7979
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: 790a14f
seed: 11
---
# intraday_momentum@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'threshold': 0.001, 'confirm_r12': True, 'sl_pct': nan}; base sizes (micros)
{'eod': 20, 'intraday': 20}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 488 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.2810 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -563.3 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0054 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0887 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0606 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 12.0 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 19.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.0887 | 0.0827 |
| eval_fail | 0.4409 | 0.5833 |
| eval_expired | 0.4704 | 0.3340 |
| median_sessions_to_pass | 12.0 | 12.0 |
| p90_sessions_to_pass | 19.0 | 19.0 |
| first_payout_given_pass | 0.0606 | 0.0244 |
| end_to_end_payout | 0.0054 | 0.0020 |
| mean_payouts_given_pass | 0.0606 | 0.0244 |
| ev_per_attempt | -556.9 | -252.3 |
| ev_p05 | -563.3 | -255.2 |
| ev_p95 | -549.1 | -248.8 |
| max_best_day_share | 1.2980 | 1.1230 |
| starts | 1488 | 1488 |
| effective_n | 74.4 | 106.3 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 488; total P&L per micro -2,603 USD
- Annualised Sharpe (daily, per micro): -0.73
- PSR (vs 0): 0.040; **Deflated Sharpe: 0.000** over 1557 recorded trials
  (Sharpe variance across trials 1.52e-03)
- Random-entry percentile: 0.281

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'threshold': 0.0025, 'confirm_r12': True, 'sl_pct': nan} | -0.0053 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'threshold': 0.0025, 'confirm_r12': True, 'sl_pct': nan} | -0.0165 | 20 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'threshold': 0.0025, 'confirm_r12': True, 'sl_pct': nan} | -0.0086 | 20 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'threshold': 0.0025, 'confirm_r12': True, 'sl_pct': nan} | -0.0155 | 20 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'threshold': 0.0025, 'confirm_r12': True, 'sl_pct': nan} | -0.0240 | 20 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2024 | {'threshold': 0.0025, 'confirm_r12': True, 'sl_pct': nan} | -0.0270 | 20 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'threshold': 0.0025, 'confirm_r12': True, 'sl_pct': nan} | -0.0360 | 20 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2407 | 0.1444 |
| end_to_end_payout | 0.0222 | 0.0222 |
| ev_per_attempt | -550.1 | -224.2 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -3.62 USD

## Evidence
![[intraday_momentum@ES-equity.png]]
![[intraday_momentum@ES-fan.png]]
![[intraday_momentum@ES-random.png]]
![[intraday_momentum@ES-drawdown.png]]
![[intraday_momentum@ES-monthly.png]]
![[intraday_momentum@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run intraday_momentum@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
