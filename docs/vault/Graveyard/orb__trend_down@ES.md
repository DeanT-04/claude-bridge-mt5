---
type: strategy
strategy: orb__trend_down@ES
family: opening_range
verdict: graveyard
plan: eod
run_id: ba9c225f9e
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# orb__trend_down@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660}; base sizes (micros)
{'eod': 8, 'intraday': 10}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.5, 0.36136917261655505), 'intraday': (0.0, 0.5, 0.36136917261655505)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 448 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.2250 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -561.8 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0054 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0780 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0690 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 6.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 17.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.0780 | 0.0309 |
| eval_fail | 0.2527 | 0.3770 |
| eval_expired | 0.6694 | 0.5921 |
| median_sessions_to_pass | 6.0000 | 3.0000 |
| p90_sessions_to_pass | 17.0 | 17.5 |
| first_payout_given_pass | 0.0690 | 0.0217 |
| end_to_end_payout | 0.0054 | 0.0007 |
| mean_payouts_given_pass | 0.1379 | 0.0217 |
| ev_per_attempt | -545.5 | -249.8 |
| ev_p05 | -561.8 | -251.6 |
| ev_p95 | -519.5 | -247.9 |
| max_best_day_share | 1.2742 | 0.7804 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 70.9 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 448; total P&L per micro -3,578 USD
- Annualised Sharpe (daily, per micro): -0.53
- PSR (vs 0): 0.091; **Deflated Sharpe: 0.000** over 1321 recorded trials
  (Sharpe variance across trials 1.26e-03)
- Random-entry percentile: 0.225

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'or_min': 30, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0064 | 12 | 10 | (0.0, 0.0, 0.2) | (0.0, 0.0, 0.2) |
| 2020 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0241 | 20 | 25 | (0.5, 1.0, 0.91) | (0.0, 1.0, 0.91) |
| 2021 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0049 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | -0.0064 | 10 | 12 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0063 | 25 | 40 | (2.0, 0.5, 0.29) | (2.0, 0.0, 0.29) |
| 2024 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0073 | 8 | 10 | (0.0, 0.5, 0.52) | (0.0, 0.5, 0.52) |
| 2025 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0099 | 8 | 10 | (0.0, 0.5, 0.69) | (0.0, 0.5, 0.69) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0926 | 0.0222 |
| end_to_end_payout | 0.0111 | 0.0037 |
| ev_per_attempt | -546.2 | -244.8 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 1.55 USD

## Evidence
![[orb__trend_down@ES-equity.png]]
![[orb__trend_down@ES-fan.png]]
![[orb__trend_down@ES-random.png]]
![[orb__trend_down@ES-drawdown.png]]
![[orb__trend_down@ES-monthly.png]]
![[orb__trend_down@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run orb__trend_down@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
