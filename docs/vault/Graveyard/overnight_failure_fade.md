---
type: strategy
strategy: overnight_failure_fade
family: overnight_failure
verdict: graveyard
plan: eod
run_id: 76d293003d
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# overnight_failure_fade: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'k': 0.5, 'c': 0.25, 'ib_mid': False}; base sizes (micros)
{'eod': 8, 'intraday': 10}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 0.967394792104161), 'intraday': (0.0, 1.0, 0.967394792104161)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 144 | >= 200 | stat | FAIL |
| Deflated Sharpe | 0.0003 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.8540 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -567.1 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0269 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1741 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1544 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 11.0 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 20.0 | <= 30 | speed | PASS |

Failed gates:
- OOS trades
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
| eval_pass | 0.1741 | 0.0276 |
| eval_fail | 0.1909 | 0.5296 |
| eval_expired | 0.6351 | 0.4429 |
| median_sessions_to_pass | 11.0 | 10.0 |
| p90_sessions_to_pass | 20.0 | 19.0 |
| first_payout_given_pass | 0.1544 | 0.0488 |
| end_to_end_payout | 0.0269 | 0.0013 |
| mean_payouts_given_pass | 0.1544 | 0.0488 |
| ev_per_attempt | -533.9 | -248.8 |
| ev_p05 | -567.1 | -250.9 |
| ev_p95 | -489.6 | -245.9 |
| max_best_day_share | 1.2760 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 82.7 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 144; total P&L per micro 1,786 USD
- Annualised Sharpe (daily, per micro): 0.35
- PSR (vs 0): 0.815; **Deflated Sharpe: 0.000** over 985 recorded trials
  (Sharpe variance across trials 1.07e-03)
- Random-entry percentile: 0.854

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'k': 0.3, 'c': 0.25, 'ib_mid': False} | -inf | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'k': 0.3, 'c': 0.4, 'ib_mid': False} | 0.0283 | 25 | 50 | (0.5, 0.5, 0.45) | (0.0, 0.0, 0.45) |
| 2021 | {'k': 0.3, 'c': 0.4, 'ib_mid': False} | 0.0239 | 25 | 50 | (0.5, 0.5, 0.79) | (0.0, 0.0, 0.79) |
| 2022 | {'k': 0.3, 'c': 0.4, 'ib_mid': False} | 0.0352 | 8 | 6 | (0.0, 1.0, 1.21) | (0.0, 0.5, 1.21) |
| 2023 | {'k': 0.3, 'c': 0.4, 'ib_mid': False} | 0.0224 | 10 | 6 | (0.0, 0.0, 0.92) | (0.0, 0.5, 0.92) |
| 2024 | {'k': 0.3, 'c': 0.4, 'ib_mid': False} | 0.0197 | 10 | 6 | (0.0, 0.0, 0.8) | (0.5, 1.0, 0.8) |
| 2025 | {'k': 0.5, 'c': 0.25, 'ib_mid': False} | 0.0242 | 8 | 10 | (0.0, 1.0, 0.81) | (0.0, 1.0, 0.81) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1667 | 0.0593 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -573.2 | -252.5 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -0.34 USD

## Evidence
![[overnight_failure_fade-equity.png]]
![[overnight_failure_fade-fan.png]]
![[overnight_failure_fade-random.png]]
![[overnight_failure_fade-drawdown.png]]
![[overnight_failure_fade-monthly.png]]
![[overnight_failure_fade-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run overnight_failure_fade`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
