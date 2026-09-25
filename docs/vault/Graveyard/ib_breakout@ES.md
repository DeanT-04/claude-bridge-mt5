---
type: strategy
strategy: ib_breakout@ES
family: initial_balance
verdict: graveyard
plan: eod
run_id: c790fd7b9c
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: 790a14f
seed: 11
---
# ib_breakout@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5}; base sizes (micros)
{'eod': 10, 'intraday': 5}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 2.088785699286008), 'intraday': (0.0, 1.0, 2.088785699286008)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1519 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9970 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -503.5 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0430 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2110 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2038 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 2.5000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 14.7 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2110 | 0.1290 |
| eval_fail | 0.6761 | 0.7083 |
| eval_expired | 0.1129 | 0.1626 |
| median_sessions_to_pass | 2.5000 | 7.5000 |
| p90_sessions_to_pass | 14.7 | 16.0 |
| first_payout_given_pass | 0.2038 | 0.1146 |
| end_to_end_payout | 0.0430 | 0.0148 |
| mean_payouts_given_pass | 0.5127 | 0.1875 |
| ev_per_attempt | -406.2 | -217.1 |
| ev_p05 | -503.5 | -240.6 |
| ev_p95 | -278.8 | -187.6 |
| max_best_day_share | 1.3824 | 1.3499 |
| starts | 1488 | 1488 |
| effective_n | 496.0 | 186.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 1,519; total P&L per micro 5,080 USD
- Annualised Sharpe (daily, per micro): 0.52
- PSR (vs 0): 0.912; **Deflated Sharpe: 0.000** over 1533 recorded trials
  (Sharpe variance across trials 1.51e-03)
- Random-entry percentile: 0.997

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | -0.0030 | 60 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | -0.0198 | 60 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | -0.0031 | 6 | 5 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | -0.0039 | 6 | 5 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0288 | 10 | 4 | (0.0, 1.0, 2.3) | (0.0, 0.5, 2.3) |
| 2024 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0191 | 10 | 4 | (0.0, 1.0, 1.51) | (0.0, 0.5, 1.51) |
| 2025 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0283 | 10 | 5 | (0.0, 1.0, 2.31) | (0.0, 1.0, 2.31) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2556 | 0.0741 |
| end_to_end_payout | 0.0963 | 0.0185 |
| ev_per_attempt | -444.5 | -238.9 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 3.03 USD

## Evidence
![[ib_breakout@ES-equity.png]]
![[ib_breakout@ES-fan.png]]
![[ib_breakout@ES-random.png]]
![[ib_breakout@ES-drawdown.png]]
![[ib_breakout@ES-monthly.png]]
![[ib_breakout@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ib_breakout@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
