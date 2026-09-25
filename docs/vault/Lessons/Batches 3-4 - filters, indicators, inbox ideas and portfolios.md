---
type: lesson
created: 2026-09-25
evidence: ["[[portfolio_timing]]", "dashboard (every run, grid and fold)", "[[Batch 1 - classic intraday families have timing but not enough edge]]"]
---
# Batches 3–4: filters, indicators, inbox ideas and portfolios

## What we tested
- **Batch 3:**
  - 33 regime-filtered variants of the three families with real timing (volatility, trend, efficiency ratio, VIX, quiet overnight, not-Monday)
  - 7 indicator templates on both 5m and 15m bars (EMA cross, Donchian, Bollinger squeeze, RSI(2), Keltner fade, Supertrend, MACD)
  - 4 inbox ideas (TWAP reversion, NR4/NR7, prior-day sweep, IB + TWAP)
- **Batch 4:** the six best-ranked concrete rule sets from triaging 336 inbox items (overnight failure fade, IB failed auction, right side of the V, opening-range reversal, wide-IB rotation, session-range sweep).
- **ES:** everything was also run on ES.
- **Portfolio:** six distinct NQ timing families traded together in one Apex account.

Every strategy was pre-registered before its first test, and every trial is counted.

## What we observed
- **Not one strategy reached Contender.** The best NQ single strategies reached a payout on ~8–11% of purchased evaluations (orb__choppy, late_trend__not_monday).
- **Real timing is common; tradeable edge is not.** 22 of 56 NQ strategies beat ≥95% of random-entry runs, yet their out-of-sample Deflated Sharpe stayed ≤ 0.28.
- **Regime filters didn't create an edge.** They mostly removed days, which cut the sample, and they cost trials.
- **The indicator templates** showed no durable timing, except macd_trend_5m, supertrend_5m and donchian_break, which beat random but had no Deflated Sharpe.
- **The inbox ideas all failed** (reach-payout ≤ 3%). That matches the inbox's own best evidence: arXiv:2605.04004, a walk-forward study on MNQ with costs, also found no surviving plain OHLC intraday signal.
- **Combining the timing families didn't help.**
  - Six families together beat 100% of random entries, but DSR was 0.15 and only 3.7% of evaluations reached a payout.
  - Apex's contract limit is shared across members, which forces tiny sizes.
  - The members' edges are individually too weak.
  - The portfolio machinery was verified: a one-member portfolio reproduces the single strategy's OOS daily P&L exactly (1,608 sessions, max difference 0.0).

## Why it matters
Beating random timing is necessary but nowhere near sufficient. After 1-tick slippage, commissions and several hundred counted trials, simple OHLC rules on NQ and ES from 2019 to 2025 don't carry the daily Sharpe (≈2 or more) that the Apex calibration needs. The honest bottleneck is **signal quality**, not sizing, filters or the prop-firm rules.

## How to apply it next time
- Stop adding OHLC rule variants; they mostly spend trials.
- Look for different **information**:
  - cross-asset data (ES/NQ divergence, bonds, dollar)
  - event and calendar structure (FOMC/CPI days from a sourced calendar)
  - dealer-positioning proxies computed from free daily data
  - the forward futures dataset (real CME bars) as it grows
- Use the forward-collected data as the next clean holdout. Every current holdout has been opened.
