---
type: lesson
created: 2026-09-25
evidence: ["config/firms/ftmo.yaml", "config/firms/blueberry.yaml", "dashboard (ftmo:* and blueberry:* runs)"]
---
# P7: firm rules matter as much as the strategy, but they can't create an edge

## What we observed
The eight NQ families with real timing were transferred to FTMO 2-Step and Blueberry Prime.

Rules (verified 2026-09-25, sources in the firm files):
- static max loss
- a daily loss limit from the day-start balance
- no time limit
- FTMO refunds the fee with the first reward

Costs:
- zero commission on index CFDs
- half the measured spread plus 1 NQ tick per fill

| Strategy | Apex: reach payout | FTMO: reach payout | FTMO: median sessions to pass | FTMO: expected profit per attempt (5th pct) |
|---|---|---|---|---|
| ib_twap | ~3% | **30%** | 85 | +$3,539 (+$2,201) |
| late_trend | 6% | 25% | 88 | +$1,045 (+$497) |
| orb | 8% | 28% | **704** | +$161 (+$6) |
| supertrend_5m | ~3% | 17% | 65 | +$1,483 (+$640) |

- **The same weak edge looks far better under static, no-time-limit rules.**
  - Apex's 30-day window and trailing drawdown punish slow edges.
  - FTMO lets a small edge grind toward the target at small size.
  - The fee refund makes a failed attempt cheaper in expectation.
- **But "better" means slow.** Median time to pass is 2–4 months, and for orb nearly 3 years. That's the opposite of passing first time.
- **Deflated Sharpe is about 0 for all of them** after 400+ counted trials, so the underlying edge still can't be told apart from luck. Every result is Graveyard, correctly.

## Why it matters
Firm choice is a real lever for expected value: static drawdown, no deadline and refunds favour weak-but-real edges. It isn't a substitute for a statistically real edge. Positive expected value with DSR ≈ 0 is exactly the pattern overfitting produces.

## How to apply it next time
- When a strategy with a real edge appears, evaluate it under all three firms and route it to the one whose rules suit its risk shape.
- For slow edges, report time-to-payout alongside the pass rate. A 30% pass rate at a 4-month median isn't what the user wants.
- Blueberry's index contract size isn't published, so its sizing is in USD per point (an assumption). Read the MT5 symbol specification before relying on those results.
