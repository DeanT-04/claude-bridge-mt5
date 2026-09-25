---
type: strategy
strategy: donchian_break_15m
family: donchian_break
verdict: graveyard
plan: eod
run_id: 699ae05611
data_hash: d223130e354eb243[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# donchian_break_15m: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'n': 55, 'sl_atr': 1.0, 'tp_atr': 4.0}; base sizes (micros)
{'eod': 4, 'intraday': 4}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 4.664533201988431), 'intraday': (0.0, 0.5, 4.664533201988431)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1996 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0098 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9520 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -536.1 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0349 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2863 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1221 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 3.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 9.0000 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2863 | 0.0672 |
| eval_fail | 0.7124 | 0.9005 |
| eval_expired | 0.0013 | 0.0323 |
| median_sessions_to_pass | 3.0000 | 4.0000 |
| p90_sessions_to_pass | 9.0000 | 11.0 |
| first_payout_given_pass | 0.1221 | 0.2600 |
| end_to_end_payout | 0.0349 | 0.0175 |
| mean_payouts_given_pass | 0.2371 | 0.2600 |
| ev_per_attempt | -482.0 | -237.1 |
| ev_p05 | -536.1 | -248.6 |
| ev_p95 | -416.5 | -223.2 |
| max_best_day_share | 1.3292 | 1.3008 |
| starts | 1488 | 1488 |
| effective_n | 372.0 | 744.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 1,996; total P&L per micro 5,559 USD
- Annualised Sharpe (daily, per micro): 0.38
- PSR (vs 0): 0.833; **Deflated Sharpe: 0.010** over 121 recorded trials
  (Sharpe variance across trials 9.84e-04)
- Random-entry percentile: 0.952

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'n': 55, 'sl_atr': 1.0, 'tp_atr': 4.0} | 0.0608 | 10 | 5 | (0.5, 1.0, 2.92) | (0.5, 1.0, 2.92) |
| 2020 | {'n': 55, 'sl_atr': 1.0, 'tp_atr': 4.0} | 0.0384 | 10 | 8 | (0.5, 1.0, 1.85) | (0.0, 1.0, 1.85) |
| 2021 | {'n': 55, 'sl_atr': 2.0, 'tp_atr': 4.0} | 0.0227 | 6 | 8 | (0.5, 1.0, 1.9) | (0.0, 1.0, 1.9) |
| 2022 | {'n': 55, 'sl_atr': 2.0, 'tp_atr': 2.0} | 0.0275 | 5 | 6 | (0.0, 1.0, 2.54) | (0.0, 1.0, 2.54) |
| 2023 | {'n': 55, 'sl_atr': 2.0, 'tp_atr': 2.0} | 0.0541 | 3 | 2 | (0.0, 1.0, 6.36) | (0.0, 1.0, 6.36) |
| 2024 | {'n': 55, 'sl_atr': 1.0, 'tp_atr': 4.0} | 0.0510 | 4 | 3 | (0.0, 1.0, 5.21) | (0.0, 1.0, 5.21) |
| 2025 | {'n': 55, 'sl_atr': 1.0, 'tp_atr': 4.0} | 0.0526 | 4 | 4 | (0.0, 1.0, 5.75) | (0.0, 0.5, 5.75) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2741 | 0.0963 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -588.1 | -254.7 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 0.90 USD

## Evidence
![[donchian_break_15m-equity.png]]
![[donchian_break_15m-fan.png]]
![[donchian_break_15m-random.png]]
![[donchian_break_15m-drawdown.png]]
![[donchian_break_15m-monthly.png]]
![[donchian_break_15m-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run donchian_break_15m`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
