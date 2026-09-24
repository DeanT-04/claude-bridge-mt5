//+------------------------------------------------------------------+
//| QB risk sizing: lots from risk % of equity and stop distance.     |
//+------------------------------------------------------------------+
#property strict

// Scale applied to balance before sizing. Used on the USD 1000 demo so a trade
// risks the same fraction the GBP 100 live account would (see settings.yaml).
input double InpBalanceScale = 1.0;

int g_qb_skipped_minlot = 0;   // trades skipped because min lot exceeds the risk cap

double QB_LotsForRisk(const string symbol, const double risk_pct, const double stop_distance)
{
   if(stop_distance <= 0.0) return 0.0;
   double tick_size  = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE);
   double tick_value = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_VALUE_LOSS);
   if(tick_value <= 0.0) tick_value = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_VALUE);
   double vmin  = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN);
   double vstep = SymbolInfoDouble(symbol, SYMBOL_VOLUME_STEP);
   double vmax  = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX);
   if(tick_size <= 0.0 || tick_value <= 0.0 || vstep <= 0.0) return 0.0;

   double equity   = AccountInfoDouble(ACCOUNT_EQUITY) * InpBalanceScale;
   double risk_cash = equity * risk_pct / 100.0;
   double loss_per_lot = stop_distance / tick_size * tick_value;
   double lots = MathFloor(risk_cash / loss_per_lot / vstep) * vstep;

   if(lots < vmin)
   {
      // Refuse rather than silently over-risk: min lot would breach the cap.
      g_qb_skipped_minlot++;
      return 0.0;
   }
   return MathMin(lots, vmax);
}
