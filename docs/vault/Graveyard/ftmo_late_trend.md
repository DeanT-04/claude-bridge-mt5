---
type: strategy
strategy: ftmo:late_trend
firm: ftmo
verdict: graveyard
run_id: c249879341
---
# ftmo:late_trend: **GRAVEYARD** (FTMO 2-Step 50K, CFD costs)

| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 632 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0342 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9990 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | 497.3 | > 0 | stat | PASS |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.2513 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.3078 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.8166 | >= 0.7 | commercial | PASS |
| Median sessions to pass | 88.5 | <= 15 | speed | FAIL |
| 90th pct sessions to pass | 526.0 | <= 30 | speed | FAIL |

| metric | value |
|---|---|
| starts | 1488 |
| eval_pass | 0.3078 |
| eval_fail | 0.5000 |
| eval_expired | 0.0000 |
| median_sessions_to_pass | 88.5 |
| p90_sessions_to_pass | 526.0 |
| first_payout_given_pass | 0.8166 |
| end_to_end_payout | 0.2513 |
| ev_per_attempt | 1,045.3 |
| ev_p05 | 497.3 |
| ev_p95 | 1,656.7 |

Fee $393 (EUR list x ECB rate), refunded with the first reward. Costs: 0.84 pts per fill, no commission. Holdout contaminated.

![[ftmo_late_trend-equity.png]]
