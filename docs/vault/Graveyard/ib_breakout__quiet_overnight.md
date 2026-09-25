---
type: strategy
strategy: ib_breakout__quiet_overnight
family: initial_balance
verdict: graveyard
plan: intraday
run_id: b9de3cd555
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# ib_breakout__quiet_overnight: **GRAVEYARD**

Best plan: **Apex intraday 50K**. Final params {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5}; base sizes (micros)
{'eod': 15, 'intraday': 4}; sizing policy (alpha, beta, mu) {'eod': (0.0, 1.0, 2.2142297354053135), 'intraday': (1.0, 1.0, 2.2142297354053135)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 358 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0137 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9290 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -252.6 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0047 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0531 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0886 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 4.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 11.2 | <= 30 | speed | PASS |

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
| eval_pass | 0.1136 | 0.0531 |
| eval_fail | 0.4422 | 0.6210 |
| eval_expired | 0.4442 | 0.3259 |
| median_sessions_to_pass | 7.0000 | 4.0000 |
| p90_sessions_to_pass | 17.2 | 11.2 |
| first_payout_given_pass | 0.0355 | 0.0886 |
| end_to_end_payout | 0.0040 | 0.0047 |
| mean_payouts_given_pass | 0.0355 | 0.0886 |
| ev_per_attempt | -559.7 | -247.4 |
| ev_p05 | -571.0 | -252.6 |
| ev_p95 | -557.7 | -239.2 |
| max_best_day_share | 1.2787 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 82.7 | 135.3 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 358; total P&L per micro 3,633 USD
- Annualised Sharpe (daily, per micro): 0.50
- PSR (vs 0): 0.908; **Deflated Sharpe: 0.014** over 201 recorded trials
  (Sharpe variance across trials 9.12e-04)
- Random-entry percentile: 0.929

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'ib_min': 60, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 0.5} | -0.0212 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2020 | {'ib_min': 60, 'narrow': 0.8, 'tp_mult': 1.0, 'sl_frac': 1.0} | 0.0055 | 20 | 20 | (2.0, 1.0, 0.11) | (0.0, 0.5, 0.11) |
| 2021 | {'ib_min': 30, 'narrow': 0.8, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0218 | 40 | 20 | (1.0, 1.0, 0.5) | (0.5, 1.0, 0.5) |
| 2022 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0221 | 20 | 20 | (0.5, 1.0, 1.01) | (0.0, 0.0, 1.01) |
| 2023 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0511 | 6 | 4 | (2.0, 1.0, 3.16) | (1.0, 1.0, 3.16) |
| 2024 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0416 | 4 | 4 | (0.0, 1.0, 2.68) | (1.0, 1.0, 2.68) |
| 2025 | {'ib_min': 60, 'narrow': inf, 'tp_mult': 2.0, 'sl_frac': 0.5} | 0.0333 | 15 | 4 | (0.0, 1.0, 2.22) | (1.0, 1.0, 2.22) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.0852 | 0.0926 |
| end_to_end_payout | 0.0778 | 0.0222 |
| ev_per_attempt | -411.8 | -224.0 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 1.10 USD

## Evidence
![[ib_breakout__quiet_overnight-equity.png]]
![[ib_breakout__quiet_overnight-fan.png]]
![[ib_breakout__quiet_overnight-random.png]]
![[ib_breakout__quiet_overnight-drawdown.png]]
![[ib_breakout__quiet_overnight-monthly.png]]
![[ib_breakout__quiet_overnight-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run ib_breakout__quiet_overnight`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
