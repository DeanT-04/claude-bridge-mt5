---
type: strategy
strategy: late_trend
family: late_trend
verdict: graveyard
plan: eod
run_id: 0178cbe966
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 5455e7a-dirty
seed: 11
---
# late_trend: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'decide': 780, 'k': 0.3, 'sl_atr': 0.25}; sizes (micros)
{'eod': 4, 'intraday': 4}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 632 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.2094 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9990 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -434.3 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0484 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2124 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2278 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 7.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 17.0 | <= 30 | speed | PASS |

Failed gates:
- Deflated Sharpe
- EV per attempt, 5th pct (USD)
- End-to-end payout rate
- Evaluation pass rate
- First payout once funded

## Challenge Monte Carlo (out-of-sample, one purchased evaluation per start session)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2124 | 0.0504 |
| eval_fail | 0.4718 | 0.7231 |
| eval_expired | 0.3159 | 0.2265 |
| median_sessions_to_pass | 7.0000 | 4.0000 |
| p90_sessions_to_pass | 17.0 | 14.6 |
| first_payout_given_pass | 0.2278 | 0.0400 |
| end_to_end_payout | 0.0484 | 0.0020 |
| mean_payouts_given_pass | 0.9146 | 0.1200 |
| ev_per_attempt | -190.4 | -239.9 |
| ev_p05 | -434.3 | -252.7 |
| ev_p95 | 98.7 | -216.2 |
| max_best_day_share | 1.3329 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 114.5 | 212.6 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 632; total P&L per micro 10,103 USD
- Annualised Sharpe (daily, per micro): 1.11
- PSR (vs 0): 0.999; **Deflated Sharpe: 0.209** over 73 recorded trials
  (Sharpe variance across trials 1.34e-03)
- Random-entry percentile: 0.999

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday |
|---|---|---|---|---|
| 2019 | {'decide': 840, 'k': 0.8, 'sl_atr': 0.25} | 0.0710 | 50 | 30 |
| 2020 | {'decide': 840, 'k': 0.8, 'sl_atr': 0.25} | 0.0504 | 50 | 30 |
| 2021 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | 0.0481 | 50 | 60 |
| 2022 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0570 | 8 | 30 |
| 2023 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0874 | 4 | 4 |
| 2024 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0843 | 4 | 4 |
| 2025 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0745 | 4 | 4 |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0926 | 0.0704 |
| end_to_end_payout | 0.0481 | 0.0481 |
| ev_per_attempt | -494.8 | -185.1 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 0.91 USD

## Evidence
![[late_trend-equity.png]]
![[late_trend-fan.png]]
![[late_trend-random.png]]
![[late_trend-drawdown.png]]
![[late_trend-monthly.png]]
![[late_trend-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run late_trend`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
