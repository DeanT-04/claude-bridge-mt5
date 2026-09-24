//+------------------------------------------------------------------+
//| QB_Donchian: channel breakout with ATR stop/target and time exit. |
//| Twin of research/strategies/donchian.py — keep the rules in sync. |
//|  - signals use closed bar [1]; entries at the open of bar [0]     |
//|  - long if close[1] > highest high of bars [2..N+1]               |
//|  - short if close[1] < lowest low of bars [2..N+1]                |
//|  - SL = k_sl*ATR[1], TP = k_tp*ATR[1]; ATR = SMA of true range    |
//|  - close at bar open once held >= InpMaxBars bars                 |
//|  - only enter when the new bar's server hour is in the session    |
//+------------------------------------------------------------------+
#property strict
#property version "1.00"

#include <Trade\Trade.mqh>
#include <QB\Risk.mqh>
#include <QB\TradeLogger.mqh>
#include <QB\Tester.mqh>

input int    InpChannel      = 20;
input int    InpAtrPeriod    = 14;
input double InpSlAtr        = 2.0;
input double InpTpAtr        = 3.0;
input int    InpMaxBars      = 48;
input int    InpSessionStart = 7;    // server hour, inclusive
input int    InpSessionEnd   = 20;   // server hour, exclusive
input double InpRiskPct      = 1.0;
input long   InpMagic        = 71001;

CTrade   g_trade;
int      g_atr = INVALID_HANDLE;
datetime g_last_bar = 0;

int OnInit()
{
   if(InpChannel < 2 || InpAtrPeriod < 1 || InpSlAtr <= 0 || InpTpAtr <= 0) return INIT_PARAMETERS_INCORRECT;
   g_atr = iATR(_Symbol, _Period, InpAtrPeriod);
   if(g_atr == INVALID_HANDLE) return INIT_FAILED;
   g_trade.SetExpertMagicNumber(InpMagic);
   g_trade.SetDeviationInPoints(20);
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   QB_DumpTrades();
   if(g_atr != INVALID_HANDLE) IndicatorRelease(g_atr);
}

double OnTester() { return QB_OnTesterScore(); }

bool InSession(datetime t)
{
   MqlDateTime dt; TimeToStruct(t, dt);
   if(InpSessionStart <= InpSessionEnd) return dt.hour >= InpSessionStart && dt.hour < InpSessionEnd;
   return dt.hour >= InpSessionStart || dt.hour < InpSessionEnd;   // wraps midnight
}

bool HasPosition(ulong &ticket)
{
   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      ulong t = PositionGetTicket(i);
      if(PositionGetString(POSITION_SYMBOL) == _Symbol && PositionGetInteger(POSITION_MAGIC) == InpMagic)
      { ticket = t; return true; }
   }
   return false;
}

void OnTick()
{
   datetime bar = iTime(_Symbol, _Period, 0);
   if(bar == g_last_bar) return;
   g_last_bar = bar;

   ulong ticket;
   if(HasPosition(ticket))
   {
      datetime opened = (datetime)PositionGetInteger(POSITION_TIME);
      int held = iBarShift(_Symbol, _Period, opened) ;   // bars since the entry bar
      if(held >= InpMaxBars) g_trade.PositionClose(ticket);
      else return;
   }
   if(!InSession(bar)) return;

   int hh = iHighest(_Symbol, _Period, MODE_HIGH, InpChannel, 2);
   int ll = iLowest(_Symbol, _Period, MODE_LOW, InpChannel, 2);
   if(hh < 0 || ll < 0) return;
   double upper = iHigh(_Symbol, _Period, hh);
   double lower = iLow(_Symbol, _Period, ll);
   double close1 = iClose(_Symbol, _Period, 1);
   double atr[1];
   if(CopyBuffer(g_atr, 0, 1, 1, atr) != 1 || atr[0] <= 0) return;

   int dir = close1 > upper ? 1 : (close1 < lower ? -1 : 0);
   if(dir == 0) return;

   double sl_dist = InpSlAtr * atr[0];
   double tp_dist = InpTpAtr * atr[0];
   double lots = QB_LotsForRisk(_Symbol, InpRiskPct, sl_dist);
   if(lots <= 0) return;

   int digits = (int)SymbolInfoInteger(_Symbol, SYMBOL_DIGITS);
   if(dir > 0)
   {
      double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
      g_trade.Buy(lots, _Symbol, ask, NormalizeDouble(ask - sl_dist, digits), NormalizeDouble(ask + tp_dist, digits));
   }
   else
   {
      double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
      g_trade.Sell(lots, _Symbol, bid, NormalizeDouble(bid + sl_dist, digits), NormalizeDouble(bid - tp_dist, digits));
   }
}
