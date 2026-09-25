---
type: strategy
strategy: overnight_failure_fade@ES
family: overnight_failure
verdict: graveyard
plan: eod
run_id: 4815de0e02
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# overnight_failure_fade@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'k': 0.3, 'c': 0.4, 'ib_mid': True}; base sizes (micros)
{'eod': 50, 'intraday': 50}; sizing policy (alpha, beta, mu) {'eod': (1.0, 0.0, 0.8449254514909712), 'intraday': (2.0, 0.5, 0.8449254514909712)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 141 | >= 200 | stat | FAIL |
| Deflated Sharpe | 0.0003 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9590 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -547.3 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0309 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1176 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2629 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 9.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 18.0 | <= 30 | speed | PASS |

Failed gates:
- OOS trades
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- Holdout consistent
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1176 | 0.0397 |
| eval_fail | 0.2399 | 0.5040 |
| eval_expired | 0.6425 | 0.4563 |
| median_sessions_to_pass | 9.0000 | 11.0 |
| p90_sessions_to_pass | 18.0 | 19.2 |
| first_payout_given_pass | 0.2629 | 0.1186 |
| end_to_end_payout | 0.0309 | 0.0047 |
| mean_payouts_given_pass | 0.3312 | 0.1250 |
| ev_per_attempt | -514.5 | -244.3 |
| ev_p05 | -547.3 | -251.9 |
| ev_p95 | -476.2 | -231.9 |
| max_best_day_share | 1.3013 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 78.3 |
| censored_pa | 15 | 3 |

## Statistics
- OOS trades: 141; total P&L per micro 1,494 USD
- Annualised Sharpe (daily, per micro): 0.53
- PSR (vs 0): 0.920; **Deflated Sharpe: 0.000** over 1279 recorded trials
  (Sharpe variance across trials 1.22e-03)
- Random-entry percentile: 0.959

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'k': 0.3, 'c': 0.4, 'ib_mid': False} | 0.0123 | 1 | 1 | (0.0, 0.0, 0.15) | (0.0, 0.0, 0.15) |
| 2020 | {'k': 0.5, 'c': 0.4, 'ib_mid': False} | 0.0217 | 50 | 40 | (0.0, 0.0, 0.24) | (2.0, 0.0, 0.24) |
| 2021 | {'k': 0.3, 'c': 0.4, 'ib_mid': True} | 0.0191 | 12 | 15 | (0.0, 1.0, 0.39) | (0.0, 0.5, 0.39) |
| 2022 | {'k': 0.3, 'c': 0.4, 'ib_mid': True} | 0.0062 | 12 | 15 | (0.0, 1.0, 0.12) | (0.0, 0.5, 0.12) |
| 2023 | {'k': 0.3, 'c': 0.4, 'ib_mid': True} | 0.0239 | 30 | 15 | (0.5, 0.5, 0.55) | (1.0, 0.5, 0.55) |
| 2024 | {'k': 0.3, 'c': 0.4, 'ib_mid': True} | 0.0297 | 12 | 15 | (2.0, 1.0, 0.66) | (2.0, 1.0, 0.66) |
| 2025 | {'k': 0.3, 'c': 0.4, 'ib_mid': True} | 0.0273 | 12 | 15 | (2.0, 1.0, 0.61) | (2.0, 1.0, 0.61) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0704 | 0.0000 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -559.8 | -249.0 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -1.77 USD

## Evidence
![[overnight_failure_fade@ES-equity.png]]
![[overnight_failure_fade@ES-fan.png]]
![[overnight_failure_fade@ES-random.png]]
![[overnight_failure_fade@ES-drawdown.png]]
![[overnight_failure_fade@ES-monthly.png]]
![[overnight_failure_fade@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run overnight_failure_fade@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
