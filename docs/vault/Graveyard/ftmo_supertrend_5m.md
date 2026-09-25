---
type: strategy
strategy: ftmo:supertrend_5m
firm: ftmo
verdict: graveyard
run_id: e62f56dcbb
---
# ftmo:supertrend_5m: **GRAVEYARD** (FTMO 2-Step 50K, CFD costs)

| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1892 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0001 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9680 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | 640.4 | > 0 | stat | PASS |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.1687 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1835 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.9194 | >= 0.7 | commercial | PASS |
| Median sessions to pass | 65.0 | <= 15 | speed | FAIL |
| 90th pct sessions to pass | 122.0 | <= 30 | speed | FAIL |

| metric | value |
|---|---|
| starts | 1488 |
| eval_pass | 0.1835 |
| eval_fail | 0.4469 |
| eval_expired | 0.0000 |
| median_sessions_to_pass | 65.0 |
| p90_sessions_to_pass | 122.0 |
| first_payout_given_pass | 0.9194 |
| end_to_end_payout | 0.1687 |
| ev_per_attempt | 1,482.5 |
| ev_p05 | 640.4 |
| ev_p95 | 2,383.6 |

Fee $393 (EUR list x ECB rate), refunded with the first reward. Costs: 0.84 pts per fill, no commission. Holdout contaminated.

![[ftmo_supertrend_5m-equity.png]]
