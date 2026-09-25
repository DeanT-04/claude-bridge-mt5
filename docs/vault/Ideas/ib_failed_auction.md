---
type: idea
status: pre-registered
created: 2026-09-25
family: failed_auction
instruments: ['NQ', 'ES']
strategy: ib_failed_auction
---
# ib_failed_auction

## Hypothesis
After 10:30, a B-minute block that pierces the IB extreme by >2 ticks but closes back inside marks a failed auction that rotates back into the IB.

## Mechanism
Market-profile failed auction: excursions outside first-hour value find no acceptance and are reversed.

## Exact rules
Enter at the next bar open toward the IB; stop 2 ticks beyond the extreme since 10:30; target IB extreme + t x IBR inside; up to one trade per side per day; entries until 15:00; flat 15:55. Optional double sweep: the excursion also takes the overnight extreme.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| block | [5, 30] | triage grid (fixed before testing) |
| t | [0.25, 0.5] | triage grid (fixed before testing) |
| double_sweep | [False, True] | triage grid (fixed before testing) |

## Expected failure modes
Inbox evidence is weak overall: arXiv:2605.04004 (walk-forward MNQ with costs) found no plain OHLC intraday signal that survived, and a video coding 10 years of ORB variants found them flat or losing after costs. Prior is low. Source credibility: Three independent educators, no statistics (a self-reported 85% win rate).

## Sources
- youtube:lOnEKIWj0S8 'Initial Balance Masterclass'
- youtube:gGrnIm9wpx0 'IB Indicator Day Trading Strategy'
- youtube:o_rVg1bAD9k 'How to use Initial Balance (TBM)'
- Triage report: research inbox (batch 4)
