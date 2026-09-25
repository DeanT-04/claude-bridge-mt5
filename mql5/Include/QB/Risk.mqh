//+------------------------------------------------------------------+
//| QB risk sizing: lots from risk % of equity and stop distance.     |
//+------------------------------------------------------------------+
#property strict

// Scale applied to equity before sizing (1.0 = size on the account's own equity).
input double InpBalanceScale = 1.0;

int g_qb_skipped_minlot = 0;   // trades skipped because min lot exceeds the risk cap

// Money lost per 1.0 lot if price moves `stop_distance` against the position.
double QB_LossPerLot(const string symbol, const double stop_distance)
{
   double tick_size  = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE);
   double tick_value = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_VALUE_LOSS);
   if(tick_value <= 0.0) tick_value = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_VALUE);
   if(tick_size <= 0.0 || tick_value <= 0.0) return 0.0;
   return stop_distance / tick_size * tick_value;
}

double QB_LotsForRiskScaled(const string symbol, const double risk_pct, const double stop_distance,
                            const double balance_scale)
{
   if(stop_distance <= 0.0) return 0.0;
   double vmin  = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN);
   double vstep = SymbolInfoDouble(symbol, SYMBOL_VOLUME_STEP);
   double vmax  = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX);
   double loss_per_lot = QB_LossPerLot(symbol, stop_distance);
   if(loss_per_lot <= 0.0 || vstep <= 0.0) return 0.0;

   double equity    = AccountInfoDouble(ACCOUNT_EQUITY) * balance_scale;
   double risk_cash = equity * risk_pct / 100.0;
   // small epsilon so 0.3/0.01 = 29.999... still floors to 30 steps
   double lots = MathFloor(risk_cash / loss_per_lot / vstep + 1e-9) * vstep;
   int    step_digits = (int)MathMax(0, MathCeil(-MathLog10(vstep)));
   lots = NormalizeDouble(lots, step_digits);

   if(lots < vmin)
   {
      // Refuse rather than silently over-risk: min lot would breach the cap.
      g_qb_skipped_minlot++;
      return 0.0;
   }
   return MathMin(lots, vmax);
}

double QB_LotsForRisk(const string symbol, const double risk_pct, const double stop_distance)
{
   return QB_LotsForRiskScaled(symbol, risk_pct, stop_distance, InpBalanceScale);
}
