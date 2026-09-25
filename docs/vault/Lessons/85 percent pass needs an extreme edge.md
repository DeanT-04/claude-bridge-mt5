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
