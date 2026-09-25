---
type: strategy
strategy: orb
family: opening_range
verdict: graveyard
plan: eod
run_id: 87f87a9f46
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 5455e7a-dirty
seed: 11
---
# orb: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660}; sizes (micros)
{'eod': 5, 'intraday': 4}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1589 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.1371 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9950 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -477.1 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0376 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2406 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1564 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 3.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 8.0000 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2406 | 0.1552 |
| eval_fail | 0.7016 | 0.8448 |
| eval_expired | 0.0578 | 0.0000 |
| median_sessions_to_pass | 3.0000 | 2.0000 |
| p90_sessions_to_pass | 8.0000 | 8.0000 |
| first_payout_given_pass | 0.1564 | 0.1991 |
| end_to_end_payout | 0.0376 | 0.0309 |
| mean_payouts_given_pass | 0.5056 | 0.5887 |
| ev_per_attempt | -344.2 | -61.3 |
| ev_p05 | -477.1 | -185.1 |
| ev_p95 | -182.9 | 101.3 |
| max_best_day_share | 1.3966 | 1.3251 |
| starts | 1488 | 1488 |
| effective_n | 297.6 | 744.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 1,589; total P&L per micro 12,552 USD
- Annualised Sharpe (daily, per micro): 0.78
- PSR (vs 0): 0.979; **Deflated Sharpe: 0.137** over 17 recorded trials
  (Sharpe variance across trials 1.71e-03)
- Random-entry percentile: 0.995

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday |
|---|---|---|---|---|
| 2019 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0107 | 12 | 60 |
| 2020 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0079 | 25 | 20 |
| 2021 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0125 | 15 | 15 |
| 2022 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0384 | 6 | 8 |
| 2023 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0381 | 6 | 8 |
| 2024 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0379 | 8 | 4 |
| 2025 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0503 | 5 | 4 |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2593 | 0.1667 |
| end_to_end_payout | 0.0259 | 0.0037 |
| ev_per_attempt | -524.9 | -245.9 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 3.66 USD

## Evidence
![[orb-equity.png]]
![[orb-fan.png]]
![[orb-random.png]]
![[orb-drawdown.png]]
![[orb-monthly.png]]
![[orb-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run orb`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
