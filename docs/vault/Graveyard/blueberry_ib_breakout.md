---
type: strategy
strategy: blueberry:ib_breakout
firm: blueberry
verdict: graveyard
run_id: b4a61a520e
---
# blueberry:ib_breakout: **GRAVEYARD** (blueberry prime 50K, CFD costs)

| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1055 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0003 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9860 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -325.0 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0094 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0470 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2000 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 16.5 | <= 15 | speed | FAIL |
| 90th pct sessions to pass | 114.1 | <= 30 | speed | FAIL |

| metric | value |
|---|---|
| starts | 1488 |
| eval_pass | 0.0470 |
| eval_fail | 0.8266 |
| eval_expired | 0.0000 |
| median_sessions_to_pass | 16.5 |
| p90_sessions_to_pass | 114.1 |
| first_payout_given_pass | 0.2000 |
| end_to_end_payout | 0.0094 |
| ev_per_attempt | -306.9 |
| ev_p05 | -325.0 |
| ev_p95 | -278.8 |

Fee $325 (list price; refunded with first reward: False). Costs: 0.84 pts per fill, no commission. Holdout contaminated.

![[blueberry_ib_breakout-equity.png]]
