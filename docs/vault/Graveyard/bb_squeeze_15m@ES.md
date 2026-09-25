---
type: strategy
strategy: bb_squeeze_15m@ES
family: bb_squeeze
verdict: graveyard
plan: eod
run_id: e20a30c457
data_hash: c21e6fe846c4f1b4[1029:3800][0:2381]
commit: 15230e7-dirty
seed: 11
---
# bb_squeeze_15m@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'q': 0.1, 'sl_atr': 1.0, 'tp_atr': 4.0}; base sizes (micros)
{'eod': 50, 'intraday': 25}; sizing policy (alpha, beta, mu) {'eod': (2.0, 1.0, 0.3236039850004073), 'intraday': (2.0, 1.0, 0.3236039850004073)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 119 | >= 200 | stat | FAIL |
| Deflated Sharpe | 0.0012 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.8620 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -510.9 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0605 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1774 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.3409 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 8.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 18.0 | <= 30 | speed | PASS |

Failed gates:
- OOS trades
- Deflated Sharpe
- Beats random entry (percentile)
- EV per attempt, 5th pct (USD)
- Holdout consistent
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1774 | 0.0208 |
| eval_fail | 0.1700 | 0.5269 |
| eval_expired | 0.6526 | 0.4523 |
| median_sessions_to_pass | 8.0000 | 7.0000 |
| p90_sessions_to_pass | 18.0 | 16.0 |
| first_payout_given_pass | 0.3409 | 0.0000 |
| end_to_end_payout | 0.0605 | 0.0000 |
| mean_payouts_given_pass | 0.7368 | 0.0000 |
| ev_per_attempt | -447.6 | -250.2 |
| ev_p05 | -510.9 | -251.5 |
| ev_p95 | -362.8 | -249.2 |
| max_best_day_share | 1.3282 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 87.5 |
| censored_pa | 93 | 10 |

## Statistics
- OOS trades: 119; total P&L per micro 554 USD
- Annualised Sharpe (daily, per micro): 0.25
- PSR (vs 0): 0.738; **Deflated Sharpe: 0.001** over 709 recorded trials
  (Sharpe variance across trials 7.97e-04)
- Random-entry percentile: 0.862

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'q': 0.1, 'sl_atr': 2.0, 'tp_atr': 4.0} | 0.0141 | 15 | 15 | (0.0, 1.0, 0.25) | (0.0, 1.0, 0.25) |
| 2020 | {'q': 0.1, 'sl_atr': 2.0, 'tp_atr': 4.0} | 0.0046 | 10 | 15 | (0.5, 1.0, 0.08) | (0.0, 1.0, 0.08) |
| 2021 | {'q': 0.1, 'sl_atr': 2.0, 'tp_atr': 4.0} | 0.0054 | 15 | 15 | (1.0, 1.0, 0.12) | (0.5, 1.0, 0.12) |
| 2022 | {'q': 0.1, 'sl_atr': 2.0, 'tp_atr': 4.0} | 0.0246 | 25 | 15 | (2.0, 1.0, 0.57) | (2.0, 0.5, 0.57) |
| 2023 | {'q': 0.1, 'sl_atr': 1.0, 'tp_atr': 4.0} | 0.0221 | 50 | 25 | (2.0, 1.0, 0.42) | (2.0, 1.0, 0.42) |
| 2024 | {'q': 0.1, 'sl_atr': 1.0, 'tp_atr': 4.0} | 0.0213 | 50 | 25 | (2.0, 1.0, 0.38) | (2.0, 1.0, 0.38) |
| 2025 | {'q': 0.1, 'sl_atr': 1.0, 'tp_atr': 4.0} | 0.0198 | 50 | 25 | (2.0, 1.0, 0.35) | (2.0, 1.0, 0.35) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2333 | 0.0000 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -582.4 | -249.0 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -0.32 USD

## Evidence
![[bb_squeeze_15m@ES-equity.png]]
![[bb_squeeze_15m@ES-fan.png]]
![[bb_squeeze_15m@ES-random.png]]
![[bb_squeeze_15m@ES-drawdown.png]]
![[bb_squeeze_15m@ES-monthly.png]]
![[bb_squeeze_15m@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run bb_squeeze_15m@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
