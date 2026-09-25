---
type: strategy
strategy: ib_breakout__trend_down
family: initial_balance
verdict: graveyard
plan: eod
run_id: 97c5ebb2af
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# ib_breakout__trend_down: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 0.5}; base sizes (micros)
{'eod': 5, 'intraday': 4}; sizing policy (alpha, beta, mu) {'eod': (1.0, 1.0, 1.4575413691726347), 'intraday': (2.0, 1.0, 1.4575413691726347)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 279 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0013 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.6650 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -561.8 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0013 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0645 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0208 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 3.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 14.5 | <= 30 | speed | PASS |

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
| eval_pass | 0.0645 | 0.0343 |
| eval_fail | 0.3737 | 0.4866 |
| eval_expired | 0.5618 | 0.4792 |
| median_sessions_to_pass | 3.0000 | 7.0000 |
| p90_sessions_to_pass | 14.5 | 16.0 |
| first_payout_given_pass | 0.0208 | 0.0000 |
| end_to_end_payout | 0.0013 | 0.0000 |
| mean_payouts_given_pass | 0.0208 | 0.0000 |
| ev_per_attempt | -557.0 | -251.0 |
| ev_p05 | -561.8 | -252.7 |
| ev_p95 | -552.1 | -249.7 |
| max_best_day_share | 1.2802 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 78.3 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 279; total P&L per micro 1,017 USD
- Annualised Sharpe (daily, per micro): 0.12
- PSR (vs 0): 0.621; **Deflated Sharpe: 0.001** over 217 recorded trials
  (Sharpe variance across trials 8.66e-04)
- Random-entry percentile: 0.665

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0351 | 12 | 12 | (0.0, 1.0, 1.47) | (0.5, 1.0, 1.47) |
| 2020 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0317 | 20 | 12 | (0.0, 0.5, 1.27) | (0.0, 1.0, 1.27) |
| 2021 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 1.0} | 0.0317 | 3 | 15 | (0.0, 1.0, 1.08) | (0.0, 1.0, 1.08) |
| 2022 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0155 | 20 | 15 | (0.0, 0.5, 0.42) | (0.0, 1.0, 0.42) |
| 2023 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0472 | 12 | 12 | (0.0, 1.0, 4.72) | (0.0, 1.0, 4.72) |
| 2024 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0445 | 20 | 12 | (1.0, 0.5, 4.35) | (0.0, 1.0, 4.35) |
| 2025 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0404 | 20 | 2 | (1.0, 0.5, 3.99) | (0.0, 0.5, 3.99) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0000 | 0.0037 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -550.0 | -249.2 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -5.97 USD

## Evidence
![[ib_breakout__trend_down-equity.png]]
![[ib_breakout__trend_down-fan.png]]
![[ib_breakout__trend_down-random.png]]
![[ib_breakout__trend_down-drawdown.png]]
![[ib_breakout__trend_down-monthly.png]]
![[ib_breakout__trend_down-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ib_breakout__trend_down`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
