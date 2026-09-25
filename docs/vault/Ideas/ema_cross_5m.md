---
type: idea
status: pre-registered
created: 2026-09-25
family: ema_cross
instruments: ['NQ', 'ES']
strategy: ema_cross_5m
---
# ema_cross_5m

## Hypothesis
[5m bars] Fast/slow EMA crossovers on intraday bars catch the start of intraday trends often enough that ATR-bracketed trades have positive expectancy.

## Mechanism
Intraday trends persist as institutions split large orders over hours; a cross marks the shift of short-term order flow.

## Exact rules
Long when EMA(fast) crosses above EMA(slow), short on the opposite cross; entries 09:35-15:00 ET, up to 3 per day; stop `sl_atr` x ATR14, target `tp_atr` x ATR14 (ATR on the strategy's bars); flat at 15:55.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| pair | [(9, 21), (20, 50), (50, 200)] | pre-set grid |
| sl_atr | [1.0, 2.0] | pre-set grid |
| tp_atr | [2.0, 4.0] | pre-set grid |

## Expected failure modes
More trials make the Deflated Sharpe stricter; a filter that only removes days also removes sample size; regime labels can flip around their thresholds. Classic indicator rules are widely known and may be arbitraged.

## Sources
- Classic technical analysis (Donchian/Turtles, Bollinger, Connors, Appel MACD, Wilder ADX)
