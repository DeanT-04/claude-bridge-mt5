//+------------------------------------------------------------------+
//| QB custom optimisation criterion (OptimizationCriterion=6).       |
//| Rewards consistency, penalises thin samples and deep drawdowns.   |
//+------------------------------------------------------------------+
#property strict

input int InpMinTradesForScore = 30;

double QB_OnTesterScore()
{
   double trades = TesterStatistics(STAT_TRADES);
   double pf     = TesterStatistics(STAT_PROFIT_FACTOR);
   double sharpe = TesterStatistics(STAT_SHARPE_RATIO);
   double ddpct  = TesterStatistics(STAT_EQUITY_DDREL_PERCENT);
   double net    = TesterStatistics(STAT_PROFIT);
   if(trades < InpMinTradesForScore || net <= 0.0) return 0.0;
   // Sharpe scaled by sample size, damped by drawdown; PF capped so a few lucky trades don't dominate.
   double score = sharpe * MathSqrt(trades) * MathMin(pf, 3.0) / (1.0 + ddpct / 20.0);
   return MathMax(score, 0.0);
}
