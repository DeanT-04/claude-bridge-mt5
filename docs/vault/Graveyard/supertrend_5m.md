---
type: strategy
strategy: supertrend_5m
family: supertrend
verdict: graveyard
plan: eod
run_id: 62d7ca9ca1
data_hash: b6e54fe4873dca2a[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# supertrend_5m: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'mult': 2.0, 'sl_atr': 2.0, 'align': True}; base sizes (micros)
{'eod': 2, 'intraday': 2}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 5.410640795478948), 'intraday': (0.0, 1.0, 5.410640795478948)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1888 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0181 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9810 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -555.5 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0417 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2211 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1884 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 5.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 13.0 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2211 | 0.1331 |
| eval_fail | 0.7722 | 0.8649 |
| eval_expired | 0.0067 | 0.0020 |
| median_sessions_to_pass | 5.0000 | 6.0000 |
| p90_sessions_to_pass | 13.0 | 12.0 |
| first_payout_given_pass | 0.1884 | 0.2475 |
| end_to_end_payout | 0.0417 | 0.0329 |
| mean_payouts_given_pass | 0.2401 | 1.0859 |
| ev_per_attempt | -520.7 | 62.4 |
| ev_p05 | -555.5 | -198.3 |
| ev_p95 | -480.6 | 407.1 |
| max_best_day_share | 1.3185 | 1.3308 |
| starts | 1488 | 1488 |
| effective_n | 372.0 | 496.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 1,888; total P&L per micro 8,270 USD
- Annualised Sharpe (daily, per micro): 0.51
- PSR (vs 0): 0.903; **Deflated Sharpe: 0.018** over 637 recorded trials
  (Sharpe variance across trials 7.08e-04)
- Random-entry percentile: 0.981

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'mult': 3.0, 'sl_atr': 2.0, 'align': True} | 0.0225 | 15 | 15 | (0.0, 1.0, 1.29) | (0.0, 0.5, 1.29) |
| 2020 | {'mult': 3.0, 'sl_atr': 2.0, 'align': True} | 0.0080 | 15 | 8 | (0.0, 1.0, 0.46) | (0.0, 1.0, 0.46) |
| 2021 | {'mult': 2.0, 'sl_atr': 2.0, 'align': True} | 0.0338 | 2 | 2 | (0.0, 1.0, 3.27) | (0.0, 1.0, 3.27) |
| 2022 | {'mult': 2.0, 'sl_atr': 2.0, 'align': True} | 0.0352 | 5 | 2 | (0.0, 1.0, 3.77) | (0.0, 1.0, 3.77) |
| 2023 | {'mult': 2.0, 'sl_atr': 2.0, 'align': True} | 0.0474 | 2 | 2 | (0.0, 1.0, 6.23) | (0.0, 1.0, 6.23) |
| 2024 | {'mult': 2.0, 'sl_atr': 2.0, 'align': True} | 0.0438 | 2 | 2 | (0.0, 1.0, 5.79) | (0.0, 1.0, 5.79) |
| 2025 | {'mult': 2.0, 'sl_atr': 2.0, 'align': True} | 0.0363 | 2 | 2 | (0.0, 1.0, 4.99) | (0.0, 1.0, 4.99) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2741 | 0.0852 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -588.1 | -254.0 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 0.92 USD

## Evidence
![[supertrend_5m-equity.png]]
![[supertrend_5m-fan.png]]
![[supertrend_5m-random.png]]
![[supertrend_5m-drawdown.png]]
![[supertrend_5m-monthly.png]]
![[supertrend_5m-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run supertrend_5m`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
