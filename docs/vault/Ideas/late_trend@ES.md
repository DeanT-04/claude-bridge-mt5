---
type: idea
status: pre-registered
created: 2026-09-25
family: instrument_extension
instruments: ['ES']
strategy: late_trend@ES
---
# late_trend@ES

## Hypothesis
The pre-registered hypothesis of [[late_trend]] also holds on ES (E-mini S&P 500).

## Mechanism
Same mechanism as [[late_trend]]; ES is the most liquid equity-index future and less tech-concentrated than NQ.

## Exact rules
Identical rules and parameter grid to [[late_trend]], run on ES proxy data.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| (same as base) | ['see base note'] | no new parameters |

## Expected failure modes
ES trends less than NQ intraday; costs per point are larger relative to its range.

## Sources
- Base idea: late_trend
