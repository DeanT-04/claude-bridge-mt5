---
type: strategy
strategy: supertrend_15m
family: supertrend
verdict: graveyard
plan: eod
run_id: c65d48b6e5
data_hash: d223130e354eb243[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# supertrend_15m: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'mult': 2.0, 'sl_atr': 3.0, 'align': True}; base sizes (micros)
{'eod': 2, 'intraday': 2}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 3.143962716062405), 'intraday': (0.0, 1.0, 3.143962716062405)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 687 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0020 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.8500 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -570.1 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0215 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2056 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1046 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 5.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 14.5 | <= 30 | speed | PASS |

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
| eval_pass | 0.2056 | 0.0410 |
| eval_fail | 0.5249 | 0.7392 |
| eval_expired | 0.2695 | 0.2198 |
| median_sessions_to_pass | 5.0000 | 8.0000 |
| p90_sessions_to_pass | 14.5 | 20.0 |
| first_payout_given_pass | 0.1046 | 0.1803 |
| end_to_end_payout | 0.0215 | 0.0074 |
| mean_payouts_given_pass | 0.1046 | 0.2787 |
| ev_per_attempt | -553.7 | -235.8 |
| ev_p05 | -570.1 | -250.5 |
| ev_p95 | -534.9 | -215.4 |
| max_best_day_share | 1.3402 | 1.1029 |
| starts | 1488 | 1488 |
| effective_n | 186.0 | 297.6 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 687; total P&L per micro 3,689 USD
- Annualised Sharpe (daily, per micro): 0.28
- PSR (vs 0): 0.763; **Deflated Sharpe: 0.002** over 709 recorded trials
  (Sharpe variance across trials 7.97e-04)
- Random-entry percentile: 0.850

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'mult': 3.0, 'sl_atr': 3.0, 'align': True} | 0.0318 | 1 | 1 | (0.0, 0.0, 1.74) | (0.0, 0.0, 1.74) |
| 2020 | {'mult': 3.0, 'sl_atr': 3.0, 'align': True} | 0.0288 | 5 | 4 | (0.0, 1.0, 1.48) | (0.0, 1.0, 1.48) |
| 2021 | {'mult': 3.0, 'sl_atr': 3.0, 'align': True} | -0.0048 | 15 | 8 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'mult': 3.0, 'sl_atr': 3.0, 'align': True} | 0.0031 | 12 | 12 | (0.0, 0.5, 0.24) | (0.0, 1.0, 0.24) |
| 2023 | {'mult': 3.0, 'sl_atr': 3.0, 'align': True} | 0.0120 | 8 | 12 | (0.0, 1.0, 1.2) | (0.0, 1.0, 1.2) |
| 2024 | {'mult': 2.0, 'sl_atr': 3.0, 'align': True} | 0.0174 | 2 | 3 | (2.0, 1.0, 1.97) | (0.0, 0.0, 1.97) |
| 2025 | {'mult': 2.0, 'sl_atr': 3.0, 'align': True} | 0.0299 | 2 | 2 | (0.0, 1.0, 3.58) | (0.0, 1.0, 3.58) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1370 | 0.0444 |
| end_to_end_payout | 0.0704 | 0.0333 |
| ev_per_attempt | -518.9 | -225.4 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -4.76 USD

## Evidence
![[supertrend_15m-equity.png]]
![[supertrend_15m-fan.png]]
![[supertrend_15m-random.png]]
![[supertrend_15m-drawdown.png]]
![[supertrend_15m-monthly.png]]
![[supertrend_15m-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run supertrend_15m`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
