---
type: idea
status: pre-registered
created: 2026-09-25
family: bb_squeeze
instruments: ['NQ', 'ES']
strategy: bb_squeeze_5m
---
# bb_squeeze_5m

## Hypothesis
[5m bars] After Bollinger bandwidth compresses to its lowest quantile, the first close outside the bands starts a directional expansion.

## Mechanism
Volatility is mean-reverting and clusters: compression precedes expansion.

## Exact rules
Squeeze = previous bar's BB(20,2) width in the lowest `q` of the last 100 bars; enter in the direction of the first close outside a band; ATR bracket; 09:35-15:00; flat 15:55.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| q | [0.1, 0.2] | pre-set grid |
| sl_atr | [1.0, 2.0] | pre-set grid |
| tp_atr | [2.0, 4.0] | pre-set grid |

## Expected failure modes
More trials make the Deflated Sharpe stricter; a filter that only removes days also removes sample size; regime labels can flip around their thresholds. Classic indicator rules are widely known and may be arbitraged.

## Sources
- Classic technical analysis (Donchian/Turtles, Bollinger, Connors, Appel MACD, Wilder ADX)
