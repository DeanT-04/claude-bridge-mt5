---
type: strategy
strategy: bb_squeeze_15m
family: bb_squeeze
verdict: graveyard
plan: eod
run_id: e0353eb767
data_hash: d223130e354eb243[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# bb_squeeze_15m: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'q': 0.2, 'sl_atr': 1.0, 'tp_atr': 4.0}; base sizes (micros)
{'eod': 60, 'intraday': 25}; sizing policy (alpha, beta, mu) {'eod': (2.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 193 | >= 200 | stat | FAIL |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.3050 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -557.1 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0329 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1378 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2390 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 7.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 17.0 | <= 30 | speed | PASS |

Failed gates:
- OOS trades
- Deflated Sharpe
- Beats random entry (percentile)
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1378 | 0.0222 |
| eval_fail | 0.2137 | 0.6552 |
| eval_expired | 0.6485 | 0.3226 |
| median_sessions_to_pass | 7.0000 | 12.0 |
| p90_sessions_to_pass | 17.0 | 20.0 |
| first_payout_given_pass | 0.2390 | 0.6667 |
| end_to_end_payout | 0.0329 | 0.0148 |
| mean_payouts_given_pass | 0.2390 | 0.6667 |
| ev_per_attempt | -519.8 | -228.1 |
| ev_p05 | -557.1 | -249.5 |
| ev_p95 | -474.5 | -195.8 |
| max_best_day_share | 1.3113 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 114.5 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 193; total P&L per micro -1,120 USD
- Annualised Sharpe (daily, per micro): -0.34
- PSR (vs 0): 0.201; **Deflated Sharpe: 0.000** over 105 recorded trials
  (Sharpe variance across trials 1.06e-03)
- Random-entry percentile: 0.305

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'q': 0.2, 'sl_atr': 1.0, 'tp_atr': 4.0} | 0.0118 | 50 | 15 | (2.0, 1.0, 0.26) | (0.0, 0.5, 0.26) |
| 2020 | {'q': 0.2, 'sl_atr': 1.0, 'tp_atr': 4.0} | -0.0034 | 60 | 25 | (2.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'q': 0.2, 'sl_atr': 1.0, 'tp_atr': 4.0} | -0.0242 | 60 | 25 | (2.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'q': 0.1, 'sl_atr': 1.0, 'tp_atr': 4.0} | -0.0092 | 60 | 30 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'q': 0.1, 'sl_atr': 1.0, 'tp_atr': 4.0} | -0.0120 | 60 | 30 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2024 | {'q': 0.1, 'sl_atr': 1.0, 'tp_atr': 4.0} | -0.0108 | 60 | 30 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'q': 0.2, 'sl_atr': 1.0, 'tp_atr': 4.0} | -0.0029 | 60 | 25 | (2.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1926 | 0.0296 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -576.8 | -250.7 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 1.55 USD

## Evidence
![[bb_squeeze_15m-equity.png]]
![[bb_squeeze_15m-fan.png]]
![[bb_squeeze_15m-random.png]]
![[bb_squeeze_15m-drawdown.png]]
![[bb_squeeze_15m-monthly.png]]
![[bb_squeeze_15m-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run bb_squeeze_15m`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
