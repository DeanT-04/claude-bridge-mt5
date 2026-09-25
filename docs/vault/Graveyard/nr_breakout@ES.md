---
type: strategy
strategy: nr_breakout@ES
family: narrow_range
verdict: graveyard
plan: eod
run_id: 7103b8cdc0
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# nr_breakout@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'nr': 7, 'sl_frac': 0.5, 'tp_mult': 2.0}; base sizes (micros)
{'eod': 8, 'intraday': 8}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 1.302759344813123), 'intraday': (0.0, 1.0, 1.302759344813123)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 333 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.8430 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -565.0 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0343 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2137 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1604 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 8.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 17.0 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- Beats random entry (percentile)
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2137 | 0.0853 |
| eval_fail | 0.4980 | 0.7466 |
| eval_expired | 0.2883 | 0.1680 |
| median_sessions_to_pass | 8.0000 | 9.0000 |
| p90_sessions_to_pass | 17.0 | 18.0 |
| first_payout_given_pass | 0.1604 | 0.2441 |
| end_to_end_payout | 0.0343 | 0.0208 |
| mean_payouts_given_pass | 0.1667 | 0.2677 |
| ev_per_attempt | -535.8 | -233.3 |
| ev_p05 | -565.0 | -249.0 |
| ev_p95 | -502.8 | -214.6 |
| max_best_day_share | 1.3001 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 106.3 | 186.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 333; total P&L per micro 711 USD
- Annualised Sharpe (daily, per micro): 0.14
- PSR (vs 0): 0.644; **Deflated Sharpe: 0.000** over 1291 recorded trials
  (Sharpe variance across trials 1.24e-03)
- Random-entry percentile: 0.843

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'nr': 4, 'sl_frac': 0.5, 'tp_mult': 2.0} | 0.0431 | 10 | 8 | (0.5, 1.0, 1.19) | (0.5, 1.0, 1.19) |
| 2020 | {'nr': 4, 'sl_frac': 0.5, 'tp_mult': 2.0} | 0.0195 | 10 | 8 | (0.5, 1.0, 0.54) | (0.5, 1.0, 0.54) |
| 2021 | {'nr': 4, 'sl_frac': 0.5, 'tp_mult': 2.0} | 0.0074 | 10 | 8 | (0.5, 1.0, 0.27) | (0.5, 1.0, 0.27) |
| 2022 | {'nr': 4, 'sl_frac': 0.5, 'tp_mult': 2.0} | 0.0137 | 10 | 8 | (0.5, 1.0, 0.5) | (0.5, 1.0, 0.5) |
| 2023 | {'nr': 7, 'sl_frac': 0.5, 'tp_mult': 1.0} | 0.0293 | 8 | 8 | (0.0, 1.0, 0.91) | (0.0, 1.0, 0.91) |
| 2024 | {'nr': 7, 'sl_frac': 1.0, 'tp_mult': 1.0} | 0.0339 | 20 | 8 | (2.0, 0.5, 1.18) | (2.0, 1.0, 1.18) |
| 2025 | {'nr': 7, 'sl_frac': 0.5, 'tp_mult': 2.0} | 0.0354 | 6 | 8 | (0.5, 1.0, 1.2) | (0.0, 1.0, 1.2) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0926 | 0.0296 |
| end_to_end_payout | 0.0519 | 0.0111 |
| ev_per_attempt | -485.1 | -234.1 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 0.22 USD

## Evidence
![[nr_breakout@ES-equity.png]]
![[nr_breakout@ES-fan.png]]
![[nr_breakout@ES-random.png]]
![[nr_breakout@ES-drawdown.png]]
![[nr_breakout@ES-monthly.png]]
![[nr_breakout@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run nr_breakout@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
