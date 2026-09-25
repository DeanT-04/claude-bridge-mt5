---
type: idea
status: pre-registered
created: 2026-09-25
family: supertrend
instruments: ['NQ', 'ES']
strategy: supertrend_15m
---
# supertrend_15m

## Hypothesis
[15m bars] Supertrend(10, mult) direction flips on intraday bars mark tradeable trend changes.

## Mechanism
An ATR-based trailing regime line filters noise from genuine trend changes.

## Exact rules
Enter on a direction flip (optionally only with the 200-EMA trend), exit on the opposite flip or an ATR stop; 09:35-15:00; flat 15:55.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| mult | [2.0, 3.0] | pre-set grid |
| sl_atr | [2.0, 3.0] | pre-set grid |
| align | [False, True] | pre-set grid |

## Expected failure modes
More trials make the Deflated Sharpe stricter; a filter that only removes days also removes sample size; regime labels can flip around their thresholds. Classic indicator rules are widely known and may be arbitraged.

## Sources
- Classic technical analysis (Donchian/Turtles, Bollinger, Connors, Appel MACD, Wilder ADX)
