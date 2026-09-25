---
type: strategy
strategy: ib_breakout__choppy
family: initial_balance
verdict: graveyard
plan: eod
run_id: 8019337196
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# ib_breakout__choppy: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'ib_min': 30, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5}; base sizes (micros)
{'eod': 4, 'intraday': 2}; sizing policy (alpha, beta, mu) {'eod': (2.0, 1.0, 6.482422721545565), 'intraday': (0.5, 1.0, 6.482422721545565)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 500 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0677 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9950 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -524.3 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0531 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1761 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.3015 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 5.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 15.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.1761 | 0.0934 |
| eval_fail | 0.5632 | 0.7675 |
| eval_expired | 0.2608 | 0.1391 |
| median_sessions_to_pass | 5.0000 | 6.0000 |
| p90_sessions_to_pass | 15.0 | 17.0 |
| first_payout_given_pass | 0.3015 | 0.2086 |
| end_to_end_payout | 0.0531 | 0.0195 |
| mean_payouts_given_pass | 0.4884 | 0.2590 |
| ev_per_attempt | -464.9 | -219.1 |
| ev_p05 | -524.3 | -242.3 |
| ev_p95 | -387.2 | -189.1 |
| max_best_day_share | 1.3228 | 1.2307 |
| starts | 1488 | 1488 |
| effective_n | 124.0 | 248.0 |
| censored_pa | 4 | 0 |

## Statistics
- OOS trades: 500; total P&L per micro 8,080 USD
- Annualised Sharpe (daily, per micro): 0.82
- PSR (vs 0): 0.986; **Deflated Sharpe: 0.068** over 169 recorded trials
  (Sharpe variance across trials 1.02e-03)
- Random-entry percentile: 0.995

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'ib_min': 60, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0535 | 20 | 20 | (0.0, 1.0, 1.06) | (0.0, 0.5, 1.06) |
| 2020 | {'ib_min': 60, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0455 | 20 | 20 | (0.0, 1.0, 0.94) | (0.0, 0.5, 0.94) |
| 2021 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0428 | 20 | 30 | (0.0, 1.0, 1.43) | (0.5, 0.5, 1.43) |
| 2022 | {'ib_min': 30, 'narrow': inf, 'tp_mult': 1.0, 'sl_frac': 0.5} | 0.0405 | 3 | 3 | (1.0, 1.0, 2.52) | (1.0, 1.0, 2.52) |
| 2023 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0561 | 4 | 4 | (0.0, 1.0, 4.96) | (0.0, 1.0, 4.96) |
| 2024 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0545 | 4 | 4 | (0.0, 1.0, 4.91) | (0.0, 1.0, 4.91) |
| 2025 | {'ib_min': 30, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0610 | 4 | 2 | (2.0, 1.0, 5.96) | (0.5, 1.0, 5.96) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2185 | 0.1037 |
| end_to_end_payout | 0.0037 | 0.0000 |
| ev_per_attempt | -575.8 | -255.1 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -1.58 USD

## Evidence
![[ib_breakout__choppy-equity.png]]
![[ib_breakout__choppy-fan.png]]
![[ib_breakout__choppy-random.png]]
![[ib_breakout__choppy-drawdown.png]]
![[ib_breakout__choppy-monthly.png]]
![[ib_breakout__choppy-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ib_breakout__choppy`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
