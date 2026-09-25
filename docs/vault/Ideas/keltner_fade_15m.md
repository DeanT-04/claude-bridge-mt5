---
type: idea
status: pre-registered
created: 2026-09-25
family: keltner_fade
instruments: ['NQ', 'ES']
strategy: keltner_fade_15m
---
# keltner_fade_15m

## Hypothesis
[15m bars] In low-ADX (range-bound) conditions, closes outside the Keltner channel revert to its middle.

## Mechanism
Without a trend, excursions are noise that market makers fade.

## Exact rules
When ADX14 < `adx_max`: fade a close outside Keltner(20, `k` x ATR), target the channel middle, stop `sl_atr` x ATR; 09:35-15:00; flat 15:55.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| k | [2.0, 2.5] | pre-set grid |
| adx_max | [20, 25] | pre-set grid |
| sl_atr | [1.0, 1.5] | pre-set grid |

## Expected failure modes
More trials make the Deflated Sharpe stricter; a filter that only removes days also removes sample size; regime labels can flip around their thresholds. Classic indicator rules are widely known and may be arbitraged.

## Sources
- Classic technical analysis (Donchian/Turtles, Bollinger, Connors, Appel MACD, Wilder ADX)
