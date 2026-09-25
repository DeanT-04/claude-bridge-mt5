---
type: strategy
strategy: orb@ES
family: opening_range
verdict: graveyard
plan: eod
run_id: 65323e5bc5
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: 790a14f
seed: 11
---
# orb@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660}; base sizes (micros)
{'eod': 30, 'intraday': 10}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1553 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.6010 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -570.0 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0195 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2056 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0948 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 3.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 7.0000 | <= 30 | speed | PASS |

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
| eval_pass | 0.2056 | 0.0820 |
| eval_fail | 0.6996 | 0.8380 |
| eval_expired | 0.0948 | 0.0800 |
| median_sessions_to_pass | 3.0000 | 1.0000 |
| p90_sessions_to_pass | 7.0000 | 3.0000 |
| first_payout_given_pass | 0.0948 | 0.0492 |
| end_to_end_payout | 0.0195 | 0.0040 |
| mean_payouts_given_pass | 0.1046 | 0.0492 |
| ev_per_attempt | -552.8 | -247.8 |
| ev_p05 | -570.0 | -253.2 |
| ev_p95 | -541.6 | -240.9 |
| max_best_day_share | 1.3367 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 496.0 | 1,488.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 1,553; total P&L per micro -4,602 USD
- Annualised Sharpe (daily, per micro): -0.52
- PSR (vs 0): 0.096; **Deflated Sharpe: 0.000** over 1533 recorded trials
  (Sharpe variance across trials 1.51e-03)
- Random-entry percentile: 0.601

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | -0.0496 | 40 | 50 | (0.0, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2020 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | -0.0359 | 40 | 50 | (0.0, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2021 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | -0.0382 | 40 | 50 | (0.0, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2022 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0111 | 25 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0010 | 6 | 40 | (0.0, 1.0, 0.08) | (0.0, 0.0, 0.08) |
| 2024 | {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0110 | 6 | 4 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0034 | 30 | 10 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2370 | 0.1222 |
| end_to_end_payout | 0.0074 | 0.0037 |
| ev_per_attempt | -571.8 | -250.7 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -1.09 USD

## Evidence
![[orb@ES-equity.png]]
![[orb@ES-fan.png]]
![[orb@ES-random.png]]
![[orb@ES-drawdown.png]]
![[orb@ES-monthly.png]]
![[orb@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run orb@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
