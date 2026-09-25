---
type: strategy
strategy: nr_breakout
family: narrow_range
verdict: graveyard
plan: eod
run_id: 412877703c
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# nr_breakout: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'nr': 4, 'sl_frac': 0.5, 'tp_mult': 2.0}; base sizes (micros)
{'eod': 5, 'intraday': 4}; sizing policy (alpha, beta, mu) {'eod': (0.5, 1.0, 3.1360930281394297), 'intraday': (0.0, 0.5, 3.1360930281394297)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 288 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0040 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.8010 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -556.7 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0423 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2392 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1770 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 7.5000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 16.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.2392 | 0.1398 |
| eval_fail | 0.5612 | 0.8159 |
| eval_expired | 0.1996 | 0.0444 |
| median_sessions_to_pass | 7.5000 | 6.0000 |
| p90_sessions_to_pass | 16.0 | 15.0 |
| first_payout_given_pass | 0.1770 | 0.1683 |
| end_to_end_payout | 0.0423 | 0.0235 |
| mean_payouts_given_pass | 0.1826 | 0.1683 |
| ev_per_attempt | -520.3 | -222.4 |
| ev_p05 | -556.7 | -248.8 |
| ev_p95 | -475.4 | -188.5 |
| max_best_day_share | 1.3053 | 1.1083 |
| starts | 1488 | 1488 |
| effective_n | 135.3 | 248.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 288; total P&L per micro 1,911 USD
- Annualised Sharpe (daily, per micro): 0.22
- PSR (vs 0): 0.716; **Deflated Sharpe: 0.004** over 477 recorded trials
  (Sharpe variance across trials 6.83e-04)
- Random-entry percentile: 0.801

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'nr': 4, 'sl_frac': 0.5, 'tp_mult': 2.0} | 0.0257 | 20 | 12 | (0.0, 0.5, 0.89) | (0.0, 1.0, 0.89) |
| 2020 | {'nr': 7, 'sl_frac': 0.5, 'tp_mult': 1.0} | 0.0252 | 40 | 25 | (0.5, 0.5, 0.54) | (0.0, 1.0, 0.54) |
| 2021 | {'nr': 7, 'sl_frac': 0.5, 'tp_mult': 2.0} | -0.0010 | 60 | 20 | (2.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2022 | {'nr': 7, 'sl_frac': 1.0, 'tp_mult': 2.0} | 0.0339 | 4 | 4 | (0.0, 0.5, 1.79) | (0.0, 0.5, 1.79) |
| 2023 | {'nr': 4, 'sl_frac': 1.0, 'tp_mult': 2.0} | 0.0269 | 4 | 5 | (0.0, 0.5, 2.43) | (1.0, 0.5, 2.43) |
| 2024 | {'nr': 7, 'sl_frac': 0.5, 'tp_mult': 2.0} | 0.0284 | 4 | 4 | (0.5, 1.0, 1.66) | (0.0, 1.0, 1.66) |
| 2025 | {'nr': 7, 'sl_frac': 0.5, 'tp_mult': 2.0} | 0.0345 | 5 | 5 | (0.5, 1.0, 2.11) | (0.5, 1.0, 2.11) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1185 | 0.0222 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -566.5 | -250.3 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -11.94 USD

## Evidence
![[nr_breakout-equity.png]]
![[nr_breakout-fan.png]]
![[nr_breakout-random.png]]
![[nr_breakout-drawdown.png]]
![[nr_breakout-monthly.png]]
![[nr_breakout-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run nr_breakout`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
