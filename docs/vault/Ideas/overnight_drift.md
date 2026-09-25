---
type: idea
status: pre-registered
created: 2026-09-25
family: overnight
instruments: ['NQ']
strategy: overnight_drift
---
# overnight_drift

## Hypothesis
Holding NQ long from the 18:00 ET session open to the 09:00/09:30 cash open earns a positive return after costs, because a large share of the equity premium accrues outside regular hours.

## Mechanism
Risk from overnight news and inventory has to be carried by someone. Market makers and institutions reduce exposure into the close and add it back at the open, so overnight holders are paid for the gap risk. Retail order flow at the open also pushes prices up.

## Exact rules
- Buy NQ at market at `entry` (18:01 or 19:00 ET), one trade per session.
- Optionally only after the previous regular session closed down (`after`=down) or up (`after`=up).
- Optional stop of `sl_pct` of price.
- Exit at `exit` (09:00 or 09:30 ET).

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| entry | [1081, 1140] | session open vs after the first hour |
| exit | [570, 540] | cash open vs before it |
| after | ['any', 'down', 'up'] | reversal vs momentum conditioning |
| sl_pct | ['none', 0.01] | unprotected vs 1% stop |

## Expected failure modes
The overnight premium is known and may have shrunk. Single overnight gaps (e.g. March 2020) are large and could breach Apex's drawdown. Costs are small relative to the move, so they're unlikely to be the problem.

## Sources
- Cliff, Cooper & Gulen (2008), Return differences between trading and non-trading hours: like night and day
- Lou, Polk & Skouras (2019), A tug of war: overnight versus intraday expected returns, JFE (in inbox via OpenAlex)
- Kelly & Clark (2011), Returns in trading versus non-trading hours
