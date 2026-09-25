---
type: strategy
strategy: blueberry:donchian_break_15m
firm: blueberry
verdict: graveyard
run_id: 0a7805a821
---
# blueberry:donchian_break_15m: **GRAVEYARD** (blueberry prime 50K, CFD costs)

| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1996 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9400 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -277.6 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0578 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0712 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.8113 | >= 0.7 | commercial | PASS |
| Median sessions to pass | 48.0 | <= 15 | speed | FAIL |
| 90th pct sessions to pass | 155.5 | <= 30 | speed | FAIL |

| metric | value |
|---|---|
| starts | 1488 |
| eval_pass | 0.0712 |
| eval_fail | 0.7419 |
| eval_expired | 0.0000 |
| median_sessions_to_pass | 48.0 |
| p90_sessions_to_pass | 155.5 |
| first_payout_given_pass | 0.8113 |
| end_to_end_payout | 0.0578 |
| ev_per_attempt | -80.1 |
| ev_p05 | -277.6 |
| ev_p95 | 162.4 |

Fee $325 (list price; refunded with first reward: False). Costs: 0.84 pts per fill, no commission. Holdout contaminated.

![[blueberry_donchian_break_15m-equity.png]]
