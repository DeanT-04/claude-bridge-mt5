---
type: idea
status: pre-registered
created: 2026-09-25
family: overnight_failure
instruments: ['NQ', 'ES']
strategy: overnight_failure_fade
---
# overnight_failure_fade

## Hypothesis
After a strong one-way overnight move (>= k x ATR, closing in the extreme c of the overnight range) that the first cash hour fails to extend, price washes back toward the prior close.

## Mechanism
Overnight moves are carried by weak, one-sided inventory. When the cash session cannot extend them, those holders liquidate (the 'overnight up, intraday down' reversal).

## Exact rules
Enter at the 10:30 close against the overnight move. Stop beyond max/min(ON, IB) extreme + 2 ticks. Target: prior RTH close. Flat 15:55. Optional: require the 10:30 close on the fading side of the IB mid.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| k | [0.3, 0.5] | triage grid (fixed before testing) |
| c | [0.25, 0.4] | triage grid (fixed before testing) |
| ib_mid | [False, True] | triage grid (fixed before testing) |

## Expected failure modes
Inbox evidence is weak overall: arXiv:2605.04004 (walk-forward MNQ with costs) found no plain OHLC intraday signal that survived, and a video coding 10 years of ORB variants found them flat or losing after costs. Prior is low. Source credibility: Educator mechanism without a backtest; supporting econometrics on another market.

## Sources
- youtube:aBC6iKIbKgQ (Axia Futures, 'What Initial Balance Should You Use?')
- openalex:W2945479896 'Intraday Return Reversals: Korean ETF Market'
- Triage report: research inbox (batch 4)
