---
type: idea
status: pre-registered
created: 2026-09-25
family: twap_reversion
instruments: ['NQ', 'ES']
strategy: twap_reversion
---
# twap_reversion

## Hypothesis
Stretches of k x ATR away from the session average price revert toward it during the middle of the day.

## Mechanism
VWAP/TWAP is an execution benchmark; algos trading against it pull price back. The proxy has no real volume, so TWAP stands in for VWAP.

## Exact rules
From `start` to 15:00, fade a close >= `k` x ATR14(daily) from the session TWAP (since 09:30); target TWAP; stop `sl_mult` x k x ATR; up to 2 per day; flat 15:55.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| k | [0.3, 0.5] | pre-set grid |
| sl_mult | [0.5, 1.0] | pre-set grid |
| start | [600, 630] | pre-set grid |

## Expected failure modes
More trials make the Deflated Sharpe stricter; a filter that only removes days also removes sample size; regime labels can flip around their thresholds.

## Sources
- YouTube inbox: several VWAP mean-reversion videos (e.g. 'Master VWAP Trading Strategy', 'My Exact Mean Reversion Trading Framework (NQ)')
