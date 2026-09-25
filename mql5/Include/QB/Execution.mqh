//+------------------------------------------------------------------+
//| QB execution with retry. An entry or time-exit decided at a bar's |
//| open stays pending and is retried on later ticks of the SAME bar  |
//| when the server rejects it transiently (market closed at session  |
//| open, requote, price moved). Research assumes a fill in the bar   |
//| the decision was made, so the pending action expires at the next |
//| bar.                                                              |
//+------------------------------------------------------------------+
#property strict

#include <Trade\Trade.mqh>

struct QBPending
{
   datetime bar;          // bar the actions belong to
   int      dir;          // pending entry direction (0 = none)
   double   sl_dist, tp_dist, lots;
   ulong    close_ticket; // pending time-exit close (0 = none)
   string   comment;
};

void QB_PendingReset(QBPending &p, const datetime bar)
{
   p.bar = bar; p.dir = 0; p.sl_dist = 0; p.tp_dist = 0; p.lots = 0; p.close_ticket = 0; p.comment = "";
}

bool QB_Retryable(const uint rc)
{
   return rc == TRADE_RETCODE_MARKET_CLOSED || rc == TRADE_RETCODE_REQUOTE || rc == TRADE_RETCODE_PRICE_OFF ||
          rc == TRADE_RETCODE_PRICE_CHANGED || rc == TRADE_RETCODE_CONNECTION || rc == TRADE_RETCODE_TIMEOUT ||
          rc == TRADE_RETCODE_TOO_MANY_REQUESTS || rc == 0;
}

// Returns true when the action is finished (done, or failed permanently).
bool QB_TryOpen(CTrade &trade, const string sym, QBPending &p)
{
   if(p.dir == 0) return true;
   int digits = (int)SymbolInfoInteger(sym, SYMBOL_DIGITS);
   bool ok;
   if(p.dir > 0)
   {
      double ask = SymbolInfoDouble(sym, SYMBOL_ASK);
      if(ask <= 0) return false;
      ok = trade.Buy(p.lots, sym, ask, NormalizeDouble(ask - p.sl_dist, digits), NormalizeDouble(ask + p.tp_dist, digits), p.comment);
   }
   else
   {
      double bid = SymbolInfoDouble(sym, SYMBOL_BID);
      if(bid <= 0) return false;
      ok = trade.Sell(p.lots, sym, bid, NormalizeDouble(bid + p.sl_dist, digits), NormalizeDouble(bid - p.tp_dist, digits), p.comment);
   }
   uint rc = trade.ResultRetcode();
   if(ok && (rc == TRADE_RETCODE_DONE || rc == TRADE_RETCODE_PLACED || rc == TRADE_RETCODE_DONE_PARTIAL)) { p.dir = 0; return true; }
   if(QB_Retryable(rc)) return false;
   PrintFormat("QB: entry on %s abandoned: %s", sym, trade.ResultRetcodeDescription());
   p.dir = 0;
   return true;
}

bool QB_TryClose(CTrade &trade, QBPending &p)
{
   if(p.close_ticket == 0) return true;
   if(!PositionSelectByTicket(p.close_ticket)) { p.close_ticket = 0; return true; }   // already gone (SL/TP)
   bool ok = trade.PositionClose(p.close_ticket);
   uint rc = trade.ResultRetcode();
   if(ok && (rc == TRADE_RETCODE_DONE || rc == TRADE_RETCODE_PLACED)) { p.close_ticket = 0; return true; }
   if(QB_Retryable(rc)) return false;
   PrintFormat("QB: close of #%I64u abandoned: %s", p.close_ticket, trade.ResultRetcodeDescription());
   p.close_ticket = 0;
   return true;
}

// Run pending actions for the current bar: close first, then entry once flat.
void QB_RunPending(CTrade &trade, const string sym, QBPending &p, const datetime bar, const bool flat_after_close)
{
   if(p.bar != bar) return;
   if(!QB_TryClose(trade, p)) return;
   if(p.dir != 0 && flat_after_close) QB_TryOpen(trade, sym, p);
}
