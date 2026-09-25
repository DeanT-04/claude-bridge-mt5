---
type: idea
status: pre-registered
created: 2026-09-25
family: instrument_extension
instruments: ['ES']
strategy: intraday_momentum@ES
---
# intraday_momentum@ES

## Hypothesis
The pre-registered hypothesis of [[intraday_momentum]] also holds on ES (E-mini S&P 500).

## Mechanism
Same mechanism as [[intraday_momentum]]; ES is the most liquid equity-index future and less tech-concentrated than NQ.

## Exact rules
Identical rules and parameter grid to [[intraday_momentum]], run on ES proxy data.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| (same as base) | ['see base note'] | no new parameters |

## Expected failure modes
ES trends less than NQ intraday; costs per point are larger relative to its range.

## Sources
- Base idea: intraday_momentum
