---
type: strategy
strategy: late_trend__vol_high
family: late_trend
verdict: graveyard
plan: eod
run_id: 708e13ce67
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# late_trend__vol_high: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'decide': 780, 'k': 0.3, 'sl_atr': 0.25}; base sizes (micros)
{'eod': 3, 'intraday': 4}; sizing policy (alpha, beta, mu) {'eod': (1.0, 1.0, 4.015704119379137), 'intraday': (2.0, 1.0, 4.015704119379137)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 344 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0035 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.7920 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -555.6 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0168 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1015 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1656 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 5.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 15.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.1015 | 0.0618 |
| eval_fail | 0.3219 | 0.4153 |
| eval_expired | 0.5766 | 0.5228 |
| median_sessions_to_pass | 5.0000 | 6.5000 |
| p90_sessions_to_pass | 15.0 | 18.0 |
| first_payout_given_pass | 0.1656 | 0.1739 |
| end_to_end_payout | 0.0168 | 0.0108 |
| mean_payouts_given_pass | 0.3245 | 0.2500 |
| ev_per_attempt | -511.4 | -226.5 |
| ev_p05 | -555.6 | -250.1 |
| ev_p95 | -452.8 | -195.1 |
| max_best_day_share | 1.3253 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 70.9 | 74.4 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 344; total P&L per micro 1,792 USD
- Annualised Sharpe (daily, per micro): 0.22
- PSR (vs 0): 0.713; **Deflated Sharpe: 0.003** over 533 recorded trials
  (Sharpe variance across trials 6.78e-04)
- Random-entry percentile: 0.792

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'decide': 840, 'k': 0.5, 'sl_atr': 0.25} | 0.0783 | 12 | 8 | (0.5, 1.0, 2.59) | (0.0, 0.5, 2.59) |
| 2020 | {'decide': 840, 'k': 0.8, 'sl_atr': 0.25} | 0.0472 | 25 | 25 | (0.0, 1.0, 1.11) | (0.0, 0.5, 1.11) |
| 2021 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | 0.0376 | 4 | 4 | (0.0, 1.0, 1.54) | (0.0, 1.0, 1.54) |
| 2022 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.5} | 0.0533 | 5 | 5 | (1.0, 1.0, 3.26) | (2.0, 1.0, 3.26) |
| 2023 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0722 | 5 | 4 | (2.0, 1.0, 5.17) | (2.0, 1.0, 5.17) |
| 2024 | {'decide': 840, 'k': 0.3, 'sl_atr': 0.25} | 0.0681 | 3 | 2 | (1.0, 1.0, 4.08) | (0.5, 1.0, 4.08) |
| 2025 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0541 | 3 | 4 | (1.0, 1.0, 3.82) | (2.0, 1.0, 3.82) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1111 | 0.0593 |
| end_to_end_payout | 0.0519 | 0.0296 |
| ev_per_attempt | -509.6 | -234.7 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 2.78 USD

## Evidence
![[late_trend__vol_high-equity.png]]
![[late_trend__vol_high-fan.png]]
![[late_trend__vol_high-random.png]]
![[late_trend__vol_high-drawdown.png]]
![[late_trend__vol_high-monthly.png]]
![[late_trend__vol_high-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run late_trend__vol_high`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
