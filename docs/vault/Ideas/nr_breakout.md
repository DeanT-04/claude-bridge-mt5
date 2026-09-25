---
type: idea
status: pre-registered
created: 2026-09-25
family: narrow_range
instruments: ['NQ', 'ES']
strategy: nr_breakout
---
# nr_breakout

## Hypothesis
After the narrowest daily range of the last 4/7 days (NR4/NR7), the next day's break of that range extends.

## Mechanism
Volatility contraction precedes expansion (Crabel).

## Exact rules
If yesterday's RTH range was the narrowest of the last `nr` days: OCO stops at yesterday's high/low from 09:30 to 12:00; stop `sl_frac` x that range; target `tp_mult` x range; flat 15:55.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| nr | [4, 7] | pre-set grid |
| sl_frac | [0.5, 1.0] | pre-set grid |
| tp_mult | [1.0, 2.0] | pre-set grid |

## Expected failure modes
More trials make the Deflated Sharpe stricter; a filter that only removes days also removes sample size; regime labels can flip around their thresholds.

## Sources
- Oxford Strat inbox article: 'Price Breakout with NR7'
- Crabel (1990)
