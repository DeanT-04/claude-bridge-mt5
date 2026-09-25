---
type: idea
status: pre-registered
created: 2026-09-25
family: macd_trend
instruments: ['NQ', 'ES']
strategy: macd_trend_15m
---
# macd_trend_15m

## Hypothesis
[15m bars] MACD histogram zero-crosses aligned with the 200-EMA trend capture intraday momentum bursts.

## Mechanism
Momentum acceleration after consolidation, in the direction of the larger trend.

## Exact rules
Enter when the MACD(12,26,9) histogram crosses zero (optionally only with the 200-EMA trend); ATR bracket; 09:35-15:00; flat 15:55.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| align | [False, True] | pre-set grid |
| sl_atr | [1.0, 2.0] | pre-set grid |
| tp_atr | [2.0, 4.0] | pre-set grid |

## Expected failure modes
More trials make the Deflated Sharpe stricter; a filter that only removes days also removes sample size; regime labels can flip around their thresholds. Classic indicator rules are widely known and may be arbitraged.

## Sources
- Classic technical analysis (Donchian/Turtles, Bollinger, Connors, Appel MACD, Wilder ADX)
