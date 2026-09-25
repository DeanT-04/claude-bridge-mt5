---
type: strategy
strategy: orb__vix_high
family: opening_range
verdict: graveyard
plan: eod
run_id: c5d6c8a9be
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# orb__vix_high: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'or_min': 30, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660}; base sizes (micros)
{'eod': 20, 'intraday': 3}; sizing policy (alpha, beta, mu) {'eod': (1.0, 0.0, 3.891335363292758), 'intraday': (0.0, 0.0, 3.891335363292758)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 607 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0049 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9170 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -531.7 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0376 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1922 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1958 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 4.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 16.5 | <= 30 | speed | PASS |

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
| eval_pass | 0.1922 | 0.0625 |
| eval_fail | 0.3703 | 0.5780 |
| eval_expired | 0.4375 | 0.3595 |
| median_sessions_to_pass | 4.0000 | 6.0000 |
| p90_sessions_to_pass | 16.5 | 15.8 |
| first_payout_given_pass | 0.1958 | 0.1935 |
| end_to_end_payout | 0.0376 | 0.0121 |
| mean_payouts_given_pass | 0.3951 | 0.6452 |
| ev_per_attempt | -444.8 | -167.6 |
| ev_p05 | -531.7 | -247.7 |
| ev_p95 | -341.6 | -69.2 |
| max_best_day_share | 1.3328 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 93.0 | 148.8 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 607; total P&L per micro 4,815 USD
- Annualised Sharpe (daily, per micro): 0.41
- PSR (vs 0): 0.854; **Deflated Sharpe: 0.005** over 673 recorded trials
  (Sharpe variance across trials 8.15e-04)
- Random-entry percentile: 0.917

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0009 | 10 | 20 | (0.0, 1.0, 0.03) | (0.0, 1.0, 0.03) |
| 2020 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0242 | 10 | 20 | (0.0, 1.0, 0.81) | (0.0, 1.0, 0.81) |
| 2021 | {'or_min': 30, 'sl_frac': 0.5, 'tp_mult': 1.0, 'last_entry': 660} | 0.0179 | 5 | 30 | (0.0, 0.5, 1.1) | (0.0, 1.0, 1.1) |
| 2022 | {'or_min': 30, 'sl_frac': 0.5, 'tp_mult': 1.0, 'last_entry': 660} | 0.0222 | 8 | 5 | (0.5, 0.0, 1.53) | (0.0, 0.0, 1.53) |
| 2023 | {'or_min': 30, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0410 | 20 | 15 | (1.0, 0.0, 4.62) | (2.0, 0.0, 4.62) |
| 2024 | {'or_min': 30, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0385 | 20 | 15 | (1.0, 0.0, 4.12) | (2.0, 0.0, 4.12) |
| 2025 | {'or_min': 30, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0421 | 20 | 3 | (1.0, 0.0, 4.38) | (0.0, 0.0, 4.38) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1963 | 0.0074 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -577.3 | -249.4 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -6.97 USD

## Evidence
![[orb__vix_high-equity.png]]
![[orb__vix_high-fan.png]]
![[orb__vix_high-random.png]]
![[orb__vix_high-drawdown.png]]
![[orb__vix_high-monthly.png]]
![[orb__vix_high-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run orb__vix_high`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
