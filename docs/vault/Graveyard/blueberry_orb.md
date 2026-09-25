---
type: strategy
strategy: blueberry:orb
firm: blueberry
verdict: graveyard
run_id: 1d1d3d92d2
---
# blueberry:orb: **GRAVEYARD** (blueberry prime 50K, CFD costs)

| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1589 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0009 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9950 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | 112.2 | > 0 | stat | PASS |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.3387 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.4409 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.7683 | >= 0.7 | commercial | PASS |
| Median sessions to pass | 574.0 | <= 15 | speed | FAIL |
| 90th pct sessions to pass | 893.5 | <= 30 | speed | FAIL |

| metric | value |
|---|---|
| starts | 1488 |
| eval_pass | 0.4409 |
| eval_fail | 0.3441 |
| eval_expired | 0.0000 |
| median_sessions_to_pass | 574.0 |
| p90_sessions_to_pass | 893.5 |
| first_payout_given_pass | 0.7683 |
| end_to_end_payout | 0.3387 |
| ev_per_attempt | 280.2 |
| ev_p05 | 112.2 |
| ev_p95 | 483.0 |

Fee $325 (list price; refunded with first reward: False). Costs: 0.84 pts per fill, no commission. Holdout contaminated.

![[blueberry_orb-equity.png]]
