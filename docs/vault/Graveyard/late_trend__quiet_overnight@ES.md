---
type: strategy
strategy: late_trend__quiet_overnight@ES
family: late_trend
verdict: graveyard
plan: eod
run_id: 2673f506f5
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# late_trend__quiet_overnight@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'decide': 780, 'k': 0.3, 'sl_atr': 0.25}; base sizes (micros)
{'eod': 8, 'intraday': 8}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 0.37525952654024225), 'intraday': (1.0, 1.0, 0.37525952654024225)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 133 | >= 200 | stat | FAIL |
| Deflated Sharpe | 0.0005 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9350 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -556.6 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0181 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0800 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2269 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 10.0 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 19.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.0800 | 0.0188 |
| eval_fail | 0.2177 | 0.4456 |
| eval_expired | 0.7023 | 0.5356 |
| median_sessions_to_pass | 10.0 | 10.5 |
| p90_sessions_to_pass | 19.0 | 17.3 |
| first_payout_given_pass | 0.2269 | 0.0357 |
| end_to_end_payout | 0.0181 | 0.0007 |
| mean_payouts_given_pass | 0.2718 | 0.3333 |
| ev_per_attempt | -537.6 | -247.8 |
| ev_p05 | -556.6 | -250.7 |
| ev_p95 | -510.6 | -243.5 |
| max_best_day_share | 1.3146 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 70.9 |
| censored_pa | 16 | 22 |

## Statistics
- OOS trades: 133; total P&L per micro 883 USD
- Annualised Sharpe (daily, per micro): 0.39
- PSR (vs 0): 0.841; **Deflated Sharpe: 0.000** over 1035 recorded trials
  (Sharpe variance across trials 1.07e-03)
- Random-entry percentile: 0.935

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | -0.0062 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | -0.0069 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | 0.0027 | 12 | 12 | (0.5, 1.0, 0.04) | (0.0, 1.0, 0.04) |
| 2022 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | 0.0065 | 12 | 12 | (0.5, 1.0, 0.1) | (0.5, 1.0, 0.1) |
| 2023 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | 0.0256 | 15 | 15 | (1.0, 1.0, 0.5) | (2.0, 1.0, 0.5) |
| 2024 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0109 | 8 | 8 | (0.5, 1.0, 0.21) | (1.0, 1.0, 0.21) |
| 2025 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0140 | 8 | 8 | (0.5, 1.0, 0.27) | (1.0, 1.0, 0.27) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0815 | 0.0815 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -561.3 | -253.8 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -2.02 USD

## Evidence
![[late_trend__quiet_overnight@ES-equity.png]]
![[late_trend__quiet_overnight@ES-fan.png]]
![[late_trend__quiet_overnight@ES-random.png]]
![[late_trend__quiet_overnight@ES-drawdown.png]]
![[late_trend__quiet_overnight@ES-monthly.png]]
![[late_trend__quiet_overnight@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run late_trend__quiet_overnight@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
