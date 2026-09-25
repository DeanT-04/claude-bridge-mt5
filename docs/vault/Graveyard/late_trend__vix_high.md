---
type: strategy
strategy: late_trend__vix_high
family: late_trend
verdict: graveyard
plan: eod
run_id: 93152835c1
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# late_trend__vix_high: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'decide': 780, 'k': 0.3, 'sl_atr': 0.25}; base sizes (micros)
{'eod': 5, 'intraday': 2}; sizing policy (alpha, beta, mu) {'eod': (1.0, 1.0, 5.552028448084863), 'intraday': (0.0, 1.0, 5.552028448084863)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 343 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.2678 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9990 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -417.1 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0598 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1579 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.3787 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 5.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 16.6 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1579 | 0.0679 |
| eval_fail | 0.3508 | 0.4684 |
| eval_expired | 0.4913 | 0.4637 |
| median_sessions_to_pass | 5.0000 | 3.0000 |
| p90_sessions_to_pass | 16.6 | 8.0000 |
| first_payout_given_pass | 0.3787 | 0.5644 |
| end_to_end_payout | 0.0598 | 0.0383 |
| mean_payouts_given_pass | 1.5355 | 1.6300 |
| ev_per_attempt | -179.1 | -55.5 |
| ev_p05 | -417.1 | -172.4 |
| ev_p95 | 117.8 | 91.9 |
| max_best_day_share | 1.3105 | 1.1868 |
| starts | 1488 | 1488 |
| effective_n | 74.4 | 87.5 |
| censored_pa | 24 | 1 |

## Statistics
- OOS trades: 343; total P&L per micro 8,841 USD
- Annualised Sharpe (daily, per micro): 1.05
- PSR (vs 0): 0.999; **Deflated Sharpe: 0.268** over 489 recorded trials
  (Sharpe variance across trials 6.94e-04)
- Random-entry percentile: 0.999

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'decide': 840, 'k': 0.3, 'sl_atr': 0.25} | 0.0603 | 15 | 12 | (0.5, 0.5, 1.83) | (0.0, 0.5, 1.83) |
| 2020 | {'decide': 840, 'k': 0.3, 'sl_atr': 0.25} | 0.0424 | 15 | 12 | (0.5, 0.5, 1.14) | (0.0, 0.5, 1.14) |
| 2021 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.5} | 0.0447 | 10 | 12 | (0.0, 1.0, 1.99) | (0.5, 0.0, 1.99) |
| 2022 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0597 | 3 | 3 | (0.0, 1.0, 3.24) | (0.0, 1.0, 3.24) |
| 2023 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0912 | 5 | 2 | (1.0, 1.0, 6.91) | (0.0, 1.0, 6.91) |
| 2024 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0812 | 5 | 2 | (1.0, 1.0, 5.87) | (0.0, 1.0, 5.87) |
| 2025 | {'decide': 840, 'k': 0.3, 'sl_atr': 0.25} | 0.0742 | 4 | 3 | (0.5, 1.0, 4.53) | (0.5, 1.0, 4.53) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0704 | 0.0185 |
| end_to_end_payout | 0.0185 | 0.0000 |
| ev_per_attempt | -532.0 | -250.1 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 9.45 USD

## Evidence
![[late_trend__vix_high-equity.png]]
![[late_trend__vix_high-fan.png]]
![[late_trend__vix_high-random.png]]
![[late_trend__vix_high-drawdown.png]]
![[late_trend__vix_high-monthly.png]]
![[late_trend__vix_high-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run late_trend__vix_high`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
