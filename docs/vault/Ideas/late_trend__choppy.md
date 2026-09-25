---
type: idea
status: pre-registered
created: 2026-09-25
family: late_trend
instruments: ['NQ', 'ES']
strategy: late_trend__choppy
---
# late_trend__choppy

## Hypothesis
The real timing edge of [[late_trend]] (beat 98-99.9% of random entries in batch 1) is concentrated in one regime: Efficiency ratio < 0.3: directionless, mean-reverting tape.

## Mechanism
Same mechanism as [[late_trend]]; the filter `choppy` (known pre-session) keeps only sessions where that mechanism should be strongest.

## Exact rules
Exactly [[late_trend]]'s rules and grid; new positions only on sessions where `choppy` is true. Filter defined in `strategies/filters.py`.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| decide | [780, 840] | pre-set grid |
| k | [0.3, 0.5, 0.8] | pre-set grid |
| sl_atr | [0.25, 0.5] | pre-set grid |

## Expected failure modes
More trials make the Deflated Sharpe stricter; a filter that only removes days also removes sample size; regime labels can flip around their thresholds.

## Sources
- Lesson: Batch 1 - classic intraday families have timing but not enough edge
- Base idea: late_trend
