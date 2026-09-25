---
type: strategy
strategy: intraday_momentum
family: intraday_momentum
verdict: graveyard
plan: intraday
run_id: de2d15a503
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 5455e7a-dirty
seed: 11
---
# intraday_momentum: **GRAVEYARD**

Best plan: **Apex intraday 50K**. Final params {'threshold': 0.0025, 'confirm_r12': True, 'sl_pct': nan}; sizes (micros)
{'eod': 1, 'intraday': 5}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 625 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0001 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.4280 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -249.7 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0000 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0060 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0000 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 3.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 15.2 | <= 30 | speed | PASS |

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
| eval_pass | 0.1082 | 0.0060 |
| eval_fail | 0.5323 | 0.2742 |
| eval_expired | 0.3595 | 0.7198 |
| median_sessions_to_pass | 7.0000 | 3.0000 |
| p90_sessions_to_pass | 16.0 | 15.2 |
| first_payout_given_pass | 0.0000 | 0.0000 |
| end_to_end_payout | 0.0000 | 0.0000 |
| mean_payouts_given_pass | 0.0000 | 0.0000 |
| ev_per_attempt | -565.0 | -249.4 |
| ev_p05 | -571.0 | -249.7 |
| ev_p95 | -560.2 | -249.1 |
| max_best_day_share | 1.3171 | 1.0292 |
| starts | 1488 | 1488 |
| effective_n | 99.2 | 70.9 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 625; total P&L per micro -1,663 USD
- Annualised Sharpe (daily, per micro): -0.30
- PSR (vs 0): 0.230; **Deflated Sharpe: 0.000** over 29 recorded trials
  (Sharpe variance across trials 1.41e-03)
- Random-entry percentile: 0.428

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday |
|---|---|---|---|---|
| 2019 | {'threshold': 0.001, 'confirm_r12': True, 'sl_pct': nan} | 0.0078 | 40 | 60 |
| 2020 | {'threshold': 0.0025, 'confirm_r12': True, 'sl_pct': nan} | -0.0195 | 20 | 1 |
| 2021 | {'threshold': 0.0025, 'confirm_r12': True, 'sl_pct': nan} | 0.0142 | 20 | 5 |
| 2022 | {'threshold': 0.0025, 'confirm_r12': True, 'sl_pct': nan} | -0.0033 | 20 | 5 |
| 2023 | {'threshold': 0.0025, 'confirm_r12': True, 'sl_pct': nan} | 0.0061 | 8 | 5 |
| 2024 | {'threshold': 0.0025, 'confirm_r12': True, 'sl_pct': nan} | -0.0053 | 1 | 5 |
| 2025 | {'threshold': 0.0025, 'confirm_r12': True, 'sl_pct': nan} | -0.0117 | 1 | 5 |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0000 | 0.0037 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -550.0 | -249.2 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -1.87 USD

## Evidence
![[intraday_momentum-equity.png]]
![[intraday_momentum-fan.png]]
![[intraday_momentum-random.png]]
![[intraday_momentum-drawdown.png]]
![[intraday_momentum-monthly.png]]
![[intraday_momentum-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run intraday_momentum`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
