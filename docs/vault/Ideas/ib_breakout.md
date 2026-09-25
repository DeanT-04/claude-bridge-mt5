---
type: idea
status: pre-registered
created: 2026-09-25
family: initial_balance
instruments: ['NQ']
strategy: ib_breakout
---
# ib_breakout

## Hypothesis
Breaks of a narrow initial balance (first 30/60 min) lead to range extension, as volatility expands after compression.

## Mechanism
Market Profile: a narrow initial balance means the market hasn't agreed on value. A break of it draws in other-timeframe participants, and the range extends.

## Exact rules
- IB = high and low from 09:30 to 09:30 + `ib_min`.
- Optionally only trade when IB range ÷ its 20-day average ≤ `narrow`.
- OCO stops at IB high and low until 14:00, one trade a day.
- Stop: `sl_frac` × IB. Target: `tp_mult` × IB. Exit at 15:55.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| ib_min | [30, 60] | half-hour vs classic hour |
| narrow | ['off', 0.8] | only compressed IBs |
| tp_mult | [1.0, 2.0] | range extension target |
| sl_frac | [0.5, 1.0] | IB mid vs other side |

## Expected failure modes
Edge already arbitraged since publication; costs (1 tick slippage per fill + commissions) eat a thin edge; regime dependence (works only in high-volatility years). Overlaps with ORB; the two may be the same edge, so correlation will be checked.

## Sources
- Dalton, Jones & Dalton, Mind Over Markets (Market Profile)
