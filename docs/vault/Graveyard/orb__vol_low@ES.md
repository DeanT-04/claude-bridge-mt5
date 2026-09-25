---
type: strategy
strategy: orb__vol_low@ES
family: opening_range
verdict: graveyard
plan: eod
run_id: 0ace5d63f2
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: 790a14f
seed: 11
---
# orb__vol_low@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660}; base sizes (micros)
{'eod': 3, 'intraday': 3}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 0.32116757664845), 'intraday': (0.0, 1.0, 0.32116757664845)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 755 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.8200 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -570.1 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0040 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1405 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0287 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 6.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 17.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.1405 | 0.0632 |
| eval_fail | 0.4651 | 0.5739 |
| eval_expired | 0.3945 | 0.3629 |
| median_sessions_to_pass | 6.0000 | 6.0000 |
| p90_sessions_to_pass | 17.0 | 13.0 |
| first_payout_given_pass | 0.0287 | 0.0426 |
| end_to_end_payout | 0.0040 | 0.0027 |
| mean_payouts_given_pass | 0.0493 | 0.0795 |
| ev_per_attempt | -559.4 | -244.7 |
| ev_p05 | -570.1 | -252.6 |
| ev_p95 | -547.6 | -234.5 |
| max_best_day_share | 1.2258 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 114.5 | 135.3 |
| censored_pa | 6 | 6 |

## Statistics
- OOS trades: 755; total P&L per micro -948 USD
- Annualised Sharpe (daily, per micro): -0.21
- PSR (vs 0): 0.303; **Deflated Sharpe: 0.000** over 1457 recorded trials
  (Sharpe variance across trials 1.38e-03)
- Random-entry percentile: 0.820

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | -0.0272 | 60 | 30 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0112 | 20 | 20 | (0.5, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2021 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0254 | 30 | 30 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0303 | 8 | 8 | (1.0, 1.0, 0.75) | (1.0, 1.0, 0.75) |
| 2023 | {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0258 | 3 | 3 | (0.0, 1.0, 0.93) | (0.0, 1.0, 0.93) |
| 2024 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0016 | 3 | 3 | (0.0, 1.0, 0.07) | (0.0, 1.0, 0.07) |
| 2025 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0048 | 3 | 3 | (0.0, 1.0, 0.22) | (0.0, 1.0, 0.22) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0963 | 0.0222 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -563.4 | -250.3 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -1.63 USD

## Evidence
![[orb__vol_low@ES-equity.png]]
![[orb__vol_low@ES-fan.png]]
![[orb__vol_low@ES-random.png]]
![[orb__vol_low@ES-drawdown.png]]
![[orb__vol_low@ES-monthly.png]]
![[orb__vol_low@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run orb__vol_low@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
