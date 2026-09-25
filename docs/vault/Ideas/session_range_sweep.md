---
type: idea
status: pre-registered
created: 2026-09-25
family: liquidity_sweep
instruments: ['NQ', 'ES']
strategy: session_range_sweep
---
# session_range_sweep

## Hypothesis
A sweep beyond a pre-open range (03:00-09:29, the 8am hour, or London 02:00-05:00) that closes back inside during 09:30-11:30 reverses toward the range middle or far side.

## Mechanism
Stops cluster beyond obvious pre-open extremes and are run at the cash open.

## Exact rules
1m bar pierces the range by > 1 tick and closes back inside -> enter at next open against the sweep; stop 2 ticks beyond the sweep bar; target range mid or far side; exit by 12:00; skip ranges < 0.15 x ATR14; one trade per day.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| range | ['premarket', 'h8', 'london'] | triage grid (fixed before testing) |
| target | ['mid', 'far'] | triage grid (fixed before testing) |

## Expected failure modes
Inbox evidence is weak overall: arXiv:2605.04004 (walk-forward MNQ with costs) found no plain OHLC intraday signal that survived, and a video coding 10 years of ORB variants found them flat or losing after costs. Prior is low. Source credibility: ICT/SMC marketing; hand-picked replays.

## Sources
- youtube:Lfa2pAZ4kUE 'I Backtested CRT... 9am CRT Model'
- youtube:E9MzEC_yNoM 'Easy Futures Day Trading Strategy (5 Minute Setups)'
- youtube:8PYgFVB0GHE 'My UPDATED Day Trading Strategy (2026)'
- Triage report: research inbox (batch 4)
