---
type: strategy
strategy: control_random
family: control
verdict: graveyard
plan: intraday
run_id: 1b506f93c5
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 7b489c2-dirty
seed: 11
---
# control_random: **GRAVEYARD**

Best plan: **Apex intraday 50K**. Final params {'seed': 3, 'p_entry': 0.004, 'sl_pts': 20.0, 'tp_pts': 20.0, 'rth_only': True}; sizes (micros)
{'eod': 30, 'intraday': 30}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 2040 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0005 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.4690 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -251.9 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0087 | >= 0.6 | commercial | FAIL |
| Evaluation pass rate | 0.1116 | >= 0.85 | commercial | FAIL |
| First payout once funded | 0.0783 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 7.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 18.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.1808 | 0.1116 |
| eval_fail | 0.6358 | 0.7103 |
| eval_expired | 0.1835 | 0.1781 |
| median_sessions_to_pass | 4.0000 | 7.0000 |
| p90_sessions_to_pass | 12.0 | 18.0 |
| first_payout_given_pass | 0.1561 | 0.0783 |
| end_to_end_payout | 0.0282 | 0.0087 |
| mean_payouts_given_pass | 0.2119 | 0.0964 |
| ev_per_attempt | -519.5 | -242.8 |
| ev_p05 | -552.6 | -251.9 |
| ev_p95 | -473.8 | -229.9 |
| max_best_day_share | 1.3295 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 248.0 | 297.6 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 2,040; total P&L per micro -4,239 USD
- Annualised Sharpe (daily, per micro): -0.92
- PSR (vs 0): 0.010; **Deflated Sharpe: 0.000** over 5 recorded trials
  (Sharpe variance across trials 4.32e-04)
- Random-entry percentile: 0.469

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday |
|---|---|---|---|---|
| 2019 | {'seed': 3, 'p_entry': 0.004, 'sl_pts': 20.0, 'tp_pts': 20.0, 'rth_only': True} | -0.0305 | 20 | 20 |
| 2020 | {'seed': 0, 'p_entry': 0.004, 'sl_pts': 20.0, 'tp_pts': 20.0, 'rth_only': True} | -0.0387 | 1 | 1 |
| 2021 | {'seed': 1, 'p_entry': 0.004, 'sl_pts': 20.0, 'tp_pts': 20.0, 'rth_only': True} | -0.0503 | 50 | 50 |
| 2022 | {'seed': 4, 'p_entry': 0.004, 'sl_pts': 20.0, 'tp_pts': 20.0, 'rth_only': True} | -0.0446 | 25 | 25 |
| 2023 | {'seed': 4, 'p_entry': 0.004, 'sl_pts': 20.0, 'tp_pts': 20.0, 'rth_only': True} | -0.0349 | 15 | 15 |
| 2024 | {'seed': 4, 'p_entry': 0.004, 'sl_pts': 20.0, 'tp_pts': 20.0, 'rth_only': True} | -0.0333 | 50 | 15 |
| 2025 | {'seed': 3, 'p_entry': 0.004, 'sl_pts': 20.0, 'tp_pts': 20.0, 'rth_only': True} | -0.0288 | 30 | 30 |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2593 | 0.0778 |
| end_to_end_payout | 0.0259 | 0.0037 |
| ev_per_attempt | -541.6 | -240.6 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -4.27 USD

## Evidence
![[control_random-equity.png]]
![[control_random-fan.png]]
![[control_random-random.png]]
![[control_random-drawdown.png]]
![[control_random-monthly.png]]
![[control_random-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run control_random`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
