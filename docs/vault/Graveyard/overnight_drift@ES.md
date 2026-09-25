---
type: strategy
strategy: overnight_drift@ES
family: overnight
verdict: graveyard
plan: intraday
run_id: f2833dcf58
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: 790a14f
seed: 11
---
# overnight_drift@ES: **GRAVEYARD**

Best plan: **Apex intraday 50K**. Final params {'entry': 1140, 'exit': 570, 'after': 'up', 'sl_pct': nan}; base sizes (micros)
{'eod': 15, 'intraday': 12}; sizing policy (alpha, beta, mu) {'eod': (2.0, 1.0, 1.6244214615707802), 'intraday': (0.0, 0.5, 1.6244214615707802)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 856 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9650 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -252.6 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0081 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0820 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0984 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 3.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 8.0000 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1526 | 0.0820 |
| eval_fail | 0.5215 | 0.7433 |
| eval_expired | 0.3259 | 0.1747 |
| median_sessions_to_pass | 3.0000 | 3.0000 |
| p90_sessions_to_pass | 11.0 | 8.0000 |
| first_payout_given_pass | 0.0264 | 0.0984 |
| end_to_end_payout | 0.0040 | 0.0081 |
| mean_payouts_given_pass | 0.0573 | 0.0984 |
| ev_per_attempt | -557.4 | -242.6 |
| ev_p05 | -571.2 | -252.6 |
| ev_p95 | -537.8 | -231.1 |
| max_best_day_share | 1.3130 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 165.3 | 496.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 856; total P&L per micro 3,321 USD
- Annualised Sharpe (daily, per micro): 0.37
- PSR (vs 0): 0.829; **Deflated Sharpe: 0.000** over 1581 recorded trials
  (Sharpe variance across trials 1.50e-03)
- Random-entry percentile: 0.965

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'entry': 1140, 'exit': 540, 'after': 'down', 'sl_pct': nan} | 0.0258 | 1 | 1 | (0.0, 0.0, 0.45) | (0.0, 0.0, 0.45) |
| 2020 | {'entry': 1140, 'exit': 540, 'after': 'any', 'sl_pct': 0.01} | 0.0655 | 12 | 8 | (2.0, 1.0, 2.38) | (2.0, 1.0, 2.38) |
| 2021 | {'entry': 1140, 'exit': 570, 'after': 'up', 'sl_pct': nan} | 0.0610 | 15 | 12 | (2.0, 1.0, 3.29) | (0.0, 0.5, 3.29) |
| 2022 | {'entry': 1140, 'exit': 570, 'after': 'up', 'sl_pct': nan} | 0.0438 | 15 | 12 | (2.0, 1.0, 2.39) | (0.0, 0.5, 2.39) |
| 2023 | {'entry': 1140, 'exit': 570, 'after': 'up', 'sl_pct': nan} | 0.0259 | 15 | 12 | (2.0, 1.0, 1.67) | (0.0, 0.5, 1.67) |
| 2024 | {'entry': 1140, 'exit': 570, 'after': 'up', 'sl_pct': nan} | 0.0202 | 15 | 12 | (2.0, 1.0, 1.31) | (0.0, 0.5, 1.31) |
| 2025 | {'entry': 1140, 'exit': 570, 'after': 'up', 'sl_pct': nan} | 0.0295 | 15 | 12 | (2.0, 1.0, 1.95) | (0.0, 0.5, 1.95) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2222 | 0.0444 |
| end_to_end_payout | 0.0407 | 0.0000 |
| ev_per_attempt | -522.1 | -251.6 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 1.31 USD

## Evidence
![[overnight_drift@ES-equity.png]]
![[overnight_drift@ES-fan.png]]
![[overnight_drift@ES-random.png]]
![[overnight_drift@ES-drawdown.png]]
![[overnight_drift@ES-monthly.png]]
![[overnight_drift@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run overnight_drift@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
