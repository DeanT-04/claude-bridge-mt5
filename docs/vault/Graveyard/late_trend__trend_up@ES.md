---
type: strategy
strategy: late_trend__trend_up@ES
family: late_trend
verdict: graveyard
plan: intraday
run_id: f0065c8706
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# late_trend__trend_up@ES: **GRAVEYARD**

Best plan: **Apex intraday 50K**. Final params {'decide': 840, 'k': 0.8, 'sl_atr': 0.25}; base sizes (micros)
{'eod': 12, 'intraday': 12}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 0.06517005188744619), 'intraday': (0.0, 0.5, 0.06517005188744619)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 332 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.7300 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -254.3 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0000 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0551 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0000 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 10.5 | <= 15 | speed | PASS |
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
| eval_pass | 0.0618 | 0.0551 |
| eval_fail | 0.2527 | 0.4825 |
| eval_expired | 0.6855 | 0.4624 |
| median_sessions_to_pass | 10.0 | 10.5 |
| p90_sessions_to_pass | 18.0 | 18.0 |
| first_payout_given_pass | 0.0000 | 0.0000 |
| end_to_end_payout | 0.0000 | 0.0000 |
| mean_payouts_given_pass | 0.0000 | 0.0000 |
| ev_per_attempt | -558.6 | -252.3 |
| ev_p05 | -564.1 | -254.3 |
| ev_p95 | -554.2 | -250.5 |
| max_best_day_share | 1.2339 | 1.2339 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 74.4 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 332; total P&L per micro -268 USD
- Annualised Sharpe (daily, per micro): -0.09
- PSR (vs 0): 0.413; **Deflated Sharpe: 0.000** over 1079 recorded trials
  (Sharpe variance across trials 1.06e-03)
- Random-entry percentile: 0.730

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'decide': 780, 'k': 0.8, 'sl_atr': 0.25} | 0.0128 | 30 | 30 | (0.0, 0.5, 0.11) | (0.0, 1.0, 0.11) |
| 2020 | {'decide': 780, 'k': 0.8, 'sl_atr': 0.25} | -0.0061 | 50 | 60 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | -0.0180 | 10 | 10 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | -0.0171 | 12 | 10 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'decide': 840, 'k': 0.5, 'sl_atr': 0.25} | -0.0082 | 10 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2024 | {'decide': 840, 'k': 0.5, 'sl_atr': 0.25} | -0.0023 | 10 | 8 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'decide': 840, 'k': 0.8, 'sl_atr': 0.25} | -0.0003 | 30 | 30 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0815 | 0.0111 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -561.3 | -249.7 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -1.42 USD

## Evidence
![[late_trend__trend_up@ES-equity.png]]
![[late_trend__trend_up@ES-fan.png]]
![[late_trend__trend_up@ES-random.png]]
![[late_trend__trend_up@ES-drawdown.png]]
![[late_trend__trend_up@ES-monthly.png]]
![[late_trend__trend_up@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run late_trend__trend_up@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
