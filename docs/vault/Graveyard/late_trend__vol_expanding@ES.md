---
type: strategy
strategy: late_trend__vol_expanding@ES
family: late_trend
verdict: graveyard
plan: eod
run_id: 4d44f1c3ed
data_hash: 6b31ed1abba2c819[1029:3800][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# late_trend__vol_expanding@ES: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'decide': 840, 'k': 0.5, 'sl_atr': 0.25}; base sizes (micros)
{'eod': 6, 'intraday': 5}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.5, 0.21004620484513614), 'intraday': (0.0, 1.0, 0.21004620484513614)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 344 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.5710 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -554.3 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0215 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1277 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1684 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 11.0 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 20.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.1277 | 0.0444 |
| eval_fail | 0.4147 | 0.5753 |
| eval_expired | 0.4577 | 0.3804 |
| median_sessions_to_pass | 11.0 | 8.5000 |
| p90_sessions_to_pass | 20.0 | 20.0 |
| first_payout_given_pass | 0.1684 | 0.3333 |
| end_to_end_payout | 0.0215 | 0.0148 |
| mean_payouts_given_pass | 0.2105 | 0.6061 |
| ev_per_attempt | -527.7 | -205.2 |
| ev_p05 | -554.3 | -249.4 |
| ev_p95 | -492.3 | -136.0 |
| max_best_day_share | 1.3130 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 74.4 | 93.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 344; total P&L per micro -914 USD
- Annualised Sharpe (daily, per micro): -0.19
- PSR (vs 0): 0.320; **Deflated Sharpe: 0.000** over 1223 recorded trials
  (Sharpe variance across trials 1.15e-03)
- Random-entry percentile: 0.571

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'decide': 840, 'k': 0.8, 'sl_atr': 0.5} | 0.0353 | 20 | 10 | (0.0, 1.0, 0.71) | (0.0, 1.0, 0.71) |
| 2020 | {'decide': 840, 'k': 0.8, 'sl_atr': 0.25} | 0.0108 | 50 | 50 | (0.0, 0.0, 0.18) | (0.0, 0.0, 0.18) |
| 2021 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | 0.0038 | 12 | 5 | (0.0, 0.0, 0.13) | (0.0, 1.0, 0.13) |
| 2022 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | -0.0091 | 12 | 15 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2023 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | 0.0160 | 8 | 6 | (0.0, 0.5, 0.72) | (0.5, 0.5, 0.72) |
| 2024 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | 0.0089 | 8 | 6 | (0.0, 0.5, 0.4) | (0.5, 0.5, 0.4) |
| 2025 | {'decide': 840, 'k': 0.5, 'sl_atr': 0.25} | -0.0029 | 10 | 15 | (0.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0778 | 0.0667 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -560.8 | -252.9 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 1.03 USD

## Evidence
![[late_trend__vol_expanding@ES-equity.png]]
![[late_trend__vol_expanding@ES-fan.png]]
![[late_trend__vol_expanding@ES-random.png]]
![[late_trend__vol_expanding@ES-drawdown.png]]
![[late_trend__vol_expanding@ES-monthly.png]]
![[late_trend__vol_expanding@ES-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run late_trend__vol_expanding@ES`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
