---
type: strategy
strategy: ftmo:ib_twap
firm: ftmo
verdict: graveyard
run_id: 85fd68f37b
---
# ftmo:ib_twap: **GRAVEYARD** (FTMO 2-Step 50K, CFD costs)

| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1215 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0048 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9980 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | 2,200.7 | > 0 | stat | PASS |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.2964 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.4099 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.7230 | >= 0.7 | commercial | PASS |
| Median sessions to pass | 85.0 | <= 15 | speed | FAIL |
| 90th pct sessions to pass | 222.1 | <= 30 | speed | FAIL |

| metric | value |
|---|---|
| starts | 1488 |
| eval_pass | 0.4099 |
| eval_fail | 0.5833 |
| eval_expired | 0.0000 |
| median_sessions_to_pass | 85.0 |
| p90_sessions_to_pass | 222.1 |
| first_payout_given_pass | 0.7230 |
| end_to_end_payout | 0.2964 |
| ev_per_attempt | 3,539.5 |
| ev_p05 | 2,200.7 |
| ev_p95 | 4,970.5 |

Fee $393 (EUR list x ECB rate), refunded with the first reward. Costs: 0.84 pts per fill, no commission. Holdout contaminated.

![[ftmo_ib_twap-equity.png]]
