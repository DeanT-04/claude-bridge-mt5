---
type: strategy
strategy: ib_breakout__vix_high
family: initial_balance
verdict: graveyard
plan: eod
run_id: 29b2dd2da2
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# ib_breakout__vix_high: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5}; base sizes (micros)
{'eod': 2, 'intraday': 1}; sizing policy (alpha, beta, mu) {'eod': (2.0, 1.0, 4.707023099538008), 'intraday': (0.0, 1.0, 4.707023099538008)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 395 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0007 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.5670 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -560.1 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0074 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0894 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0827 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 3.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 15.8 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- Beats random entry (percentile)
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0894 | 0.0276 |
| eval_fail | 0.3051 | 0.4563 |
| eval_expired | 0.6055 | 0.5161 |
| median_sessions_to_pass | 3.0000 | 7.0000 |
| p90_sessions_to_pass | 15.8 | 20.0 |
| first_payout_given_pass | 0.0827 | 0.0000 |
| end_to_end_payout | 0.0074 | 0.0000 |
| mean_payouts_given_pass | 0.1043 | 0.0000 |
| ev_per_attempt | -550.3 | -250.6 |
| ev_p05 | -560.1 | -252.0 |
| ev_p95 | -537.4 | -249.5 |
| max_best_day_share | 1.3280 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 74.4 |
| censored_pa | 18 | 2 |

## Statistics
- OOS trades: 395; total P&L per micro -386 USD
- Annualised Sharpe (daily, per micro): -0.04
- PSR (vs 0): 0.461; **Deflated Sharpe: 0.001** over 333 recorded trials
  (Sharpe variance across trials 6.96e-04)
- Random-entry percentile: 0.567

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0063 | 6 | 4 | (0.0, 1.0, 0.25) | (0.0, 1.0, 0.25) |
| 2020 | {'ib_min': 30, 'narrow': inf, 'tp_mult': 1.0, 'sl_frac': 1.0} | 0.0167 | 10 | 20 | (0.5, 1.0, 0.58) | (0.0, 1.0, 0.58) |
| 2021 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 1.0} | 0.0341 | 12 | 10 | (0.0, 1.0, 1.49) | (0.0, 1.0, 1.49) |
| 2022 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 1.0} | 0.0259 | 12 | 10 | (0.0, 1.0, 1.13) | (0.0, 1.0, 1.13) |
| 2023 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0503 | 2 | 1 | (2.0, 1.0, 5.89) | (0.0, 1.0, 5.89) |
| 2024 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0452 | 2 | 1 | (2.0, 1.0, 5.08) | (0.0, 1.0, 5.08) |
| 2025 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0450 | 2 | 1 | (2.0, 1.0, 4.91) | (0.0, 1.0, 4.91) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1111 | 0.0333 |
| end_to_end_payout | 0.0000 | 0.0148 |
| ev_per_attempt | -565.4 | -235.5 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 6.58 USD

## Evidence
![[ib_breakout__vix_high-equity.png]]
![[ib_breakout__vix_high-fan.png]]
![[ib_breakout__vix_high-random.png]]
![[ib_breakout__vix_high-drawdown.png]]
![[ib_breakout__vix_high-monthly.png]]
![[ib_breakout__vix_high-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ib_breakout__vix_high`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
