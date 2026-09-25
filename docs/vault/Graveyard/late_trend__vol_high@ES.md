---
type: strategy
strategy: late_trend__vol_high@ES
family: late_trend
verdict: graveyard
plan: eod
run_id: ec7e640d57
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# late_trend__vol_high@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'decide': 840, 'k': 0.3, 'sl_atr': 0.25}; base sizes (micros)
{'eod': 8, 'intraday': 6}; sizing policy (alpha, beta, mu) {'eod': (1.0, 0.5, 1.0076577189610285), 'intraday': (1.0, 0.5, 1.0076577189610285)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 350 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.6790 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -557.4 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0020 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0423 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0476 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 3.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 7.0000 | <= 30 | speed | PASS |

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
| eval_pass | 0.0423 | 0.0181 |
| eval_fail | 0.2312 | 0.3159 |
| eval_expired | 0.7265 | 0.6660 |
| median_sessions_to_pass | 3.0000 | 3.0000 |
| p90_sessions_to_pass | 7.0000 | 5.0000 |
| first_payout_given_pass | 0.0476 | 0.0000 |
| end_to_end_payout | 0.0020 | 0.0000 |
| mean_payouts_given_pass | 0.2381 | 0.0000 |
| ev_per_attempt | -535.7 | -250.1 |
| ev_p05 | -557.4 | -250.7 |
| ev_p95 | -497.5 | -249.5 |
| max_best_day_share | 1.3109 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 70.9 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 350; total P&L per micro -393 USD
- Annualised Sharpe (daily, per micro): -0.08
- PSR (vs 0): 0.421; **Deflated Sharpe: 0.000** over 1235 recorded trials
  (Sharpe variance across trials 1.15e-03)
- Random-entry percentile: 0.679

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | 0.0403 | 6 | 6 | (0.5, 1.0, 1.1) | (0.5, 1.0, 1.1) |
| 2020 | {'decide': 840, 'k': 0.8, 'sl_atr': 0.5} | 0.0147 | 1 | 1 | (0.0, 0.0, 0.28) | (0.0, 0.0, 0.28) |
| 2021 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | 0.0294 | 20 | 20 | (0.5, 0.5, 1.2) | (0.0, 0.0, 1.2) |
| 2022 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | 0.0202 | 20 | 20 | (0.5, 0.5, 0.81) | (0.0, 0.0, 0.81) |
| 2023 | {'decide': 840, 'k': 0.3, 'sl_atr': 0.25} | 0.0418 | 5 | 4 | (1.0, 1.0, 1.78) | (0.5, 1.0, 1.78) |
| 2024 | {'decide': 840, 'k': 0.3, 'sl_atr': 0.25} | 0.0379 | 5 | 5 | (1.0, 1.0, 1.53) | (1.0, 1.0, 1.53) |
| 2025 | {'decide': 840, 'k': 0.3, 'sl_atr': 0.25} | 0.0195 | 8 | 6 | (1.0, 0.5, 0.78) | (1.0, 0.5, 0.78) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1074 | 0.0444 |
| end_to_end_payout | 0.0074 | 0.0000 |
| ev_per_attempt | -558.0 | -251.6 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -1.65 USD

## Evidence
![[late_trend__vol_high@ES-equity.png]]
![[late_trend__vol_high@ES-fan.png]]
![[late_trend__vol_high@ES-random.png]]
![[late_trend__vol_high@ES-drawdown.png]]
![[late_trend__vol_high@ES-monthly.png]]
![[late_trend__vol_high@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run late_trend__vol_high@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
