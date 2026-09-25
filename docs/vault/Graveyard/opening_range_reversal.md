---
type: strategy
strategy: opening_range_reversal
family: opening_reversal
verdict: graveyard
plan: eod
run_id: 58642be00b
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# opening_range_reversal: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'p': 0.3, 'g': 1.0, 'bias': False}; base sizes (micros)
{'eod': 20, 'intraday': 20}; sizing policy (alpha, beta, mu) {'eod': (0.5, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1013 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.4270 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -568.8 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0114 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1586 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0720 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 6.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 15.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.1586 | 0.0927 |
| eval_fail | 0.5659 | 0.7332 |
| eval_expired | 0.2755 | 0.1741 |
| median_sessions_to_pass | 6.0000 | 4.0000 |
| p90_sessions_to_pass | 15.0 | 12.3 |
| first_payout_given_pass | 0.0720 | 0.0507 |
| end_to_end_payout | 0.0114 | 0.0047 |
| mean_payouts_given_pass | 0.0847 | 0.0507 |
| ev_per_attempt | -556.0 | -251.0 |
| ev_p05 | -568.8 | -254.5 |
| ev_p95 | -539.4 | -246.8 |
| max_best_day_share | 1.3091 | 1.3393 |
| starts | 1488 | 1488 |
| effective_n | 135.3 | 297.6 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 1,013; total P&L per micro -2,441 USD
- Annualised Sharpe (daily, per micro): -0.29
- PSR (vs 0): 0.237; **Deflated Sharpe: 0.000** over 937 recorded trials
  (Sharpe variance across trials 1.03e-03)
- Random-entry percentile: 0.427

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'p': 0.2, 'g': 1.0, 'bias': True} | -0.0215 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'p': 0.3, 'g': 1.0, 'bias': False} | -0.0301 | 20 | 20 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'p': 0.4, 'g': 1.0, 'bias': False} | -0.0071 | 15 | 15 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'p': 0.4, 'g': 1.0, 'bias': False} | -0.0051 | 15 | 15 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'p': 0.4, 'g': 1.0, 'bias': False} | 0.0152 | 6 | 5 | (0.0, 0.0, 0.96) | (0.0, 0.5, 0.96) |
| 2024 | {'p': 0.4, 'g': 1.0, 'bias': False} | 0.0027 | 6 | 3 | (0.0, 0.0, 0.17) | (0.0, 1.0, 0.17) |
| 2025 | {'p': 0.4, 'g': 1.0, 'bias': False} | -0.0053 | 6 | 6 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1630 | 0.1000 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -572.7 | -254.9 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -4.17 USD

## Evidence
![[opening_range_reversal-equity.png]]
![[opening_range_reversal-fan.png]]
![[opening_range_reversal-random.png]]
![[opening_range_reversal-drawdown.png]]
![[opening_range_reversal-monthly.png]]
![[opening_range_reversal-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run opening_range_reversal`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
