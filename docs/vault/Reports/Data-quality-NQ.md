---
type: report
kind: data-quality
symbol: NQ
generated: 2026-09-25
---
# Data quality: NQ proxy 1m bars

| check | value |
|---|---|
| rows | 4535234 |
| first | 2012-01-19 16:15:00+00:00 |
| last | 2026-09-25 08:29:00+00:00 |
| sessions | 3793 |
| duplicate_ts | 0 |
| ohlc_violations | 363 |
| negative_spread | 14 |
| intra_session_gaps_gt5m | 1886 |
| return_outliers_gt20mad | 12804 |
| dropped_weekend_bars | 229930 |
| dropped_thin_sessions | 1 |
| dropped_thin_bars | 1 |
| data_hash | 3a26012ed92b62d5 |

Reproduce: `uv run propquant data build --symbol NQ`
