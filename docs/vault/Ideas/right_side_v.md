---
type: idea
status: pre-registered
created: 2026-09-25
family: capitulation_reversal
instruments: ['NQ', 'ES']
strategy: right_side_v
---
# right_side_v

## Hypothesis
After a fast drop (60-minute high to low >= m x ATR14) between 10:00 and 14:30, buying the first 5-minute close above the prior 5-minute high has positive expectancy (long only).

## Mechanism
Sell-side liquidity shocks overshoot and are replenished; waiting for the turn avoids catching the falling knife.

## Exact rules
Long at the next open after the confirming 5m close; stop 2 ticks under the V low; target V low + f x (60-minute high - V low); time stop `hold` minutes; one trade per day; flat 15:55.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| m | [0.35, 0.5, 0.7] | triage grid (fixed before testing) |
| f | [0.5, 1.0] | triage grid (fixed before testing) |
| hold | [30, 90] | triage grid (fixed before testing) |

## Expected failure modes
Inbox evidence is weak overall: arXiv:2605.04004 (walk-forward MNQ with costs) found no plain OHLC intraday signal that survived, and a video coding 10 years of ORB variants found them flat or losing after costs. Prior is low. Source credibility: Tick-level SPY asymmetry without costs; anecdotal trader method.

## Sources
- arXiv:2511.06177 'Push-response anomalies in high-frequency S&P 500 price series'
- youtube:wtQIj6Apiq0 'Right Side of the V' (Breitstein)
- Triage report: research inbox (batch 4)
