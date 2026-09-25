---
type: strategy
strategy: bb_squeeze_5m
family: bb_squeeze
verdict: graveyard
plan: eod
run_id: df27882891
data_hash: b6e54fe4873dca2a[1022:3793][0:2381]
commit: 15230e7-dirty
seed: 11
---
# bb_squeeze_5m: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'q': 0.1, 'sl_atr': 1.0, 'tp_atr': 4.0}; base sizes (micros)
{'eod': 8, 'intraday': 6}; sizing policy (alpha, beta, mu) {'eod': (0.5, 1.0, 0.08233375611968961), 'intraday': (0.0, 1.0, 0.08233375611968961)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 281 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.0002 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.6080 | >= 0.95 | stat | FAIL |
| EV per attempt, 5th pct (USD) | -560.6 | > 0 | stat | FAIL |
| Holdout consistent | 1.0000 | >= 1 | stat | PASS |
| End-to-end payout rate | 0.0027 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.0531 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.0506 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 9.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 16.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.0531 | 0.0067 |
| eval_fail | 0.2097 | 0.2372 |
| eval_expired | 0.7372 | 0.7560 |
| median_sessions_to_pass | 9.0000 | 7.5000 |
| p90_sessions_to_pass | 16.0 | 14.4 |
| first_payout_given_pass | 0.0506 | 0.0000 |
| end_to_end_payout | 0.0027 | 0.0000 |
| mean_payouts_given_pass | 0.0506 | 0.0000 |
| ev_per_attempt | -556.0 | -249.4 |
| ev_p05 | -560.6 | -249.8 |
| ev_p95 | -551.8 | -249.1 |
| max_best_day_share | 1.0000 | 0.5424 |
| starts | 1488 | 1488 |
| effective_n | 67.6 | 67.6 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 281; total P&L per micro -277 USD
- Annualised Sharpe (daily, per micro): -0.10
- PSR (vs 0): 0.404; **Deflated Sharpe: 0.000** over 113 recorded trials
  (Sharpe variance across trials 1.03e-03)
- Random-entry percentile: 0.608

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'q': 0.1, 'sl_atr': 2.0, 'tp_atr': 2.0} | 0.0091 | 25 | 25 | (0.5, 0.5, 0.07) | (0.0, 1.0, 0.07) |
| 2020 | {'q': 0.1, 'sl_atr': 2.0, 'tp_atr': 2.0} | -0.0022 | 1 | 1 | (0.0, 0.0, 0.0) | (0.0, 0.0, 0.0) |
| 2021 | {'q': 0.1, 'sl_atr': 2.0, 'tp_atr': 2.0} | 0.0048 | 10 | 10 | (0.5, 0.5, 0.11) | (0.5, 0.0, 0.11) |
| 2022 | {'q': 0.1, 'sl_atr': 2.0, 'tp_atr': 2.0} | 0.0063 | 10 | 10 | (0.5, 0.5, 0.14) | (0.5, 0.0, 0.14) |
| 2023 | {'q': 0.1, 'sl_atr': 2.0, 'tp_atr': 2.0} | 0.0178 | 12 | 10 | (0.0, 1.0, 0.42) | (0.5, 0.0, 0.42) |
| 2024 | {'q': 0.1, 'sl_atr': 2.0, 'tp_atr': 4.0} | 0.0139 | 20 | 5 | (0.5, 0.5, 0.43) | (0.0, 1.0, 0.43) |
| 2025 | {'q': 0.1, 'sl_atr': 1.0, 'tp_atr': 4.0} | 0.0107 | 8 | 6 | (0.5, 1.0, 0.26) | (0.0, 1.0, 0.26) |

## Holdout (first access)
| metric | eod | intraday |
|---|---|---|
| eval_pass | 0.1519 | 0.0778 |
| end_to_end_payout | 0.0000 | 0.0000 |
| ev_per_attempt | -571.1 | -253.6 |
| starts | 270 | 270 |

Holdout daily mean P&L per micro: 0.51 USD

## Evidence
![[bb_squeeze_5m-equity.png]]
![[bb_squeeze_5m-fan.png]]
![[bb_squeeze_5m-random.png]]
![[bb_squeeze_5m-drawdown.png]]
![[bb_squeeze_5m-monthly.png]]
![[bb_squeeze_5m-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run bb_squeeze_5m`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
