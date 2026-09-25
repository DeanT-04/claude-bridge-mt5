---
type: idea
status: pre-registered
created: 2026-09-25
family: opening_range
instruments: ['NQ']
strategy: orb
---
# orb

## Hypothesis
Breaks of the first 5-30 minutes' range on NQ carry follow-through for the rest of the morning often enough, with a range-scaled stop, to be profitable after costs.

## Mechanism
Overnight orders and news are digested at the cash open. A range break signals which side won the opening auction, and it pulls stop and momentum flows the same way.

## Exact rules
- Opening range: high and low of the RTH bars from 09:30 to 09:30 + `or_min` minutes.
- From the close of the range, place an OCO order: a buy stop at the range high and a sell stop at the range low. It stays live until 11:00, with at most one trade a day.
- Stop: `sl_frac` × range. Target: `tp_mult` × range. Time exit at 15:55.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| or_min | [5, 15, 30] | classic Crabel / recent ORB papers |
| sl_frac | [0.5, 1.0] | half range vs other side |
| tp_mult | [1.0, 2.0] | 1R vs 2R |

## Expected failure modes
Edge already arbitraged since publication; costs (1 tick slippage per fill + commissions) eat a thin edge; regime dependence (works only in high-volatility years). False breakouts in range-bound days.

## Sources
- Crabel, T. (1990), Day Trading with Short Term Price Patterns and Opening Range Breakout
- Zarattini & Aziz (2023), SSRN: opening range breakout day trading on QQQ
- YouTube inbox: many ORB videos, e.g. 'Backtested Opening Range Breakout: Here's the Truth' (IRONCLAD TRADING)
