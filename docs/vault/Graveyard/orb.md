---
type: strategy
strategy: orb
family: opening_range
verdict: graveyard
plan: eod
run_id: 28733b9457
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 38a600e-dirty
seed: 11
---
# orb: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660}; base sizes (micros)
{'eod': 2, 'intraday': 1}; sizing policy (alpha, beta, mu) {'eod': (0.5, 1.0, 8.39037757244852), 'intraday': (0.0, 1.0, 8.39037757244852)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1589 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0621 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9950 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -295.9 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0847 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2681 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.3158 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 3.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 8.0000 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- Holdout consistent
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2681 | 0.1687 |
| eval_fail | 0.7319 | 0.8280 |
| eval_expired | 0.0000 | 0.0034 |
| median_sessions_to_pass | 3.0000 | 3.0000 |
| p90_sessions_to_pass | 8.0000 | 12.0 |
| first_payout_given_pass | 0.3158 | 0.3347 |
| end_to_end_payout | 0.0847 | 0.0565 |
| mean_payouts_given_pass | 1.0576 | 0.7849 |
| ev_per_attempt | -93.1 | -92.3 |
| ev_p05 | -295.9 | -174.4 |
| ev_p95 | 155.4 | 11.0 |
| max_best_day_share | 1.3283 | 1.3251 |
| starts | 1488 | 1488 |
| effective_n | 496.0 | 496.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 1,589; total P&L per micro 12,552 USD
- Annualised Sharpe (daily, per micro): 0.78
- PSR (vs 0): 0.979; **Deflated Sharpe: 0.062** over 73 recorded trials
  (Sharpe variance across trials 1.28e-03)
- Random-entry percentile: 0.995

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0107 | 10 | 12 | (0.0, 1.0, 0.36) | (0.0, 1.0, 0.36) |
| 2020 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0079 | 10 | 12 | (0.0, 1.0, 0.28) | (0.0, 1.0, 0.28) |
| 2021 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0125 | 15 | 15 | (0.0, 1.0, 0.94) | (0.0, 0.0, 0.94) |
| 2022 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0384 | 4 | 2 | (0.0, 1.0, 3.47) | (0.5, 1.0, 3.47) |
| 2023 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0381 | 4 | 5 | (0.0, 1.0, 4.34) | (0.0, 0.5, 4.34) |
| 2024 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0379 | 2 | 1 | (0.5, 1.0, 5.92) | (0.0, 1.0, 5.92) |
| 2025 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0503 | 2 | 1 | (0.5, 1.0, 8.22) | (0.0, 1.0, 8.22) |

## Holdout (holdout already used 1x for these params: not re-run)
not run

## Evidence
![[orb-equity.png]]
![[orb-fan.png]]
![[orb-random.png]]
![[orb-drawdown.png]]
![[orb-monthly.png]]
![[orb-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run orb`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
