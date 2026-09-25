---
type: strategy
strategy: ib_breakout__vol_low
family: initial_balance
verdict: graveyard
plan: intraday
run_id: 0ea7788230
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# ib_breakout__vol_low: **GRAVEYARD**

Best plan: **Apex intraday 50K**. Final params {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 1.0}; base sizes (micros)
{'eod': 3, 'intraday': 2}; sizing policy (alpha, beta, mu) {'eod': (2.0, 1.0, 4.6504304913901455), 'intraday': (0.5, 1.0, 4.6504304913901455)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 602 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.1071 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9810 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -253.0 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0027 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0571 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0471 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 6.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 14.0 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- Holdout consistent
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0733 | 0.0571 |
| eval_fail | 0.3743 | 0.4610 |
| eval_expired | 0.5524 | 0.4819 |
| median_sessions_to_pass | 5.0000 | 6.0000 |
| p90_sessions_to_pass | 14.0 | 14.0 |
| first_payout_given_pass | 0.0183 | 0.0471 |
| end_to_end_payout | 0.0013 | 0.0027 |
| mean_payouts_given_pass | 0.0244 | 0.0471 |
| ev_per_attempt | -558.2 | -250.9 |
| ev_p05 | -562.9 | -253.0 |
| ev_p95 | -553.8 | -248.7 |
| max_best_day_share | 1.3138 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 78.3 |
| censored_pa | 27 | 0 |

## Statistics
- OOS trades: 602; total P&L per micro 6,654 USD
- Annualised Sharpe (daily, per micro): 0.72
- PSR (vs 0): 0.966; **Deflated Sharpe: 0.107** over 377 recorded trials
  (Sharpe variance across trials 6.61e-04)
- Random-entry percentile: 0.981

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 1.0, 'sl_frac': 0.5} | 0.0347 | 1 | 1 | (0.0, 0.0, 0.18) | (0.0, 0.0, 0.18) |
| 2020 | {'ib_min': 60, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0374 | 15 | 12 | (0.0, 1.0, 0.53) | (0.0, 1.0, 0.53) |
| 2021 | {'ib_min': 30, 'narrow': inf, 'tp_mult': 1.0, 'sl_frac': 1.0} | 0.0344 | 25 | 25 | (0.0, 1.0, 0.99) | (0.0, 0.5, 0.99) |
| 2022 | {'ib_min': 30, 'narrow': inf, 'tp_mult': 1.0, 'sl_frac': 1.0} | 0.0501 | 20 | 25 | (0.0, 0.5, 2.31) | (0.0, 0.5, 2.31) |
| 2023 | {'ib_min': 30, 'narrow': inf, 'tp_mult': 1.0, 'sl_frac': 1.0} | 0.0655 | 2 | 2 | (0.0, 1.0, 4.18) | (0.0, 1.0, 4.18) |
| 2024 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 1.0} | 0.0552 | 3 | 2 | (2.0, 1.0, 4.82) | (0.5, 1.0, 4.82) |
| 2025 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 1.0} | 0.0516 | 3 | 2 | (2.0, 1.0, 4.52) | (0.5, 1.0, 4.52) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0963 | 0.0667 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -563.4 | -252.9 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -4.76 USD

## Evidence
![[ib_breakout__vol_low-equity.png]]
![[ib_breakout__vol_low-fan.png]]
![[ib_breakout__vol_low-random.png]]
![[ib_breakout__vol_low-drawdown.png]]
![[ib_breakout__vol_low-monthly.png]]
![[ib_breakout__vol_low-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ib_breakout__vol_low`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
