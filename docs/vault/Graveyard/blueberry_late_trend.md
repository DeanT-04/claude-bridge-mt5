---
type: strategy
strategy: blueberry:late_trend
firm: blueberry
verdict: graveyard
run_id: 24ff075bf5
---
# blueberry:late_trend: **GRAVEYARD** (blueberry prime 50K, CFD costs)

| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 632 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0110 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9990 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | 297.9 | > 0 | stat | PASS |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.2413 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2749 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.8778 | >= 0.7 | commercial | PASS |
| Median sessions to pass | 78.0 | <= 15 | speed | FAIL |
| 90th pct sessions to pass | 398.0 | <= 30 | speed | FAIL |

| metric | value |
|---|---|
| starts | 1488 |
| eval_pass | 0.2749 |
| eval_fail | 0.5047 |
| eval_expired | 0.0000 |
| median_sessions_to_pass | 78.0 |
| p90_sessions_to_pass | 398.0 |
| first_payout_given_pass | 0.8778 |
| end_to_end_payout | 0.2413 |
| ev_per_attempt | 829.7 |
| ev_p05 | 297.9 |
| ev_p95 | 1,408.1 |

Fee $325 (list price; refunded with first reward: False). Costs: 0.84 pts per fill, no commission. Holdout contaminated.

![[blueberry_late_trend-equity.png]]
