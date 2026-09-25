---
type: strategy
strategy: ftmo:orb
firm: ftmo
verdict: graveyard
run_id: 43ff63c490
---
# ftmo:orb: **GRAVEYARD** (FTMO 2-Step 50K, CFD costs)

| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1589 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0031 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9950 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | 5.8909 | > 0 | stat | PASS |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.2802 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.3481 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.8050 | >= 0.7 | commercial | PASS |
| Median sessions to pass | 703.5 | <= 15 | speed | FAIL |
| 90th pct sessions to pass | 923.3 | <= 30 | speed | FAIL |

| metric | value |
|---|---|
| starts | 1488 |
| eval_pass | 0.3481 |
| eval_fail | 0.3360 |
| eval_expired | 0.0000 |
| median_sessions_to_pass | 703.5 |
| p90_sessions_to_pass | 923.3 |
| first_payout_given_pass | 0.8050 |
| end_to_end_payout | 0.2802 |
| ev_per_attempt | 161.2 |
| ev_p05 | 5.8909 |
| ev_p95 | 349.9 |

Fee $393 (EUR list x ECB rate), refunded with the first reward. Costs: 0.84 pts per fill, no commission. Holdout contaminated.

![[ftmo_orb-equity.png]]
