---
type: strategy
strategy: ib_breakout__vol_high
family: initial_balance
verdict: graveyard
plan: eod
run_id: 896bbc28a1
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# ib_breakout__vol_high: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 0.5}; base sizes (micros)
{'eod': 3, 'intraday': 3}; sizing policy (alpha, beta, mu) {'eod': (0.5, 1.0, 1.6038089038219185), 'intraday': (0.5, 1.0, 1.6038089038219185)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 614 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0175 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9150 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -559.7 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0208 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1552 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1342 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 3.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 14.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.1552 | 0.0410 |
| eval_fail | 0.4543 | 0.6035 |
| eval_expired | 0.3905 | 0.3555 |
| median_sessions_to_pass | 3.0000 | 2.0000 |
| p90_sessions_to_pass | 14.0 | 14.0 |
| first_payout_given_pass | 0.1342 | 0.3115 |
| end_to_end_payout | 0.0208 | 0.0128 |
| mean_payouts_given_pass | 0.1948 | 0.3443 |
| ev_per_attempt | -529.5 | -233.9 |
| ev_p05 | -559.7 | -246.4 |
| ev_p95 | -489.9 | -218.6 |
| max_best_day_share | 1.5992 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 114.5 | 135.3 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 614; total P&L per micro 4,900 USD
- Annualised Sharpe (daily, per micro): 0.40
- PSR (vs 0): 0.851; **Deflated Sharpe: 0.018** over 377 recorded trials
  (Sharpe variance across trials 6.61e-04)
- Random-entry percentile: 0.915

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0151 | 25 | 12 | (0.0, 0.0, 0.76) | (0.0, 0.5, 0.76) |
| 2020 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0144 | 20 | 30 | (0.5, 1.0, 0.29) | (0.5, 0.5, 0.29) |
| 2021 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0231 | 20 | 30 | (0.5, 1.0, 0.86) | (0.5, 0.5, 0.86) |
| 2022 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0192 | 12 | 6 | (1.0, 0.0, 1.65) | (0.5, 0.5, 1.65) |
| 2023 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0419 | 3 | 2 | (0.0, 1.0, 4.6) | (0.5, 1.0, 4.6) |
| 2024 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0400 | 3 | 2 | (0.0, 1.0, 4.21) | (0.5, 1.0, 4.21) |
| 2025 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0389 | 2 | 2 | (0.5, 1.0, 4.45) | (0.5, 1.0, 4.45) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0926 | 0.0259 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -562.9 | -250.5 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -7.66 USD

## Evidence
![[ib_breakout__vol_high-equity.png]]
![[ib_breakout__vol_high-fan.png]]
![[ib_breakout__vol_high-random.png]]
![[ib_breakout__vol_high-drawdown.png]]
![[ib_breakout__vol_high-monthly.png]]
![[ib_breakout__vol_high-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ib_breakout__vol_high`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
