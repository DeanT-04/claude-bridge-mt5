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
| # | Strategy | Tier | Plan | Reach payout | Eval pass | EV/attempt | DSR | Beats random |
|---|---|---|---|---|---|---|---|---|
| 1 | [[orb]] | graveyard | eod | 8% | 27% | $-93 | 0.06 | 100% |
| 2 | [[late_trend]] | graveyard | eod | 6% | 26% | $-219 | 0.21 | 100% |
| 3 | [[gap_fade]] | graveyard | eod | 4% | 28% | $-462 | 0.01 | 94% |
| 4 | [[ib_breakout]] | graveyard | intraday | 2% | 13% | $-82 | 0.03 | 98% |
| 5 | [[control_random]] | graveyard | intraday | 1% | 11% | $-243 | 0.00 | 47% |
| 6 | [[intraday_momentum]] | graveyard | intraday | 0% | 1% | $-249 | 0.00 | 43% |

_6 strategies. Ranked by tier, then by reach-payout rate._
<!-- AUTO:leaderboard:end -->

## Map
- `Ideas/`: pre-registered hypotheses
- `Sources/`: papers, videos, articles (our own summaries)
- `Strategies/`: one note per tested strategy, with evidence charts
- `Graveyard/`: rejected strategies and why they failed
- `Lessons/`: what we've learned across runs
- `Firms/`: verified firm rules with source URLs and dates
- `Reports/`: batch run summaries and data-quality reports
