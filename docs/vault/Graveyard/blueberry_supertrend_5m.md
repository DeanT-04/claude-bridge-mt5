---
type: strategy
strategy: blueberry:supertrend_5m
firm: blueberry
verdict: graveyard
run_id: 7af14f8426
---
# blueberry:supertrend_5m: **GRAVEYARD** (blueberry prime 50K, CFD costs)

| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1892 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9680 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | 250.9 | > 0 | stat | PASS |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.1478 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1747 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.8462 | >= 0.7 | commercial | PASS |
| Median sessions to pass | 68.5 | <= 15 | speed | FAIL |
| 90th pct sessions to pass | 118.1 | <= 30 | speed | FAIL |

| metric | value |
|---|---|
| starts | 1488 |
| eval_pass | 0.1747 |
| eval_fail | 0.4133 |
| eval_expired | 0.0000 |
| median_sessions_to_pass | 68.5 |
| p90_sessions_to_pass | 118.1 |
| first_payout_given_pass | 0.8462 |
| end_to_end_payout | 0.1478 |
| ev_per_attempt | 798.8 |
| ev_p05 | 250.9 |
| ev_p95 | 1,371.2 |

Fee $325 (list price; refunded with first reward: False). Costs: 0.84 pts per fill, no commission. Holdout contaminated.

![[blueberry_supertrend_5m-equity.png]]
