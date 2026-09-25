---
type: strategy
strategy: late_trend__trending@ES
family: late_trend
verdict: graveyard
plan: eod
run_id: 898f80f95b
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# late_trend__trending@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'decide': 780, 'k': 0.3, 'sl_atr': 0.25}; base sizes (micros)
{'eod': 8, 'intraday': 4}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 0.5366663354232822), 'intraday': (0.0, 1.0, 0.5366663354232822)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 291 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.6730 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -549.2 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0235 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0638 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.3684 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 8.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 17.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.0638 | 0.0336 |
| eval_fail | 0.3380 | 0.3353 |
| eval_expired | 0.5981 | 0.6310 |
| median_sessions_to_pass | 8.0000 | 10.5 |
| p90_sessions_to_pass | 17.0 | 18.1 |
| first_payout_given_pass | 0.3684 | 0.0200 |
| end_to_end_payout | 0.0235 | 0.0007 |
| mean_payouts_given_pass | 0.5474 | 0.0200 |
| ev_per_attempt | -509.2 | -250.0 |
| ev_p05 | -549.2 | -252.2 |
| ev_p95 | -454.3 | -247.8 |
| max_best_day_share | 1.2305 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 70.9 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 291; total P&L per micro -372 USD
- Annualised Sharpe (daily, per micro): -0.09
- PSR (vs 0): 0.409; **Deflated Sharpe: 0.000** over 1139 recorded trials
  (Sharpe variance across trials 1.08e-03)
- Random-entry percentile: 0.673

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'decide': 840, 'k': 0.5, 'sl_atr': 0.5} | 0.0235 | 15 | 1 | (0.0, 1.0, 0.51) | (0.0, 0.0, 0.51) |
| 2020 | {'decide': 840, 'k': 0.8, 'sl_atr': 0.5} | 0.0196 | 1 | 1 | (0.0, 0.0, 0.35) | (0.0, 0.0, 0.35) |
| 2021 | {'decide': 840, 'k': 0.8, 'sl_atr': 0.25} | 0.0150 | 1 | 1 | (0.0, 0.0, 0.25) | (0.0, 0.0, 0.25) |
| 2022 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | 0.0026 | 8 | 12 | (0.0, 1.0, 0.09) | (0.0, 0.0, 0.09) |
| 2023 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | 0.0232 | 8 | 4 | (0.0, 1.0, 0.97) | (0.0, 1.0, 0.97) |
| 2024 | {'decide': 840, 'k': 0.5, 'sl_atr': 0.25} | 0.0147 | 6 | 5 | (2.0, 1.0, 0.38) | (0.0, 1.0, 0.38) |
| 2025 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0135 | 8 | 4 | (0.0, 1.0, 0.48) | (0.0, 1.0, 0.48) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1630 | 0.0296 |
| end_to_end_payout | 0.0704 | 0.0259 |
| ev_per_attempt | -439.3 | -236.2 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 7.69 USD

## Evidence
![[late_trend__trending@ES-equity.png]]
![[late_trend__trending@ES-fan.png]]
![[late_trend__trending@ES-random.png]]
![[late_trend__trending@ES-drawdown.png]]
![[late_trend__trending@ES-monthly.png]]
![[late_trend__trending@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run late_trend__trending@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
