---
type: strategy
strategy: keltner_fade_15m
family: keltner_fade
verdict: graveyard
plan: intraday
run_id: b8a2ebab49
data_hash: d223130e354eb243[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# keltner_fade_15m: **GRAVEYARD**

Best plan: **Apex intraday 50K**. Final params {'k': 2.0, 'adx_max': 20, 'sl_atr': 1.5}; base sizes (micros)
{'eod': 4, 'intraday': 3}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 0.280071593939451), 'intraday': (0.0, 1.0, 0.280071593939451)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 425 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0003 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.4670 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -251.3 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0000 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0202 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0000 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 12.0 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 19.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.0531 | 0.0202 |
| eval_fail | 0.1169 | 0.5907 |
| eval_expired | 0.8300 | 0.3891 |
| median_sessions_to_pass | 10.0 | 12.0 |
| p90_sessions_to_pass | 18.2 | 19.0 |
| first_payout_given_pass | 0.0000 | 0.0000 |
| end_to_end_payout | 0.0000 | 0.0000 |
| mean_payouts_given_pass | 0.0000 | 0.0000 |
| ev_per_attempt | -557.4 | -250.2 |
| ev_p05 | -562.1 | -251.3 |
| ev_p95 | -553.5 | -249.4 |
| max_best_day_share | 1.0525 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 67.6 | 124.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 425; total P&L per micro -1,089 USD
- Annualised Sharpe (daily, per micro): -0.17
- PSR (vs 0): 0.340; **Deflated Sharpe: 0.000** over 385 recorded trials
  (Sharpe variance across trials 6.83e-04)
- Random-entry percentile: 0.467

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'k': 2.5, 'adx_max': 20, 'sl_atr': 1.5} | -0.0301 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'k': 2.5, 'adx_max': 20, 'sl_atr': 1.5} | -0.0257 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'k': 2.0, 'adx_max': 25, 'sl_atr': 1.5} | -0.0137 | 6 | 5 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'k': 2.0, 'adx_max': 20, 'sl_atr': 1.0} | -0.0179 | 15 | 30 | (1.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'k': 2.0, 'adx_max': 20, 'sl_atr': 1.5} | -0.0182 | 1 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2024 | {'k': 2.0, 'adx_max': 20, 'sl_atr': 1.5} | -0.0122 | 1 | 20 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'k': 2.0, 'adx_max': 20, 'sl_atr': 1.5} | -0.0019 | 3 | 3 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0926 | 0.0111 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -562.9 | -249.7 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 1.97 USD

## Evidence
![[keltner_fade_15m-equity.png]]
![[keltner_fade_15m-fan.png]]
![[keltner_fade_15m-random.png]]
![[keltner_fade_15m-drawdown.png]]
![[keltner_fade_15m-monthly.png]]
![[keltner_fade_15m-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run keltner_fade_15m`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
