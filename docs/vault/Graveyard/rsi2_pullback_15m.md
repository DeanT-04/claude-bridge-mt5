---
type: strategy
strategy: rsi2_pullback_15m
family: rsi2_pullback
verdict: graveyard
plan: eod
run_id: 6d46718aea
data_hash: d223130e354eb243[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# rsi2_pullback_15m: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'trend': 200, 'lo': 5, 'sl_atr': 2.0, 'tp_atr': 2.0}; base sizes (micros)
{'eod': 8, 'intraday': 6}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 1.3543118274522417), 'intraday': (0.0, 0.0, 1.3543118274522417)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 986 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0024 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.8600 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -489.5 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0632 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2265 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2789 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 5.0000 | <= 15 | speed | PASS |
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
| eval_pass | 0.2265 | 0.0504 |
| eval_fail | 0.7050 | 0.8185 |
| eval_expired | 0.0685 | 0.1310 |
| median_sessions_to_pass | 5.0000 | 10.0 |
| p90_sessions_to_pass | 15.0 | 18.6 |
| first_payout_given_pass | 0.2789 | 0.2267 |
| end_to_end_payout | 0.0632 | 0.0114 |
| mean_payouts_given_pass | 0.6528 | 0.2400 |
| ev_per_attempt | -341.9 | -236.6 |
| ev_p05 | -489.5 | -248.8 |
| ev_p95 | -150.8 | -219.6 |
| max_best_day_share | 1.4437 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 248.0 | 372.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 986; total P&L per micro 1,898 USD
- Annualised Sharpe (daily, per micro): 0.20
- PSR (vs 0): 0.697; **Deflated Sharpe: 0.002** over 629 recorded trials
  (Sharpe variance across trials 7.15e-04)
- Random-entry percentile: 0.860

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'trend': 200, 'lo': 5, 'sl_atr': 2.0, 'tp_atr': 1.0} | -0.0090 | 50 | 40 | (0.0, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2020 | {'trend': 200, 'lo': 5, 'sl_atr': 2.0, 'tp_atr': 1.0} | -0.0093 | 20 | 40 | (0.0, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2021 | {'trend': 200, 'lo': 5, 'sl_atr': 2.0, 'tp_atr': 1.0} | 0.0217 | 12 | 10 | (0.0, 0.5, 0.72) | (0.0, 1.0, 0.72) |
| 2022 | {'trend': 200, 'lo': 10, 'sl_atr': 1.0, 'tp_atr': 2.0} | 0.0149 | 8 | 6 | (0.0, 0.5, 0.92) | (0.0, 1.0, 0.92) |
| 2023 | {'trend': 200, 'lo': 10, 'sl_atr': 2.0, 'tp_atr': 2.0} | 0.0256 | 8 | 3 | (0.0, 1.0, 2.24) | (0.0, 0.0, 2.24) |
| 2024 | {'trend': 200, 'lo': 10, 'sl_atr': 2.0, 'tp_atr': 2.0} | 0.0215 | 8 | 3 | (0.0, 1.0, 1.9) | (0.0, 1.0, 1.9) |
| 2025 | {'trend': 200, 'lo': 10, 'sl_atr': 2.0, 'tp_atr': 2.0} | 0.0179 | 8 | 3 | (0.0, 1.0, 1.64) | (0.0, 1.0, 1.64) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1630 | 0.0000 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -572.7 | -249.0 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -4.27 USD

## Evidence
![[rsi2_pullback_15m-equity.png]]
![[rsi2_pullback_15m-fan.png]]
![[rsi2_pullback_15m-random.png]]
![[rsi2_pullback_15m-drawdown.png]]
![[rsi2_pullback_15m-monthly.png]]
![[rsi2_pullback_15m-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run rsi2_pullback_15m`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
