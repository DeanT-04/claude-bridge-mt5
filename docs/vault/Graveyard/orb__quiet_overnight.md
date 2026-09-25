---
type: strategy
strategy: orb__quiet_overnight
family: opening_range
verdict: graveyard
plan: eod
run_id: 9d8c63c03d
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# orb__quiet_overnight: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660}; base sizes (micros)
{'eod': 12, 'intraday': 4}; sizing policy (alpha, beta, mu) {'eod': (1.0, 1.0, 2.42130785384295), 'intraday': (0.0, 1.0, 2.42130785384295)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 426 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0160 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9380 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -543.0 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0148 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1371 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1078 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 6.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 12.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.1371 | 0.0780 |
| eval_fail | 0.5766 | 0.8185 |
| eval_expired | 0.2863 | 0.1035 |
| median_sessions_to_pass | 6.0000 | 4.5000 |
| p90_sessions_to_pass | 12.0 | 12.5 |
| first_payout_given_pass | 0.1078 | 0.0345 |
| end_to_end_payout | 0.0148 | 0.0027 |
| mean_payouts_given_pass | 0.3578 | 0.0345 |
| ev_per_attempt | -482.0 | -250.1 |
| ev_p05 | -543.0 | -253.9 |
| ev_p95 | -403.7 | -245.6 |
| max_best_day_share | 1.3266 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 148.8 | 372.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 426; total P&L per micro 4,111 USD
- Annualised Sharpe (daily, per micro): 0.47
- PSR (vs 0): 0.887; **Deflated Sharpe: 0.016** over 565 recorded trials
  (Sharpe variance across trials 6.99e-04)
- Random-entry percentile: 0.938

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0055 | 50 | 60 | (2.0, 0.0, 0.1) | (2.0, 0.0, 0.1) |
| 2020 | {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0041 | 15 | 15 | (0.0, 1.0, 0.14) | (0.0, 1.0, 0.14) |
| 2021 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0182 | 15 | 12 | (2.0, 1.0, 0.65) | (1.0, 1.0, 0.65) |
| 2022 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0120 | 25 | 15 | (0.5, 0.0, 0.62) | (0.0, 0.5, 0.62) |
| 2023 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0316 | 12 | 12 | (1.0, 1.0, 2.12) | (1.0, 1.0, 2.12) |
| 2024 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0349 | 12 | 4 | (1.0, 1.0, 2.5) | (0.0, 1.0, 2.5) |
| 2025 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0320 | 12 | 4 | (1.0, 1.0, 2.39) | (0.0, 1.0, 2.39) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1407 | 0.0852 |
| end_to_end_payout | 0.0593 | 0.0778 |
| ev_per_attempt | -480.7 | -105.3 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 1.58 USD

## Evidence
![[orb__quiet_overnight-equity.png]]
![[orb__quiet_overnight-fan.png]]
![[orb__quiet_overnight-random.png]]
![[orb__quiet_overnight-drawdown.png]]
![[orb__quiet_overnight-monthly.png]]
![[orb__quiet_overnight-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run orb__quiet_overnight`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
