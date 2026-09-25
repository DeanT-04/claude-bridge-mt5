---
type: strategy
strategy: ftmo:donchian_break_15m
firm: ftmo
verdict: graveyard
run_id: 78150ac8ea
---
# ftmo:donchian_break_15m: **GRAVEYARD** (FTMO 2-Step 50K, CFD costs)

| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1996 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9400 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -228.5 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0733 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0806 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.9083 | >= 0.7 | commercial | PASS |
| Median sessions to pass | 53.0 | <= 15 | speed | FAIL |
| 90th pct sessions to pass | 97.1 | <= 30 | speed | FAIL |

| metric | value |
|---|---|
| starts | 1488 |
| eval_pass | 0.0806 |
| eval_fail | 0.7070 |
| eval_expired | 0.0000 |
| median_sessions_to_pass | 53.0 |
| p90_sessions_to_pass | 97.1 |
| first_payout_given_pass | 0.9083 |
| end_to_end_payout | 0.0733 |
| ev_per_attempt | 87.7 |
| ev_p05 | -228.5 |
| ev_p95 | 438.4 |

Fee $393 (EUR list x ECB rate), refunded with the first reward. Costs: 0.84 pts per fill, no commission. Holdout contaminated.

![[ftmo_donchian_break_15m-equity.png]]
