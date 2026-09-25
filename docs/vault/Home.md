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
| 1 | [[blueberry:orb]] | graveyard | blueberry_prime | 34% | 44% | $280 | 0.00 | 100% |
| 2 | [[ftmo:ib_twap]] | graveyard | ftmo_2step | 30% | 41% | $3,539 | 0.00 | 100% |
| 3 | [[ftmo:orb]] | graveyard | ftmo_2step | 28% | 35% | $161 | 0.00 | 100% |
| 4 | [[ftmo:late_trend]] | graveyard | ftmo_2step | 25% | 31% | $1,045 | 0.03 | 100% |
| 5 | [[blueberry:late_trend]] | graveyard | blueberry_prime | 24% | 27% | $830 | 0.01 | 100% |
| 6 | [[ftmo:supertrend_5m]] | graveyard | ftmo_2step | 17% | 18% | $1,483 | 0.00 | 97% |
| 7 | [[orb__choppy]] | graveyard | eod | 11% | 20% | $-323 | 0.05 | 99% |
| 8 | [[ftmo:ib_breakout]] | graveyard | ftmo_2step | 10% | 15% | $331 | 0.00 | 99% |
| 9 | [[late_trend__not_monday]] | graveyard | eod | 10% | 20% | $113 | 0.19 | 100% |
| 10 | [[ftmo:macd_trend_5m]] | graveyard | ftmo_2step | 10% | 12% | $560 | 0.00 | 100% |
| 11 | [[orb__not_monday]] | graveyard | eod | 9% | 24% | $-45 | 0.14 | 100% |
| 12 | [[orb]] | graveyard | eod | 8% | 27% | $-93 | 0.06 | 100% |
| 13 | [[ib_breakout__vix_low]] | graveyard | eod | 8% | 21% | $-464 | 0.04 | 98% |
| 14 | [[ftmo:donchian_break_15m]] | graveyard | ftmo_2step | 7% | 8% | $88 | 0.00 | 94% |
| 15 | [[ib_breakout__trend_up]] | graveyard | eod | 7% | 19% | $-430 | 0.01 | 93% |
| 16 | [[late_trend__choppy]] | graveyard | eod | 7% | 27% | $-238 | 0.18 | 99% |
| 17 | [[ema_cross_15m]] | graveyard | eod | 7% | 21% | $-457 | 0.00 | 53% |
| 18 | [[rsi2_pullback_15m]] | graveyard | eod | 6% | 23% | $-342 | 0.00 | 86% |
| 19 | [[late_trend]] | graveyard | eod | 6% | 26% | $-219 | 0.21 | 100% |
| 20 | [[late_trend__trend_down]] | graveyard | eod | 6% | 9% | $-134 | 0.25 | 100% |
| 21 | [[bb_squeeze_15m@ES]] | graveyard | eod | 6% | 18% | $-448 | 0.00 | 86% |
| 22 | [[late_trend__vix_high]] | graveyard | eod | 6% | 16% | $-179 | 0.27 | 100% |
| 23 | [[orb__vol_high]] | graveyard | eod | 6% | 15% | $-296 | 0.00 | 92% |
| 24 | [[overnight_drift]] | graveyard | eod | 5% | 19% | $-494 | 0.01 | 84% |
| 25 | [[ib_breakout__choppy]] | graveyard | eod | 5% | 18% | $-465 | 0.07 | 100% |
| 26 | [[ib_breakout__quiet_overnight@ES]] | graveyard | eod | 5% | 22% | $-337 | 0.00 | 98% |
| 27 | [[macd_trend_5m]] | graveyard | eod | 5% | 16% | $-171 | 0.10 | 100% |
| 28 | [[late_trend__vol_low]] | graveyard | eod | 5% | 21% | $-326 | 0.28 | 100% |
| 29 | [[orb__vol_expanding]] | graveyard | eod | 5% | 20% | $-477 | 0.02 | 95% |
| 30 | [[late_trend__trend_up]] | graveyard | eod | 5% | 22% | $-508 | 0.04 | 96% |
| 31 | [[orb__trend_up]] | graveyard | eod | 5% | 20% | $-426 | 0.08 | 99% |
| 32 | [[gap_fade]] | graveyard | eod | 4% | 28% | $-462 | 0.01 | 94% |
| 33 | [[late_trend__trend_down@ES]] | graveyard | eod | 4% | 12% | $-464 | 0.00 | 96% |
| 34 | [[nr_breakout]] | graveyard | eod | 4% | 24% | $-520 | 0.00 | 80% |
| 35 | [[supertrend_5m]] | graveyard | eod | 4% | 22% | $-521 | 0.02 | 98% |
| 36 | [[ib_twap]] | graveyard | eod | 4% | 22% | $-538 | 0.19 | 100% |
| 37 | [[orb__vix_high]] | graveyard | eod | 4% | 19% | $-445 | 0.00 | 92% |
| 38 | [[portfolio_timing]] | graveyard | eod | 4% | 16% | $-389 | 0.15 | 100% |
| 39 | [[ib_breakout__choppy@ES]] | graveyard | eod | 4% | 14% | $-430 | 0.01 | 99% |
| 40 | [[late_trend__not_monday@ES]] | graveyard | eod | 4% | 13% | $-459 | 0.00 | 87% |
| 41 | [[donchian_break_15m]] | graveyard | eod | 3% | 29% | $-482 | 0.01 | 95% |
| 42 | [[ib_twap@ES]] | graveyard | eod | 3% | 17% | $-459 | 0.00 | 100% |
| 43 | [[nr_breakout@ES]] | graveyard | eod | 3% | 21% | $-536 | 0.00 | 84% |
| 44 | [[orb__vix_low]] | graveyard | eod | 3% | 19% | $-522 | 0.02 | 96% |
| 45 | [[bb_squeeze_15m]] | graveyard | eod | 3% | 14% | $-520 | 0.00 | 30% |
| 46 | [[ib_breakout__trend_up@ES]] | graveyard | eod | 3% | 15% | $-483 | 0.00 | 99% |
| 47 | [[late_trend__trending]] | graveyard | eod | 3% | 17% | $-486 | 0.02 | 94% |
| 48 | [[macd_trend_5m@ES]] | graveyard | eod | 3% | 15% | $-511 | 0.00 | 99% |
| 49 | [[overnight_failure_fade@ES]] | graveyard | eod | 3% | 12% | $-515 | 0.00 | 96% |
| 50 | [[ib_breakout__not_monday]] | graveyard | eod | 3% | 15% | $-535 | 0.00 | 88% |
| 51 | [[late_trend__vol_expanding]] | graveyard | intraday | 3% | 9% | $-116 | 0.01 | 90% |
| 52 | [[ib_breakout__trending]] | graveyard | eod | 3% | 16% | $-510 | 0.00 | 85% |
| 53 | [[orb__trending]] | graveyard | eod | 3% | 17% | $-530 | 0.00 | 67% |
| 54 | [[ib_breakout__not_monday@ES]] | graveyard | eod | 3% | 25% | $-465 | 0.00 | 99% |
| 55 | [[donchian_break_5m]] | graveyard | eod | 3% | 24% | $-530 | 0.00 | 95% |
| 56 | [[overnight_failure_fade]] | graveyard | eod | 3% | 17% | $-534 | 0.00 | 85% |
| 57 | [[ib_breakout__vol_expanding]] | graveyard | eod | 3% | 17% | $-507 | 0.00 | 71% |
| 58 | [[orb__not_monday@ES]] | graveyard | eod | 3% | 18% | $-540 | 0.00 | 75% |
| 59 | [[ib_breakout__vol_high@ES]] | graveyard | eod | 3% | 21% | $-521 | 0.00 | 46% |
| 60 | [[ema_cross_5m]] | graveyard | eod | 2% | 21% | $-513 | 0.00 | 33% |
| 61 | [[ib_failed_auction]] | graveyard | eod | 2% | 23% | $-493 | 0.00 | 55% |
| 62 | [[macd_trend_15m@ES]] | graveyard | eod | 2% | 19% | $-514 | 0.00 | 96% |
| 63 | [[ib_breakout__trend_down@ES]] | graveyard | eod | 2% | 9% | $-531 | 0.00 | 45% |
| 64 | [[ib_breakout__vol_low@ES]] | graveyard | eod | 2% | 12% | $-539 | 0.00 | 92% |
| 65 | [[late_trend__trending@ES]] | graveyard | eod | 2% | 6% | $-509 | 0.00 | 67% |
| 66 | [[late_trend__vix_high@ES]] | graveyard | eod | 2% | 11% | $-451 | 0.00 | 96% |
| 67 | [[ib_breakout]] | graveyard | intraday | 2% | 13% | $-82 | 0.03 | 98% |
| 68 | [[ib_breakout__vix_low@ES]] | graveyard | eod | 2% | 18% | $-537 | 0.00 | 85% |
| 69 | [[supertrend_15m]] | graveyard | eod | 2% | 21% | $-554 | 0.00 | 85% |
| 70 | [[ib_breakout__vix_high@ES]] | graveyard | intraday | 2% | 9% | $-195 | 0.00 | 61% |
| 71 | [[late_trend__vol_expanding@ES]] | graveyard | eod | 2% | 13% | $-528 | 0.00 | 57% |
| 72 | [[ib_breakout__vol_high]] | graveyard | eod | 2% | 16% | $-529 | 0.02 | 92% |
| 73 | [[session_range_sweep]] | graveyard | eod | 2% | 19% | $-562 | 0.00 | 63% |
| 74 | [[late_trend__quiet_overnight@ES]] | graveyard | eod | 2% | 8% | $-538 | 0.00 | 94% |
| 75 | [[macd_trend_15m]] | graveyard | eod | 2% | 25% | $-554 | 0.00 | 81% |
| 76 | [[rsi2_pullback_5m]] | graveyard | eod | 2% | 16% | $-545 | 0.00 | 40% |
| 77 | [[late_trend__vol_high]] | graveyard | eod | 2% | 10% | $-511 | 0.00 | 79% |
| 78 | [[orb__trend_down]] | graveyard | intraday | 2% | 6% | $-142 | 0.02 | 94% |
| 79 | [[donchian_break_15m@ES]] | graveyard | eod | 2% | 16% | $-548 | 0.00 | 93% |
| 80 | [[ema_cross_5m@ES]] | graveyard | eod | 2% | 15% | $-495 | 0.00 | 39% |
| 81 | [[late_trend__quiet_overnight]] | graveyard | eod | 1% | 7% | $-538 | 0.02 | 87% |
| 82 | [[orb__quiet_overnight]] | graveyard | eod | 1% | 14% | $-482 | 0.02 | 94% |
| 83 | [[right_side_v@ES]] | graveyard | eod | 1% | 13% | $-548 | 0.00 | 40% |
| 84 | [[ib_breakout__vol_expanding@ES]] | graveyard | eod | 1% | 10% | $-545 | 0.00 | 35% |
| 85 | [[right_side_v]] | graveyard | eod | 1% | 23% | $-565 | 0.00 | 41% |
| 86 | [[orb__vol_low]] | graveyard | intraday | 1% | 9% | $-235 | 0.07 | 99% |
| 87 | [[late_trend__choppy@ES]] | graveyard | intraday | 1% | 5% | $-234 | 0.00 | 69% |
| 88 | [[opening_range_reversal]] | graveyard | eod | 1% | 16% | $-556 | 0.00 | 43% |
| 89 | [[pd_sweep]] | graveyard | eod | 1% | 18% | $-560 | 0.00 | 54% |
| 90 | [[control_random]] | graveyard | intraday | 1% | 11% | $-243 | 0.00 | 47% |
| 91 | [[ftmo:donchian_break_5m]] | graveyard | ftmo_2step | 1% | 2% | $-382 | 0.00 | 92% |
| 92 | [[opening_range_reversal@ES]] | graveyard | intraday | 1% | 11% | $-235 | 0.00 | 91% |
| 93 | [[ib_breakout__vix_high]] | graveyard | eod | 1% | 9% | $-550 | 0.00 | 57% |
| 94 | [[keltner_fade_5m@ES]] | graveyard | eod | 1% | 2% | $-547 | 0.00 | 51% |
| 95 | [[twap_reversion]] | graveyard | eod | 1% | 5% | $-550 | 0.00 | 57% |
| 96 | [[ib_failed_auction@ES]] | graveyard | eod | 1% | 8% | $-555 | 0.00 | 28% |
| 97 | [[late_trend__vol_low@ES]] | graveyard | eod | 1% | 9% | $-554 | 0.00 | 88% |
| 98 | [[ib_breakout__quiet_overnight]] | graveyard | intraday | 0% | 5% | $-247 | 0.01 | 93% |
| 99 | [[ib_breakout__trending@ES]] | graveyard | eod | 0% | 24% | $-579 | 0.00 | 93% |
| 100 | [[bb_squeeze_5m]] | graveyard | eod | 0% | 5% | $-556 | 0.00 | 61% |
| 101 | [[ib_breakout__vol_low]] | graveyard | intraday | 0% | 6% | $-251 | 0.11 | 98% |
| 102 | [[bb_squeeze_5m@ES]] | graveyard | intraday | 0% | 2% | $-247 | 0.00 | 21% |
| 103 | [[late_trend__vol_high@ES]] | graveyard | eod | 0% | 4% | $-536 | 0.00 | 68% |
| 104 | [[ib_breakout__trend_down]] | graveyard | eod | 0% | 6% | $-557 | 0.00 | 66% |
| 105 | [[donchian_break_5m@ES]] | graveyard | intraday | 0% | 5% | $-249 | 0.00 | 82% |
| 106 | [[intraday_momentum]] | graveyard | intraday | 0% | 1% | $-249 | 0.00 | 43% |
| 107 | [[keltner_fade_5m]] | graveyard | intraday | 0% | 2% | $-250 | 0.00 | 19% |
| 108 | [[keltner_fade_15m]] | graveyard | intraday | 0% | 2% | $-250 | 0.00 | 47% |
| 109 | [[late_trend__vix_low]] | graveyard | intraday | 0% | 2% | $-250 | 0.01 | 86% |
| 110 | [[ema_cross_15m@ES]] | graveyard | intraday | 0% | 7% | $-253 | 0.00 | 5% |
| 111 | [[keltner_fade_15m@ES]] | graveyard | intraday | 0% | 0% | $-249 | 0.00 | 62% |
| 112 | [[wide_ib_rotation]] | graveyard | intraday | 0% | 0% | $-249 | 0.00 | 0% |
| 113 | [[late_trend__trend_up@ES]] | graveyard | intraday | 0% | 6% | $-252 | 0.00 | 73% |
| 114 | [[late_trend__vix_low@ES]] | graveyard | intraday | 0% | 0% | $-249 | 0.00 | 45% |

_114 strategies. Ranked by tier, then by reach-payout rate._
<!-- AUTO:leaderboard:end -->

## Map
- `Ideas/`: pre-registered hypotheses
- `Sources/`: papers, videos, articles (our own summaries)
- `Strategies/`: one note per tested strategy, with evidence charts
- `Graveyard/`: rejected strategies and why they failed
- `Lessons/`: what we've learned across runs
- `Firms/`: verified firm rules with source URLs and dates
- `Reports/`: batch run summaries and data-quality reports
