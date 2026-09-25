---
type: idea
status: pre-registered
created: 2026-09-25
family: late_trend
instruments: ['NQ']
strategy: late_trend
---
# late_trend

## Hypothesis
If NQ has already moved at least k × ATR from the open by 13:00 or 14:00, it keeps going into the close more often than it reverses.

## Mechanism
Dealers' gamma hedging and fund flows at the end of the day follow the day's direction. Strong trend days attract late momentum.

## Exact rules
- At `decide`, move = price − RTH open.
- If |move| ≥ `k` × ATR14 (average RTH range of the previous 14 days), enter at market in the direction of the move.
- Stop: `sl_atr` × ATR. Exit at 15:55.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| decide | [780, 840] | 13:00 vs 14:00 |
| k | [0.3, 0.5, 0.8] | strength of the day's move |
| sl_atr | [0.25, 0.5] | tight vs loose |

## Expected failure modes
Edge already arbitraged since publication; costs (1 tick slippage per fill + commissions) eat a thin edge; regime dependence (works only in high-volatility years). News-driven reversals at 14:00 on FOMC days.

## Sources
- Zarattini, Aziz & Barbon (2024), Beat the Market: an effective intraday momentum strategy for SPY (SSRN)
