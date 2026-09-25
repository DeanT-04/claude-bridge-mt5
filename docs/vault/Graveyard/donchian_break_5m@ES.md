---
type: strategy
strategy: donchian_break_5m@ES
family: donchian_break
verdict: graveyard
plan: intraday
run_id: 610caf8b8e
data_hash: 2caacdca76e5ba37[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# donchian_break_5m@ES: **GRAVEYARD**

Best plan: **Apex intraday 50K**. Final params {'n': 20, 'sl_atr': 2.0, 'tp_atr': 4.0}; base sizes (micros)
{'eod': 6, 'intraday': 6}; sizing policy (alpha, beta, mu) {'eod': (1.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 3767 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.8210 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -252.3 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0007 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0457 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0147 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 8.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 18.3 | <= 30 | speed | PASS |

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
| eval_pass | 0.0558 | 0.0457 |
| eval_fail | 0.3663 | 0.8562 |
| eval_expired | 0.5780 | 0.0981 |
| median_sessions_to_pass | 6.0000 | 8.0000 |
| p90_sessions_to_pass | 18.8 | 18.3 |
| first_payout_given_pass | 0.0000 | 0.0147 |
| end_to_end_payout | 0.0000 | 0.0007 |
| mean_payouts_given_pass | 0.0000 | 0.0294 |
| ev_per_attempt | -557.8 | -249.3 |
| ev_p05 | -560.9 | -252.3 |
| ev_p95 | -555.0 | -245.1 |
| max_best_day_share | 1.1205 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 212.6 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 3,767; total P&L per micro -9,311 USD
- Annualised Sharpe (daily, per micro): -0.85
- PSR (vs 0): 0.017; **Deflated Sharpe: 0.000** over 777 recorded trials
  (Sharpe variance across trials 9.74e-04)
- Random-entry percentile: 0.821

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'n': 20, 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0945 | 6 | 6 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'n': 55, 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.1027 | 1 | 20 | (0.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2021 | {'n': 20, 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.1131 | 6 | 6 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'n': 55, 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0884 | 10 | 30 | (1.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'n': 20, 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0563 | 6 | 6 | (1.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2024 | {'n': 20, 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0540 | 6 | 6 | (1.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'n': 20, 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0476 | 6 | 6 | (1.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2074 | 0.2000 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -578.8 | -260.8 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 4.38 USD

## Evidence
![[donchian_break_5m@ES-equity.png]]
![[donchian_break_5m@ES-fan.png]]
![[donchian_break_5m@ES-random.png]]
![[donchian_break_5m@ES-drawdown.png]]
![[donchian_break_5m@ES-monthly.png]]
![[donchian_break_5m@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run donchian_break_5m@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
