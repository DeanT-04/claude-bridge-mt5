---
type: lesson
created: 2026-09-25
evidence: ["[[orb]]", "[[late_trend]]", "[[ib_breakout]]", "[[gap_fade]]", "[[intraday_momentum]]"]
---
# Batch 1: the classic intraday families have timing information, but not enough edge

## What we observed
All five went to the Graveyard. They tested NQ from 2016 to 2025-03 with walk-forward, and 73 trials are recorded.

| Strategy | Beats random timing | DSR | Reach payout | Expected profit per attempt |
|---|---|---|---|---|
| late_trend | 99.9% | 0.21 | 4.8% | −$190 |
| orb | 99.5% | 0.14 | 3.8% | −$344 |
| ib_breakout | 98.3% | 0.03 | 2.2% | −$82 |
| gap_fade | 94.3% | 0.01 | 4.3% | −$462 |
| intraday_momentum | 42.8% | 0.00 | 0% | −$249 |

- **Real but weak.** Late-day trend continuation, opening-range breakout and initial-balance breakout time their entries far better than chance. They still fall short of what the Deflated Sharpe demands after costs and 73 trials.
- **The published intraday momentum effect** (Gao et al. 2018) **isn't present** in NQ out-of-sample from 2019 to 2025. That fits the known decay of published anomalies.
- Gap fading is marginal on every measure.

## Why it matters
Timing that beats chance but has a low Sharpe is ideal **raw material for combining**. If the daily P&L of these families is weakly correlated, a portfolio could lift the daily Sharpe. The calibration lesson shows that daily Sharpe is exactly what drives the pass rate.

## How to apply it next time
1. Check the correlation between the daily P&L of late_trend, orb and ib_breakout, and test the combination as a single strategy (P7, brought forward).
2. Add regime filters that are known before the session (prior-day volatility, overnight range, calendar days) to the families with real timing, and register them as new ideas, since they are new trials.
3. Try ES as well as NQ for the same families.
4. Drop intraday momentum and plain gap fade unless there is new evidence.
