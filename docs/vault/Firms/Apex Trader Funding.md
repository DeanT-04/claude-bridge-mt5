---
type: firm
firm: apex
verified_on: 2026-09-25
---
# Apex Trader Funding

Rules verified **2026-09-25** from the firm's own pages (Internet Archive captures;
the live site blocks automated readers). Platform modelled: **rithmic**.
Source of truth: `config/firms/apex.yaml`.

## EOD plan

### Evaluation

| size | balance | target | drawdown | dll | max_contracts | price |
|---|---|---|---|---|---|---|
| 25K | 25000 | 1500 | 1000 | 500 | 4 | 450 |
| 50K | 50000 | 3000 | 2000 | 1000 | 6 | 550 |
| 100K | 100000 | 6000 | 3000 | 1500 | 8 | 990 |
| 150K | 150000 | 9000 | 4000 | 2000 | 12 | 1890 |

- Drawdown trails: **eod**; stops trailing at the target balance
- Access: 30 calendar days; min trading days: 0; DLL pauses the day: True

### Performance account

- Drawdown trails **eod**, locks at start + $100
- Payouts: {'min_days': 5, 'consistency': 0.5, 'min_amount': 500, 'max_payouts': 6}
- Min profit for a qualifying day: {'50K': 250, '100K': 300, '150K': 350}
- Activation fee: {'50K': 139, '100K': 149, '150K': 159}

Payout caps:

| size | #1 | #2 | #3 | #4 | #5 | #6 |
|---|---|---|---|---|---|---|
| 50K | 1500 | 1500 | 2000 | 2500 | 2500 | 3000 |
| 100K | 2000 | 2500 | 2500 | 3000 | 4000 | 4000 |
| 150K | 2500 | 3000 | 3000 | 3000 | 4000 | 5000 |

## INTRADAY plan

### Evaluation

| size | balance | target | drawdown | dll | max_contracts | price |
|---|---|---|---|---|---|---|
| 25K | 25000 | 1500 | 1000 | 0 | 4 | 167 |
| 50K | 50000 | 3000 | 2000 | 0 | 6 | 249 |
| 150K | 150000 | 9000 | 4000 | 0 | 12 | 599 |

- Drawdown trails: **intraday**; stops trailing at the target balance
- Access: 30 calendar days; min trading days: 0; DLL pauses the day: False

### Performance account

- Drawdown trails **intraday**, locks at start + $100
- Payouts: {'min_days': 5, 'consistency': 0.5, 'min_amount': 500, 'max_payouts': 6}
- Min profit for a qualifying day: {'50K': 200, '100K': 250, '150K': 300}
- Activation fee: {'50K': 59}

Payout caps:

| size | #1 | #2 | #3 | #4 | #5 | #6 |
|---|---|---|---|---|---|---|
| 50K | 1500 | 2000 | 2500 | 2500 | 3000 | 3000 |
| 100K | 2000 | 2500 | 3000 | 3000 | 4000 | 4000 |
| 150K | 2500 | 3000 | 3000 | 4000 | 4000 | 5000 |

## PA scaling tiers

**50K**

| profit_from | max_contracts | dll |
|---|---|---|
| 0 | 2 | 1000 |
| 1500 | 3 | 1000 |
| 3000 | 4 | 2000 |
| 6000 | 4 | 3000 |

**100K**

| profit_from | max_contracts | dll |
|---|---|---|
| 0 | 3 | 1750 |
| 2000 | 4 | 1750 |
| 3000 | 5 | 1750 |
| 5000 | 6 | 2500 |
| 10000 | 6 | 3500 |

**150K**

| profit_from | max_contracts | dll |
|---|---|---|
| 0 | 4 | 2500 |
| 2000 | 5 | 2500 |
| 3000 | 7 | 2500 |
| 5000 | 10 | 3000 |
| 10000 | 10 | 4000 |

## Commissions (per side)

{'standard': 1.99, 'micro': 0.51}

## Open questions / modelling assumptions

- Product JSON carries consistency_rule_percentage=30 and max_eval_daily_profit_percent=30 on evals, but the help pages say evals have no consistency rule. We follow the help pages and REPORT each strategy's largest-day share of eval profit so a 30% cap can be checked.
- Eval pass is modelled as the session CLOSE balance >= target (the pass is reviewed at 16:59:59 ET). Touching the target intraday and giving it back does not count.
- Payout qualifying days (5) and the consistency window are assumed to reset after each approved payout (the pages describe weekly payouts and 'since your last approved payout').
- Payouts are assumed to be requested as soon as eligible, for the largest allowed amount.
- PA activation fee = pa_features.price in the product JSON; the help pages give no amount.
- The proxy has no bars 16:15-17:00 ET, so strategies must be flat by 16:10 ET (stricter than Apex).

## Sources

- `eod_eval`: https://apextraderfunding.com/help-center/eod-trailing-drawdown-accounts/eod-evaluations/ (capture 20260325193319) 
- `eod_drawdown`: https://apextraderfunding.com/help-center/eod-trailing-drawdown-accounts/eod-drawdown-explained/ (capture 20260325193331) 
- `eod_pa`: https://apextraderfunding.com/help-center/eod-trailing-drawdown-accounts/eod-performance-accounts-pa/ (capture 20260325193329) 
- `eod_payouts`: https://apextraderfunding.com/help-center/eod-trailing-drawdown-accounts/eod-payouts/ (capture 20260504202951) 
- `intraday_eval`: https://apextraderfunding.com/help-center/intraday-trailing-drawdown-accounts/intraday-trailing-drawdown-evaluations/ (capture 20260325193329) 
- `intraday_drawdown`: https://apextraderfunding.com/help-center/intraday-trailing-drawdown-accounts/intraday-trailing-drawdown-explained/ (capture 20260527202906) 
- `intraday_pa`: https://apextraderfunding.com/help-center/intraday-trailing-drawdown-accounts/intraday-trailing-drawdown-performance-accounts-pa/ (capture 20260325193329) 
- `intraday_payouts`: https://apextraderfunding.com/help-center/intraday-trailing-drawdown-accounts/intraday-trailing-drawdown-payouts/ (capture 20260506000251) 
- `scaling`: https://apextraderfunding.com/help-center/additional-helpful-items/scaling-levels-pa-explained/ (capture 20260325193407) 
- `consistency`: https://apextraderfunding.com/help-center/additional-helpful-items/50-consistency-requirement/ (capture 20260630155758) 
- `fees_access`: https://apextraderfunding.com/help-center/billing/evaluation-plan-fees-and-access-explained/ (capture 20260325193331) 
- `pricing_json`: https://apextraderfunding.com/?picker_type=eod-trail&picker_vendor=Wealthcharts&picker_balance=150k (capture 20260812233313) embedded product JSON: eval `price`, PA `pa_features.price`
- `commissions`: https://apextraderfunding.com/help-center/rithmic/rithmic-commissions-instruments/ (capture search-snippet 2026-09-25) NQ/ES $1.99/side confirmed; micro $0.51/side from epicctrader.com (2026-07-30), second-hand
