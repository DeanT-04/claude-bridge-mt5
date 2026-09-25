---
type: strategy
strategy: ib_breakout
family: initial_balance
verdict: graveyard
plan: intraday
run_id: e6d7598aa8
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 5455e7a-dirty
seed: 11
---
# ib_breakout: **GRAVEYARD**

Best plan: **Apex intraday 50K**. Final params {'ib_min': 30, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 1.0}; sizes (micros)
{'eod': 5, 'intraday': 4}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1055 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0271 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9830 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -243.4 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0222 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1337 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1658 | >= 0.7 | commercial | FAIL |
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
| eval_pass | 0.1902 | 0.1337 |
| eval_fail | 0.7366 | 0.7278 |
| eval_expired | 0.0733 | 0.1384 |
| median_sessions_to_pass | 4.0000 | 6.0000 |
| p90_sessions_to_pass | 11.0 | 17.0 |
| first_payout_given_pass | 0.0671 | 0.1658 |
| end_to_end_payout | 0.0128 | 0.0222 |
| mean_payouts_given_pass | 0.1201 | 0.5879 |
| ev_per_attempt | -539.8 | -82.1 |
| ev_p05 | -562.2 | -243.4 |
| ev_p95 | -517.7 | 149.1 |
| max_best_day_share | 1.3184 | 1.1794 |
| starts | 1488 | 1488 |
| effective_n | 297.6 | 165.3 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 1,055; total P&L per micro 8,758 USD
- Annualised Sharpe (daily, per micro): 0.59
- PSR (vs 0): 0.940; **Deflated Sharpe: 0.027** over 61 recorded trials
  (Sharpe variance across trials 1.27e-03)
- Random-entry percentile: 0.983

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday |
|---|---|---|---|---|
| 2019 | {'ib_min': 60, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0087 | 20 | 15 |
| 2020 | {'ib_min': 60, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0140 | 20 | 15 |
| 2021 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0185 | 50 | 30 |
| 2022 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0279 | 25 | 4 |
| 2023 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0589 | 8 | 3 |
| 2024 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0541 | 8 | 3 |
| 2025 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0501 | 8 | 3 |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2593 | 0.1704 |
| end_to_end_payout | 0.0074 | 0.0037 |
| ev_per_attempt | -574.9 | -246.1 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 6.74 USD

## Evidence
![[ib_breakout-equity.png]]
![[ib_breakout-fan.png]]
![[ib_breakout-random.png]]
![[ib_breakout-drawdown.png]]
![[ib_breakout-monthly.png]]
![[ib_breakout-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ib_breakout`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
