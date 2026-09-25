---
type: strategy
strategy: ema_cross_5m
family: ema_cross
verdict: graveyard
plan: eod
run_id: db90272088
data_hash: b6e54fe4873dca2a[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# ema_cross_5m: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'pair': (20, 50), 'sl_atr': 2.0, 'tp_atr': 4.0}; base sizes (micros)
{'eod': 5, 'intraday': 2}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 2.0405218287779876), 'intraday': (0.0, 1.0, 2.0405218287779876)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1062 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.3320 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -551.6 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0249 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2090 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1190 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 4.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 11.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.2090 | 0.0538 |
| eval_fail | 0.7628 | 0.9409 |
| eval_expired | 0.0282 | 0.0054 |
| median_sessions_to_pass | 4.0000 | 3.0000 |
| p90_sessions_to_pass | 11.0 | 8.0000 |
| first_payout_given_pass | 0.1190 | 0.0625 |
| end_to_end_payout | 0.0249 | 0.0034 |
| mean_payouts_given_pass | 0.2122 | 0.1000 |
| ev_per_attempt | -512.5 | -243.1 |
| ev_p05 | -551.6 | -250.5 |
| ev_p95 | -465.6 | -232.9 |
| max_best_day_share | 1.3329 | 1.0877 |
| starts | 1488 | 1488 |
| effective_n | 297.6 | 744.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 1,062; total P&L per micro -3,759 USD
- Annualised Sharpe (daily, per micro): -0.34
- PSR (vs 0): 0.196; **Deflated Sharpe: 0.000** over 153 recorded trials
  (Sharpe variance across trials 1.00e-03)
- Random-entry percentile: 0.332

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'pair': (50, 200), 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0062 | 60 | 40 | (1.0, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2020 | {'pair': (20, 50), 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0305 | 15 | 15 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'pair': (50, 200), 'sl_atr': 1.0, 'tp_atr': 4.0} | 0.0191 | 4 | 6 | (0.0, 1.0, 0.75) | (0.0, 1.0, 0.75) |
| 2022 | {'pair': (50, 200), 'sl_atr': 2.0, 'tp_atr': 4.0} | 0.0200 | 20 | 20 | (0.5, 0.5, 1.18) | (0.0, 0.5, 1.18) |
| 2023 | {'pair': (50, 200), 'sl_atr': 2.0, 'tp_atr': 4.0} | 0.0217 | 20 | 20 | (0.5, 0.5, 1.6) | (0.0, 0.5, 1.6) |
| 2024 | {'pair': (50, 200), 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0004 | 25 | 25 | (0.5, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2025 | {'pair': (20, 50), 'sl_atr': 2.0, 'tp_atr': 4.0} | 0.0124 | 5 | 2 | (0.0, 1.0, 1.39) | (0.0, 1.0, 1.39) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2185 | 0.1926 |
| end_to_end_payout | 0.0852 | 0.0222 |
| ev_per_attempt | -387.5 | -178.7 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -5.46 USD

## Evidence
![[ema_cross_5m-equity.png]]
![[ema_cross_5m-fan.png]]
![[ema_cross_5m-random.png]]
![[ema_cross_5m-drawdown.png]]
![[ema_cross_5m-monthly.png]]
![[ema_cross_5m-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ema_cross_5m`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
