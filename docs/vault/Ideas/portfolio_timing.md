---
type: idea
status: pre-registered
created: 2026-09-25
family: portfolio
instruments: ['NQ']
strategy: portfolio_timing
---
# portfolio_timing

## Hypothesis
Six distinct NQ intraday families that each showed real timing (beat >=95% of random-entry runs out of sample), traded together as one Apex account, raise the daily Sharpe enough to lift the chance of reaching a payout.

## Mechanism
The members capture different flows: the morning breakout (orb), afternoon continuation (late_trend), and intraday momentum/breakout on 5m-15m bars (macd_trend_5m, donchian_break_15m, supertrend_5m), plus a VWAP-side IB break (ib_twap). If their daily P&L is only weakly correlated, the combined Sharpe grows roughly with the square root of the number of independent members.

## Exact rules
- One unit = 1 micro of every member. Each member uses its own pre-registered rules, and its parameters are re-selected per walk-forward fold on training years only.
- Sizes and the sizing policy are chosen per fold on the combined training P&L.
- Apex's contract limit is shared across members.
- Members are combined per session, pessimistically: worst and best intraday points are summed as if they happened simultaneously.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| members | ['late_trend', 'orb', 'macd_trend_5m', 'donchian_break_15m', 'supertrend_5m', 'ib_twap'] | distinct families with random-entry percentile >= 0.95; ib_breakout excluded (0.98 correlated with orb) |

## Expected failure modes
**Selection bias:** members were chosen using their out-of-sample random-entry results, so this portfolio's out-of-sample record is biased upward and can't count as independent evidence. Every member's holdout has already been opened, so the portfolio holdout is contaminated. Confirmation has to come from forward data (the yfinance collector). Correlations may rise in stress periods.

## Sources
- [[Batch 1 - classic intraday families have timing but not enough edge]]
- Batch 3 NQ results (dashboard)
