---
type: strategy
strategy: ib_breakout__trend_down@ES
family: initial_balance
verdict: graveyard
plan: eod
run_id: 5afc04e1fd
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# ib_breakout__trend_down@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 1.0}; base sizes (micros)
{'eod': 5, 'intraday': 5}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 0.789058168836627), 'intraday': (0.0, 1.0, 0.789058168836627)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 290 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.4520 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -555.8 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0235 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0914 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2574 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 3.5000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 18.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.0914 | 0.0484 |
| eval_fail | 0.2984 | 0.3918 |
| eval_expired | 0.6102 | 0.5598 |
| median_sessions_to_pass | 3.5000 | 4.0000 |
| p90_sessions_to_pass | 18.0 | 18.9 |
| first_payout_given_pass | 0.2574 | 0.0972 |
| end_to_end_payout | 0.0235 | 0.0047 |
| mean_payouts_given_pass | 0.2574 | 0.0972 |
| ev_per_attempt | -531.4 | -248.6 |
| ev_p05 | -555.8 | -251.5 |
| ev_p95 | -499.4 | -244.7 |
| max_best_day_share | 1.3012 | 1.2884 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 70.9 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 290; total P&L per micro -1,191 USD
- Annualised Sharpe (daily, per micro): -0.22
- PSR (vs 0): 0.289; **Deflated Sharpe: 0.000** over 861 recorded trials
  (Sharpe variance across trials 1.04e-03)
- Random-entry percentile: 0.452

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0439 | 10 | 10 | (0.0, 1.0, 1.59) | (0.0, 1.0, 1.59) |
| 2020 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0448 | 10 | 10 | (0.0, 1.0, 1.54) | (0.0, 1.0, 1.54) |
| 2021 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 1.0} | 0.0272 | 5 | 5 | (0.0, 1.0, 0.67) | (0.0, 1.0, 0.67) |
| 2022 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 1.0} | 0.0324 | 5 | 5 | (0.0, 1.0, 0.75) | (0.0, 1.0, 0.75) |
| 2023 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0354 | 10 | 10 | (0.0, 1.0, 2.21) | (0.0, 1.0, 2.21) |
| 2024 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0320 | 10 | 10 | (0.0, 1.0, 1.96) | (0.0, 1.0, 1.96) |
| 2025 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0260 | 10 | 10 | (0.0, 1.0, 1.56) | (0.0, 1.0, 1.56) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0296 | 0.0333 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -554.1 | -251.0 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 0.09 USD

## Evidence
![[ib_breakout__trend_down@ES-equity.png]]
![[ib_breakout__trend_down@ES-fan.png]]
![[ib_breakout__trend_down@ES-random.png]]
![[ib_breakout__trend_down@ES-drawdown.png]]
![[ib_breakout__trend_down@ES-monthly.png]]
![[ib_breakout__trend_down@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ib_breakout__trend_down@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
