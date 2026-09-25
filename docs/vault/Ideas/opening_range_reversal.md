---
type: idea
status: pre-registered
created: 2026-09-25
family: opening_reversal
instruments: ['NQ', 'ES']
strategy: opening_range_reversal
---
# opening_range_reversal

## Hypothesis
An early move against the 50-day trend of >= p x ATR (before 11:00) is reversed: a stop above the last completed 5-minute bar catches the turn.

## Mechanism
Early counter-trend moves are liquidity-seeking; the daily trend reasserts.

## Exact rules
Bias from the prior close vs its 50-day SMA (or off). Buy stop 1 tick above the last completed 5m high (sell mirror) until 11:30; stop 2 ticks beyond the session extreme; target a g fraction of the move back toward the open; one trade; flat 15:55.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| p | [0.2, 0.3, 0.4] | triage grid (fixed before testing) |
| g | [0.5, 1.0] | triage grid (fixed before testing) |
| bias | [True, False] | triage grid (fixed before testing) |

## Expected failure modes
Inbox evidence is weak overall: arXiv:2605.04004 (walk-forward MNQ with costs) found no plain OHLC intraday signal that survived, and a video coding 10 years of ORB variants found them flat or losing after costs. Prior is low. Source credibility: Newsletter marketing with explicit rules; no backtest shown.

## Sources
- youtube:8vufTzGZqiI 'The One Day Trading Strategy I Make A Living From'
- Triage report: research inbox (batch 4)
