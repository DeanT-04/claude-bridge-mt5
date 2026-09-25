---
type: strategy
strategy: rsi2_pullback_5m@ES
family: rsi2_pullback
verdict: graveyard
plan: intraday
run_id: 33e8cc578c
data_hash: 2caacdca76e5ba37[1029:3800][0:2381]
commit: 790a14f
seed: 11
---
# rsi2_pullback_5m@ES: **GRAVEYARD**

Best plan: **Apex intraday 50K**. Final params {'trend': 100, 'lo': 5, 'sl_atr': 2.0, 'tp_atr': 1.0}; base sizes (micros)
{'eod': 1, 'intraday': 1}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1674 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.1330 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -252.1 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0000 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0390 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0000 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 3.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 5.3000 | <= 30 | speed | PASS |

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
| eval_pass | 0.0349 | 0.0390 |
| eval_fail | 0.2870 | 0.6310 |
| eval_expired | 0.6781 | 0.3300 |
| median_sessions_to_pass | 3.5000 | 3.0000 |
| p90_sessions_to_pass | 7.0000 | 5.3000 |
| first_payout_given_pass | 0.0000 | 0.0000 |
| end_to_end_payout | 0.0000 | 0.0000 |
| mean_payouts_given_pass | 0.0000 | 0.0000 |
| ev_per_attempt | -554.9 | -251.3 |
| ev_p05 | -557.2 | -252.1 |
| ev_p95 | -552.6 | -250.6 |
| max_best_day_share | 1.3222 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 248.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 1,674; total P&L per micro -8,290 USD
- Annualised Sharpe (daily, per micro): -1.51
- PSR (vs 0): 0.000; **Deflated Sharpe: 0.000** over 1481 recorded trials
  (Sharpe variance across trials 1.50e-03)
- Random-entry percentile: 0.133

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'trend': 100, 'lo': 5, 'sl_atr': 2.0, 'tp_atr': 2.0} | -0.0461 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'trend': 100, 'lo': 5, 'sl_atr': 2.0, 'tp_atr': 2.0} | -0.0749 | 1 | 50 | (0.0, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2021 | {'trend': 200, 'lo': 5, 'sl_atr': 2.0, 'tp_atr': 2.0} | -0.0490 | 50 | 20 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'trend': 100, 'lo': 5, 'sl_atr': 2.0, 'tp_atr': 2.0} | -0.0619 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'trend': 200, 'lo': 5, 'sl_atr': 2.0, 'tp_atr': 2.0} | -0.0618 | 1 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2024 | {'trend': 200, 'lo': 5, 'sl_atr': 2.0, 'tp_atr': 2.0} | -0.0664 | 15 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'trend': 200, 'lo': 5, 'sl_atr': 2.0, 'tp_atr': 2.0} | -0.0709 | 15 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0000 | 0.0000 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -550.0 | -249.0 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 0.40 USD

## Evidence
![[rsi2_pullback_5m@ES-equity.png]]
![[rsi2_pullback_5m@ES-fan.png]]
![[rsi2_pullback_5m@ES-random.png]]
![[rsi2_pullback_5m@ES-drawdown.png]]
![[rsi2_pullback_5m@ES-monthly.png]]
![[rsi2_pullback_5m@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run rsi2_pullback_5m@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
