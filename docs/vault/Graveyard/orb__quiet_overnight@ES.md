---
type: strategy
strategy: orb__quiet_overnight@ES
family: opening_range
verdict: graveyard
plan: eod
run_id: 807d7542da
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: 790a14f
seed: 11
---
# orb__quiet_overnight@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660}; base sizes (micros)
{'eod': 60, 'intraday': 8}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 376 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.8360 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -583.5 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0195 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2460 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0792 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 7.0000 | <= 15 | speed | PASS |
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
| eval_pass | 0.2460 | 0.0679 |
| eval_fail | 0.5282 | 0.8333 |
| eval_expired | 0.2258 | 0.0988 |
| median_sessions_to_pass | 7.0000 | 4.0000 |
| p90_sessions_to_pass | 17.0 | 9.0000 |
| first_payout_given_pass | 0.0792 | 0.0000 |
| end_to_end_payout | 0.0195 | 0.0000 |
| mean_payouts_given_pass | 0.0792 | 0.0000 |
| ev_per_attempt | -555.0 | -253.0 |
| ev_p05 | -583.5 | -254.8 |
| ev_p95 | -524.9 | -251.4 |
| max_best_day_share | 1.3182 | 1.1464 |
| starts | 1488 | 1488 |
| effective_n | 165.3 | 297.6 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 376; total P&L per micro 346 USD
- Annualised Sharpe (daily, per micro): 0.08
- PSR (vs 0): 0.580; **Deflated Sharpe: 0.000** over 1365 recorded trials
  (Sharpe variance across trials 1.32e-03)
- Random-entry percentile: 0.836

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0310 | 50 | 60 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0215 | 50 | 50 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0084 | 50 | 50 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0171 | 50 | 50 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0062 | 50 | 50 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2024 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0127 | 60 | 60 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0101 | 1 | 60 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1556 | 0.1963 |
| end_to_end_payout | 0.0074 | 0.0815 |
| ev_per_attempt | -549.4 | -121.7 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 6.70 USD

## Evidence
![[orb__quiet_overnight@ES-equity.png]]
![[orb__quiet_overnight@ES-fan.png]]
![[orb__quiet_overnight@ES-random.png]]
![[orb__quiet_overnight@ES-drawdown.png]]
![[orb__quiet_overnight@ES-monthly.png]]
![[orb__quiet_overnight@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run orb__quiet_overnight@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
