//+------------------------------------------------------------------+
//| QB_Rules: one EA for every rule-based signal family.             |
//| Execution identical to QB_Donchian / research/engine.py:          |
//|  - new bar only; time exit first (held >= InpMaxBars)             |
//|  - entry at bar open when flat, in session and the signal fires   |
//|  - SL = InpSlAtr*ATR[1], TP = InpTpAtr*ATR[1] (ATR = SMA of TR)   |
//+------------------------------------------------------------------+
#property strict
#property version "1.00"

#include <Trade\Trade.mqh>
#include <QB\Risk.mqh>
#include <QB\TradeLogger.mqh>
#include <QB\Tester.mqh>
#include <QB\Signals.mqh>

input ENUM_QB_FAMILY InpFamily = QB_DONCHIAN;
// --- exits / session (common)
input int    InpAtrPeriod    = 14;
input double InpSlAtr        = 2.0;
input double InpTpAtr        = 3.0;
input int    InpMaxBars      = 24;
input int    InpSessionStart = 0;    // server hour, inclusive
input int    InpSessionEnd   = 24;   // server hour, exclusive
input double InpRiskPct      = 1.0;
input long   InpMagic        = 72000;
// --- family parameters (unused ones are ignored)
input int    InpChannel   = 20;
input int    InpFast      = 20;
input int    InpSlow      = 100;
input int    InpRsiPeriod = 14;
input double InpRsiLo     = 30;
input double InpRsiHi     = 70;
input int    InpBbPeriod  = 20;
input double InpBbDev     = 2.0;
input int    InpOrStart   = 8;
input int    InpOrHours   = 2;
input int    InpKcPeriod  = 20;
input double InpKcMult    = 1.5;
input int    InpEntryHour = 10;
input int    InpLookback  = 4;
// --- generic family (QB_GENERIC)
input int    InpTrig   = 0;
input int    InpTrigP1 = 20;
input double InpTrigP2 = 2.0;
input int    InpInvert = 0;
input int    InpF1     = 0;
input int    InpF1P1   = 100;
input double InpF1P2   = 1.0;
input int    InpF2     = 0;
input int    InpF2P1   = 100;
input double InpF2P2   = 1.0;

CTrade     g_trade;
CQBSignal *g_sig = NULL;
int        g_atr = INVALID_HANDLE;
datetime   g_last_bar = 0;

int OnInit()
{
   if(InpSlAtr <= 0 || InpTpAtr <= 0 || InpMaxBars < 1) return INIT_PARAMETERS_INCORRECT;
   QBSignalParams p;
   p.channel = InpChannel; p.fast = InpFast; p.slow = InpSlow;
   p.rsi_period = InpRsiPeriod; p.rsi_lo = InpRsiLo; p.rsi_hi = InpRsiHi;
   p.bb_period = InpBbPeriod; p.bb_dev = InpBbDev;
   p.or_start = InpOrStart; p.or_hours = InpOrHours;
   p.kc_period = InpKcPeriod; p.kc_mult = InpKcMult;
   p.entry_hour = InpEntryHour; p.lookback = InpLookback;
   p.trig = InpTrig; p.trig_p1 = InpTrigP1; p.trig_p2 = InpTrigP2; p.invert = InpInvert;
   p.f1 = InpF1; p.f1_p1 = InpF1P1; p.f1_p2 = InpF1P2;
   p.f2 = InpF2; p.f2_p1 = InpF2P1; p.f2_p2 = InpF2P2;
   g_sig = QB_CreateSignal(InpFamily);
   if(g_sig == NULL || !g_sig.Init(_Symbol, _Period, p)) return INIT_FAILED;
   g_atr = iATR(_Symbol, _Period, InpAtrPeriod);
   if(g_atr == INVALID_HANDLE) return INIT_FAILED;
   g_trade.SetExpertMagicNumber(InpMagic + (long)InpFamily);
   g_trade.SetDeviationInPoints(20);
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   QB_DumpTrades();
   if(g_sig != NULL) { delete g_sig; g_sig = NULL; }
   if(g_atr != INVALID_HANDLE) IndicatorRelease(g_atr);
}

double OnTester() { return QB_OnTesterScore(); }

bool InSession(datetime t)
{
   MqlDateTime dt; TimeToStruct(t, dt);
   if(InpSessionStart <= InpSessionEnd) return dt.hour >= InpSessionStart && dt.hour < InpSessionEnd;
   return dt.hour >= InpSessionStart || dt.hour < InpSessionEnd;
}

bool HasPosition(ulong &ticket)
{
   long magic = InpMagic + (long)InpFamily;
   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      ulong t = PositionGetTicket(i);
      if(PositionGetString(POSITION_SYMBOL) == _Symbol && PositionGetInteger(POSITION_MAGIC) == magic)
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
      int held = iBarShift(_Symbol, _Period, (datetime)PositionGetInteger(POSITION_TIME));
      if(held >= InpMaxBars) g_trade.PositionClose(ticket);
      else return;
   }
   if(!InSession(bar)) return;

   int dir = g_sig.Direction();
   if(dir == 0) return;
   double atr[1];
   if(CopyBuffer(g_atr, 0, 1, 1, atr) != 1 || atr[0] <= 0) return;

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
