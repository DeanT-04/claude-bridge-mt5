---
type: strategy
strategy: late_trend@ES
family: late_trend
verdict: graveyard
plan: intraday
run_id: ef31822ce9
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: 790a14f
seed: 11
---
# late_trend@ES: **GRAVEYARD**

Best plan: **Apex intraday 50K**. Final params {'decide': 780, 'k': 0.3, 'sl_atr': 0.25}; base sizes (micros)
{'eod': 6, 'intraday': 4}; sizing policy (alpha, beta, mu) {'eod': (2.0, 1.0, 0.584106757768684), 'intraday': (0.0, 0.5, 0.584106757768684)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 629 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.8670 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -228.2 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0262 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0444 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.5909 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 7.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 13.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.1237 | 0.0444 |
| eval_fail | 0.4866 | 0.4852 |
| eval_expired | 0.3898 | 0.4704 |
| median_sessions_to_pass | 6.0000 | 7.0000 |
| p90_sessions_to_pass | 13.0 | 13.0 |
| first_payout_given_pass | 0.1304 | 0.5909 |
| end_to_end_payout | 0.0161 | 0.0262 |
| mean_payouts_given_pass | 0.3675 | 1.0758 |
| ev_per_attempt | -497.0 | -164.9 |
| ev_p05 | -551.0 | -228.2 |
| ev_p95 | -424.7 | -81.0 |
| max_best_day_share | 1.2702 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 99.2 | 74.4 |
| censored_pa | 18 | 0 |

## Statistics
- OOS trades: 629; total P&L per micro 381 USD
- Annualised Sharpe (daily, per micro): 0.06
- PSR (vs 0): 0.563; **Deflated Sharpe: 0.000** over 1557 recorded trials
  (Sharpe variance across trials 1.52e-03)
- Random-entry percentile: 0.867

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'decide': 840, 'k': 0.8, 'sl_atr': 0.5} | 0.0012 | 20 | 12 | (0.5, 1.0, 0.03) | (0.0, 1.0, 0.03) |
| 2020 | {'decide': 840, 'k': 0.8, 'sl_atr': 0.5} | -0.0115 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | -0.0018 | 20 | 10 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | -0.0086 | 15 | 8 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | 0.0174 | 4 | 3 | (0.0, 1.0, 0.99) | (0.0, 0.5, 0.99) |
| 2024 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0148 | 6 | 4 | (2.0, 1.0, 0.72) | (0.0, 0.5, 0.72) |
| 2025 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0102 | 6 | 4 | (2.0, 1.0, 0.5) | (0.0, 0.5, 0.5) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1778 | 0.0222 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -574.7 | -250.3 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 1.99 USD

## Evidence
![[late_trend@ES-equity.png]]
![[late_trend@ES-fan.png]]
![[late_trend@ES-random.png]]
![[late_trend@ES-drawdown.png]]
![[late_trend@ES-monthly.png]]
![[late_trend@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run late_trend@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
