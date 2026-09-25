---
type: strategy
strategy: supertrend_5m@ES
family: supertrend
verdict: graveyard
plan: intraday
run_id: 5f2eb52855
data_hash: 2caacdca76e5ba37[1029:3800][0:2381]
commit: 790a14f
seed: 11
---
# supertrend_5m@ES: **GRAVEYARD**

Best plan: **Apex intraday 50K**. Final params {'mult': 3.0, 'sl_atr': 3.0, 'align': False}; base sizes (micros)
{'eod': 15, 'intraday': 4}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1964 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.6450 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -252.1 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0087 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0847 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1032 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 5.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 17.5 | <= 30 | speed | PASS |

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
| eval_pass | 0.1196 | 0.0847 |
| eval_fail | 0.5927 | 0.8017 |
| eval_expired | 0.2876 | 0.1136 |
| median_sessions_to_pass | 4.0000 | 5.0000 |
| p90_sessions_to_pass | 13.3 | 17.5 |
| first_payout_given_pass | 0.0112 | 0.1032 |
| end_to_end_payout | 0.0013 | 0.0087 |
| mean_payouts_given_pass | 0.0112 | 0.1032 |
| ev_per_attempt | -565.2 | -245.5 |
| ev_p05 | -570.3 | -252.1 |
| ev_p95 | -561.1 | -236.5 |
| max_best_day_share | 1.4492 | 1.1659 |
| starts | 1488 | 1488 |
| effective_n | 124.0 | 372.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 1,964; total P&L per micro -5,213 USD
- Annualised Sharpe (daily, per micro): -0.53
- PSR (vs 0): 0.093; **Deflated Sharpe: 0.000** over 1489 recorded trials
  (Sharpe variance across trials 1.50e-03)
- Random-entry percentile: 0.645

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'mult': 2.0, 'sl_atr': 2.0, 'align': True} | -0.0574 | 30 | 20 | (1.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'mult': 3.0, 'sl_atr': 3.0, 'align': True} | -0.0646 | 5 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'mult': 2.0, 'sl_atr': 2.0, 'align': True} | -0.0329 | 4 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'mult': 3.0, 'sl_atr': 3.0, 'align': True} | -0.0242 | 15 | 10 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'mult': 2.0, 'sl_atr': 2.0, 'align': True} | -0.0292 | 5 | 4 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2024 | {'mult': 3.0, 'sl_atr': 3.0, 'align': False} | -0.0194 | 15 | 4 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'mult': 3.0, 'sl_atr': 3.0, 'align': False} | -0.0107 | 15 | 4 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2481 | 0.1704 |
| end_to_end_payout | 0.0593 | 0.0481 |
| ev_per_attempt | -495.6 | -225.7 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 3.00 USD

## Evidence
![[supertrend_5m@ES-equity.png]]
![[supertrend_5m@ES-fan.png]]
![[supertrend_5m@ES-random.png]]
![[supertrend_5m@ES-drawdown.png]]
![[supertrend_5m@ES-monthly.png]]
![[supertrend_5m@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run supertrend_5m@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
