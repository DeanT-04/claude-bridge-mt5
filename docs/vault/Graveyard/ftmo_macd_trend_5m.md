---
type: strategy
strategy: ftmo:macd_trend_5m
firm: ftmo
verdict: graveyard
run_id: d8bbb58709
---
# ftmo:macd_trend_5m: **GRAVEYARD** (FTMO 2-Step 50K, CFD costs)

| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 2894 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0003 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9960 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -5.7070 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0988 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1210 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.8167 | >= 0.7 | commercial | PASS |
| Median sessions to pass | 64.0 | <= 15 | speed | FAIL |
| 90th pct sessions to pass | 120.1 | <= 30 | speed | FAIL |

| metric | value |
|---|---|
| starts | 1488 |
| eval_pass | 0.1210 |
| eval_fail | 0.5168 |
| eval_expired | 0.0000 |
| median_sessions_to_pass | 64.0 |
| p90_sessions_to_pass | 120.1 |
| first_payout_given_pass | 0.8167 |
| end_to_end_payout | 0.0988 |
| ev_per_attempt | 560.0 |
| ev_p05 | -5.7070 |
| ev_p95 | 1,165.5 |

Fee $393 (EUR list x ECB rate), refunded with the first reward. Costs: 0.84 pts per fill, no commission. Holdout contaminated.

![[ftmo_macd_trend_5m-equity.png]]
