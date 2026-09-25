---
type: strategy
strategy: rsi2_pullback_15m@ES
family: rsi2_pullback
verdict: graveyard
plan: eod
run_id: 13eafebb98
data_hash: c21e6fe846c4f1b4[1029:3800][0:2381]
commit: 790a14f
seed: 11
---
# rsi2_pullback_15m@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'trend': 100, 'lo': 5, 'sl_atr': 2.0, 'tp_atr': 1.0}; base sizes (micros)
{'eod': 50, 'intraday': 15}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.5, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 764 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.2420 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -556.1 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0108 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0524 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2051 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 10.0 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 17.3 | <= 30 | speed | PASS |

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
| eval_pass | 0.0524 | 0.0087 |
| eval_fail | 0.3038 | 0.3407 |
| eval_expired | 0.6438 | 0.6505 |
| median_sessions_to_pass | 10.0 | 11.0 |
| p90_sessions_to_pass | 17.3 | 13.0 |
| first_payout_given_pass | 0.2051 | 0.0000 |
| end_to_end_payout | 0.0108 | 0.0000 |
| mean_payouts_given_pass | 0.2051 | 0.0000 |
| ev_per_attempt | -541.2 | -249.5 |
| ev_p05 | -556.1 | -250.3 |
| ev_p95 | -517.0 | -249.0 |
| max_best_day_share | 1.2952 | 0.4263 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 70.9 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 764; total P&L per micro -3,878 USD
- Annualised Sharpe (daily, per micro): -0.88
- PSR (vs 0): 0.012; **Deflated Sharpe: 0.000** over 1417 recorded trials
  (Sharpe variance across trials 1.35e-03)
- Random-entry percentile: 0.242

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'trend': 100, 'lo': 5, 'sl_atr': 2.0, 'tp_atr': 1.0} | -0.0379 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'trend': 100, 'lo': 5, 'sl_atr': 2.0, 'tp_atr': 1.0} | -0.0416 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'trend': 200, 'lo': 5, 'sl_atr': 2.0, 'tp_atr': 1.0} | -0.0182 | 40 | 40 | (0.5, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2022 | {'trend': 200, 'lo': 5, 'sl_atr': 2.0, 'tp_atr': 1.0} | -0.0152 | 30 | 40 | (0.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |
| 2023 | {'trend': 200, 'lo': 10, 'sl_atr': 2.0, 'tp_atr': 2.0} | -0.0063 | 4 | 5 | (0.0, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2024 | {'trend': 200, 'lo': 10, 'sl_atr': 2.0, 'tp_atr': 2.0} | -0.0142 | 4 | 5 | (0.0, 0.0, 0.0) | (1.0, 0.0, 0.0) |
| 2025 | {'trend': 100, 'lo': 5, 'sl_atr': 2.0, 'tp_atr': 1.0} | -0.0209 | 50 | 15 | (0.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1926 | 0.0741 |
| end_to_end_payout | 0.0000 | 0.0333 |
| ev_per_attempt | -576.8 | -158.7 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -1.04 USD

## Evidence
![[rsi2_pullback_15m@ES-equity.png]]
![[rsi2_pullback_15m@ES-fan.png]]
![[rsi2_pullback_15m@ES-random.png]]
![[rsi2_pullback_15m@ES-drawdown.png]]
![[rsi2_pullback_15m@ES-monthly.png]]
![[rsi2_pullback_15m@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run rsi2_pullback_15m@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
