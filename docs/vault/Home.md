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
| 2 | [[blueberry:ib_twap]] | graveyard | blueberry_prime | 33% | 41% | $3,648 | 0.00 | 100% |
| 3 | [[ftmo:ib_twap]] | graveyard | ftmo_2step | 30% | 41% | $3,539 | 0.00 | 100% |
| 4 | [[ftmo:orb]] | graveyard | ftmo_2step | 28% | 35% | $161 | 0.00 | 100% |
| 5 | [[ftmo:late_trend]] | graveyard | ftmo_2step | 25% | 31% | $1,045 | 0.03 | 100% |
| 6 | [[blueberry:late_trend]] | graveyard | blueberry_prime | 24% | 27% | $830 | 0.01 | 100% |
| 7 | [[ftmo:supertrend_5m]] | graveyard | ftmo_2step | 17% | 18% | $1,483 | 0.00 | 97% |
| 8 | [[blueberry:supertrend_5m]] | graveyard | blueberry_prime | 15% | 17% | $799 | 0.00 | 97% |
| 9 | [[orb__choppy]] | graveyard | eod | 11% | 20% | $-323 | 0.05 | 99% |
| 10 | [[ftmo:ib_breakout]] | graveyard | ftmo_2step | 10% | 15% | $331 | 0.00 | 99% |
| 11 | [[blueberry:macd_trend_5m]] | graveyard | blueberry_prime | 10% | 14% | $646 | 0.00 | 100% |
| 12 | [[late_trend__not_monday]] | graveyard | eod | 10% | 20% | $113 | 0.19 | 100% |
| 13 | [[ftmo:macd_trend_5m]] | graveyard | ftmo_2step | 10% | 12% | $560 | 0.00 | 100% |
| 14 | [[orb__not_monday]] | graveyard | eod | 9% | 24% | $-45 | 0.14 | 100% |
| 15 | [[orb]] | graveyard | eod | 8% | 27% | $-93 | 0.06 | 100% |
| 16 | [[ib_breakout__vix_low]] | graveyard | eod | 8% | 21% | $-464 | 0.04 | 98% |
| 17 | [[ftmo:donchian_break_15m]] | graveyard | ftmo_2step | 7% | 8% | $88 | 0.00 | 94% |
| 18 | [[ib_breakout__trend_up]] | graveyard | eod | 7% | 19% | $-430 | 0.01 | 93% |
| 19 | [[late_trend__choppy]] | graveyard | eod | 7% | 27% | $-238 | 0.18 | 99% |
| 20 | [[ema_cross_15m]] | graveyard | eod | 7% | 21% | $-457 | 0.00 | 53% |
| 21 | [[rsi2_pullback_15m]] | graveyard | eod | 6% | 23% | $-342 | 0.00 | 86% |
| 22 | [[late_trend]] | graveyard | eod | 6% | 26% | $-219 | 0.21 | 100% |
| 23 | [[late_trend__trend_down]] | graveyard | eod | 6% | 9% | $-134 | 0.25 | 100% |
| 24 | [[bb_squeeze_15m@ES]] | graveyard | eod | 6% | 18% | $-448 | 0.00 | 86% |
| 25 | [[late_trend__vix_high]] | graveyard | eod | 6% | 16% | $-179 | 0.27 | 100% |
| 26 | [[orb__vol_high]] | graveyard | eod | 6% | 15% | $-296 | 0.00 | 92% |
| 27 | [[blueberry:donchian_break_15m]] | graveyard | blueberry_prime | 6% | 7% | $-80 | 0.00 | 94% |
| 28 | [[orb__choppy@ES]] | graveyard | eod | 6% | 22% | $-398 | 0.00 | 94% |
| 29 | [[overnight_drift]] | graveyard | eod | 5% | 19% | $-494 | 0.01 | 84% |
| 30 | [[ib_breakout__choppy]] | graveyard | eod | 5% | 18% | $-465 | 0.07 | 100% |
| 31 | [[ib_breakout__quiet_overnight@ES]] | graveyard | eod | 5% | 22% | $-337 | 0.00 | 98% |
| 32 | [[macd_trend_5m]] | graveyard | eod | 5% | 16% | $-171 | 0.10 | 100% |
| 33 | [[late_trend__vol_low]] | graveyard | eod | 5% | 21% | $-326 | 0.28 | 100% |
| 34 | [[orb__vol_expanding]] | graveyard | eod | 5% | 20% | $-477 | 0.02 | 95% |
| 35 | [[late_trend__trend_up]] | graveyard | eod | 5% | 22% | $-508 | 0.04 | 96% |
| 36 | [[orb__trend_up]] | graveyard | eod | 5% | 20% | $-426 | 0.08 | 99% |
| 37 | [[gap_fade]] | graveyard | eod | 4% | 28% | $-462 | 0.01 | 94% |
| 38 | [[late_trend__trend_down@ES]] | graveyard | eod | 4% | 12% | $-464 | 0.00 | 96% |
| 39 | [[ib_breakout@ES]] | graveyard | eod | 4% | 21% | $-406 | 0.00 | 100% |
| 40 | [[nr_breakout]] | graveyard | eod | 4% | 24% | $-520 | 0.00 | 80% |
| 41 | [[supertrend_5m]] | graveyard | eod | 4% | 22% | $-521 | 0.02 | 98% |
| 42 | [[orb__vol_expanding@ES]] | graveyard | eod | 4% | 25% | $-448 | 0.00 | 50% |
| 43 | [[ib_twap]] | graveyard | eod | 4% | 22% | $-538 | 0.19 | 100% |
| 44 | [[orb__vix_high]] | graveyard | eod | 4% | 19% | $-445 | 0.00 | 92% |
| 45 | [[portfolio_timing]] | graveyard | eod | 4% | 16% | $-389 | 0.15 | 100% |
| 46 | [[ib_breakout__choppy@ES]] | graveyard | eod | 4% | 14% | $-430 | 0.01 | 99% |
| 47 | [[late_trend__not_monday@ES]] | graveyard | eod | 4% | 13% | $-459 | 0.00 | 87% |
| 48 | [[donchian_break_15m]] | graveyard | eod | 3% | 29% | $-482 | 0.01 | 95% |
| 49 | [[ib_twap@ES]] | graveyard | eod | 3% | 17% | $-459 | 0.00 | 100% |
| 50 | [[nr_breakout@ES]] | graveyard | eod | 3% | 21% | $-536 | 0.00 | 84% |
| 51 | [[orb__vix_high@ES]] | graveyard | eod | 3% | 11% | $-511 | 0.00 | 65% |
| 52 | [[orb__vix_low]] | graveyard | eod | 3% | 19% | $-522 | 0.02 | 96% |
| 53 | [[bb_squeeze_15m]] | graveyard | eod | 3% | 14% | $-520 | 0.00 | 30% |
| 54 | [[ib_breakout__trend_up@ES]] | graveyard | eod | 3% | 15% | $-483 | 0.00 | 99% |
| 55 | [[late_trend__trending]] | graveyard | eod | 3% | 17% | $-486 | 0.02 | 94% |
| 56 | [[macd_trend_5m@ES]] | graveyard | eod | 3% | 15% | $-511 | 0.00 | 99% |
| 57 | [[overnight_failure_fade@ES]] | graveyard | eod | 3% | 12% | $-515 | 0.00 | 96% |
| 58 | [[ib_breakout__not_monday]] | graveyard | eod | 3% | 15% | $-535 | 0.00 | 88% |
| 59 | [[late_trend__vol_expanding]] | graveyard | intraday | 3% | 9% | $-116 | 0.01 | 90% |
| 60 | [[ib_breakout__trending]] | graveyard | eod | 3% | 16% | $-510 | 0.00 | 85% |
| 61 | [[orb__trending]] | graveyard | eod | 3% | 17% | $-530 | 0.00 | 67% |
| 62 | [[ib_breakout__not_monday@ES]] | graveyard | eod | 3% | 25% | $-465 | 0.00 | 99% |
| 63 | [[donchian_break_5m]] | graveyard | eod | 3% | 24% | $-530 | 0.00 | 95% |
| 64 | [[overnight_failure_fade]] | graveyard | eod | 3% | 17% | $-534 | 0.00 | 85% |
| 65 | [[ib_breakout__vol_expanding]] | graveyard | eod | 3% | 17% | $-507 | 0.00 | 71% |
| 66 | [[orb__not_monday@ES]] | graveyard | eod | 3% | 18% | $-540 | 0.00 | 75% |
| 67 | [[orb__vol_high@ES]] | graveyard | eod | 3% | 17% | $-507 | 0.00 | 62% |
| 68 | [[late_trend@ES]] | graveyard | intraday | 3% | 4% | $-165 | 0.00 | 87% |
| 69 | [[ib_breakout__vol_high@ES]] | graveyard | eod | 3% | 21% | $-521 | 0.00 | 46% |
| 70 | [[ema_cross_5m]] | graveyard | eod | 2% | 21% | $-513 | 0.00 | 33% |
| 71 | [[ib_failed_auction]] | graveyard | eod | 2% | 23% | $-493 | 0.00 | 55% |
| 72 | [[macd_trend_15m@ES]] | graveyard | eod | 2% | 19% | $-514 | 0.00 | 96% |
| 73 | [[ib_breakout__trend_down@ES]] | graveyard | eod | 2% | 9% | $-531 | 0.00 | 45% |
| 74 | [[ib_breakout__vol_low@ES]] | graveyard | eod | 2% | 12% | $-539 | 0.00 | 92% |
| 75 | [[late_trend__trending@ES]] | graveyard | eod | 2% | 6% | $-509 | 0.00 | 67% |
| 76 | [[late_trend__vix_high@ES]] | graveyard | eod | 2% | 11% | $-451 | 0.00 | 96% |
| 77 | [[ib_breakout]] | graveyard | intraday | 2% | 13% | $-82 | 0.03 | 98% |
| 78 | [[ib_breakout__vix_low@ES]] | graveyard | eod | 2% | 18% | $-537 | 0.00 | 85% |
| 79 | [[supertrend_15m]] | graveyard | eod | 2% | 21% | $-554 | 0.00 | 85% |
| 80 | [[ib_breakout__vix_high@ES]] | graveyard | intraday | 2% | 9% | $-195 | 0.00 | 61% |
| 81 | [[late_trend__vol_expanding@ES]] | graveyard | eod | 2% | 13% | $-528 | 0.00 | 57% |
| 82 | [[ib_breakout__vol_high]] | graveyard | eod | 2% | 16% | $-529 | 0.02 | 92% |
| 83 | [[session_range_sweep]] | graveyard | eod | 2% | 19% | $-562 | 0.00 | 63% |
| 84 | [[orb__quiet_overnight@ES]] | graveyard | eod | 2% | 25% | $-555 | 0.00 | 84% |
| 85 | [[orb@ES]] | graveyard | eod | 2% | 21% | $-553 | 0.00 | 60% |
| 86 | [[gap_fade@ES]] | graveyard | eod | 2% | 21% | $-538 | 0.00 | 81% |
| 87 | [[late_trend__quiet_overnight@ES]] | graveyard | eod | 2% | 8% | $-538 | 0.00 | 94% |
| 88 | [[macd_trend_15m]] | graveyard | eod | 2% | 25% | $-554 | 0.00 | 81% |
| 89 | [[rsi2_pullback_5m]] | graveyard | eod | 2% | 16% | $-545 | 0.00 | 40% |
| 90 | [[session_range_sweep@ES]] | graveyard | eod | 2% | 13% | $-543 | 0.00 | 96% |
| 91 | [[late_trend__vol_high]] | graveyard | eod | 2% | 10% | $-511 | 0.00 | 79% |
| 92 | [[orb__trend_down]] | graveyard | intraday | 2% | 6% | $-142 | 0.02 | 94% |
| 93 | [[donchian_break_15m@ES]] | graveyard | eod | 2% | 16% | $-548 | 0.00 | 93% |
| 94 | [[ema_cross_5m@ES]] | graveyard | eod | 2% | 15% | $-495 | 0.00 | 39% |
| 95 | [[supertrend_15m@ES]] | graveyard | eod | 2% | 16% | $-553 | 0.00 | 70% |
| 96 | [[late_trend__quiet_overnight]] | graveyard | eod | 1% | 7% | $-538 | 0.02 | 87% |
| 97 | [[orb__quiet_overnight]] | graveyard | eod | 1% | 14% | $-482 | 0.02 | 94% |
| 98 | [[right_side_v@ES]] | graveyard | eod | 1% | 13% | $-548 | 0.00 | 40% |
| 99 | [[blueberry:donchian_break_5m]] | graveyard | blueberry_prime | 1% | 2% | $-313 | 0.00 | 92% |
| 100 | [[ib_breakout__vol_expanding@ES]] | graveyard | eod | 1% | 10% | $-545 | 0.00 | 35% |
| 101 | [[right_side_v]] | graveyard | eod | 1% | 23% | $-565 | 0.00 | 41% |
| 102 | [[orb__vol_low]] | graveyard | intraday | 1% | 9% | $-235 | 0.07 | 99% |
| 103 | [[late_trend__choppy@ES]] | graveyard | intraday | 1% | 5% | $-234 | 0.00 | 69% |
| 104 | [[opening_range_reversal]] | graveyard | eod | 1% | 16% | $-556 | 0.00 | 43% |
| 105 | [[orb__trend_up@ES]] | graveyard | eod | 1% | 17% | $-542 | 0.00 | 84% |
| 106 | [[rsi2_pullback_15m@ES]] | graveyard | eod | 1% | 5% | $-541 | 0.00 | 24% |
| 107 | [[pd_sweep]] | graveyard | eod | 1% | 18% | $-560 | 0.00 | 54% |
| 108 | [[blueberry:ib_breakout]] | graveyard | blueberry_prime | 1% | 5% | $-307 | 0.00 | 99% |
| 109 | [[pd_sweep@ES]] | graveyard | eod | 1% | 11% | $-551 | 0.00 | 17% |
| 110 | [[control_random]] | graveyard | intraday | 1% | 11% | $-243 | 0.00 | 47% |
| 111 | [[ftmo:donchian_break_5m]] | graveyard | ftmo_2step | 1% | 2% | $-382 | 0.00 | 92% |
| 112 | [[opening_range_reversal@ES]] | graveyard | intraday | 1% | 11% | $-235 | 0.00 | 91% |
| 113 | [[orb__trending@ES]] | graveyard | intraday | 1% | 11% | $-228 | 0.00 | 43% |
| 114 | [[supertrend_5m@ES]] | graveyard | intraday | 1% | 8% | $-246 | 0.00 | 64% |
| 115 | [[overnight_drift@ES]] | graveyard | intraday | 1% | 8% | $-243 | 0.00 | 96% |
| 116 | [[ib_breakout__vix_high]] | graveyard | eod | 1% | 9% | $-550 | 0.00 | 57% |
| 117 | [[keltner_fade_5m@ES]] | graveyard | eod | 1% | 2% | $-547 | 0.00 | 51% |
| 118 | [[orb__vix_low@ES]] | graveyard | eod | 1% | 15% | $-559 | 0.00 | 84% |
| 119 | [[twap_reversion]] | graveyard | eod | 1% | 5% | $-550 | 0.00 | 57% |
| 120 | [[ib_failed_auction@ES]] | graveyard | eod | 1% | 8% | $-555 | 0.00 | 28% |
| 121 | [[late_trend__vol_low@ES]] | graveyard | eod | 1% | 9% | $-554 | 0.00 | 88% |
| 122 | [[orb__trend_down@ES]] | graveyard | eod | 1% | 8% | $-546 | 0.00 | 22% |
| 123 | [[intraday_momentum@ES]] | graveyard | eod | 1% | 9% | $-557 | 0.00 | 28% |
| 124 | [[ib_breakout__quiet_overnight]] | graveyard | intraday | 0% | 5% | $-247 | 0.01 | 93% |
| 125 | [[twap_reversion@ES]] | graveyard | eod | 0% | 8% | $-555 | 0.00 | 72% |
| 126 | [[orb__vol_low@ES]] | graveyard | eod | 0% | 14% | $-559 | 0.00 | 82% |
| 127 | [[ib_breakout__trending@ES]] | graveyard | eod | 0% | 24% | $-579 | 0.00 | 93% |
| 128 | [[bb_squeeze_5m]] | graveyard | eod | 0% | 5% | $-556 | 0.00 | 61% |
| 129 | [[ib_breakout__vol_low]] | graveyard | intraday | 0% | 6% | $-251 | 0.11 | 98% |
| 130 | [[bb_squeeze_5m@ES]] | graveyard | intraday | 0% | 2% | $-247 | 0.00 | 21% |
| 131 | [[late_trend__vol_high@ES]] | graveyard | eod | 0% | 4% | $-536 | 0.00 | 68% |
| 132 | [[ib_breakout__trend_down]] | graveyard | eod | 0% | 6% | $-557 | 0.00 | 66% |
| 133 | [[donchian_break_5m@ES]] | graveyard | intraday | 0% | 5% | $-249 | 0.00 | 82% |
| 134 | [[intraday_momentum]] | graveyard | intraday | 0% | 1% | $-249 | 0.00 | 43% |
| 135 | [[keltner_fade_5m]] | graveyard | intraday | 0% | 2% | $-250 | 0.00 | 19% |
| 136 | [[keltner_fade_15m]] | graveyard | intraday | 0% | 2% | $-250 | 0.00 | 47% |
| 137 | [[late_trend__vix_low]] | graveyard | intraday | 0% | 2% | $-250 | 0.01 | 86% |
| 138 | [[ema_cross_15m@ES]] | graveyard | intraday | 0% | 7% | $-253 | 0.00 | 5% |
| 139 | [[keltner_fade_15m@ES]] | graveyard | intraday | 0% | 0% | $-249 | 0.00 | 62% |
| 140 | [[wide_ib_rotation]] | graveyard | intraday | 0% | 0% | $-249 | 0.00 | 0% |
| 141 | [[late_trend__trend_up@ES]] | graveyard | intraday | 0% | 6% | $-252 | 0.00 | 73% |
| 142 | [[late_trend__vix_low@ES]] | graveyard | intraday | 0% | 0% | $-249 | 0.00 | 45% |
| 143 | [[wide_ib_rotation@ES]] | graveyard | intraday | 0% | 0% | $-249 | 0.00 | 27% |
| 144 | [[rsi2_pullback_5m@ES]] | graveyard | intraday | 0% | 4% | $-251 | 0.00 | 13% |

_144 strategies. Ranked by tier, then by reach-payout rate._
<!-- AUTO:leaderboard:end -->

## Map
- `Ideas/`: pre-registered hypotheses
- `Sources/`: papers, videos, articles (our own summaries)
- `Strategies/`: one note per tested strategy, with evidence charts
- `Graveyard/`: rejected strategies and why they failed
- `Lessons/`: what we've learned across runs
- `Firms/`: verified firm rules with source URLs and dates
- `Reports/`: batch run summaries and data-quality reports
