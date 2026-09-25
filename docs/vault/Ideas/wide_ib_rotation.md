---
type: idea
status: pre-registered
created: 2026-09-25
family: ib_rotation
instruments: ['NQ', 'ES']
strategy: wide_ib_rotation
---
# wide_ib_rotation

## Hypothesis
On days whose IB is >= q x its 20-day median, the rest of the day rotates inside it: fading the IB extremes with limit orders pays.

## Mechanism
A wide first hour completes much of the day's business, so the afternoon ranges.

## Exact rules
From 10:30 to 14:30, a limit at the IB extreme nearer to price (sell the high / buy the low); stop s x IBR beyond it; target IB mid or 75% across; up to two trades; flat 15:55.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| q | [1.3, 1.6] | triage grid (fixed before testing) |
| s | [0.1, 0.2] | triage grid (fixed before testing) |
| target | ['mid', 'far25'] | triage grid (fixed before testing) |

## Expected failure modes
Inbox evidence is weak overall: arXiv:2605.04004 (walk-forward MNQ with costs) found no plain OHLC intraday signal that survived, and a video coding 10 years of ORB variants found them flat or losing after costs. Prior is low. Source credibility: Conceptual only; vendor statistics (one-sided IB breaks on ~85% of days) argue against it.

## Sources
- youtube:aBC6iKIbKgQ (Axia)
- youtube:o_rVg1bAD9k (TBM)
- Triage report: research inbox (batch 4)
