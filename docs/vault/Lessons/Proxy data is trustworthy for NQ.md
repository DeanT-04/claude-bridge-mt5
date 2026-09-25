---
type: lesson
created: 2026-09-25
evidence: ["[[Proxy-fidelity-NQ]]", "[[Data-quality-NQ]]"]
---
# Proxy data is trustworthy for NQ and ES (2016 onward)

## What we observed
- Dukascopy's free NASDAQ-100 CFD, taken as the mid of bid and ask, tracks real CME NQ futures almost perfectly:
  - bar return correlation: 0.992 at 1m, 0.998 at 5m, 1.000 at 1h
  - high and low excursions from the bar open: correlation ≥ 0.98
  - session highs and lows at the same minute (±5) on every session compared
  - the high-before-low order inside 15m bars matches **98.7%** of the time
- The data before 2016 is poor:
  - weekend quotes (230k bars dropped)
  - many gaps inside sessions in 2012–2015
  - every OHLC inconsistency is in 2013

- **ES** also passes:
  - return correlation 0.985 (1m), 0.997 (5m), 0.999 (1h)
  - the high-before-low order inside a bar matches 96.1% of the time
  - since 2016 there are only 86 gaps during regular trading hours; the 2020 ones are most likely the March 2020 limit-down halts
  - overnight gaps are quiet periods with no quotes

  See [[Proxy-fidelity-ES]].

## Why it matters
Stop and target fills depend on bar highs, lows and their order. That fidelity is what makes backtest fills on proxy data believable for futures.

## How to apply it next time
- Research history starts **2016-01-01**. Treat earlier data as unreliable.
- Strategies must be flat by 16:10 ET, because the proxy has no bars from 16:15 to 17:00.
- Don't build rules on proxy volume: it's tick activity, not contracts.
- Re-run `propquant data tracking` as the forward futures dataset grows. The 1m comparison currently covers only 6 sessions.
