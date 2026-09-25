---
type: strategy
strategy: late_trend__vol_expanding
family: late_trend
verdict: graveyard
plan: intraday
run_id: c02bb6e1ba
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# late_trend__vol_expanding: **GRAVEYARD**

Best plan: **Apex intraday 50K**. Final params {'decide': 780, 'k': 0.3, 'sl_atr': 0.25}; base sizes (micros)
{'eod': 8, 'intraday': 3}; sizing policy (alpha, beta, mu) {'eod': (2.0, 1.0, 3.703421829063414), 'intraday': (1.0, 1.0, 3.703421829063414)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 307 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0109 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9030 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -226.5 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0302 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0894 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.3383 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 11.0 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 19.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.1700 | 0.0894 |
| eval_fail | 0.2171 | 0.5074 |
| eval_expired | 0.6129 | 0.4032 |
| median_sessions_to_pass | 7.0000 | 11.0 |
| p90_sessions_to_pass | 18.0 | 19.0 |
| first_payout_given_pass | 0.1107 | 0.3383 |
| end_to_end_payout | 0.0188 | 0.0302 |
| mean_payouts_given_pass | 0.4190 | 0.8195 |
| ev_per_attempt | -441.2 | -115.8 |
| ev_p05 | -568.6 | -226.5 |
| ev_p95 | -280.5 | 35.1 |
| max_best_day_share | 1.2561 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 87.5 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 307; total P&L per micro 2,494 USD
- Annualised Sharpe (daily, per micro): 0.40
- PSR (vs 0): 0.854; **Deflated Sharpe: 0.011** over 501 recorded trials
  (Sharpe variance across trials 6.91e-04)
- Random-entry percentile: 0.903

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'decide': 840, 'k': 0.8, 'sl_atr': 0.25} | 0.0857 | 10 | 12 | (0.5, 1.0, 2.19) | (0.0, 1.0, 2.19) |
| 2020 | {'decide': 840, 'k': 0.8, 'sl_atr': 0.25} | 0.0572 | 10 | 12 | (0.5, 1.0, 1.31) | (0.0, 1.0, 1.31) |
| 2021 | {'decide': 840, 'k': 0.8, 'sl_atr': 0.25} | 0.0449 | 25 | 15 | (1.0, 0.5, 1.16) | (0.0, 0.5, 1.16) |
| 2022 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0632 | 8 | 4 | (2.0, 1.0, 3.33) | (1.0, 1.0, 3.33) |
| 2023 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0671 | 8 | 3 | (2.0, 1.0, 3.94) | (1.0, 1.0, 3.94) |
| 2024 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0660 | 8 | 3 | (2.0, 1.0, 3.88) | (1.0, 1.0, 3.88) |
| 2025 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0545 | 8 | 3 | (2.0, 1.0, 3.34) | (1.0, 1.0, 3.34) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1704 | 0.0000 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -573.7 | -249.0 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 5.41 USD

## Evidence
![[late_trend__vol_expanding-equity.png]]
![[late_trend__vol_expanding-fan.png]]
![[late_trend__vol_expanding-random.png]]
![[late_trend__vol_expanding-drawdown.png]]
![[late_trend__vol_expanding-monthly.png]]
![[late_trend__vol_expanding-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run late_trend__vol_expanding`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
