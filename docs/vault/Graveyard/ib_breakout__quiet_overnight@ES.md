---
type: strategy
strategy: ib_breakout__quiet_overnight@ES
family: initial_balance
verdict: graveyard
plan: eod
run_id: d8315eca57
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# ib_breakout__quiet_overnight@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5}; base sizes (micros)
{'eod': 8, 'intraday': 5}; sizing policy (alpha, beta, mu) {'eod': (1.0, 1.0, 1.0258158336833305), 'intraday': (0.5, 1.0, 1.0258158336833305)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 375 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0010 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9800 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -500.7 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0531 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2245 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2365 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 6.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 17.0 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2245 | 0.0585 |
| eval_fail | 0.5336 | 0.8172 |
| eval_expired | 0.2419 | 0.1243 |
| median_sessions_to_pass | 6.0000 | 3.0000 |
| p90_sessions_to_pass | 17.0 | 11.0 |
| first_payout_given_pass | 0.2365 | 0.3448 |
| end_to_end_payout | 0.0531 | 0.0202 |
| mean_payouts_given_pass | 0.6377 | 0.9310 |
| ev_per_attempt | -336.6 | -146.6 |
| ev_p05 | -500.7 | -228.8 |
| ev_p95 | -141.9 | -56.8 |
| max_best_day_share | 1.4100 | 1.0588 |
| starts | 1488 | 1488 |
| effective_n | 148.8 | 248.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 375; total P&L per micro 1,473 USD
- Annualised Sharpe (daily, per micro): 0.45
- PSR (vs 0): 0.875; **Deflated Sharpe: 0.001** over 805 recorded trials
  (Sharpe variance across trials 1.05e-03)
- Random-entry percentile: 0.980

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 1.0, 'sl_frac': 0.5} | 0.0394 | 25 | 20 | (0.0, 1.0, 0.82) | (0.0, 1.0, 0.82) |
| 2020 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 1.0, 'sl_frac': 0.5} | 0.0254 | 25 | 20 | (0.0, 1.0, 0.51) | (0.0, 1.0, 0.51) |
| 2021 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 1.0, 'sl_frac': 0.5} | 0.0377 | 20 | 20 | (0.0, 1.0, 0.76) | (0.0, 1.0, 0.76) |
| 2022 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 1.0, 'sl_frac': 0.5} | 0.0214 | 20 | 20 | (0.0, 1.0, 0.44) | (0.0, 1.0, 0.44) |
| 2023 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 1.0, 'sl_frac': 0.5} | 0.0277 | 20 | 20 | (0.0, 1.0, 0.73) | (0.0, 1.0, 0.73) |
| 2024 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 1.0, 'sl_frac': 0.5} | 0.0191 | 20 | 20 | (0.0, 1.0, 0.53) | (0.0, 1.0, 0.53) |
| 2025 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 1.0, 'sl_frac': 0.5} | 0.0233 | 20 | 20 | (0.0, 1.0, 0.66) | (0.0, 1.0, 0.66) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2222 | 0.0778 |
| end_to_end_payout | 0.2000 | 0.0444 |
| ev_per_attempt | -13.5 | -190.8 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 5.31 USD

## Evidence
![[ib_breakout__quiet_overnight@ES-equity.png]]
![[ib_breakout__quiet_overnight@ES-fan.png]]
![[ib_breakout__quiet_overnight@ES-random.png]]
![[ib_breakout__quiet_overnight@ES-drawdown.png]]
![[ib_breakout__quiet_overnight@ES-monthly.png]]
![[ib_breakout__quiet_overnight@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ib_breakout__quiet_overnight@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
