---
type: strategy
strategy: ib_breakout__trend_up@ES
family: initial_balance
verdict: graveyard
plan: eod
run_id: c607849460
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# ib_breakout__trend_up@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5}; base sizes (micros)
{'eod': 4, 'intraday': 5}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 1.1021692566148822), 'intraday': (0.0, 0.5, 1.1021692566148822)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 891 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0003 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9880 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -530.5 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0329 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1458 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2258 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 4.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 14.0 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1458 | 0.0901 |
| eval_fail | 0.4509 | 0.6243 |
| eval_expired | 0.4032 | 0.2856 |
| median_sessions_to_pass | 4.0000 | 5.5000 |
| p90_sessions_to_pass | 14.0 | 15.0 |
| first_payout_given_pass | 0.2258 | 0.0597 |
| end_to_end_payout | 0.0329 | 0.0054 |
| mean_payouts_given_pass | 0.3687 | 0.1791 |
| ev_per_attempt | -482.9 | -221.7 |
| ev_p05 | -530.5 | -243.5 |
| ev_p95 | -426.0 | -195.7 |
| max_best_day_share | 1.3824 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 99.2 | 135.3 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 891; total P&L per micro 1,760 USD
- Annualised Sharpe (daily, per micro): 0.29
- PSR (vs 0): 0.776; **Deflated Sharpe: 0.000** over 837 recorded trials
  (Sharpe variance across trials 1.03e-03)
- Random-entry percentile: 0.988

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'ib_min': 60, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 1.0} | -0.0164 | 30 | 50 | (0.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2020 | {'ib_min': 60, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 1.0} | -0.0553 | 1 | 50 | (0.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2021 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | -0.0135 | 8 | 15 | (0.5, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2022 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | -0.0153 | 20 | 15 | (0.0, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2023 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0058 | 10 | 4 | (0.0, 1.0, 0.29) | (0.0, 0.5, 0.29) |
| 2024 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | -0.0055 | 20 | 10 | (0.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2025 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0166 | 4 | 5 | (0.0, 1.0, 0.91) | (0.5, 0.5, 0.91) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2556 | 0.2074 |
| end_to_end_payout | 0.1074 | 0.0815 |
| ev_per_attempt | -512.0 | -214.1 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 1.53 USD

## Evidence
![[ib_breakout__trend_up@ES-equity.png]]
![[ib_breakout__trend_up@ES-fan.png]]
![[ib_breakout__trend_up@ES-random.png]]
![[ib_breakout__trend_up@ES-drawdown.png]]
![[ib_breakout__trend_up@ES-monthly.png]]
![[ib_breakout__trend_up@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ib_breakout__trend_up@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
