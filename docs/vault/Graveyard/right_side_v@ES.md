---
type: strategy
strategy: right_side_v@ES
family: capitulation_reversal
verdict: graveyard
plan: eod
run_id: dfefa283b3
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# right_side_v@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'m': 0.7, 'f': 0.5, 'hold': 90}; base sizes (micros)
{'eod': 40, 'intraday': 50}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (1.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 375 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.4040 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -565.4 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0134 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1290 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1042 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 7.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 16.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.1290 | 0.0531 |
| eval_fail | 0.5323 | 0.6868 |
| eval_expired | 0.3387 | 0.2601 |
| median_sessions_to_pass | 7.0000 | 9.0000 |
| p90_sessions_to_pass | 16.0 | 17.2 |
| first_payout_given_pass | 0.1042 | 0.0506 |
| end_to_end_payout | 0.0134 | 0.0027 |
| mean_payouts_given_pass | 0.1042 | 0.0506 |
| ev_per_attempt | -547.8 | -248.1 |
| ev_p05 | -565.4 | -253.0 |
| ev_p95 | -526.3 | -240.6 |
| max_best_day_share | 1.3097 | 1.2196 |
| starts | 1488 | 1488 |
| effective_n | 99.2 | 165.3 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 375; total P&L per micro -1,649 USD
- Annualised Sharpe (daily, per micro): -0.51
- PSR (vs 0): 0.106; **Deflated Sharpe: 0.000** over 1315 recorded trials
  (Sharpe variance across trials 1.24e-03)
- Random-entry percentile: 0.404

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'m': 0.7, 'f': 0.5, 'hold': 90} | -0.0500 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'m': 0.7, 'f': 0.5, 'hold': 90} | -0.0071 | 40 | 40 | (0.5, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2021 | {'m': 0.7, 'f': 0.5, 'hold': 90} | 0.0070 | 25 | 50 | (0.5, 0.5, 0.14) | (1.0, 0.0, 0.14) |
| 2022 | {'m': 0.7, 'f': 1.0, 'hold': 90} | 0.0110 | 25 | 25 | (0.5, 1.0, 0.32) | (0.5, 0.5, 0.32) |
| 2023 | {'m': 0.7, 'f': 1.0, 'hold': 90} | -0.0009 | 50 | 25 | (0.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2024 | {'m': 0.7, 'f': 0.5, 'hold': 90} | -0.0016 | 40 | 50 | (0.0, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2025 | {'m': 0.7, 'f': 1.0, 'hold': 90} | -0.0130 | 30 | 25 | (1.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1037 | 0.0148 |
| end_to_end_payout | 0.0037 | 0.0000 |
| ev_per_attempt | -558.9 | -249.9 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -1.20 USD

## Evidence
![[right_side_v@ES-equity.png]]
![[right_side_v@ES-fan.png]]
![[right_side_v@ES-random.png]]
![[right_side_v@ES-drawdown.png]]
![[right_side_v@ES-monthly.png]]
![[right_side_v@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run right_side_v@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
