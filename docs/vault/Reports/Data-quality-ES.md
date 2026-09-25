---
type: report
kind: data-quality
symbol: ES
generated: 2026-09-25
---
# Data quality: ES proxy 1m bars

| check | value |
|---|---|
| rows | 4382060 |
| first | 2012-01-16 00:00:00+00:00 |
| last | 2026-09-25 09:01:00+00:00 |
| sessions | 3800 |
| duplicate_ts | 0 |
| ohlc_violations | 0 |
| negative_spread | 41 |
| intra_session_gaps_gt5m | 5571 |
| return_outliers_gt20mad | 10101 |
| dropped_weekend_bars | 229997 |
| dropped_thin_sessions | 1 |
| dropped_thin_bars | 28 |
| data_hash | 6b31ed1abba2c819 |

Reproduce: `uv run propquant data build --symbol ES`
