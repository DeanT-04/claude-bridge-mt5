---
type: idea
status: pre-registered
created: 2026-09-25
family: rsi2_pullback
instruments: ['NQ', 'ES']
strategy: rsi2_pullback_5m
---
# rsi2_pullback_5m

## Hypothesis
[5m bars] Connors RSI(2): short, sharp pullbacks inside an intraday trend revert in the trend's direction.

## Mechanism
Liquidity-providing flows absorb over-extended moves against the prevailing trend.

## Exact rules
Long when close > EMA(`trend`) and RSI(2) < `lo`; short when close < EMA and RSI(2) > 100-`lo`; ATR bracket; 09:35-15:00; flat 15:55.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| trend | [100, 200] | pre-set grid |
| lo | [5, 10] | pre-set grid |
| sl_atr | [1.0, 2.0] | pre-set grid |
| tp_atr | [1.0, 2.0] | pre-set grid |

## Expected failure modes
More trials make the Deflated Sharpe stricter; a filter that only removes days also removes sample size; regime labels can flip around their thresholds. Classic indicator rules are widely known and may be arbitraged.

## Sources
- Classic technical analysis (Donchian/Turtles, Bollinger, Connors, Appel MACD, Wilder ADX)
