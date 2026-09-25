---
type: idea
status: pre-registered
created: 2026-09-25
family: donchian_break
instruments: ['NQ', 'ES']
strategy: donchian_break_5m
---
# donchian_break_5m

## Hypothesis
[5m bars] Closes beyond the prior n-bar high/low (Turtle-style Donchian breaks) continue far enough intraday to pay for the losers.

## Mechanism
Breaking a range triggers resting stops and momentum algos.

## Exact rules
Long when the close exceeds the highest high of the previous `n` bars, short below the lowest low; ATR bracket; 09:35-15:00; flat 15:55.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| n | [20, 55] | pre-set grid |
| sl_atr | [1.0, 2.0] | pre-set grid |
| tp_atr | [2.0, 4.0] | pre-set grid |

## Expected failure modes
More trials make the Deflated Sharpe stricter; a filter that only removes days also removes sample size; regime labels can flip around their thresholds. Classic indicator rules are widely known and may be arbitraged.

## Sources
- Classic technical analysis (Donchian/Turtles, Bollinger, Connors, Appel MACD, Wilder ADX)
