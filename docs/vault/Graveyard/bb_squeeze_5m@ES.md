---
type: strategy
strategy: bb_squeeze_5m@ES
family: bb_squeeze
verdict: graveyard
plan: intraday
run_id: 28f2279347
data_hash: 2caacdca76e5ba37[1029:3800][0:2381]
commit: 15230e7-dirty
seed: 11
---
# bb_squeeze_5m@ES: **GRAVEYARD**

Best plan: **Apex intraday 50K**. Final params {'q': 0.1, 'sl_atr': 2.0, 'tp_atr': 4.0}; base sizes (micros)
{'eod': 40, 'intraday': 15}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 400 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.2100 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -250.3 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0020 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0249 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0811 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 8.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 18.4 | <= 30 | speed | PASS |

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
| eval_pass | 0.0343 | 0.0249 |
| eval_fail | 0.1848 | 0.2661 |
| eval_expired | 0.7809 | 0.7090 |
| median_sessions_to_pass | 10.0 | 8.0000 |
| p90_sessions_to_pass | 17.0 | 18.4 |
| first_payout_given_pass | 0.0000 | 0.0811 |
| end_to_end_payout | 0.0000 | 0.0020 |
| mean_payouts_given_pass | 0.0000 | 0.0811 |
| ev_per_attempt | -554.8 | -247.4 |
| ev_p05 | -559.2 | -250.3 |
| ev_p95 | -551.3 | -242.8 |
| max_best_day_share | 1.3195 | 0.6439 |
| starts | 1488 | 1488 |
| effective_n | 67.6 | 70.9 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 400; total P&L per micro -2,175 USD
- Annualised Sharpe (daily, per micro): -0.89
- PSR (vs 0): 0.016; **Deflated Sharpe: 0.000** over 769 recorded trials
  (Sharpe variance across trials 8.60e-04)
- Random-entry percentile: 0.210

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'q': 0.1, 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.1028 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'q': 0.1, 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.1248 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'q': 0.1, 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0867 | 15 | 15 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'q': 0.1, 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0715 | 1 | 15 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'q': 0.1, 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0616 | 40 | 15 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2024 | {'q': 0.2, 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0553 | 30 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'q': 0.1, 'sl_atr': 2.0, 'tp_atr': 4.0} | -0.0491 | 40 | 15 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1259 | 0.0741 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -567.5 | -253.4 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -1.13 USD

## Evidence
![[bb_squeeze_5m@ES-equity.png]]
![[bb_squeeze_5m@ES-fan.png]]
![[bb_squeeze_5m@ES-random.png]]
![[bb_squeeze_5m@ES-drawdown.png]]
![[bb_squeeze_5m@ES-monthly.png]]
![[bb_squeeze_5m@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run bb_squeeze_5m@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
