---
type: strategy
strategy: blueberry:donchian_break_5m
firm: blueberry
verdict: graveyard
run_id: bac9db3bff
---
# blueberry:donchian_break_5m: **GRAVEYARD** (blueberry prime 50K, CFD costs)

| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 3572 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9240 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -325.0 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0134 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0202 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.6667 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 96.5 | <= 15 | speed | FAIL |
| 90th pct sessions to pass | 125.0 | <= 30 | speed | FAIL |

| metric | value |
|---|---|
| starts | 1488 |
| eval_pass | 0.0202 |
| eval_fail | 0.9798 |
| eval_expired | 0.0000 |
| median_sessions_to_pass | 96.5 |
| p90_sessions_to_pass | 125.0 |
| first_payout_given_pass | 0.6667 |
| end_to_end_payout | 0.0134 |
| ev_per_attempt | -313.3 |
| ev_p05 | -325.0 |
| ev_p95 | -295.2 |

Fee $325 (list price; refunded with first reward: False). Costs: 0.84 pts per fill, no commission. Holdout contaminated.

![[blueberry_donchian_break_5m-equity.png]]
