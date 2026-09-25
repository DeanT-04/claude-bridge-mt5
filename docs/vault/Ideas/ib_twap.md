---
type: idea
status: pre-registered
created: 2026-09-25
family: initial_balance
instruments: ['NQ', 'ES']
strategy: ib_twap
---
# ib_twap

## Hypothesis
Initial-balance breakouts in the direction of price vs the session average (VWAP side) at 10:30 are the profitable half of IB breaks.

## Mechanism
Price above VWAP at the end of the IB signals buyers in control; breaks with that flow extend.

## Exact rules
IB = 09:30-10:30 range; at 10:30 take the side of close vs session TWAP; single stop order at IB high (long) or low (short) until 14:00; stop `sl_frac` x IB; target `tp_mult` x IB; flat 15:55.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| sl_frac | [0.5, 1.0] | pre-set grid |
| tp_mult | [1.0, 2.0] | pre-set grid |

## Expected failure modes
More trials make the Deflated Sharpe stricter; a filter that only removes days also removes sample size; regime labels can flip around their thresholds.

## Sources
- YouTube inbox: 'How I Used Initial Balance & VWAP to Get 7 Payouts in 10 Days'
