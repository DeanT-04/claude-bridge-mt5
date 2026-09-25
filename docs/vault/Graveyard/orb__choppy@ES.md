---
type: strategy
strategy: orb__choppy@ES
family: opening_range
verdict: graveyard
plan: eod
run_id: b032ab5641
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# orb__choppy@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660}; base sizes (micros)
{'eod': 6, 'intraday': 5}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 1.076330848383023), 'intraday': (0.0, 1.0, 1.076330848383023)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 741 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9440 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -507.0 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0571 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2231 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2560 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 5.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 15.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.2231 | 0.0981 |
| eval_fail | 0.7144 | 0.7977 |
| eval_expired | 0.0625 | 0.1042 |
| median_sessions_to_pass | 5.0000 | 3.0000 |
| p90_sessions_to_pass | 15.0 | 12.0 |
| first_payout_given_pass | 0.2560 | 0.1233 |
| end_to_end_payout | 0.0571 | 0.0121 |
| mean_payouts_given_pass | 0.5452 | 0.1644 |
| ev_per_attempt | -397.8 | -229.7 |
| ev_p05 | -507.0 | -245.2 |
| ev_p95 | -286.4 | -210.3 |
| max_best_day_share | 1.3159 | 1.2100 |
| starts | 1488 | 1488 |
| effective_n | 248.0 | 372.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 741; total P&L per micro 827 USD
- Annualised Sharpe (daily, per micro): 0.14
- PSR (vs 0): 0.641; **Deflated Sharpe: 0.000** over 1333 recorded trials
  (Sharpe variance across trials 1.29e-03)
- Random-entry percentile: 0.944

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0016 | 60 | 30 | (2.0, 1.0, 0.04) | (2.0, 0.0, 0.04) |
| 2020 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0106 | 15 | 15 | (0.0, 1.0, 0.29) | (0.0, 1.0, 0.29) |
| 2021 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0067 | 15 | 15 | (0.0, 1.0, 0.27) | (1.0, 1.0, 0.27) |
| 2022 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0105 | 12 | 6 | (0.0, 1.0, 0.39) | (0.0, 1.0, 0.39) |
| 2023 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0249 | 6 | 6 | (0.0, 1.0, 1.15) | (0.0, 1.0, 1.15) |
| 2024 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0177 | 6 | 6 | (0.0, 1.0, 0.8) | (0.0, 1.0, 0.8) |
| 2025 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0195 | 6 | 6 | (0.0, 1.0, 0.89) | (0.0, 1.0, 0.89) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2963 | 0.1630 |
| end_to_end_payout | 0.0148 | 0.0074 |
| ev_per_attempt | -572.4 | -251.2 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -0.86 USD

## Evidence
![[orb__choppy@ES-equity.png]]
![[orb__choppy@ES-fan.png]]
![[orb__choppy@ES-random.png]]
![[orb__choppy@ES-drawdown.png]]
![[orb__choppy@ES-monthly.png]]
![[orb__choppy@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run orb__choppy@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
