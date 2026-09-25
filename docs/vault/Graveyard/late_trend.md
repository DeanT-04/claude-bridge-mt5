---
type: strategy
strategy: late_trend
family: late_trend
verdict: graveyard
plan: eod
run_id: 3280099539
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]
commit: 38a600e-dirty
seed: 11
---
# late_trend: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'decide': 780, 'k': 0.3, 'sl_atr': 0.25}; base sizes (micros)
{'eod': 5, 'intraday': 3}; sizing policy (alpha, beta, mu) {'eod': (2.0, 1.0, 6.6260748946559165), 'intraday': (0.5, 1.0, 6.6260748946559165)}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 632 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.2121 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 0.9990 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -444.3 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0612 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.2567 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2382 | >= 0.7 | commercial | FAIL |
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
| eval_pass | 0.2567 | 0.1270 |
| eval_fail | 0.4503 | 0.8172 |
| eval_expired | 0.2930 | 0.0558 |
| median_sessions_to_pass | 5.0000 | 9.0000 |
| p90_sessions_to_pass | 15.0 | 17.2 |
| first_payout_given_pass | 0.2382 | 0.2169 |
| end_to_end_payout | 0.0612 | 0.0276 |
| mean_payouts_given_pass | 0.7487 | 0.3280 |
| ev_per_attempt | -219.0 | -196.6 |
| ev_p05 | -444.3 | -237.1 |
| ev_p95 | 48.1 | -139.2 |
| max_best_day_share | 1.3253 | 1.0000 |
| starts | 1488 | 1488 |
| effective_n | 135.3 | 248.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 632; total P&L per micro 10,103 USD
- Annualised Sharpe (daily, per micro): 1.11
- PSR (vs 0): 0.999; **Deflated Sharpe: 0.212** over 73 recorded trials
  (Sharpe variance across trials 1.33e-03)
- Random-entry percentile: 0.999

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'decide': 840, 'k': 0.8, 'sl_atr': 0.25} | 0.0710 | 20 | 20 | (0.5, 1.0, 1.92) | (0.0, 1.0, 1.92) |
| 2020 | {'decide': 840, 'k': 0.8, 'sl_atr': 0.25} | 0.0504 | 20 | 12 | (0.5, 1.0, 1.26) | (0.0, 1.0, 1.26) |
| 2021 | {'decide': 780, 'k': 0.5, 'sl_atr': 0.25} | 0.0481 | 25 | 4 | (0.0, 1.0, 2.13) | (0.0, 1.0, 2.13) |
| 2022 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0570 | 10 | 8 | (2.0, 1.0, 3.56) | (2.0, 1.0, 3.56) |
| 2023 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0874 | 5 | 3 | (2.0, 1.0, 7.12) | (0.5, 1.0, 7.12) |
| 2024 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0843 | 5 | 3 | (2.0, 1.0, 6.89) | (0.5, 1.0, 6.89) |
| 2025 | {'decide': 780, 'k': 0.3, 'sl_atr': 0.25} | 0.0745 | 5 | 3 | (2.0, 1.0, 6.23) | (0.5, 1.0, 6.23) |

## Holdout (holdout already used 1x for these params: not re-run)
not run

## Evidence
![[late_trend-equity.png]]
![[late_trend-fan.png]]
![[late_trend-random.png]]
![[late_trend-drawdown.png]]
![[late_trend-monthly.png]]
![[late_trend-sensitivity.png]]

Reproduce: `uv run propquant gauntlet run late_trend`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
