---
type: strategy
strategy: donchian_break_5m
family: donchian_break
verdict: graveyard
plan: eod
run_id: 937e43d235
data_hash: b6e54fe4873dca2a[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# donchian_break_5m: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'n': 20, 'sl_atr': 2.0, 'tp_atr': 4.0}; base sizes (micros)
{'eod': 8, 'intraday': 4}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 1.7931677176076608), 'intraday': (0.0, 0.0, 1.7931677176076608)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 3570 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0024 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9500 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -557.6 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0269 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2426 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1108 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 3.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 10.0 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2426 | 0.1075 |
| eval_fail | 0.7534 | 0.8723 |
| eval_expired | 0.0040 | 0.0202 |
| median_sessions_to_pass | 3.0000 | 4.0000 |
| p90_sessions_to_pass | 10.0 | 15.1 |
| first_payout_given_pass | 0.1108 | 0.1250 |
| end_to_end_payout | 0.0269 | 0.0134 |
| mean_payouts_given_pass | 0.1468 | 0.1750 |
| ev_per_attempt | -529.6 | -224.2 |
| ev_p05 | -557.6 | -245.2 |
| ev_p95 | -497.9 | -197.5 |
| max_best_day_share | 1.4344 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 496.0 | 744.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 3,570; total P&L per micro 4,410 USD
- Annualised Sharpe (daily, per micro): 0.22
- PSR (vs 0): 0.714; **Deflated Sharpe: 0.002** over 129 recorded trials
  (Sharpe variance across trials 1.03e-03)
- Random-entry percentile: 0.950

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'n': 55, 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0350 | 25 | 20 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'n': 55, 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0277 | 20 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'n': 55, 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0346 | 20 | 25 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'n': 20, 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0121 | 4 | 4 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'n': 20, 'sl_atr': 2.0, 'tp_atr': 4.0} | 0.0095 | 8 | 4 | (0.0, 0.0, 1.46) | (0.0, 0.0, 1.46) |
| 2024 | {'n': 20, 'sl_atr': 2.0, 'tp_atr': 4.0} | 0.0064 | 8 | 4 | (0.0, 0.0, 1.0) | (0.0, 0.0, 1.0) |
| 2025 | {'n': 20, 'sl_atr': 2.0, 'tp_atr': 4.0} | 0.0119 | 8 | 4 | (0.0, 0.0, 1.99) | (0.0, 0.0, 1.99) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2037 | 0.1407 |
| end_to_end_payout | 0.0074 | 0.0037 |
| ev_per_attempt | -567.2 | -252.5 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 5.75 USD

## Evidence
![[donchian_break_5m-equity.png]]
![[donchian_break_5m-fan.png]]
![[donchian_break_5m-random.png]]
![[donchian_break_5m-drawdown.png]]
![[donchian_break_5m-monthly.png]]
![[donchian_break_5m-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run donchian_break_5m`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
