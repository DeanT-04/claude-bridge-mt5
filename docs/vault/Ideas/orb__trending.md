---
type: idea
status: pre-registered
created: 2026-09-25
family: opening_range
instruments: ['NQ', 'ES']
strategy: orb__trending
---
# orb__trending

## Hypothesis
The real timing edge of [[orb]] (beat 98-99.9% of random entries in batch 1) is concentrated in one regime: Kaufman efficiency ratio of the last 10 daily closes >= 0.3: the market has been moving directionally.

## Mechanism
Same mechanism as [[orb]]; the filter `trending` (known pre-session) keeps only sessions where that mechanism should be strongest.

## Exact rules
Exactly [[orb]]'s rules and grid; new positions only on sessions where `trending` is true. Filter defined in `strategies/filters.py`.

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
