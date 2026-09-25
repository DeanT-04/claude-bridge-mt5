---
type: strategy
strategy: wide_ib_rotation
family: ib_rotation
verdict: graveyard
plan: intraday
run_id: 780c169520
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# wide_ib_rotation: **GRAVEYARD**

Best plan: **Apex intraday 50K**. Final params {'q': 1.3, 's': 0.1, 'target': 'far25'}; base sizes (micros)
{'eod': 1, 'intraday': 1}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 521 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.0050 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -249.0 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0000 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0000 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0000 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | inf | <= 15 | speed | FAIL |
| 90th pct sessions to pass | inf | <= 30 | speed | FAIL |

Failed gates:
- Deflated Sharpe
- Beats random entry (percentile)
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded
- Median sessions to pass
- 90th pct sessions to pass

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0121 | 0.0000 |
| eval_fail | 0.1109 | 0.0000 |
| eval_expired | 0.8770 | 1.0000 |
| median_sessions_to_pass | 9.5000 | inf |
| p90_sessions_to_pass | 16.3 | inf |
| first_payout_given_pass | 0.0000 | 0.0000 |
| end_to_end_payout | 0.0000 | 0.0000 |
| mean_payouts_given_pass | 0.0000 | 0.0000 |
| ev_per_attempt | -551.7 | -249.0 |
| ev_p05 | -554.2 | -249.0 |
| ev_p95 | -550.0 | -249.0 |
| max_best_day_share | 1.2613 | 0.0000 |
| starts | 1488 | 1488 |
| effective_n | 67.6 | 67.6 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 521; total P&L per micro -6,853 USD
- Annualised Sharpe (daily, per micro): -1.00
- PSR (vs 0): 0.011; **Deflated Sharpe: 0.000** over 1079 recorded trials
  (Sharpe variance across trials 1.06e-03)
- Random-entry percentile: 0.005

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'q': 1.6, 's': 0.2, 'target': 'far25'} | -0.0092 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'q': 1.6, 's': 0.2, 'target': 'far25'} | -0.0418 | 60 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'q': 1.3, 's': 0.2, 'target': 'far25'} | -0.0189 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'q': 1.6, 's': 0.1, 'target': 'far25'} | -0.0207 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'q': 1.3, 's': 0.1, 'target': 'far25'} | -0.0129 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2024 | {'q': 1.3, 's': 0.1, 'target': 'far25'} | -0.0196 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'q': 1.6, 's': 0.2, 'target': 'far25'} | -0.0210 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0000 | 0.0000 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -550.0 | -249.0 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 3.26 USD

## Evidence
![[wide_ib_rotation-equity.png]]
![[wide_ib_rotation-fan.png]]
![[wide_ib_rotation-random.png]]
![[wide_ib_rotation-drawdown.png]]
![[wide_ib_rotation-monthly.png]]
![[wide_ib_rotation-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run wide_ib_rotation`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
