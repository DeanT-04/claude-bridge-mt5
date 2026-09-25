---
type: strategy
strategy: pd_sweep
family: liquidity_sweep
verdict: graveyard
plan: eod
run_id: 5a3c347ff7
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# pd_sweep: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'end': 720, 'buf': 0.1, 'tp_frac': 1.0}; base sizes (micros)
{'eod': 15, 'intraday': 25}; sizing policy (alpha, beta, mu) {'eod': (0.0, 0.0, 0.0), 'intraday': (0.0, 0.0, 0.0)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 945 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0001 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.5400 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -573.1 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0101 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1821 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0554 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 2.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 7.0000 | <= 30 | speed | PASS |

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
| eval_pass | 0.1821 | 0.0215 |
| eval_fail | 0.6888 | 0.9765 |
| eval_expired | 0.1290 | 0.0020 |
| median_sessions_to_pass | 2.0000 | 2.0000 |
| p90_sessions_to_pass | 7.0000 | 5.9000 |
| first_payout_given_pass | 0.0554 | 0.2500 |
| end_to_end_payout | 0.0101 | 0.0054 |
| mean_payouts_given_pass | 0.0554 | 0.2500 |
| ev_per_attempt | -560.2 | -242.2 |
| ev_p05 | -573.1 | -250.0 |
| ev_p95 | -544.4 | -231.6 |
| max_best_day_share | 1.3290 | 1.2442 |
| starts | 1488 | 1488 |
| effective_n | 372.0 | 744.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 945; total P&L per micro -1,484 USD
- Annualised Sharpe (daily, per micro): -0.13
- PSR (vs 0): 0.375; **Deflated Sharpe: 0.000** over 693 recorded trials
  (Sharpe variance across trials 8.07e-04)
- Random-entry percentile: 0.540

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'end': 720, 'buf': 0.05, 'tp_frac': 1.0} | 0.0254 | 15 | 8 | (1.0, 1.0, 0.88) | (0.0, 1.0, 0.88) |
| 2020 | {'end': 720, 'buf': 0.05, 'tp_frac': 1.0} | 0.0181 | 20 | 8 | (1.0, 1.0, 0.64) | (0.0, 1.0, 0.64) |
| 2021 | {'end': 720, 'buf': 0.05, 'tp_frac': 1.0} | -0.0139 | 60 | 60 | (2.0, 0.0, 0.0) | (2.0, 0.0, 0.0) |
| 2022 | {'end': 720, 'buf': 0.1, 'tp_frac': 1.0} | 0.0048 | 10 | 10 | (0.5, 1.0, 0.33) | (0.5, 1.0, 0.33) |
| 2023 | {'end': 720, 'buf': 0.1, 'tp_frac': 1.0} | 0.0078 | 10 | 10 | (0.5, 1.0, 0.72) | (0.5, 1.0, 0.72) |
| 2024 | {'end': 720, 'buf': 0.1, 'tp_frac': 1.0} | 0.0073 | 10 | 10 | (0.5, 1.0, 0.69) | (0.5, 1.0, 0.69) |
| 2025 | {'end': 720, 'buf': 0.1, 'tp_frac': 1.0} | 0.0032 | 10 | 10 | (0.5, 1.0, 0.32) | (0.5, 1.0, 0.32) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.2519 | 0.0148 |
| end_to_end_payout | 0.0407 | 0.0000 |
| ev_per_attempt | -485.0 | -249.9 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: -0.17 USD

## Evidence
![[pd_sweep-equity.png]]
![[pd_sweep-fan.png]]
![[pd_sweep-random.png]]
![[pd_sweep-drawdown.png]]
![[pd_sweep-monthly.png]]
![[pd_sweep-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run pd_sweep`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
