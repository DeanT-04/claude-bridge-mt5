---
type: strategy
strategy: opening_range_reversal@ES
family: opening_reversal
verdict: graveyard
plan: intraday
run_id: 478029a072
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# opening_range_reversal@ES: **GRAVEYARD**

Best plan: **Apex intraday 50K**. Final params {'p': 0.4, 'g': 1.0, 'bias': False}; base sizes (micros)
{'eod': 12, 'intraday': 12}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 842 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9120 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -249.9 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0087 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1075 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0813 | >= 0.7 | commercial | FAIL |
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
| eval_pass | 0.1109 | 0.1075 |
| eval_fail | 0.6008 | 0.6405 |
| eval_expired | 0.2883 | 0.2520 |
| median_sessions_to_pass | 7.0000 | 6.0000 |
| p90_sessions_to_pass | 15.0 | 15.0 |
| first_payout_given_pass | 0.0667 | 0.0813 |
| end_to_end_payout | 0.0074 | 0.0087 |
| mean_payouts_given_pass | 0.0788 | 0.1125 |
| ev_per_attempt | -552.3 | -234.8 |
| ev_p05 | -561.7 | -249.9 |
| ev_p95 | -541.6 | -216.2 |
| max_best_day_share | 1.3072 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 124.0 | 148.8 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 842; total P&L per micro -763 USD
- Annualised Sharpe (daily, per micro): -0.17
- PSR (vs 0): 0.336; **Deflated Sharpe: 0.000** over 1235 recorded trials
  (Sharpe variance across trials 1.15e-03)
- Random-entry percentile: 0.912

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'p': 0.4, 'g': 1.0, 'bias': False} | -0.0437 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'p': 0.4, 'g': 1.0, 'bias': False} | -0.0550 | 20 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'p': 0.4, 'g': 1.0, 'bias': False} | -0.0108 | 20 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'p': 0.4, 'g': 1.0, 'bias': False} | -0.0087 | 50 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'p': 0.4, 'g': 1.0, 'bias': False} | -0.0137 | 12 | 12 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2024 | {'p': 0.4, 'g': 1.0, 'bias': False} | -0.0167 | 12 | 12 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'p': 0.4, 'g': 1.0, 'bias': False} | -0.0199 | 12 | 12 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1296 | 0.1074 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -568.0 | -255.3 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -4.99 USD

## Evidence
![[opening_range_reversal@ES-equity.png]]
![[opening_range_reversal@ES-fan.png]]
![[opening_range_reversal@ES-random.png]]
![[opening_range_reversal@ES-drawdown.png]]
![[opening_range_reversal@ES-monthly.png]]
![[opening_range_reversal@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run opening_range_reversal@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
