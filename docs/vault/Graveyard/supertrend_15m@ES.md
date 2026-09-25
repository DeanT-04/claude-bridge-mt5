---
type: strategy
strategy: supertrend_15m@ES
family: supertrend
verdict: graveyard
plan: eod
run_id: 4834b49467
data_hash: c21e6fe846c4f1b4[1029:3800][0:2381]
commit: 790a14f
seed: 11
---
# supertrend_15m@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'mult': 3.0, 'sl_atr': 2.0, 'align': True}; base sizes (micros)
{'eod': 8, 'intraday': 8}; sizing policy (alpha, beta, mu) {'eod': (1.0, 1.0, 0.9329363727479677), 'intraday': (1.0, 1.0, 0.9329363727479677)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 980 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.6980 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -567.2 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0168 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1593 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1055 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 6.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 15.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.1593 | 0.0598 |
| eval_fail | 0.5773 | 0.8165 |
| eval_expired | 0.2634 | 0.1237 |
| median_sessions_to_pass | 6.0000 | 6.0000 |
| p90_sessions_to_pass | 15.0 | 15.0 |
| first_payout_given_pass | 0.1055 | 0.2022 |
| end_to_end_payout | 0.0168 | 0.0121 |
| mean_payouts_given_pass | 0.1055 | 0.2022 |
| ev_per_attempt | -552.5 | -234.4 |
| ev_p05 | -567.2 | -251.2 |
| ev_p95 | -534.5 | -210.1 |
| max_best_day_share | 1.3085 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 114.5 | 297.6 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 980; total P&L per micro -1,725 USD
- Annualised Sharpe (daily, per micro): -0.20
- PSR (vs 0): 0.311; **Deflated Sharpe: 0.000** over 1425 recorded trials
  (Sharpe variance across trials 1.34e-03)
- Random-entry percentile: 0.698

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'mult': 3.0, 'sl_atr': 3.0, 'align': False} | 0.0477 | 8 | 8 | (1.0, 1.0, 2.39) | (0.5, 1.0, 2.39) |
| 2020 | {'mult': 3.0, 'sl_atr': 2.0, 'align': False} | 0.0218 | 6 | 8 | (1.0, 1.0, 1.04) | (0.0, 1.0, 1.04) |
| 2021 | {'mult': 3.0, 'sl_atr': 3.0, 'align': False} | -0.0099 | 6 | 4 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'mult': 3.0, 'sl_atr': 2.0, 'align': False} | -0.0082 | 10 | 6 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'mult': 3.0, 'sl_atr': 2.0, 'align': False} | 0.0080 | 6 | 8 | (1.0, 1.0, 0.6) | (0.0, 1.0, 0.6) |
| 2024 | {'mult': 3.0, 'sl_atr': 2.0, 'align': True} | 0.0149 | 8 | 5 | (1.0, 1.0, 0.85) | (0.0, 1.0, 0.85) |
| 2025 | {'mult': 3.0, 'sl_atr': 2.0, 'align': True} | 0.0166 | 8 | 8 | (1.0, 1.0, 0.98) | (1.0, 1.0, 0.98) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1741 | 0.0704 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -574.2 | -253.2 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -7.83 USD

## Evidence
![[supertrend_15m@ES-equity.png]]
![[supertrend_15m@ES-fan.png]]
![[supertrend_15m@ES-random.png]]
![[supertrend_15m@ES-drawdown.png]]
![[supertrend_15m@ES-monthly.png]]
![[supertrend_15m@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run supertrend_15m@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
