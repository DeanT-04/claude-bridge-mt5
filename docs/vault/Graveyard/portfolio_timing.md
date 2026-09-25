---
type: strategy
strategy: portfolio_timing
family: portfolio
verdict: graveyard
plan: eod
run_id: 4c78ceb312
data_hash: 3a26012ed92b62d5[1022:3793][0:2381]+3a26012ed92b62d5[1022:3793][0:2381]+b6e54fe4873dca2a[1022:3793][0:2381]+d223130e354eb243[1022:3793][0:2381]+b6e54fe4873dca2a[1022:3793][0:2381]+3a26012ed92b62d5[1022:3793][0:2381]
commit: ba53fe8-dirty
seed: 11
---
# portfolio_timing: **GRAVEYARD**

Best plan: **Apex eod 50K**. Final params {'late_trend': {'decide': 780, 'k': 0.3, 'sl_atr': 0.25}, 'orb': {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660}, 'macd_trend_5m': {'align': True, 'sl_atr': 1.0, 'tp_atr': 4.0}, 'donchian_break_15m': {'n': 55, 'sl_atr': 1.0, 'tp_atr': 4.0}, 'supertrend_5m': {'mult': 2.0, 'sl_atr': 2.0, 'align': True}, 'ib_twap': {'sl_frac': 0.5, 'tp_mult': 2.0}}; base sizes (micros)
{}; sizing policy (alpha, beta, mu) {}.

## Gates (out-of-sample unless noted)
| gate | value | needs | kind | result |
|---|---|---|---|---|
| OOS trades | 10359 | >= 200 | stat | PASS |
| Deflated Sharpe | 0.1519 | >= 0.95 | stat | FAIL |
| Beats random entry (percentile) | 1.0000 | >= 0.95 | stat | PASS |
| EV per attempt, 5th pct (USD) | -512.3 | > 0 | stat | FAIL |
| Holdout consistent | 0.0000 | >= 1 | stat | FAIL |
| End-to-end payout rate | 0.0370 | >= 0.5 | commercial | FAIL |
| Evaluation pass rate | 0.1620 | >= 0.6 | commercial | FAIL |
| First payout once funded | 0.2282 | >= 0.7 | commercial | FAIL |
| Median sessions to pass | 4.0000 | <= 15 | speed | PASS |
| 90th pct sessions to pass | 11.0 | <= 30 | speed | PASS |

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
| eval_pass | 0.1620 | 0.0007 |
| eval_fail | 0.8017 | 0.9993 |
| eval_expired | 0.0363 | 0.0000 |
| median_sessions_to_pass | 4.0000 | 11.0 |
| p90_sessions_to_pass | 11.0 | 11.0 |
| first_payout_given_pass | 0.2282 | 0.0000 |
| end_to_end_payout | 0.0370 | 0.0000 |
| mean_payouts_given_pass | 0.6224 | 0.0000 |
| ev_per_attempt | -388.6 | -249.0 |
| ev_p05 | -512.3 | -249.1 |
| ev_p95 | -237.7 | -249.0 |
| max_best_day_share | 1.3325 | 0.5066 |
| starts | 1488 | 1488 |
| effective_n | 297.6 | 1,488.0 |
| censored_pa | 0 | 0 |

## Statistics
- OOS trades: 10,359; total P&L per micro 61,009 USD
- Annualised Sharpe (daily, per micro): 1.05
- PSR (vs 0): 0.997; **Deflated Sharpe: 0.152** over 745 recorded trials
  (Sharpe variance across trials 8.17e-04)
- Random-entry percentile: 1.000

## Walk-forward folds (params and size picked on training years only)
| test year | params | train SR (daily) | size eod | size intraday | policy eod | policy intraday |
|---|---|---|---|---|---|---|
| 2019 | {'late_trend': {'decide': 840, 'k': 0.8, 'sl_atr': 0.25}, 'orb': {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660}, 'macd_trend_5m': {'align': True, 'sl_atr': 2.0, 'tp_atr': 2.0}, 'donchian_break_15m': {'n': 55, 'sl_atr': 1.0, 'tp_atr': 4.0}, 'supertrend_5m': {'mult': 3.0, 'sl_atr': 2.0, 'align': True}, 'ib_twap': {'sl_frac': 0.5, 'tp_mult': 2.0}} | 0.0266 | 2 | 3 | (0.5, 1.0, 4.27) | (0.0, 0.5, 4.27) |
| 2020 | {'late_trend': {'decide': 840, 'k': 0.8, 'sl_atr': 0.25}, 'orb': {'or_min': 5, 'sl_frac': 1.0, 'tp_mult': 1.0, 'last_entry': 660}, 'macd_trend_5m': {'align': True, 'sl_atr': 1.0, 'tp_atr': 4.0}, 'donchian_break_15m': {'n': 55, 'sl_atr': 1.0, 'tp_atr': 4.0}, 'supertrend_5m': {'mult': 3.0, 'sl_atr': 2.0, 'align': True}, 'ib_twap': {'sl_frac': 0.5, 'tp_mult': 2.0}} | 0.0144 | 2 | 4 | (0.5, 1.0, 2.32) | (0.0, 0.0, 2.32) |
| 2021 | {'late_trend': {'decide': 780, 'k': 0.5, 'sl_atr': 0.25}, 'orb': {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660}, 'macd_trend_5m': {'align': True, 'sl_atr': 1.0, 'tp_atr': 4.0}, 'donchian_break_15m': {'n': 55, 'sl_atr': 2.0, 'tp_atr': 4.0}, 'supertrend_5m': {'mult': 2.0, 'sl_atr': 2.0, 'align': True}, 'ib_twap': {'sl_frac': 0.5, 'tp_mult': 2.0}} | 0.0368 | 1 | 3 | (0.0, 1.0, 10.99) | (0.0, 0.0, 10.99) |
| 2022 | {'late_trend': {'decide': 780, 'k': 0.3, 'sl_atr': 0.25}, 'orb': {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660}, 'macd_trend_5m': {'align': True, 'sl_atr': 1.0, 'tp_atr': 4.0}, 'donchian_break_15m': {'n': 55, 'sl_atr': 2.0, 'tp_atr': 2.0}, 'supertrend_5m': {'mult': 2.0, 'sl_atr': 2.0, 'align': True}, 'ib_twap': {'sl_frac': 0.5, 'tp_mult': 2.0}} | 0.0450 | 1 | 3 | (0.0, 0.5, 15.71) | (0.0, 0.0, 15.71) |
| 2023 | {'late_trend': {'decide': 780, 'k': 0.3, 'sl_atr': 0.25}, 'orb': {'or_min': 15, 'sl_frac': 0.5, 'tp_mult': 2.0, 'last_entry': 660}, 'macd_trend_5m': {'align': True, 'sl_atr': 1.0, 'tp_atr': 4.0}, 'donchian_break_15m': {'n': 55, 'sl_atr': 2.0, 'tp_atr': 2.0}, 'supertrend_5m': {'mult': 2.0, 'sl_atr': 2.0, 'align': True}, 'ib_twap': {'sl_frac': 0.5, 'tp_mult': 2.0}} | 0.0772 | 1 | 3 | (0.0, 0.5, 35.89) | (0.0, 1.0, 35.89) |
| 2024 | {'late_trend': {'decide': 780, 'k': 0.3, 'sl_atr': 0.25}, 'orb': {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660}, 'macd_trend_5m': {'align': True, 'sl_atr': 1.0, 'tp_atr': 4.0}, 'donchian_break_15m': {'n': 55, 'sl_atr': 1.0, 'tp_atr': 4.0}, 'supertrend_5m': {'mult': 2.0, 'sl_atr': 2.0, 'align': True}, 'ib_twap': {'sl_frac': 0.5, 'tp_mult': 2.0}} | 0.0697 | 1 | 1 | (0.0, 0.0, 34.43) | (0.5, 1.0, 34.43) |
| 2025 | {'late_trend': {'decide': 780, 'k': 0.3, 'sl_atr': 0.25}, 'orb': {'or_min': 30, 'sl_frac': 1.0, 'tp_mult': 2.0, 'last_entry': 660}, 'macd_trend_5m': {'align': True, 'sl_atr': 1.0, 'tp_atr': 4.0}, 'donchian_break_15m': {'n': 55, 'sl_atr': 1.0, 'tp_atr': 4.0}, 'supertrend_5m': {'mult': 2.0, 'sl_atr': 2.0, 'align': True}, 'ib_twap': {'sl_frac': 0.5, 'tp_mult': 2.0}} | 0.0700 | 1 | 1 | (0.0, 0.0, 35.98) | (0.0, 1.0, 35.98) |

## Holdout (CONTAMINATED: member holdouts already opened (late_trend, orb, macd_trend_5m, donchian_break_15m, supertrend_5m, ib_twap); needs forward data)
not run

## Evidence
![[portfolio_timing-equity.png]]
![[portfolio_timing-fan.png]]
![[portfolio_timing-random.png]]
![[portfolio_timing-drawdown.png]]
![[portfolio_timing-monthly.png]]


Reproduce: `uv run propquant gauntlet run portfolio_timing`. Firm-rule assumptions: see
[[Apex Trader Funding]] (open questions).
