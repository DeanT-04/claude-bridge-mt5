---
type: strategy
strategy: blueberry:ib_twap
firm: blueberry
verdict: graveyard
run_id: 1176487bbc
---
# blueberry:ib_twap: **GRAVEYARD** (blueberry prime 50K, CFD costs)

| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1215 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0015 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9980 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | 2,361.1 | > 0 | stat | PASS |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.3259 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.4073 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.8003 | >= 0.7 | commercial | PASS |
| Median sessions to pass | 76.0 | <= 15 | speed | FAIL |
| 90th pct sessions to pass | 169.0 | <= 30 | speed | FAIL |

| metric | value |
|---|---|
| starts | 1488 |
| eval_pass | 0.4073 |
| eval_fail | 0.5860 |
| eval_expired | 0.0000 |
| median_sessions_to_pass | 76.0 |
| p90_sessions_to_pass | 169.0 |
| first_payout_given_pass | 0.8003 |
| end_to_end_payout | 0.3259 |
| ev_per_attempt | 3,647.7 |
| ev_p05 | 2,361.1 |
| ev_p95 | 5,036.7 |

Fee $325 (list price; refunded with first reward: False). Costs: 0.84 pts per fill, no commission. Holdout contaminated.

![[blueberry_ib_twap-equity.png]]
