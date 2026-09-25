# Prop Quant Lab

Knowledge base for the prop-firm strategy research pipeline. Every discovery lives here:
winners, contenders, failures and lessons. **Read [[Lessons]] before designing anything new.**

## Rules
- **No faking.** Every number comes from a recorded run (data hash + git commit + seed).
- Hypotheses are pre-registered in `Ideas/` *before* testing. Every trial is counted.
- The holdout (2025-03-25 → 2026-09-25) is opened once per strategy and logged.

## Promotion gates (out-of-sample, ≥ 1,000 random-start challenge simulations)
| Gate | Threshold |
|---|---|
| **End-to-end payout rate** (eval bought → ≥ 1 payout) | **≥ 60%** |
| Evaluation pass rate | ≥ 85% |
| First payout, once funded | ≥ 70% |
| Days to pass | median ≤ 15, 90th pct ≤ 30 |
| Expected profit per attempt after fees | 5th-pct bootstrap > 0 |
| Statistics | DSR > 0.95, beats 95% random-entry, holdout consistent |

Verdicts: **Elite** (all gates) · **Contender** (misses only speed gates or narrowly)
· **Graveyard**.

## Leaderboard
<!-- AUTO:leaderboard:start -->
_No strategies tested yet._
<!-- AUTO:leaderboard:end -->

## Map
- `Ideas/`: pre-registered hypotheses
- `Sources/`: papers, videos, articles (our own summaries)
- `Strategies/`: one note per tested strategy, with evidence charts
- `Graveyard/`: rejected strategies and why they failed
- `Lessons/`: what we've learned across runs
- `Firms/`: verified firm rules with source URLs and dates
- `Reports/`: batch run summaries and data-quality reports
