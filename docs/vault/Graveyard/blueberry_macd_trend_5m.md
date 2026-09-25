---
type: strategy
strategy: blueberry:macd_trend_5m
firm: blueberry
verdict: graveyard
run_id: b6a41c7c12
---
# blueberry:macd_trend_5m: **GRAVEYARD** (blueberry prime 50K, CFD costs)

| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 2894 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0001 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9960 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | 74.0 | > 0 | stat | PASS |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.1042 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1411 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.7381 | >= 0.7 | commercial | PASS |
| Median sessions to pass | 60.0 | <= 15 | speed | FAIL |
| 90th pct sessions to pass | 117.1 | <= 30 | speed | FAIL |

| metric | value |
|---|---|
| starts | 1488 |
| eval_pass | 0.1411 |
| eval_fail | 0.5148 |
| eval_expired | 0.0000 |
| median_sessions_to_pass | 60.0 |
| p90_sessions_to_pass | 117.1 |
| first_payout_given_pass | 0.7381 |
| end_to_end_payout | 0.1042 |
| ev_per_attempt | 645.6 |
| ev_p05 | 74.0 |
| ev_p95 | 1,258.5 |

Fee $325 (list price; refunded with first reward: False). Costs: 0.84 pts per fill, no commission. Holdout contaminated.

![[blueberry_macd_trend_5m-equity.png]]
