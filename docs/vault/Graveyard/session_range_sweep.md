---
type: strategy
strategy: session_range_sweep
family: liquidity_sweep
verdict: graveyard
plan: eod
run_id: 5a9d70cbf1
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# session_range_sweep: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'range': 'london', 'target': 'far'}; base sizes (micros)
{'eod': 6, 'intraday': 8}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 0.33036245275090564), 'intraday': (0.5, 0.0, 0.33036245275090564)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 1208 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0000 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.6300 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -573.7 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0208 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1922 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.1084 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 6.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 15.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.1922 | 0.1163 |
| eval_fail | 0.5995 | 0.8024 |
| eval_expired | 0.2083 | 0.0813 |
| median_sessions_to_pass | 6.0000 | 8.0000 |
| p90_sessions_to_pass | 15.0 | 17.0 |
| first_payout_given_pass | 0.1084 | 0.0983 |
| end_to_end_payout | 0.0208 | 0.0114 |
| mean_payouts_given_pass | 0.1119 | 0.0983 |
| ev_per_attempt | -561.7 | -249.1 |
| ev_p05 | -573.7 | -255.8 |
| ev_p95 | -546.9 | -239.2 |
| max_best_day_share | 1.4032 | 1.2184 |
| starts | 1488 | 1488 |
| effective_n | 186.0 | 248.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 1,208; total P&L per micro -1,652 USD
- Annualised Sharpe (daily, per micro): -0.28
- PSR (vs 0): 0.242; **Deflated Sharpe: 0.000** over 1047 recorded trials
  (Sharpe variance across trials 1.07e-03)
- Random-entry percentile: 0.630

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'range': 'london', 'target': 'far'} | 0.0041 | 1 | 15 | (0.0, 0.0, 0.08) | (0.5, 1.0, 0.08) |
| 2020 | {'range': 'premarket', 'target': 'far'} | -0.0167 | 30 | 50 | (0.5, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'range': 'premarket', 'target': 'mid'} | 0.0185 | 6 | 5 | (0.0, 1.0, 0.56) | (0.0, 1.0, 0.56) |
| 2022 | {'range': 'premarket', 'target': 'mid'} | 0.0106 | 6 | 5 | (0.0, 1.0, 0.35) | (0.0, 1.0, 0.35) |
| 2023 | {'range': 'london', 'target': 'far'} | 0.0152 | 4 | 4 | (0.0, 1.0, 0.73) | (0.0, 1.0, 0.73) |
| 2024 | {'range': 'london', 'target': 'far'} | 0.0184 | 6 | 8 | (0.0, 1.0, 0.89) | (0.5, 0.0, 0.89) |
| 2025 | {'range': 'london', 'target': 'far'} | -0.0006 | 8 | 8 | (0.0, 0.0, 0.0) | (0.5, 0.0, 0.0) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.3111 | 0.0852 |
| end_to_end_payout | 0.0148 | 0.0037 |
| ev_per_attempt | -571.0 | -248.5 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -8.52 USD

## Evidence
![[session_range_sweep-equity.png]]
![[session_range_sweep-fan.png]]
![[session_range_sweep-random.png]]
![[session_range_sweep-drawdown.png]]
![[session_range_sweep-monthly.png]]
![[session_range_sweep-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run session_range_sweep`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
