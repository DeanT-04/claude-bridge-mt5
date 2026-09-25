---
type: strategy
strategy: rsi2_pullback_5m
family: rsi2_pullback
verdict: graveyard
plan: eod
run_id: 204545b970
data_hash: b6e54fe4873dca2a[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# rsi2_pullback_5m: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'trend': 100, 'lo': 10, 'sl_atr': 2.0, 'tp_atr': 2.0}; base sizes (micros)
{'eod': 5, 'intraday': 4}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 2768 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.3950 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -559.6 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0175 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1633 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1070 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 5.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 15.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.1633 | 0.1136 |
| eval_fail | 0.5934 | 0.8784 |
| eval_expired | 0.2433 | 0.0081 |
| median_sessions_to_pass | 5.0000 | 4.0000 |
| p90_sessions_to_pass | 15.0 | 12.0 |
| first_payout_given_pass | 0.1070 | 0.0769 |
| end_to_end_payout | 0.0175 | 0.0087 |
| mean_payouts_given_pass | 0.1358 | 0.0888 |
| ev_per_attempt | -544.7 | -241.8 |
| ev_p05 | -559.6 | -249.9 |
| ev_p95 | -527.1 | -231.5 |
| max_best_day_share | 1.0283 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 186.0 | 496.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 2,768; total P&L per micro -6,576 USD
- Annualised Sharpe (daily, per micro): -0.59
- PSR (vs 0): 0.065; **Deflated Sharpe: 0.000** over 653 recorded trials
  (Sharpe variance across trials 7.79e-04)
- Random-entry percentile: 0.395

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'trend': 100, 'lo': 10, 'sl_atr': 2.0, 'tp_atr': 2.0} | -0.0290 | 1 | 12 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'trend': 100, 'lo': 5, 'sl_atr': 2.0, 'tp_atr': 1.0} | -0.0356 | 50 | 25 | (1.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'trend': 100, 'lo': 10, 'sl_atr': 2.0, 'tp_atr': 1.0} | -0.0135 | 15 | 12 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'trend': 100, 'lo': 10, 'sl_atr': 2.0, 'tp_atr': 1.0} | 0.0007 | 15 | 12 | (0.5, 0.0, 0.04) | (0.0, 0.5, 0.04) |
| 2023 | {'trend': 100, 'lo': 10, 'sl_atr': 2.0, 'tp_atr': 2.0} | 0.0064 | 5 | 12 | (0.0, 0.0, 0.6) | (0.0, 0.0, 0.6) |
| 2024 | {'trend': 200, 'lo': 10, 'sl_atr': 2.0, 'tp_atr': 2.0} | -0.0066 | 4 | 12 | (0.5, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2025 | {'trend': 200, 'lo': 10, 'sl_atr': 2.0, 'tp_atr': 2.0} | -0.0111 | 4 | 12 | (0.5, 0.0, 0.0) | (0.5, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2111 | 0.1222 |
| end_to_end_payout | 0.0111 | 0.0000 |
| ev_per_attempt | -562.7 | -256.2 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 7.77 USD

## Evidence
![[rsi2_pullback_5m-equity.png]]
![[rsi2_pullback_5m-fan.png]]
![[rsi2_pullback_5m-random.png]]
![[rsi2_pullback_5m-drawdown.png]]
![[rsi2_pullback_5m-monthly.png]]
![[rsi2_pullback_5m-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run rsi2_pullback_5m`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
