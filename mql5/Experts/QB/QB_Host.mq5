//+------------------------------------------------------------------+
//| QB_Host: portfolio host. Attach once to any chart; it trades     |
//| every sleeve listed in Common\Files\QB\<InpConfig> and reloads    |
//| the file whenever it changes.                                     |
//|                                                                   |
//| Each sleeve = one signal family on one symbol/timeframe, with     |
//| execution identical to QB_Rules (and research/engine.py).         |
//|                                                                   |
//| Safety enforced here, independent of Claude or the bridge:        |
//|  - config account=demo|live must match the account's trade mode  |
//|  - enabled=0 closes every QB position and stops trading           |
//|  - daily loss limit: close all, pause until the next server day   |
//|  - total drawdown from peak: close all, halt until reset_halt     |
//|  - max open risk (sum of sleeve risk % with an open position)     |
//|  - per-sleeve max spread filter                                   |
//+------------------------------------------------------------------+
#property strict
#property version "1.00"

#include <Trade\Trade.mqh>
#include <QB\Risk.mqh>
#include <QB\Signals.mqh>
#include <QB\Execution.mqh>

input string InpConfig    = "portfolio_demo.cfg";  // file in Common\Files\QB
input long   InpMagicBase = 900000;                 // sleeve magic = base + sleeve id
input int    InpTimerSec  = 1;

#define QB_MAGIC_SPAN 100000

//+------------------------------------------------------------------+
class CSleeve
{
public:
   int             id;
   string          sym;
   ENUM_TIMEFRAMES tf;
   ENUM_QB_FAMILY  fam;
   double          risk;          // % of (scaled) equity per trade
   int             atr_period;
   double          sl_atr, tp_atr;
   int             max_bars, s_start, s_end;
   double          max_spread;    // points; 0 = no filter
   QBSignalParams  sp;
   CQBSignal      *sig;
   int             atr;
   datetime        last_bar;
   long            magic;
   string          error;
   QBPending       pend;

   CSleeve() : sig(NULL), atr(INVALID_HANDLE), last_bar(0), risk(0), max_spread(0),
               atr_period(14), sl_atr(2), tp_atr(3), max_bars(24), s_start(0), s_end(24), error("")
   {
      sp.channel = 20; sp.fast = 20; sp.slow = 100; sp.rsi_period = 14; sp.rsi_lo = 30; sp.rsi_hi = 70;
      sp.bb_period = 20; sp.bb_dev = 2.0; sp.or_start = 8; sp.or_hours = 2; sp.kc_period = 20;
      sp.kc_mult = 1.5; sp.entry_hour = 10; sp.lookback = 4;
      sp.trig = 0; sp.trig_p1 = 20; sp.trig_p2 = 2.0; sp.invert = 0;
      sp.f1 = 0; sp.f1_p1 = 100; sp.f1_p2 = 1.0; sp.f2 = 0; sp.f2_p1 = 100; sp.f2_p2 = 1.0;
      sp.ml_thr = 0.56; sp.ml_model = "";
   }
   ~CSleeve() { Release(); }

   void Release()
   {
      if(sig != NULL) { delete sig; sig = NULL; }
      if(atr != INVALID_HANDLE) { IndicatorRelease(atr); atr = INVALID_HANDLE; }
   }

   bool Init()
   {
      if(!SymbolSelect(sym, true)) { error = "unknown symbol"; return false; }
      sig = QB_CreateSignal(fam);
      if(sig == NULL || !sig.Init(sym, tf, sp)) { error = "signal init failed"; return false; }
      atr = iATR(sym, tf, atr_period);
      if(atr == INVALID_HANDLE) { error = "atr init failed"; return false; }
      last_bar = iTime(sym, tf, 0);   // never act on a bar that opened before we loaded
      return true;
   }
};

CTrade    g_trade;
CSleeve  *g_sleeves[];
string    g_path;
datetime  g_cfg_mtime = 0;
string    g_gv;                        // global-variable prefix
// config
int       g_version = 0;
bool      g_enabled = false;
string    g_account = "";
double    g_scale = 1.0, g_max_daily = 0, g_max_dd = 0, g_max_open = 0;
int       g_reset_halt = 0;
// prop-firm rules (all optional; 0/"" = off)
double    g_prop_initial = 0;          // limits become % of this initial balance
string    g_daily_basis = "equity";    // start-of-day reference: balance | equity | max
string    g_daily_ref = "initial";     // daily limit is % of: initial (prop_initial_balance) | baseline (day start)
string    g_dd_mode = "trailing";      // trailing (from peak) | static (from prop_initial_balance)
string    g_trail_basis = "equity";    // trailing peak: equity | balance | eod_balance (end-of-day high)
int       g_trail_lock = 0;            // 1 = the trailing floor stops rising at prop_initial_balance
int       g_weekend_flat_hour = 0;     // Friday server hour to flatten; blocks entries until Monday
int       g_news_min = 0;              // no entries within +/- N min of high-impact news
// state
string    g_error = "";
datetime  g_last_status = 0;

//+------------------------------------------------------------------+
ENUM_TIMEFRAMES TfFromString(const string s)
{
   if(s == "M1")  return PERIOD_M1;  if(s == "M5")  return PERIOD_M5;
   if(s == "M15") return PERIOD_M15; if(s == "M30") return PERIOD_M30;
   if(s == "H1")  return PERIOD_H1;  if(s == "H4")  return PERIOD_H4;
   if(s == "D1")  return PERIOD_D1;
   return PERIOD_CURRENT;
}

string TfToString(const ENUM_TIMEFRAMES tf)
{
   switch(tf)
   {
      case PERIOD_M1: return "M1"; case PERIOD_M5: return "M5"; case PERIOD_M15: return "M15";
      case PERIOD_M30: return "M30"; case PERIOD_H1: return "H1"; case PERIOD_H4: return "H4";
      case PERIOD_D1: return "D1";
   }
   return "?";
}

void SetSleeveField(CSleeve &s, const string k, const string v)
{
   if(k == "id") s.id = (int)StringToInteger(v);
   else if(k == "family" || k == "InpFamily") s.fam = (ENUM_QB_FAMILY)StringToInteger(v);
   else if(k == "symbol") s.sym = v;
   else if(k == "tf") s.tf = TfFromString(v);
   else if(k == "risk") s.risk = StringToDouble(v);
   else if(k == "max_spread") s.max_spread = StringToDouble(v);
   else if(k == "InpAtrPeriod") s.atr_period = (int)StringToInteger(v);
   else if(k == "InpSlAtr") s.sl_atr = StringToDouble(v);
   else if(k == "InpTpAtr") s.tp_atr = StringToDouble(v);
   else if(k == "InpMaxBars") s.max_bars = (int)StringToInteger(v);
   else if(k == "InpSessionStart") s.s_start = (int)StringToInteger(v);
   else if(k == "InpSessionEnd") s.s_end = (int)StringToInteger(v);
   else if(k == "InpChannel") s.sp.channel = (int)StringToInteger(v);
   else if(k == "InpFast") s.sp.fast = (int)StringToInteger(v);
   else if(k == "InpSlow") s.sp.slow = (int)StringToInteger(v);
   else if(k == "InpRsiPeriod") s.sp.rsi_period = (int)StringToInteger(v);
   else if(k == "InpRsiLo") s.sp.rsi_lo = StringToDouble(v);
   else if(k == "InpRsiHi") s.sp.rsi_hi = StringToDouble(v);
   else if(k == "InpBbPeriod") s.sp.bb_period = (int)StringToInteger(v);
   else if(k == "InpBbDev") s.sp.bb_dev = StringToDouble(v);
   else if(k == "InpOrStart") s.sp.or_start = (int)StringToInteger(v);
   else if(k == "InpOrHours") s.sp.or_hours = (int)StringToInteger(v);
   else if(k == "InpKcPeriod") s.sp.kc_period = (int)StringToInteger(v);
   else if(k == "InpKcMult") s.sp.kc_mult = StringToDouble(v);
   else if(k == "InpEntryHour") s.sp.entry_hour = (int)StringToInteger(v);
   else if(k == "InpLookback") s.sp.lookback = (int)StringToInteger(v);
   else if(k == "InpTrig") s.sp.trig = (int)StringToInteger(v);
   else if(k == "InpTrigP1") s.sp.trig_p1 = (int)StringToInteger(v);
   else if(k == "InpTrigP2") s.sp.trig_p2 = StringToDouble(v);
   else if(k == "InpInvert") s.sp.invert = (int)StringToInteger(v);
   else if(k == "InpF1") s.sp.f1 = (int)StringToInteger(v);
   else if(k == "InpF1P1") s.sp.f1_p1 = (int)StringToInteger(v);
   else if(k == "InpF1P2") s.sp.f1_p2 = StringToDouble(v);
   else if(k == "InpF2") s.sp.f2 = (int)StringToInteger(v);
   else if(k == "InpF2P1") s.sp.f2_p1 = (int)StringToInteger(v);
   else if(k == "InpF2P2") s.sp.f2_p2 = StringToDouble(v);
   else if(k == "InpMlThr") s.sp.ml_thr = StringToDouble(v);
   else if(k == "InpMlModel") s.sp.ml_model = v;
}

void ClearSleeves()
{
   for(int i = 0; i < ArraySize(g_sleeves); i++) if(g_sleeves[i] != NULL) delete g_sleeves[i];
   ArrayResize(g_sleeves, 0);
}

bool LoadConfig()
{
   int h = FileOpen(g_path, FILE_READ | FILE_TXT | FILE_ANSI | FILE_COMMON);
   if(h == INVALID_HANDLE) { g_error = "config not found: " + g_path; g_enabled = false; return false; }
   ClearSleeves();
   g_version = 0; g_enabled = false; g_account = ""; g_scale = 1.0;
   g_max_daily = 0; g_max_dd = 0; g_max_open = 0; g_reset_halt = 0; g_error = "";
   g_prop_initial = 0; g_daily_basis = "equity"; g_dd_mode = "trailing"; g_weekend_flat_hour = 0; g_news_min = 0;
   g_daily_ref = "initial"; g_trail_basis = "equity"; g_trail_lock = 0;
   while(!FileIsEnding(h))
   {
      string line = FileReadString(h);
      StringTrimLeft(line); StringTrimRight(line);
      if(line == "" || StringGetCharacter(line, 0) == '#') continue;
      int eq = StringFind(line, "=");
      if(eq < 0) continue;
      string key = StringSubstr(line, 0, eq), val = StringSubstr(line, eq + 1);
      if(key == "version") g_version = (int)StringToInteger(val);
      else if(key == "enabled") g_enabled = StringToInteger(val) != 0;
      else if(key == "account") g_account = val;
      else if(key == "balance_scale") g_scale = StringToDouble(val);
      else if(key == "max_daily_loss_pct") g_max_daily = StringToDouble(val);
      else if(key == "max_total_dd_pct") g_max_dd = StringToDouble(val);
      else if(key == "max_open_risk_pct") g_max_open = StringToDouble(val);
      else if(key == "reset_halt") g_reset_halt = (int)StringToInteger(val);
      else if(key == "prop_initial_balance") g_prop_initial = StringToDouble(val);
      else if(key == "daily_loss_basis") g_daily_basis = val;
      else if(key == "max_dd_mode") g_dd_mode = val;
      else if(key == "daily_loss_ref") g_daily_ref = val;
      else if(key == "trailing_basis") g_trail_basis = val;
      else if(key == "trailing_lock") g_trail_lock = (int)StringToInteger(val);
      else if(key == "weekend_flat_hour") g_weekend_flat_hour = (int)StringToInteger(val);
      else if(key == "news_blackout_min") g_news_min = (int)StringToInteger(val);
      else if(key == "sleeve")
      {
         CSleeve *s = new CSleeve();
         string parts[];
         int n = StringSplit(val, ';', parts);
         for(int i = 0; i < n; i++)
         {
            int c = StringFind(parts[i], ":");
            if(c > 0) SetSleeveField(s, StringSubstr(parts[i], 0, c), StringSubstr(parts[i], c + 1));
         }
         s.magic = InpMagicBase + s.id;
         if(!s.Init()) Print("QB_Host: sleeve ", s.id, " ", s.sym, " disabled: ", s.error);
         int k = ArraySize(g_sleeves);
         ArrayResize(g_sleeves, k + 1);
         g_sleeves[k] = s;
      }
   }
   FileClose(h);

   // Refuse a config written for the other kind of account.
   bool is_demo = AccountInfoInteger(ACCOUNT_TRADE_MODE) == ACCOUNT_TRADE_MODE_DEMO;
   if((g_account == "demo" && !is_demo) || (g_account == "live" && is_demo) || g_account == "")
   {
      g_error = "account mismatch: config account=" + g_account + " but terminal is " + (is_demo ? "demo" : "live");
      g_enabled = false;
   }
   if(g_scale <= 0 || g_scale > 10) { g_error = "balance_scale out of range"; g_enabled = false; }

   // Reset a drawdown halt when the config carries a newer reset_halt counter.
   if(g_reset_halt > (int)GvGet("reset", 0))
   {
      GvSet("reset", g_reset_halt);
      GvSet("halted", 0);
      GvSet("peak", AccountInfoDouble(ACCOUNT_EQUITY));
   }
   CloseOrphans();
   PrintFormat("QB_Host: loaded %s v%d, %d sleeves, enabled=%d %s", g_path, g_version,
               ArraySize(g_sleeves), g_enabled, g_error);
   return true;
}

//+------------------------------------------------------------------+
double GvGet(const string k, const double def)
{
   string n = g_gv + k;
   return GlobalVariableCheck(n) ? GlobalVariableGet(n) : def;
}
void GvSet(const string k, const double v) { GlobalVariableSet(g_gv + k, v); }

bool IsQbMagic(const long m) { return m >= InpMagicBase && m < InpMagicBase + QB_MAGIC_SPAN; }

CSleeve *SleeveByMagic(const long m)
{
   for(int i = 0; i < ArraySize(g_sleeves); i++) if(g_sleeves[i].magic == m) return g_sleeves[i];
   return NULL;
}

void CloseAll(const string why)
{
   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      ulong t = PositionGetTicket(i);
      if(t == 0 || !IsQbMagic(PositionGetInteger(POSITION_MAGIC))) continue;
      g_trade.SetExpertMagicNumber(PositionGetInteger(POSITION_MAGIC));
      if(!g_trade.PositionClose(t)) Print("QB_Host: close failed ", t, " ", g_trade.ResultRetcodeDescription());
   }
   if(why != "") Print("QB_Host: closed all positions: ", why);
}

// Positions whose sleeve is no longer in the config are closed.
void CloseOrphans()
{
   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      ulong t = PositionGetTicket(i);
      long m = PositionGetInteger(POSITION_MAGIC);
      if(t == 0 || !IsQbMagic(m) || SleeveByMagic(m) != NULL) continue;
      g_trade.PositionClose(t);
      Print("QB_Host: closed orphan position ", t, " magic ", m);
   }
}

bool PositionFor(CSleeve *s, ulong &ticket)
{
   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      ulong t = PositionGetTicket(i);
      if(t != 0 && PositionGetInteger(POSITION_MAGIC) == s.magic && PositionGetString(POSITION_SYMBOL) == s.sym)
      { ticket = t; return true; }
   }
   return false;
}

double OpenRiskPct()
{
   double r = 0; ulong t;
   for(int i = 0; i < ArraySize(g_sleeves); i++) if(PositionFor(g_sleeves[i], t)) r += g_sleeves[i].risk;
   return r;
}

//+------------------------------------------------------------------+
// Returns true when trading may continue this tick.
bool RiskGate()
{
   double eq = AccountInfoDouble(ACCOUNT_EQUITY), bal = AccountInfoDouble(ACCOUNT_BALANCE);
   MqlDateTime now; TimeToStruct(TimeTradeServer(), now);
   double today = now.year * 1000 + now.day_of_year;
   if(GvGet("day", 0) != today)
   {
      double sod = g_daily_basis == "balance" ? bal : (g_daily_basis == "max" ? MathMax(bal, eq) : eq);
      GvSet("day", today); GvSet("day_start", sod); GvSet("halted_today", 0);
      GvSet("peak_eod", MathMax(GvGet("peak_eod", g_prop_initial > 0 ? g_prop_initial : bal), bal));
   }
   double peak = MathMax(GvGet("peak", eq), eq);
   GvSet("peak", peak);
   double peak_bal = MathMax(GvGet("peak_bal", bal), bal);
   GvSet("peak_bal", peak_bal);

   if(!g_enabled)
   {
      if(g_error == "") CloseAll("");   // explicit disable closes everything; errors just stop entries
      return false;
   }
   if(GvGet("halted", 0) > 0) return false;
   if(GvGet("halted_today", 0) > 0) return false;

   double day_start = GvGet("day_start", eq);
   // Prop rules measure limits as % of the initial balance (unless the firm uses the day's own
   // baseline); otherwise % of the reference itself.
   double daily_base = (g_prop_initial > 0 && g_daily_ref != "baseline") ? g_prop_initial : day_start;
   if(g_max_daily > 0 && eq <= day_start - daily_base * g_max_daily / 100.0)
   {
      GvSet("halted_today", 1);
      CloseAll(StringFormat("daily loss limit %.1f%% hit", g_max_daily));
      return false;
   }
   double floor;
   if(g_dd_mode == "static" && g_prop_initial > 0) floor = g_prop_initial * (1 - g_max_dd / 100.0);
   else
   {
      double top = peak;
      if(g_trail_basis == "balance") top = peak_bal;
      else if(g_trail_basis == "eod_balance") top = MathMax(GvGet("peak_eod", g_prop_initial), g_prop_initial);
      floor = top - (g_prop_initial > 0 ? g_prop_initial : top) * g_max_dd / 100.0;
      if(g_trail_lock && g_prop_initial > 0) floor = MathMin(floor, g_prop_initial);
   }
   if(g_max_dd > 0 && eq <= floor)
   {
      GvSet("halted", 1);
      CloseAll(StringFormat("total drawdown limit %.1f%% (%s) hit; halted until reset_halt", g_max_dd, g_dd_mode));
      return false;
   }
   if(g_weekend_flat_hour > 0 && WeekendWindow(now))
   {
      CloseAll("");                         // no positions over the weekend
      return false;
   }
   return true;
}

// From Friday weekend_flat_hour until Monday 00:00 server time.
bool WeekendWindow(const MqlDateTime &now)
{
   return (now.day_of_week == 5 && now.hour >= g_weekend_flat_hour) || now.day_of_week == 6 || now.day_of_week == 0;
}

// High-impact calendar event for either of the symbol's currencies within +/- g_news_min minutes.
bool NewsNear(const string sym)
{
   if(g_news_min <= 0 || MQLInfoInteger(MQL_TESTER)) return false;   // calendar unavailable in tester
   datetime t = TimeTradeServer();
   string ccys[2];
   ccys[0] = SymbolInfoString(sym, SYMBOL_CURRENCY_BASE);
   ccys[1] = SymbolInfoString(sym, SYMBOL_CURRENCY_PROFIT);
   for(int c = 0; c < 2; c++)
   {
      if(ccys[c] == "" || (c == 1 && ccys[1] == ccys[0])) continue;
      MqlCalendarValue vals[];
      if(CalendarValueHistory(vals, t - g_news_min * 60, t + g_news_min * 60, NULL, ccys[c]) <= 0) continue;
      for(int i = 0; i < ArraySize(vals); i++)
      {
         MqlCalendarEvent ev;
         if(CalendarEventById(vals[i].event_id, ev) && ev.importance == CALENDAR_IMPORTANCE_HIGH) return true;
      }
   }
   return false;
}

bool InSession(CSleeve *s, datetime t)
{
   MqlDateTime dt; TimeToStruct(t, dt);
   if(s.s_start <= s.s_end) return dt.hour >= s.s_start && dt.hour < s.s_end;
   return dt.hour >= s.s_start || dt.hour < s.s_end;
}

void ProcessSleeve(CSleeve *s, const bool may_enter)
{
   if(s.sig == NULL) return;
   datetime bar = iTime(s.sym, s.tf, 0);
   if(bar == 0) return;
   g_trade.SetExpertMagicNumber(s.magic);
   if(bar != s.last_bar)
   {
      s.last_bar = bar;
      QB_PendingReset(s.pend, bar);
      DecideSleeve(s, bar, may_enter);
   }
   if(!may_enter) s.pend.dir = 0;             // a halt mid-bar cancels a pending entry
   ulong t;
   QB_RunPending(g_trade, s.sym, s.pend, bar, s.pend.close_ticket == 0 && !PositionFor(s, t));
}

// Decisions are made once per bar; Execution.mqh retries them within the bar if rejected.
void DecideSleeve(CSleeve *s, const datetime bar, const bool may_enter)
{
   ulong ticket;
   if(PositionFor(s, ticket))
   {
      int held = iBarShift(s.sym, s.tf, (datetime)PositionGetInteger(POSITION_TIME));
      if(held < s.max_bars) return;
      s.pend.close_ticket = ticket;
   }
   if(!may_enter || !InSession(s, bar)) return;
   int dir = s.sig.Direction();
   if(dir == 0) return;
   double open_risk = OpenRiskPct() - (s.pend.close_ticket != 0 ? s.risk : 0);
   if(g_max_open > 0 && open_risk + s.risk > g_max_open + 1e-9) return;
   if(s.max_spread > 0 && SymbolInfoInteger(s.sym, SYMBOL_SPREAD) > s.max_spread) return;
   if(NewsNear(s.sym)) return;

   double atr[1];
   if(CopyBuffer(s.atr, 0, 1, 1, atr) != 1 || atr[0] <= 0) return;
   double sl_dist = s.sl_atr * atr[0];
   double lots = QB_LotsForRiskScaled(s.sym, s.risk, sl_dist, g_scale);
   if(lots <= 0) return;
   s.pend.dir = dir;
   s.pend.sl_dist = sl_dist;
   s.pend.tp_dist = s.tp_atr * atr[0];
   s.pend.lots = lots;
   s.pend.comment = StringFormat("QB s%d f%d", s.id, (int)s.fam);
}

//+------------------------------------------------------------------+
string JsonEsc(string s) { StringReplace(s, "\\", "\\\\"); StringReplace(s, "\"", "\\\""); return s; }

void WriteStatus(const bool trading)
{
   string base = InpConfig;
   StringReplace(base, ".cfg", "");
   int h = FileOpen("QB\\host_status_" + base + ".json", FILE_WRITE | FILE_TXT | FILE_ANSI | FILE_COMMON);
   if(h == INVALID_HANDLE) return;
   bool is_demo = AccountInfoInteger(ACCOUNT_TRADE_MODE) == ACCOUNT_TRADE_MODE_DEMO;
   string js = StringFormat(
      "{\"time\":\"%s\",\"config\":\"%s\",\"version\":%d,\"enabled\":%s,\"trading\":%s,"
      "\"account_mode\":\"%s\",\"currency\":\"%s\",\"balance\":%.2f,\"equity\":%.2f,"
      "\"day_start\":%.2f,\"peak\":%.2f,\"halted\":%s,\"halted_today\":%s,"
      "\"algo_trading_allowed\":%s,\"skipped_minlot\":%d,\"open_risk_pct\":%.3f,\"error\":\"%s\",\"sleeves\":[",
      TimeToString(TimeTradeServer(), TIME_DATE | TIME_SECONDS), InpConfig, g_version,
      g_enabled ? "true" : "false", trading ? "true" : "false", is_demo ? "demo" : "live",
      AccountInfoString(ACCOUNT_CURRENCY), AccountInfoDouble(ACCOUNT_BALANCE), AccountInfoDouble(ACCOUNT_EQUITY),
      GvGet("day_start", 0), GvGet("peak", 0), GvGet("halted", 0) > 0 ? "true" : "false",
      GvGet("halted_today", 0) > 0 ? "true" : "false",
      (TerminalInfoInteger(TERMINAL_TRADE_ALLOWED) && MQLInfoInteger(MQL_TRADE_ALLOWED)) ? "true" : "false",
      g_qb_skipped_minlot, OpenRiskPct(), JsonEsc(g_error));
   for(int i = 0; i < ArraySize(g_sleeves); i++)
   {
      CSleeve *s = g_sleeves[i];
      ulong t; bool open = PositionFor(s, t);
      js += StringFormat("%s{\"id\":%d,\"symbol\":\"%s\",\"tf\":\"%s\",\"family\":%d,\"risk\":%.3f,"
                         "\"magic\":%I64d,\"open\":%s,\"error\":\"%s\"}",
                         i ? "," : "", s.id, s.sym, TfToString(s.tf), (int)s.fam, s.risk, s.magic,
                         open ? "true" : "false", JsonEsc(s.error));
   }
   js += "]}";
   FileWriteString(h, js);
   FileClose(h);
}

//+------------------------------------------------------------------+
int OnInit()
{
   g_path = "QB\\" + InpConfig;
   string base = InpConfig; StringReplace(base, ".cfg", "");
   g_gv = "QB_" + base + "_";
   g_trade.SetDeviationInPoints(20);
   LoadConfig();
   g_cfg_mtime = (datetime)FileGetInteger(g_path, FILE_MODIFY_DATE, true);
   EventSetTimer(InpTimerSec);
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   ClearSleeves();
}

void OnTimer()
{
   datetime m = (datetime)FileGetInteger(g_path, FILE_MODIFY_DATE, true);
   if(m != g_cfg_mtime) { g_cfg_mtime = m; LoadConfig(); }

   bool trading = RiskGate();
   for(int i = 0; i < ArraySize(g_sleeves); i++) ProcessSleeve(g_sleeves[i], trading);

   datetime now = TimeLocal();
   if(now - g_last_status >= 5) { WriteStatus(trading); g_last_status = now; }
}

void OnTick() {}
