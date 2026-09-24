//+------------------------------------------------------------------+
//| QB trade logger: dumps closed positions to Common\Files\QB\*.csv  |
//| One row per position (entry deal paired with its exit deals).     |
//+------------------------------------------------------------------+
#property strict

input string InpRunTag = "";   // bridge sets this per run; empty = no CSV

void QB_DumpTrades()
{
   if(InpRunTag == "" || MQLInfoInteger(MQL_OPTIMIZATION)) return;
   if(!HistorySelect(0, TimeCurrent() + 86400)) return;

   string fname = "QB\\trades_" + InpRunTag + ".csv";
   int h = FileOpen(fname, FILE_WRITE | FILE_CSV | FILE_ANSI | FILE_COMMON, ',');
   if(h == INVALID_HANDLE) { Print("QB: cannot open ", fname, " err=", GetLastError()); return; }
   FileWrite(h, "position_id", "symbol", "direction", "volume", "open_time", "open_price",
             "close_time", "close_price", "sl", "profit", "commission", "swap");

   int total = HistoryDealsTotal();
   for(int i = 0; i < total; i++)
   {
      ulong d = HistoryDealGetTicket(i);
      if(HistoryDealGetInteger(d, DEAL_ENTRY) != DEAL_ENTRY_IN) continue;
      long   pos   = HistoryDealGetInteger(d, DEAL_POSITION_ID);
      long   type  = HistoryDealGetInteger(d, DEAL_TYPE);
      double vol   = HistoryDealGetDouble(d, DEAL_VOLUME);
      double oprice = HistoryDealGetDouble(d, DEAL_PRICE);
      datetime otime = (datetime)HistoryDealGetInteger(d, DEAL_TIME);
      double sl    = HistoryDealGetDouble(d, DEAL_SL);
      double comm  = HistoryDealGetDouble(d, DEAL_COMMISSION);
      double profit = 0, swap = 0, cvol = 0, cval = 0;
      datetime ctime = 0;
      for(int j = i + 1; j < total; j++)
      {
         ulong e = HistoryDealGetTicket(j);
         if(HistoryDealGetInteger(e, DEAL_POSITION_ID) != pos) continue;
         long entry = HistoryDealGetInteger(e, DEAL_ENTRY);
         if(entry != DEAL_ENTRY_OUT && entry != DEAL_ENTRY_OUT_BY) continue;
         double v = HistoryDealGetDouble(e, DEAL_VOLUME);
         cvol += v;
         cval += v * HistoryDealGetDouble(e, DEAL_PRICE);
         profit += HistoryDealGetDouble(e, DEAL_PROFIT);
         swap   += HistoryDealGetDouble(e, DEAL_SWAP);
         comm   += HistoryDealGetDouble(e, DEAL_COMMISSION);
         ctime = (datetime)HistoryDealGetInteger(e, DEAL_TIME);
      }
      if(cvol <= 0) continue;   // still open at test end
      FileWrite(h, pos, HistoryDealGetString(d, DEAL_SYMBOL), type == DEAL_TYPE_BUY ? 1 : -1,
                DoubleToString(vol, 2), TimeToString(otime, TIME_DATE | TIME_SECONDS),
                DoubleToString(oprice, 8), TimeToString(ctime, TIME_DATE | TIME_SECONDS),
                DoubleToString(cval / cvol, 8), DoubleToString(sl, 8),
                DoubleToString(profit, 2), DoubleToString(comm, 2), DoubleToString(swap, 2));
   }
   FileClose(h);
}
