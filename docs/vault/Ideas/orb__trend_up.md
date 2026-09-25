---
type: idea
status: pre-registered
created: 2026-09-25
family: opening_range
instruments: ['NQ', 'ES']
strategy: orb__trend_up
---
# orb__trend_up

## Hypothesis
The real timing edge of [[orb]] (beat 98-99.9% of random entries in batch 1) is concentrated in one regime: Trade only when the prior close is above its 50-day SMA (bull regime; buy-the-dip and long breakouts work better).

## Mechanism
Same mechanism as [[orb]]; the filter `trend_up` (known pre-session) keeps only sessions where that mechanism should be strongest.

## Exact rules
Exactly [[orb]]'s rules and grid; new positions only on sessions where `trend_up` is true. Filter defined in `strategies/filters.py`.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| or_min | [5, 15, 30] | pre-set grid |
| sl_frac | [0.5, 1.0] | pre-set grid |
| tp_mult | [1.0, 2.0] | pre-set grid |

## Expected failure modes
More trials make the Deflated Sharpe stricter; a filter that only removes days also removes sample size; regime labels can flip around their thresholds.

## Sources
- Lesson: Batch 1 - classic intraday families have timing but not enough edge
- Base idea: orb
