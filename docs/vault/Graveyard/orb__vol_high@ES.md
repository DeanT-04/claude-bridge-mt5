---
type: strategy
strategy: orb__vol_high@ES
family: opening_range
verdict: graveyard
plan: eod
run_id: e1478f52a3
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: 790a14f
seed: 11
---
# orb__vol_high@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660}; base sizes (micros)
{'eod': 6, 'intraday': 5}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.5, 0.3216526669466487), 'intraday': (0.0, 0.0, 0.3216526669466487)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 812 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.6230 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -563.7 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0262 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1747 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1500 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 6.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 17.1 | <= 30 | speed | PASS |

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
| eval_pass | 0.1747 | 0.0430 |
| eval_fail | 0.4845 | 0.5565 |
| eval_expired | 0.3407 | 0.4005 |
| median_sessions_to_pass | 6.0000 | 1.0000 |
| p90_sessions_to_pass | 17.1 | 17.7 |
| first_payout_given_pass | 0.1500 | 0.2812 |
| end_to_end_payout | 0.0262 | 0.0121 |
| mean_payouts_given_pass | 0.2692 | 0.2969 |
| ev_per_attempt | -507.2 | -237.2 |
| ev_p05 | -563.7 | -248.0 |
| ev_p95 | -465.6 | -230.5 |
| max_best_day_share | 1.3219 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 148.8 | 114.5 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 812; total P&L per micro -1,736 USD
- Annualised Sharpe (daily, per micro): -0.20
- PSR (vs 0): 0.310; **Deflated Sharpe: 0.000** over 1401 recorded trials
  (Sharpe variance across trials 1.34e-03)
- Random-entry percentile: 0.623

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0054 | 12 | 10 | (0.0, 1.0, 0.22) | (0.0, 1.0, 0.22) |
| 2020 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0249 | 12 | 10 | (0.0, 1.0, 1.04) | (0.0, 1.0, 1.04) |
| 2021 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | -0.0065 | 60 | 60 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0118 | 8 | 15 | (0.0, 0.0, 0.0) | (2.0, 0.0, 0.0) |
| 2023 | {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0006 | 8 | 15 | (0.0, 0.0, 0.0) | (2.0, 0.0, 0.0) |
| 2024 | {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0003 | 6 | 5 | (0.0, 0.5, 0.02) | (0.0, 0.0, 0.02) |
| 2025 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0034 | 12 | 10 | (0.0, 1.0, 0.27) | (0.0, 1.0, 0.27) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2074 | 0.0815 |
| end_to_end_payout | 0.0148 | 0.0000 |
| ev_per_attempt | -556.6 | -253.8 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -3.23 USD

## Evidence
![[orb__vol_high@ES-equity.png]]
![[orb__vol_high@ES-fan.png]]
![[orb__vol_high@ES-random.png]]
![[orb__vol_high@ES-drawdown.png]]
![[orb__vol_high@ES-monthly.png]]
![[orb__vol_high@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run orb__vol_high@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
