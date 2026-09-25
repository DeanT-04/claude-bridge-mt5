---
type: strategy
strategy: late_trend__vol_low
family: late_trend
verdict: graveyard
plan: eod
run_id: fff4a1ff04
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# late_trend__vol_low: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'decide': 780, 'k': 0.3, 'sl_atr': 0.25}; base sizes (micros)
{'eod': 8, 'intraday': 3}; sizing policy (alpha, beta, mu) {'eod': (1.0, 1.0, 2.779440966372957), 'intraday': (0.0, 1.0, 2.779440966372957)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 378 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.2815 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 1.0000 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -529.2 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0504 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2117 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2381 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 5.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 15.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.2117 | 0.0800 |
| eval_fail | 0.2809 | 0.3992 |
| eval_expired | 0.5074 | 0.5208 |
| median_sessions_to_pass | 5.0000 | 7.0000 |
| p90_sessions_to_pass | 15.0 | 16.2 |
| first_payout_given_pass | 0.2381 | 0.3866 |
| end_to_end_payout | 0.0504 | 0.0309 |
| mean_payouts_given_pass | 0.7976 | 0.8829 |
| ev_per_attempt | -326.3 | -151.6 |
| ev_p05 | -529.2 | -230.6 |
| ev_p95 | -32.6 | -39.6 |
| max_best_day_share | 1.3185 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 70.9 |
| censored_pa | 63 | 8 |

## Statistics
- OOS trades: 378; total P&L per micro 5,385 USD
- Annualised Sharpe (daily, per micro): 1.03
- PSR (vs 0): 0.998; **Deflated Sharpe: 0.282** over 445 recorded trials
  (Sharpe variance across trials 6.76e-04)
- Random-entry percentile: 1.000

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0064 | 1 | 1 | (0.0, 0.0, 0.07) | (0.0, 0.0, 0.07) |
| 2020 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | 0.0393 | 30 | 30 | (0.5, 1.0, 0.54) | (0.5, 1.0, 0.54) |
| 2021 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | 0.0462 | 30 | 60 | (0.5, 1.0, 0.7) | (0.0, 0.0, 0.7) |
| 2022 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0370 | 6 | 5 | (0.0, 1.0, 1.03) | (0.0, 1.0, 1.03) |
| 2023 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0565 | 6 | 3 | (0.0, 1.0, 2.17) | (0.0, 1.0, 2.17) |
| 2024 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0611 | 8 | 3 | (1.0, 1.0, 2.76) | (0.0, 1.0, 2.76) |
| 2025 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0579 | 8 | 3 | (1.0, 1.0, 2.58) | (0.0, 1.0, 2.58) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1037 | 0.0222 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -564.4 | -250.3 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -1.87 USD

## Evidence
![[late_trend__vol_low-equity.png]]
![[late_trend__vol_low-fan.png]]
![[late_trend__vol_low-random.png]]
![[late_trend__vol_low-drawdown.png]]
![[late_trend__vol_low-monthly.png]]
![[late_trend__vol_low-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run late_trend__vol_low`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
