---
type: idea
status: pre-registered
created: 2026-09-25
family: gap
instruments: ['NQ']
strategy: gap_fade
---
# gap_fade

## Hypothesis
Moderate opening gaps (0.1-1.2%) in NQ tend to partly refill toward the prior close during the morning.

## Mechanism
Overnight moves on thin liquidity overshoot. When the cash session opens, liquidity providers and mean-reversion traders fade the imbalance.

## Exact rules
- gap = RTH open − prior RTH close.
- If `g_min` ≤ |gap %| ≤ `g_max` and the gap is still unfilled at the 09:31 close, fade it at market from 09:31.
- Target: the prior close. Stop: `sl_mult` × |gap|. Time exit at `exit_min`.

## Parameter ranges (fixed before testing)
| param | values | why |
|---|---|---|
| g_min | [0.001, 0.0025] | ignore noise gaps |
| g_max | [0.006, 0.012] | avoid news-driven large gaps |
| sl_mult | [0.5, 1.0] | tight vs full-gap stop |
| exit_min | [660, 720] | 11:00 vs 12:00 |

## Expected failure modes
Edge already arbitraged since publication; costs (1 tick slippage per fill + commissions) eat a thin edge; regime dependence (works only in high-volatility years). Trend days where the gap is never filled produce large losses.

## Sources
- Common practitioner idea: gap fill (quantifiedstrategies.com has several gap articles in the inbox)
