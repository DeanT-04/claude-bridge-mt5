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
| 1 | [[orb__choppy]] | graveyard | eod | 11% | 20% | $-323 | 0.05 | 99% |
| 2 | [[late_trend__not_monday]] | graveyard | eod | 10% | 20% | $113 | 0.19 | 100% |
| 3 | [[orb__not_monday]] | graveyard | eod | 9% | 24% | $-45 | 0.14 | 100% |
| 4 | [[orb]] | graveyard | eod | 8% | 27% | $-93 | 0.06 | 100% |
| 5 | [[ib_breakout__vix_low]] | graveyard | eod | 8% | 21% | $-464 | 0.04 | 98% |
| 6 | [[ib_breakout__trend_up]] | graveyard | eod | 7% | 19% | $-430 | 0.01 | 93% |
| 7 | [[late_trend__choppy]] | graveyard | eod | 7% | 27% | $-238 | 0.18 | 99% |
| 8 | [[ema_cross_15m]] | graveyard | eod | 7% | 21% | $-457 | 0.00 | 53% |
| 9 | [[rsi2_pullback_15m]] | graveyard | eod | 6% | 23% | $-342 | 0.00 | 86% |
| 10 | [[late_trend]] | graveyard | eod | 6% | 26% | $-219 | 0.21 | 100% |
| 11 | [[late_trend__trend_down]] | graveyard | eod | 6% | 9% | $-134 | 0.25 | 100% |
| 12 | [[bb_squeeze_15m@ES]] | graveyard | eod | 6% | 18% | $-448 | 0.00 | 86% |
| 13 | [[late_trend__vix_high]] | graveyard | eod | 6% | 16% | $-179 | 0.27 | 100% |
| 14 | [[orb__vol_high]] | graveyard | eod | 6% | 15% | $-296 | 0.00 | 92% |
| 15 | [[overnight_drift]] | graveyard | eod | 5% | 19% | $-494 | 0.01 | 84% |
| 16 | [[ib_breakout__choppy]] | graveyard | eod | 5% | 18% | $-465 | 0.07 | 100% |
| 17 | [[macd_trend_5m]] | graveyard | eod | 5% | 16% | $-171 | 0.10 | 100% |
| 18 | [[late_trend__vol_low]] | graveyard | eod | 5% | 21% | $-326 | 0.28 | 100% |
| 19 | [[orb__vol_expanding]] | graveyard | eod | 5% | 20% | $-477 | 0.02 | 95% |
| 20 | [[late_trend__trend_up]] | graveyard | eod | 5% | 22% | $-508 | 0.04 | 96% |
| 21 | [[orb__trend_up]] | graveyard | eod | 5% | 20% | $-426 | 0.08 | 99% |
| 22 | [[gap_fade]] | graveyard | eod | 4% | 28% | $-462 | 0.01 | 94% |
| 23 | [[nr_breakout]] | graveyard | eod | 4% | 24% | $-520 | 0.00 | 80% |
| 24 | [[supertrend_5m]] | graveyard | eod | 4% | 22% | $-521 | 0.02 | 98% |
| 25 | [[ib_twap]] | graveyard | eod | 4% | 22% | $-538 | 0.19 | 100% |
| 26 | [[orb__vix_high]] | graveyard | eod | 4% | 19% | $-445 | 0.00 | 92% |
| 27 | [[donchian_break_15m]] | graveyard | eod | 3% | 29% | $-482 | 0.01 | 95% |
| 28 | [[orb__vix_low]] | graveyard | eod | 3% | 19% | $-522 | 0.02 | 96% |
| 29 | [[bb_squeeze_15m]] | graveyard | eod | 3% | 14% | $-520 | 0.00 | 30% |
| 30 | [[late_trend__trending]] | graveyard | eod | 3% | 17% | $-486 | 0.02 | 94% |
| 31 | [[ib_breakout__not_monday]] | graveyard | eod | 3% | 15% | $-535 | 0.00 | 88% |
| 32 | [[late_trend__vol_expanding]] | graveyard | intraday | 3% | 9% | $-116 | 0.01 | 90% |
| 33 | [[ib_breakout__trending]] | graveyard | eod | 3% | 16% | $-510 | 0.00 | 85% |
| 34 | [[orb__trending]] | graveyard | eod | 3% | 17% | $-530 | 0.00 | 67% |
| 35 | [[donchian_break_5m]] | graveyard | eod | 3% | 24% | $-530 | 0.00 | 95% |
| 36 | [[ib_breakout__vol_expanding]] | graveyard | eod | 3% | 17% | $-507 | 0.00 | 71% |
| 37 | [[ema_cross_5m]] | graveyard | eod | 2% | 21% | $-513 | 0.00 | 33% |
| 38 | [[ib_breakout]] | graveyard | intraday | 2% | 13% | $-82 | 0.03 | 98% |
| 39 | [[supertrend_15m]] | graveyard | eod | 2% | 21% | $-554 | 0.00 | 85% |
| 40 | [[ib_breakout__vol_high]] | graveyard | eod | 2% | 16% | $-529 | 0.02 | 92% |
| 41 | [[macd_trend_15m]] | graveyard | eod | 2% | 25% | $-554 | 0.00 | 81% |
| 42 | [[rsi2_pullback_5m]] | graveyard | eod | 2% | 16% | $-545 | 0.00 | 40% |
| 43 | [[late_trend__vol_high]] | graveyard | eod | 2% | 10% | $-511 | 0.00 | 79% |
| 44 | [[orb__trend_down]] | graveyard | intraday | 2% | 6% | $-142 | 0.02 | 94% |
| 45 | [[donchian_break_15m@ES]] | graveyard | eod | 2% | 16% | $-548 | 0.00 | 93% |
| 46 | [[late_trend__quiet_overnight]] | graveyard | eod | 1% | 7% | $-538 | 0.02 | 87% |
| 47 | [[orb__quiet_overnight]] | graveyard | eod | 1% | 14% | $-482 | 0.02 | 94% |
| 48 | [[orb__vol_low]] | graveyard | intraday | 1% | 9% | $-235 | 0.07 | 99% |
| 49 | [[pd_sweep]] | graveyard | eod | 1% | 18% | $-560 | 0.00 | 54% |
| 50 | [[control_random]] | graveyard | intraday | 1% | 11% | $-243 | 0.00 | 47% |
| 51 | [[ib_breakout__vix_high]] | graveyard | eod | 1% | 9% | $-550 | 0.00 | 57% |
| 52 | [[twap_reversion]] | graveyard | eod | 1% | 5% | $-550 | 0.00 | 57% |
| 53 | [[ib_breakout__quiet_overnight]] | graveyard | intraday | 0% | 5% | $-247 | 0.01 | 93% |
| 54 | [[bb_squeeze_5m]] | graveyard | eod | 0% | 5% | $-556 | 0.00 | 61% |
| 55 | [[ib_breakout__vol_low]] | graveyard | intraday | 0% | 6% | $-251 | 0.11 | 98% |
| 56 | [[ib_breakout__trend_down]] | graveyard | eod | 0% | 6% | $-557 | 0.00 | 66% |
| 57 | [[intraday_momentum]] | graveyard | intraday | 0% | 1% | $-249 | 0.00 | 43% |
| 58 | [[keltner_fade_5m]] | graveyard | intraday | 0% | 2% | $-250 | 0.00 | 19% |
| 59 | [[keltner_fade_15m]] | graveyard | intraday | 0% | 2% | $-250 | 0.00 | 47% |
| 60 | [[late_trend__vix_low]] | graveyard | intraday | 0% | 2% | $-250 | 0.01 | 86% |

_60 strategies. Ranked by tier, then by reach-payout rate._
<!-- AUTO:leaderboard:end -->

## Map
- `Ideas/`: pre-registered hypotheses
- `Sources/`: papers, videos, articles (our own summaries)
- `Strategies/`: one note per tested strategy, with evidence charts
- `Graveyard/`: rejected strategies and why they failed
- `Lessons/`: what we've learned across runs
- `Firms/`: verified firm rules with source URLs and dates
- `Reports/`: batch run summaries and data-quality reports
