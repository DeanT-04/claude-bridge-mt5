---
type: idea
status: pre-registered
created: 2026-09-25
family: intraday_momentum
instruments: ['NQ']
strategy: intraday_momentum
---
# intraday_momentum

## Hypothesis
The return from the prior RTH close to 10:00 ET predicts the sign of the last half hour's return (15:30-16:00).

## Mechanism
Late-day hedging by option dealers and leveraged ETFs rebalancing push the close in the day's direction. Traders who arrive late also trade in the direction of the morning's information.

## Exact rules
- r1 = close at 10:00 ÷ prior RTH close − 1.
- At the 15:30 bar, buy (sell) at market if r1 > 0 (< 0) and |r1| > `threshold`.
- If `confirm_r12` is set, also require the 15:00–15:30 return to have the same sign.
- Optional stop of `sl_pct` of price. Exit at the 15:59 open.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| threshold | [0.0, 0.001, 0.0025] | all days vs only meaningful first-half-hour moves |
| confirm_r12 | [False, True] | paper finds r12 adds information |
| sl_pct | ['none', 0.005] | unprotected vs 0.5% stop |

## Expected failure modes
Edge already arbitraged since publication; costs (1 tick slippage per fill + commissions) eat a thin edge; regime dependence (works only in high-volatility years). The effect is documented on SPY; its strength on NQ and after 2018 is unknown.

## Sources
- Gao, Han, Li & Zhou (2018), Market intraday momentum, Journal of Financial Economics
- Baltussen, Da, Lammers & Martens (2021), Hedging demand and market intraday momentum, JFE (found via OpenAlex)
