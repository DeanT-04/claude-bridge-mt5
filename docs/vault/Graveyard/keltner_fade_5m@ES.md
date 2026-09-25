---
type: strategy
strategy: keltner_fade_5m@ES
family: keltner_fade
verdict: graveyard
plan: eod
run_id: 46315faadd
data_hash: 2caacdca76e5ba37[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# keltner_fade_5m@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'k': 2.5, 'adx_max': 25, 'sl_atr': 1.5}; base sizes (micros)
{'eod': 6, 'intraday': 6}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1164 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.5060 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -552.5 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0074 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0222 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.3333 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 18.0 | <= 15 | speed | FAIL |
| 90th pct sessions to pass | 21.0 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- Beats random entry (percentile)
- EV per attempt, 5th pct (USD)
- Holdout consistent
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded
- Median sessions to pass

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0222 | 0.0108 |
| eval_fail | 0.2567 | 0.1163 |
| eval_expired | 0.7211 | 0.8730 |
| median_sessions_to_pass | 18.0 | 19.5 |
| p90_sessions_to_pass | 21.0 | 21.5 |
| first_payout_given_pass | 0.3333 | 0.0000 |
| end_to_end_payout | 0.0074 | 0.0000 |
| mean_payouts_given_pass | 0.3333 | 0.0000 |
| ev_per_attempt | -547.0 | -249.6 |
| ev_p05 | -552.5 | -250.4 |
| ev_p95 | -538.8 | -249.0 |
| max_best_day_share | 0.6293 | 0.4926 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 67.6 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 1,164; total P&L per micro -4,058 USD
- Annualised Sharpe (daily, per micro): -0.85
- PSR (vs 0): 0.021; **Deflated Sharpe: 0.000** over 969 recorded trials
  (Sharpe variance across trials 1.09e-03)
- Random-entry percentile: 0.506

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'k': 2.5, 'adx_max': 25, 'sl_atr': 1.5} | -0.0972 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'k': 2.5, 'adx_max': 25, 'sl_atr': 1.5} | -0.0873 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'k': 2.5, 'adx_max': 25, 'sl_atr': 1.5} | -0.0214 | 12 | 6 | (0.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2022 | {'k': 2.5, 'adx_max': 25, 'sl_atr': 1.5} | -0.0548 | 6 | 6 | (0.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2023 | {'k': 2.5, 'adx_max': 25, 'sl_atr': 1.5} | -0.0504 | 8 | 6 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2024 | {'k': 2.5, 'adx_max': 25, 'sl_atr': 1.5} | -0.0592 | 6 | 6 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2025 | {'k': 2.5, 'adx_max': 25, 'sl_atr': 1.5} | -0.0539 | 6 | 6 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0741 | 0.0741 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -560.3 | -253.4 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -5.08 USD

## Evidence
![[keltner_fade_5m@ES-equity.png]]
![[keltner_fade_5m@ES-fan.png]]
![[keltner_fade_5m@ES-random.png]]
![[keltner_fade_5m@ES-drawdown.png]]
![[keltner_fade_5m@ES-monthly.png]]
![[keltner_fade_5m@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run keltner_fade_5m@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
