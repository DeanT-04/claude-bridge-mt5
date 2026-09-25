---
type: strategy
strategy: ib_breakout__vix_low
family: initial_balance
verdict: graveyard
plan: eod
run_id: 5c7e066953
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# ib_breakout__vix_low: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'ib_min': 30, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 1.0}; base sizes (micros)
{'eod': 2, 'intraday': 2}; sizing policy (alpha, beta, mu) {'eod': (2.0, 1.0, 4.601590928181388), 'intraday': (1.0, 1.0, 4.601590928181388)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 882 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0357 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9750 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -505.2 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0827 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2124 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.3892 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 4.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 13.0 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2124 | 0.1237 |
| eval_fail | 0.4617 | 0.5907 |
| eval_expired | 0.3259 | 0.2856 |
| median_sessions_to_pass | 4.0000 | 4.0000 |
| p90_sessions_to_pass | 13.0 | 11.0 |
| first_payout_given_pass | 0.3892 | 0.3207 |
| end_to_end_payout | 0.0827 | 0.0397 |
| mean_payouts_given_pass | 0.4905 | 0.5761 |
| ev_per_attempt | -464.2 | -160.6 |
| ev_p05 | -505.2 | -210.7 |
| ev_p95 | -416.4 | -96.2 |
| max_best_day_share | 1.3018 | 1.0741 |
| starts | 1488 | 1488 |
| effective_n | 186.0 | 297.6 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 882; total P&L per micro 5,828 USD
- Annualised Sharpe (daily, per micro): 0.52
- PSR (vs 0): 0.910; **Deflated Sharpe: 0.036** over 333 recorded trials
  (Sharpe variance across trials 6.96e-04)
- Random-entry percentile: 0.975

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 1.0, 'sl_frac': 0.5} | 0.0032 | 12 | 10 | (0.0, 1.0, 0.12) | (0.0, 0.5, 0.12) |
| 2020 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 1.0, 'sl_frac': 0.5} | 0.0105 | 10 | 10 | (0.0, 1.0, 0.43) | (0.0, 0.5, 0.43) |
| 2021 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 1.0, 'sl_frac': 0.5} | 0.0184 | 12 | 10 | (0.0, 1.0, 0.71) | (0.0, 0.5, 0.71) |
| 2022 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 1.0, 'sl_frac': 0.5} | 0.0352 | 3 | 3 | (0.0, 1.0, 1.75) | (0.0, 1.0, 1.75) |
| 2023 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 1.0, 'sl_frac': 0.5} | 0.0341 | 3 | 3 | (0.0, 1.0, 1.7) | (0.0, 1.0, 1.7) |
| 2024 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 1.0} | 0.0394 | 2 | 2 | (1.0, 1.0, 3.05) | (0.0, 1.0, 3.05) |
| 2025 | {'ib_min': 30, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 1.0} | 0.0407 | 2 | 2 | (2.0, 1.0, 4.2) | (1.0, 1.0, 4.2) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2111 | 0.1148 |
| end_to_end_payout | 0.1481 | 0.0704 |
| ev_per_attempt | -205.2 | 20.4 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 2.03 USD

## Evidence
![[ib_breakout__vix_low-equity.png]]
![[ib_breakout__vix_low-fan.png]]
![[ib_breakout__vix_low-random.png]]
![[ib_breakout__vix_low-drawdown.png]]
![[ib_breakout__vix_low-monthly.png]]
![[ib_breakout__vix_low-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ib_breakout__vix_low`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
