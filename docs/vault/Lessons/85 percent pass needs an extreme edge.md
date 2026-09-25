---
type: lesson
created: 2026-09-25
evidence: ["synthetic planted-edge calibration (tests/gauntlet/test_planted_edge.py::synthetic)"]
---
# An 85% Apex pass rate needs an extreme edge; the 30-day window is the binding rule

## What we observed
Setup:
- a synthetic market with a planted edge of **known** strength
- one trade a day
- real Apex 50K rules
- real costs ($0.51 per side per micro plus 1 tick of slippage per fill)
- every position size from 1 to 60 micros
- a simulated evaluation started on every session

| Annualised Sharpe | Best eval pass (EOD) | End-to-end payout | Expected profit per attempt |
|---|---|---|---|
| 1 | 30% | 15% | −$27 |
| 2 | 38% | 25% | **+$977** |
| 3 | 47% | 38% | +$2,889 |
| 4 | 57% | 51% | +$4,883 |
| 6 | 75% | 72% | +$8,038 |
| 9 | 92% | 91% | +$10,510 |

The intraday-trailing plan does slightly worse on pass rate at the same Sharpe.

![[calibration-apex-edge-vs-pass.png]]

## Why it matters
- **Evaluation pass rate ≥ 85%** needs an annualised Sharpe of about **8 or more**, which is extremely rare for one strategy. Trading smaller doesn't help, because the account runs out of its 30 calendar days. Trading bigger doesn't help either, because the $2,000 trailing drawdown catches it.
- **Expected profit turns positive at a Sharpe of about 2**. Payout caps and 100% profit split make each pass worth far more than the fee. On expected value, a 40–50% pass rate is already very profitable.
- Once funded, strong edges reach the first payout 90%+ of the time. The difficult part is the evaluation window, not the funded account.

## How to apply it next time
- Rank on end-to-end payout and expected profit per attempt. Evaluation pass rate is a consequence of those, not the goal.
- To raise the pass rate, raise the **daily** Sharpe: more independent trades per day, more instruments, portfolios of uncorrelated strategies. P7 portfolios are the realistic route to 85%.

## Update: challenge-aware sizing (same day)
Sizing each session from the account's state gives a large lift for the **same** edge:
- cushion scaling: size × (cushion ÷ drawdown)^α
- a deadline boost when the account is behind the pace needed to hit the target

Best of 48 settings on the synthetic data (so somewhat optimistic):

| Sharpe | Reach payout, fixed size | Reach payout, aware sizing | Expected profit per attempt |
|---|---|---|---|
| 2 | 25% | 40% | $977 → $3,537 |
| 3 | 38% | 51% | $2,889 → $5,390 |
| 4 | 51% | 61% | $4,883 → $5,415 |
| 6 | 72% | 78% | $8,038 → $8,781 |

The gauntlet now chooses the base size and (α, β) on each fold's training data (`config/research.yaml: sizing_policy`). On the real batch-1 strategies the lift was small: late_trend reached a payout 4.8% → 6.1% of the time, orb 3.8% → 8.5%. Sizing multiplies an edge; it can't create one.
