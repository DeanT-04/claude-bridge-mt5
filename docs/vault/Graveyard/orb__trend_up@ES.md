---
type: strategy
strategy: orb__trend_up@ES
family: opening_range
verdict: graveyard
plan: eod
run_id: 8a582e8c11
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: 790a14f
seed: 11
---
# orb__trend_up@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660}; base sizes (micros)
{'eod': 30, 'intraday': 25}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1108 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.8390 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -570.8 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0114 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1734 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0659 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 3.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 10.3 | <= 30 | speed | PASS |

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
| eval_pass | 0.1734 | 0.0699 |
| eval_fail | 0.7036 | 0.8401 |
| eval_expired | 0.1230 | 0.0901 |
| median_sessions_to_pass | 3.0000 | 2.0000 |
| p90_sessions_to_pass | 10.3 | 7.7000 |
| first_payout_given_pass | 0.0659 | 0.0481 |
| end_to_end_payout | 0.0114 | 0.0034 |
| mean_payouts_given_pass | 0.1240 | 0.0577 |
| ev_per_attempt | -541.5 | -247.1 |
| ev_p05 | -570.8 | -252.6 |
| ev_p95 | -520.7 | -243.4 |
| max_best_day_share | 1.3367 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 297.6 | 496.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 1,108; total P&L per micro -1,442 USD
- Annualised Sharpe (daily, per micro): -0.23
- PSR (vs 0): 0.280; **Deflated Sharpe: 0.000** over 1389 recorded trials
  (Sharpe variance across trials 1.34e-03)
- Random-entry percentile: 0.839

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0720 | 30 | 25 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | -0.0754 | 40 | 50 | (0.0, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2021 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | -0.0308 | 40 | 50 | (0.0, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2022 | {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0065 | 15 | 15 | (0.5, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2023 | {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0022 | 20 | 20 | (1.0, 0.5, 0.11) | (1.0, 0.5, 0.11) |
| 2024 | {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0138 | 15 | 10 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0121 | 15 | 10 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2333 | 0.0593 |
| end_to_end_payout | 0.0259 | 0.0037 |
| ev_per_attempt | -504.7 | -246.9 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -2.65 USD

## Evidence
![[orb__trend_up@ES-equity.png]]
![[orb__trend_up@ES-fan.png]]
![[orb__trend_up@ES-random.png]]
![[orb__trend_up@ES-drawdown.png]]
![[orb__trend_up@ES-monthly.png]]
![[orb__trend_up@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run orb__trend_up@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
