---
type: strategy
strategy: ftmo:ib_breakout
firm: ftmo
verdict: graveyard
run_id: d05c31ac27
---
# ftmo:ib_breakout: **GRAVEYARD** (FTMO 2-Step 50K, CFD costs)

| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1055 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0011 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9860 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -114.4 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.1042 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1458 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.7143 | >= 0.7 | commercial | PASS |
| Median sessions to pass | 45.0 | <= 15 | speed | FAIL |
| 90th pct sessions to pass | 121.4 | <= 30 | speed | FAIL |

| metric | value |
|---|---|
| starts | 1488 |
| eval_pass | 0.1458 |
| eval_fail | 0.7655 |
| eval_expired | 0.0000 |
| median_sessions_to_pass | 45.0 |
| p90_sessions_to_pass | 121.4 |
| first_payout_given_pass | 0.7143 |
| end_to_end_payout | 0.1042 |
| ev_per_attempt | 330.5 |
| ev_p05 | -114.4 |
| ev_p95 | 818.6 |

Fee $393 (EUR list x ECB rate), refunded with the first reward. Costs: 0.84 pts per fill, no commission. Holdout contaminated.

![[ftmo_ib_breakout-equity.png]]
