---
type: strategy
strategy: orb__vol_expanding@ES
family: opening_range
verdict: graveyard
plan: eod
run_id: c2b13fdae6
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: 790a14f
seed: 11
---
# orb__vol_expanding@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660}; base sizes (micros)
{'eod': 20, 'intraday': 6}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.5, 0.19518584628312072), 'intraday': (0.0, 1.0, 0.19518584628312072)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 718 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.4980 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -548.0 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0397 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2466 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1608 | >= 0.7 | commercial | FAIL |
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
| eval_pass | 0.2466 | 0.1290 |
| eval_fail | 0.6539 | 0.8199 |
| eval_expired | 0.0995 | 0.0511 |
| median_sessions_to_pass | 5.0000 | 5.0000 |
| p90_sessions_to_pass | 15.0 | 14.0 |
| first_payout_given_pass | 0.1608 | 0.1615 |
| end_to_end_payout | 0.0397 | 0.0208 |
| mean_payouts_given_pass | 0.3270 | 0.3802 |
| ev_per_attempt | -448.1 | -163.2 |
| ev_p05 | -548.0 | -246.1 |
| ev_p95 | -312.4 | -48.5 |
| max_best_day_share | 1.3328 | 1.2767 |
| starts | 1488 | 1488 |
| effective_n | 212.6 | 297.6 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 718; total P&L per micro -2,691 USD
- Annualised Sharpe (daily, per micro): -0.36
- PSR (vs 0): 0.184; **Deflated Sharpe: 0.000** over 1445 recorded trials
  (Sharpe variance across trials 1.37e-03)
- Random-entry percentile: 0.498

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | -0.0129 | 60 | 50 | (1.0, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2020 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0107 | 40 | 15 | (1.0, 0.5, 0.33) | (0.0, 0.5, 0.33) |
| 2021 | {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | -0.0183 | 25 | 15 | (1.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0098 | 20 | 6 | (0.0, 0.5, 0.52) | (0.0, 1.0, 0.52) |
| 2023 | {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0105 | 20 | 6 | (0.0, 0.5, 0.66) | (0.0, 1.0, 0.66) |
| 2024 | {'or_min': 15, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0061 | 20 | 6 | (0.0, 0.5, 0.38) | (0.0, 1.0, 0.38) |
| 2025 | {'or_min': 30, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | -0.0010 | 20 | 8 | (0.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1630 | 0.1444 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -572.7 | -257.5 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -4.75 USD

## Evidence
![[orb__vol_expanding@ES-equity.png]]
![[orb__vol_expanding@ES-fan.png]]
![[orb__vol_expanding@ES-random.png]]
![[orb__vol_expanding@ES-drawdown.png]]
![[orb__vol_expanding@ES-monthly.png]]
![[orb__vol_expanding@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run orb__vol_expanding@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
