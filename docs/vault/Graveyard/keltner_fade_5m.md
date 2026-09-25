---
type: strategy
strategy: keltner_fade_5m
family: keltner_fade
verdict: graveyard
plan: intraday
run_id: 123f2c4b2f
data_hash: b6e54fe4873dca2a[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# keltner_fade_5m: **GRAVEYARD**

Best plan: **Apex intraday 50K**. Final params {'k': 2.5, 'adx_max': 20, 'sl_atr': 1.5}; base sizes (micros)
{'eod': 15, 'intraday': 15}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 381 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.1900 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -251.0 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0000 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0155 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0000 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 9.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 14.8 | <= 30 | speed | PASS |

Failed gates:
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
| eval_pass | 0.0437 | 0.0155 |
| eval_fail | 0.3327 | 0.3884 |
| eval_expired | 0.6237 | 0.5961 |
| median_sessions_to_pass | 6.0000 | 9.0000 |
| p90_sessions_to_pass | 16.6 | 14.8 |
| first_payout_given_pass | 0.0000 | 0.0000 |
| end_to_end_payout | 0.0000 | 0.0000 |
| mean_payouts_given_pass | 0.0000 | 0.0000 |
| ev_per_attempt | -556.1 | -249.9 |
| ev_p05 | -559.6 | -251.0 |
| ev_p95 | -553.0 | -249.1 |
| max_best_day_share | 1.2966 | 1.1828 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 70.9 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 381; total P&L per micro -2,022 USD
- Annualised Sharpe (daily, per micro): -0.44
- PSR (vs 0): 0.133; **Deflated Sharpe: 0.000** over 293 recorded trials
  (Sharpe variance across trials 7.57e-04)
- Random-entry percentile: 0.190

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'k': 2.5, 'adx_max': 20, 'sl_atr': 1.0} | -0.0164 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'k': 2.5, 'adx_max': 20, 'sl_atr': 1.0} | -0.0163 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'k': 2.5, 'adx_max': 20, 'sl_atr': 1.0} | 0.0084 | 1 | 1 | (0.0, 0.0, 0.2) | (0.0, 0.0, 0.2) |
| 2022 | {'k': 2.5, 'adx_max': 20, 'sl_atr': 1.0} | 0.0137 | 15 | 6 | (0.5, 1.0, 0.35) | (0.0, 1.0, 0.35) |
| 2023 | {'k': 2.5, 'adx_max': 20, 'sl_atr': 1.5} | 0.0076 | 8 | 10 | (0.0, 1.0, 0.26) | (0.5, 0.5, 0.26) |
| 2024 | {'k': 2.5, 'adx_max': 20, 'sl_atr': 1.5} | -0.0009 | 15 | 15 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'k': 2.5, 'adx_max': 20, 'sl_atr': 1.5} | -0.0048 | 15 | 15 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2889 | 0.1148 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -590.2 | -255.8 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -4.86 USD

## Evidence
![[keltner_fade_5m-equity.png]]
![[keltner_fade_5m-fan.png]]
![[keltner_fade_5m-random.png]]
![[keltner_fade_5m-drawdown.png]]
![[keltner_fade_5m-monthly.png]]
![[keltner_fade_5m-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run keltner_fade_5m`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
