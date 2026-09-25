---
type: strategy
strategy: orb__trending
family: opening_range
verdict: graveyard
plan: eod
run_id: 8be5716edb
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# orb__trending: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660}; base sizes (micros)
{'eod': 5, 'intraday': 3}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 1.8205306593867805), 'intraday': (0.0, 1.0, 1.8205306593867805)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 840 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0005 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.6700 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -552.4 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0296 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1660 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1781 | >= 0.7 | commercial | FAIL |
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
| eval_pass | 0.1660 | 0.1008 |
| eval_fail | 0.6310 | 0.8804 |
| eval_expired | 0.2030 | 0.0188 |
| median_sessions_to_pass | 5.0000 | 3.0000 |
| p90_sessions_to_pass | 15.0 | 14.0 |
| first_payout_given_pass | 0.1781 | 0.1267 |
| end_to_end_payout | 0.0296 | 0.0128 |
| mean_payouts_given_pass | 0.2105 | 0.1467 |
| ev_per_attempt | -529.6 | -232.2 |
| ev_p05 | -552.4 | -247.5 |
| ev_p95 | -502.3 | -211.4 |
| max_best_day_share | 1.3302 | 1.2098 |
| starts | 1488 | 1488 |
| effective_n | 212.6 | 496.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 840; total P&L per micro -62 USD
- Annualised Sharpe (daily, per micro): -0.01
- PSR (vs 0): 0.494; **Deflated Sharpe: 0.000** over 589 recorded trials
  (Sharpe variance across trials 7.05e-04)
- Random-entry percentile: 0.670

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | -0.0056 | 15 | 60 | (1.0, 0.0, 0.0) | (2.0, 0.0, 0.0) |
| 2020 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | -0.0189 | 60 | 40 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0027 | 15 | 12 | (0.5, 1.0, 0.1) | (0.0, 1.0, 0.1) |
| 2022 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0048 | 2 | 2 | (0.0, 1.0, 0.29) | (0.0, 1.0, 0.29) |
| 2023 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0156 | 5 | 5 | (0.0, 1.0, 1.25) | (0.0, 1.0, 1.25) |
| 2024 | {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0112 | 12 | 12 | (0.5, 0.0, 1.19) | (0.5, 0.0, 1.19) |
| 2025 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0235 | 5 | 5 | (0.0, 1.0, 1.99) | (0.0, 1.0, 1.99) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2037 | 0.1926 |
| end_to_end_payout | 0.0185 | 0.0111 |
| ev_per_attempt | -550.5 | -243.7 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 1.75 USD

## Evidence
![[orb__trending-equity.png]]
![[orb__trending-fan.png]]
![[orb__trending-random.png]]
![[orb__trending-drawdown.png]]
![[orb__trending-monthly.png]]
![[orb__trending-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run orb__trending`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
