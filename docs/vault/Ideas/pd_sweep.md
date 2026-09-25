---
type: idea
status: pre-registered
created: 2026-09-25
family: liquidity_sweep
instruments: ['NQ', 'ES']
strategy: pd_sweep
---
# pd_sweep

## Hypothesis
A run of yesterday's high (low) that closes back inside on a 1m bar is a failed breakout that reverses toward the middle of yesterday's range.

## Mechanism
ICT/SMC 'liquidity sweep': stops above obvious highs get taken, then price returns once that liquidity is absorbed.

## Exact rules
09:30 to `end`: short when a bar's high > yesterday's RTH high and it closes below it (long mirror at the low); stop beyond the sweep extreme + `buf` x ATR14(daily); target `tp_frac` x yesterday's range; 1 per day; flat 15:55.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| end | [720, 900] | pre-set grid |
| buf | [0.05, 0.1] | pre-set grid |
| tp_frac | [0.5, 1.0] | pre-set grid |

## Expected failure modes
More trials make the Deflated Sharpe stricter; a filter that only removes days also removes sample size; regime labels can flip around their thresholds.

## Sources
- YouTube inbox: SMC/ICT sweep videos (e.g. 'Copy This 5 Rule SMC Trading Strategy (Backtested Results)')
