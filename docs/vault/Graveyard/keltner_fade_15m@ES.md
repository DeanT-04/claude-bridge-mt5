---
type: strategy
strategy: keltner_fade_15m@ES
family: keltner_fade
verdict: graveyard
plan: intraday
run_id: 3eeab048b5
data_hash: c21e6fe846c4f1b4[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# keltner_fade_15m@ES: **GRAVEYARD**

Best plan: **Apex intraday 50K**. Final params {'k': 2.5, 'adx_max': 20, 'sl_atr': 1.5}; base sizes (micros)
{'eod': 1, 'intraday': 1}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 171 | >= 200 | stat | FAIL |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.6170 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -249.0 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0000 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0000 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0000 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | inf | <= 15 | speed | FAIL |
| 90th pct sessions to pass | inf | <= 30 | speed | FAIL |

Failed gates:
- OOS trades
- Deflated Sharpe
- Beats random entry (percentile)
- EV per attempt, 5th pct (USD)
- Holdout consistent
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded
- Median sessions to pass
- 90th pct sessions to pass

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0000 | 0.0000 |
| eval_fail | 0.0000 | 0.0000 |
| eval_expired | 1.0000 | 1.0000 |
| median_sessions_to_pass | inf | inf |
| p90_sessions_to_pass | inf | inf |
| first_payout_given_pass | 0.0000 | 0.0000 |
| end_to_end_payout | 0.0000 | 0.0000 |
| mean_payouts_given_pass | 0.0000 | 0.0000 |
| ev_per_attempt | -550.0 | -249.0 |
| ev_p05 | -550.0 | -249.0 |
| ev_p95 | -550.0 | -249.0 |
| max_best_day_share | 0.0000 | 0.0000 |
| starts | 1488 | 1488 |
| effective_n | 67.6 | 67.6 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 171; total P&L per micro -280 USD
- Annualised Sharpe (daily, per micro): -0.12
- PSR (vs 0): 0.385; **Deflated Sharpe: 0.000** over 1005 recorded trials
  (Sharpe variance across trials 1.09e-03)
- Random-entry percentile: 0.617

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'k': 2.5, 'adx_max': 20, 'sl_atr': 1.5} | -0.0252 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'k': 2.5, 'adx_max': 20, 'sl_atr': 1.5} | -0.0271 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'k': 2.5, 'adx_max': 20, 'sl_atr': 1.5} | -0.0104 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2022 | {'k': 2.5, 'adx_max': 20, 'sl_atr': 1.5} | -0.0214 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'k': 2.5, 'adx_max': 20, 'sl_atr': 1.5} | -0.0137 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2024 | {'k': 2.5, 'adx_max': 20, 'sl_atr': 1.0} | -0.0035 | 15 | 8 | (1.0, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2025 | {'k': 2.5, 'adx_max': 20, 'sl_atr': 1.5} | -0.0033 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0000 | 0.0000 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -550.0 | -249.0 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -0.83 USD

## Evidence
![[keltner_fade_15m@ES-equity.png]]
![[keltner_fade_15m@ES-fan.png]]
![[keltner_fade_15m@ES-random.png]]
![[keltner_fade_15m@ES-drawdown.png]]
![[keltner_fade_15m@ES-monthly.png]]
![[keltner_fade_15m@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run keltner_fade_15m@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
