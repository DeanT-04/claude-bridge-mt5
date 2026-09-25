---
type: strategy
strategy: orb__trend_up
family: opening_range
verdict: graveyard
plan: eod
run_id: 91845a2dfa
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# orb__trend_up: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660}; base sizes (micros)
{'eod': 1, 'intraday': 4}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 5.100703485930247), 'intraday': (0.0, 0.5, 5.100703485930247)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1097 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0818 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9940 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -503.4 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0450 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1969 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2287 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 4.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 11.0 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- Holdout consistent
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1969 | 0.1492 |
| eval_fail | 0.6761 | 0.7191 |
| eval_expired | 0.1270 | 0.1317 |
| median_sessions_to_pass | 4.0000 | 4.0000 |
| p90_sessions_to_pass | 11.0 | 14.0 |
| first_payout_given_pass | 0.2287 | 0.2027 |
| end_to_end_payout | 0.0450 | 0.0302 |
| mean_payouts_given_pass | 0.5085 | 0.7207 |
| ev_per_attempt | -426.4 | -31.0 |
| ev_p05 | -503.4 | -220.5 |
| ev_p95 | -328.6 | 221.3 |
| max_best_day_share | 1.2956 | 1.3986 |
| starts | 1488 | 1488 |
| effective_n | 297.6 | 372.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 1,097; total P&L per micro 8,440 USD
- Annualised Sharpe (daily, per micro): 0.73
- PSR (vs 0): 0.970; **Deflated Sharpe: 0.082** over 533 recorded trials
  (Sharpe variance across trials 6.78e-04)
- Random-entry percentile: 0.994

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0178 | 10 | 10 | (0.0, 1.0, 0.4) | (0.0, 1.0, 0.4) |
| 2020 | {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0263 | 10 | 10 | (0.0, 1.0, 0.66) | (0.0, 1.0, 0.66) |
| 2021 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0159 | 12 | 8 | (0.0, 1.0, 0.94) | (0.0, 1.0, 0.94) |
| 2022 | {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660} | 0.0451 | 5 | 3 | (0.0, 1.0, 3.34) | (0.0, 0.5, 3.34) |
| 2023 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660} | 0.0296 | 2 | 2 | (0.0, 1.0, 2.45) | (0.5, 1.0, 2.45) |
| 2024 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0333 | 2 | 4 | (0.0, 1.0, 3.34) | (0.0, 0.5, 3.34) |
| 2025 | {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660} | 0.0488 | 1 | 4 | (0.0, 1.0, 5.46) | (0.0, 0.5, 5.46) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1815 | 0.1519 |
| end_to_end_payout | 0.0852 | 0.0000 |
| ev_per_attempt | -504.1 | -258.0 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -2.95 USD

## Evidence
![[orb__trend_up-equity.png]]
![[orb__trend_up-fan.png]]
![[orb__trend_up-random.png]]
![[orb__trend_up-drawdown.png]]
![[orb__trend_up-monthly.png]]
![[orb__trend_up-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run orb__trend_up`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
