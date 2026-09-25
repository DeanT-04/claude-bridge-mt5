---
type: strategy
strategy: late_trend__vix_high@ES
family: late_trend
verdict: graveyard
plan: eod
run_id: 6b5c7ba718
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# late_trend__vix_high@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'decide': 780, 'k': 0.3, 'sl_atr': 0.25}; base sizes (micros)
{'eod': 6, 'intraday': 5}; sizing policy (alpha, beta, mu) {'eod': (2.0, 1.0, 1.8955275812753103), 'intraday': (1.0, 1.0, 1.8955275812753103)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 349 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0004 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9640 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -544.0 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0235 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1129 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2083 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 6.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 17.0 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1129 | 0.0558 |
| eval_fail | 0.3273 | 0.4254 |
| eval_expired | 0.5598 | 0.5188 |
| median_sessions_to_pass | 6.0000 | 4.0000 |
| p90_sessions_to_pass | 17.0 | 12.0 |
| first_payout_given_pass | 0.2083 | 0.0120 |
| end_to_end_payout | 0.0235 | 0.0007 |
| mean_payouts_given_pass | 0.6828 | 0.0122 |
| ev_per_attempt | -450.8 | -251.3 |
| ev_p05 | -544.0 | -252.9 |
| ev_p95 | -322.1 | -249.6 |
| max_best_day_share | 1.2857 | 1.1907 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 74.4 |
| censored_pa | 23 | 1 |

## Statistics
- OOS trades: 349; total P&L per micro 2,443 USD
- Annualised Sharpe (daily, per micro): 0.45
- PSR (vs 0): 0.878; **Deflated Sharpe: 0.000** over 1151 recorded trials
  (Sharpe variance across trials 1.09e-03)
- Random-entry percentile: 0.964

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'decide': 840, 'k': 0.3, 'sl_atr': 0.25} | 0.0312 | 10 | 20 | (0.0, 0.5, 0.78) | (0.0, 0.0, 0.78) |
| 2020 | {'decide': 840, 'k': 0.3, 'sl_atr': 0.25} | 0.0199 | 10 | 8 | (0.0, 0.5, 0.44) | (0.0, 0.5, 0.44) |
| 2021 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | 0.0427 | 12 | 20 | (0.0, 1.0, 1.69) | (1.0, 0.0, 1.69) |
| 2022 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | 0.0239 | 15 | 20 | (0.0, 0.0, 0.97) | (1.0, 0.0, 0.97) |
| 2023 | {'decide': 840, 'k': 0.3, 'sl_atr': 0.25} | 0.0466 | 6 | 5 | (2.0, 1.0, 2.07) | (2.0, 1.0, 2.07) |
| 2024 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0441 | 6 | 5 | (2.0, 1.0, 1.92) | (1.0, 1.0, 1.92) |
| 2025 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0427 | 6 | 5 | (2.0, 1.0, 1.79) | (1.0, 1.0, 1.79) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0815 | 0.0519 |
| end_to_end_payout | 0.0185 | 0.0296 |
| ev_per_attempt | -551.6 | -213.7 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 7.25 USD

## Evidence
![[late_trend__vix_high@ES-equity.png]]
![[late_trend__vix_high@ES-fan.png]]
![[late_trend__vix_high@ES-random.png]]
![[late_trend__vix_high@ES-drawdown.png]]
![[late_trend__vix_high@ES-monthly.png]]
![[late_trend__vix_high@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run late_trend__vix_high@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
