# Prop Quant Lab

Knowledge base for the prop-firm strategy research pipeline. Every discovery lives here:
winners, contenders, failures and lessons. **Read [[Lessons]] before designing anything new.**

## Rules
- **No faking.** Every number comes from a recorded run (data hash + git commit + seed).
- Hypotheses are pre-registered in `Ideas/` *before* testing. Every trial is counted.
- The holdout (2025-03-25 → 2026-09-25) is opened once per strategy and logged.

## Promotion tiers (out-of-sample, >= 1,000 random-start challenge simulations)
Ranked by **end-to-end payout rate**, meaning a purchased evaluation passes and reaches a payout.

| Tier | Needs |
|---|---|
| **Champion** | Elite, plus eval pass >= 85% and end-to-end payout >= 80% (the P7 portfolio goal) |
| **Elite** | eval pass >= 60%, end-to-end payout >= 50%, first payout once funded >= 70%, median <= 15 and p90 <= 30 sessions to pass, 5th-pct expected profit per attempt > 0, DSR > 0.95, beats 95% of random-entry runs, holdout consistent |
| **Contender** | all statistical gates pass, and end-to-end payout >= 35% and eval pass >= 45% |
| **Graveyard** | everything else, with the reason |

Why the tiers look like this: [[85 percent pass needs an extreme edge]].

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
