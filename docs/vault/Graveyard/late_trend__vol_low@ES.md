---
type: strategy
strategy: late_trend__vol_low@ES
family: late_trend
verdict: graveyard
plan: eod
run_id: 25f1e105b6
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# late_trend__vol_low@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'decide': 780, 'k': 0.5, 'sl_atr': 0.25}; base sizes (micros)
{'eod': 8, 'intraday': 4}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 0.2698574466010691), 'intraday': (0.0, 1.0, 0.2698574466010691)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 299 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.8750 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -562.2 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0054 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0853 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0630 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 5.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 18.4 | <= 30 | speed | PASS |

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
| eval_pass | 0.0853 | 0.0477 |
| eval_fail | 0.1559 | 0.4099 |
| eval_expired | 0.7587 | 0.5423 |
| median_sessions_to_pass | 5.0000 | 6.0000 |
| p90_sessions_to_pass | 18.4 | 19.0 |
| first_payout_given_pass | 0.0630 | 0.0282 |
| end_to_end_payout | 0.0054 | 0.0013 |
| mean_payouts_given_pass | 0.0630 | 0.0282 |
| ev_per_attempt | -553.8 | -249.8 |
| ev_p05 | -562.2 | -252.9 |
| ev_p95 | -543.8 | -245.9 |
| max_best_day_share | 1.3185 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 67.6 | 70.9 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 299; total P&L per micro 183 USD
- Annualised Sharpe (daily, per micro): 0.06
- PSR (vs 0): 0.565; **Deflated Sharpe: 0.000** over 1259 recorded trials
  (Sharpe variance across trials 1.14e-03)
- Random-entry percentile: 0.875

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'decide': 840, 'k': 0.5, 'sl_atr': 0.25} | -0.0330 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'decide': 840, 'k': 0.5, 'sl_atr': 0.5} | -0.0227 | 1 | 60 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'decide': 840, 'k': 0.5, 'sl_atr': 0.5} | -0.0115 | 1 | 60 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | -0.0168 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0005 | 15 | 10 | (0.0, 1.0, 0.01) | (1.0, 1.0, 0.01) |
| 2024 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | 0.0080 | 8 | 30 | (0.0, 1.0, 0.15) | (1.0, 0.0, 0.15) |
| 2025 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | 0.0103 | 8 | 4 | (0.0, 1.0, 0.2) | (0.0, 1.0, 0.2) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0444 | 0.0000 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -556.2 | -249.0 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -0.79 USD

## Evidence
![[late_trend__vol_low@ES-equity.png]]
![[late_trend__vol_low@ES-fan.png]]
![[late_trend__vol_low@ES-random.png]]
![[late_trend__vol_low@ES-drawdown.png]]
![[late_trend__vol_low@ES-monthly.png]]
![[late_trend__vol_low@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run late_trend__vol_low@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
