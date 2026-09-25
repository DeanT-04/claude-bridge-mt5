---
type: strategy
strategy: ftmo:donchian_break_5m
firm: ftmo
verdict: graveyard
run_id: 96a7fb5268
---
# ftmo:donchian_break_5m: **GRAVEYARD** (FTMO 2-Step 50K, CFD costs)

| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 3572 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9240 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -393.4 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0087 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0155 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.5652 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 98.0 | <= 15 | speed | FAIL |
| 90th pct sessions to pass | 117.8 | <= 30 | speed | FAIL |

| metric | value |
|---|---|
| starts | 1488 |
| eval_pass | 0.0155 |
| eval_fail | 0.9765 |
| eval_expired | 0.0000 |
| median_sessions_to_pass | 98.0 |
| p90_sessions_to_pass | 117.8 |
| first_payout_given_pass | 0.5652 |
| end_to_end_payout | 0.0087 |
| ev_per_attempt | -382.4 |
| ev_p05 | -393.4 |
| ev_p95 | -363.5 |

Fee $393 (EUR list x ECB rate), refunded with the first reward. Costs: 0.84 pts per fill, no commission. Holdout contaminated.

![[ftmo_donchian_break_5m-equity.png]]
