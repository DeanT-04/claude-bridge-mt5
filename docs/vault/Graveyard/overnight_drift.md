---
type: strategy
strategy: overnight_drift
family: overnight
verdict: graveyard
plan: eod
run_id: 9a8cd361c7
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 9e9a3a2-dirty
seed: 11
---
# overnight_drift: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'entry': 1081, 'exit': 540, 'after': 'up', 'sl_pct': 0.01}; base sizes (micros)
{'eod': 3, 'intraday': 4}; sizing policy (alpha, beta, mu) {'eod': (1.0, 1.0, 2.7035018311633343), 'intraday': (1.0, 1.0, 2.7035018311633343)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 781 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0057 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.8430 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -531.7 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0538 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1902 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2827 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 5.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 12.0 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- Beats random entry (percentile)
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1902 | 0.1169 |
| eval_fail | 0.4987 | 0.6808 |
| eval_expired | 0.3112 | 0.2023 |
| median_sessions_to_pass | 5.0000 | 5.0000 |
| p90_sessions_to_pass | 12.0 | 13.0 |
| first_payout_given_pass | 0.2827 | 0.2299 |
| end_to_end_payout | 0.0538 | 0.0269 |
| mean_payouts_given_pass | 0.3675 | 0.2529 |
| ev_per_attempt | -493.6 | -222.9 |
| ev_p05 | -531.7 | -243.8 |
| ev_p95 | -450.6 | -198.4 |
| max_best_day_share | 1.3237 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 186.0 | 372.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 781; total P&L per micro 3,640 USD
- Annualised Sharpe (daily, per micro): 0.29
- PSR (vs 0): 0.764; **Deflated Sharpe: 0.006** over 97 recorded trials
  (Sharpe variance across trials 1.04e-03)
- Random-entry percentile: 0.843

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'entry': 1081, 'exit': 540, 'after': 'up', 'sl_pct': nan} | 0.0297 | 1 | 1 | (0.0, 0.0, 0.71) | (0.0, 0.0, 0.71) |
| 2020 | {'entry': 1081, 'exit': 540, 'after': 'up', 'sl_pct': nan} | 0.0656 | 10 | 8 | (0.0, 0.0, 2.27) | (0.0, 0.0, 2.27) |
| 2021 | {'entry': 1081, 'exit': 570, 'after': 'up', 'sl_pct': nan} | 0.0752 | 10 | 12 | (0.0, 1.0, 5.41) | (0.0, 0.0, 5.41) |
| 2022 | {'entry': 1140, 'exit': 570, 'after': 'up', 'sl_pct': nan} | 0.0572 | 8 | 6 | (0.0, 1.0, 4.41) | (0.0, 0.5, 4.41) |
| 2023 | {'entry': 1081, 'exit': 540, 'after': 'up', 'sl_pct': 0.01} | 0.0289 | 3 | 4 | (1.0, 1.0, 2.65) | (1.0, 1.0, 2.65) |
| 2024 | {'entry': 1081, 'exit': 540, 'after': 'up', 'sl_pct': 0.01} | 0.0243 | 3 | 4 | (1.0, 1.0, 2.31) | (1.0, 1.0, 2.31) |
| 2025 | {'entry': 1140, 'exit': 540, 'after': 'up', 'sl_pct': nan} | 0.0336 | 8 | 10 | (0.5, 1.0, 3.46) | (0.0, 0.0, 3.46) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2778 | 0.0444 |
| end_to_end_payout | 0.1889 | 0.0185 |
| ev_per_attempt | -299.0 | -232.1 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 11.05 USD

## Evidence
![[overnight_drift-equity.png]]
![[overnight_drift-fan.png]]
![[overnight_drift-random.png]]
![[overnight_drift-drawdown.png]]
![[overnight_drift-monthly.png]]
![[overnight_drift-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run overnight_drift`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
