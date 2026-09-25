---
type: idea
status: pre-registered
created: 2026-09-25
family: initial_balance
instruments: ['NQ', 'ES']
strategy: ib_breakout__trend_up
---
# ib_breakout__trend_up

## Hypothesis
The real timing edge of [[ib_breakout]] (beat 98-99.9% of random entries in batch 1) is concentrated in one regime: Trade only when the prior close is above its 50-day SMA (bull regime; buy-the-dip and long breakouts work better).

## Mechanism
Same mechanism as [[ib_breakout]]; the filter `trend_up` (known pre-session) keeps only sessions where that mechanism should be strongest.

## Exact rules
Exactly [[ib_breakout]]'s rules and grid; new positions only on sessions where `trend_up` is true. Filter defined in `strategies/filters.py`.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| ib_min | [30, 60] | pre-set grid |
| narrow | [inf, 0.8] | pre-set grid |
| tp_mult | [1.0, 2.0] | pre-set grid |
| sl_frac | [0.5, 1.0] | pre-set grid |

## Expected failure modes
More trials make the Deflated Sharpe stricter; a filter that only removes days also removes sample size; regime labels can flip around their thresholds.

## Sources
- Lesson: Batch 1 - classic intraday families have timing but not enough edge
- Base idea: ib_breakout
