---
type: idea
status: pre-registered
created: 2026-09-25
family: initial_balance
instruments: ['NQ', 'ES']
strategy: ib_breakout__quiet_overnight
---
# ib_breakout__quiet_overnight

## Hypothesis
The real timing edge of [[ib_breakout]] (beat 98-99.9% of random entries in batch 1) is concentrated in one regime: Overnight range below 0.5 x ATR: the cash open has not been pre-empted, so opening breakouts have room to run.

## Mechanism
Same mechanism as [[ib_breakout]]; the filter `quiet_overnight` (known 09:29 ET) keeps only sessions where that mechanism should be strongest.

## Exact rules
Exactly [[ib_breakout]]'s rules and grid; new positions only on sessions where `quiet_overnight` is true. Filter defined in `strategies/filters.py`.

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
