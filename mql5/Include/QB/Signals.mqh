//+------------------------------------------------------------------+
//| QB signal library. Each signal looks only at closed bars [1],[2] |
//| and returns +1 / -1 / 0 for an entry at the open of bar [0].     |
//| Python twins: research/strategies/*.py — keep rules in sync.     |
//+------------------------------------------------------------------+
#property strict

enum ENUM_QB_FAMILY
{
   QB_DONCHIAN      = 0,
   QB_EMA_PULLBACK  = 1,
   QB_RSI_REVERSION = 2,
   QB_BB_REVERSION  = 3,
   QB_ORB           = 4,
   QB_KELTNER       = 5,
   QB_HOUR_MOMENTUM = 6,
};

struct QBSignalParams
{
   int    channel;        // donchian
   int    fast, slow;     // ema pullback
   int    rsi_period; double rsi_lo, rsi_hi;
   int    bb_period;  double bb_dev;
   int    or_start, or_hours;
   int    kc_period;  double kc_mult;
   int    entry_hour, lookback;
};

class CQBSignal
{
public:
   virtual bool Init(const string sym, const ENUM_TIMEFRAMES tf, const QBSignalParams &p) { m_sym = sym; m_tf = tf; m_p = p; return true; }
   virtual int  Direction() { return 0; }
   virtual     ~CQBSignal() {}
protected:
   string          m_sym;
   ENUM_TIMEFRAMES m_tf;
   QBSignalParams  m_p;
   bool Buf(const int handle, const int buffer, const int shift, const int count, double &out[])
   {
      ArraySetAsSeries(out, true);
      return CopyBuffer(handle, buffer, shift, count, out) == count;
   }
};

//--- close[1] beyond the channel of bars [2..N+1]
class CSigDonchian : public CQBSignal
{
public:
   int Direction()
   {
      int hh = iHighest(m_sym, m_tf, MODE_HIGH, m_p.channel, 2);
      int ll = iLowest(m_sym, m_tf, MODE_LOW, m_p.channel, 2);
      if(hh < 0 || ll < 0) return 0;
      double c1 = iClose(m_sym, m_tf, 1);
      if(c1 > iHigh(m_sym, m_tf, hh)) return 1;
      if(c1 < iLow(m_sym, m_tf, ll)) return -1;
      return 0;
   }
};

//--- trend by EMA fast vs slow; bar [1] tags the fast EMA and closes back on the trend side
class CSigEmaPullback : public CQBSignal
{
   int m_f, m_s;
public:
   bool Init(const string sym, const ENUM_TIMEFRAMES tf, const QBSignalParams &p)
   {
      CQBSignal::Init(sym, tf, p);
      m_f = iMA(sym, tf, p.fast, 0, MODE_EMA, PRICE_CLOSE);
      m_s = iMA(sym, tf, p.slow, 0, MODE_EMA, PRICE_CLOSE);
      return m_f != INVALID_HANDLE && m_s != INVALID_HANDLE;
   }
   int Direction()
   {
      double f[], s[];
      if(!Buf(m_f, 0, 1, 1, f) || !Buf(m_s, 0, 1, 1, s)) return 0;
      double h1 = iHigh(m_sym, m_tf, 1), l1 = iLow(m_sym, m_tf, 1), c1 = iClose(m_sym, m_tf, 1);
      if(f[0] > s[0] && l1 <= f[0] && c1 > f[0]) return 1;
      if(f[0] < s[0] && h1 >= f[0] && c1 < f[0]) return -1;
      return 0;
   }
   ~CSigEmaPullback() { IndicatorRelease(m_f); IndicatorRelease(m_s); }
};

//--- RSI crosses back out of an extreme zone
class CSigRsiReversion : public CQBSignal
{
   int m_h;
public:
   bool Init(const string sym, const ENUM_TIMEFRAMES tf, const QBSignalParams &p)
   {
      CQBSignal::Init(sym, tf, p);
      m_h = iRSI(sym, tf, p.rsi_period, PRICE_CLOSE);
      return m_h != INVALID_HANDLE;
   }
   int Direction()
   {
      double r[];
      if(!Buf(m_h, 0, 1, 2, r)) return 0;       // r[0]=bar1, r[1]=bar2
      if(r[1] < m_p.rsi_lo && r[0] >= m_p.rsi_lo) return 1;
      if(r[1] > m_p.rsi_hi && r[0] <= m_p.rsi_hi) return -1;
      return 0;
   }
   ~CSigRsiReversion() { IndicatorRelease(m_h); }
};

//--- close re-enters the Bollinger band from outside
class CSigBbReversion : public CQBSignal
{
   int m_h;
public:
   bool Init(const string sym, const ENUM_TIMEFRAMES tf, const QBSignalParams &p)
   {
      CQBSignal::Init(sym, tf, p);
      m_h = iBands(sym, tf, p.bb_period, 0, p.bb_dev, PRICE_CLOSE);
      return m_h != INVALID_HANDLE;
   }
   int Direction()
   {
      double up[], lo[];
      if(!Buf(m_h, 1, 1, 2, up) || !Buf(m_h, 2, 1, 2, lo)) return 0;
      double c1 = iClose(m_sym, m_tf, 1), c2 = iClose(m_sym, m_tf, 2);
      if(c2 < lo[1] && c1 > lo[0]) return 1;
      if(c2 > up[1] && c1 < up[0]) return -1;
      return 0;
   }
   ~CSigBbReversion() { IndicatorRelease(m_h); }
};

//--- opening range: bars of today whose server hour is in [or_start, or_start+or_hours);
//    signal when close[1] crosses the range (close[2] was inside or equal)
class CSigOrb : public CQBSignal
{
public:
   int Direction()
   {
      datetime t1 = iTime(m_sym, m_tf, 1);
      MqlDateTime d1; TimeToStruct(t1, d1);
      if(d1.hour < m_p.or_start + m_p.or_hours) return 0;          // range not finished
      double hi = -DBL_MAX, lo = DBL_MAX; int n = 0;
      for(int k = 2; k < 400; k++)
      {
         datetime tk = iTime(m_sym, m_tf, k);
         if(tk == 0) break;
         MqlDateTime dk; TimeToStruct(tk, dk);
         if(dk.day_of_year != d1.day_of_year || dk.year != d1.year) break;
         if(dk.hour >= m_p.or_start && dk.hour < m_p.or_start + m_p.or_hours)
         { hi = MathMax(hi, iHigh(m_sym, m_tf, k)); lo = MathMin(lo, iLow(m_sym, m_tf, k)); n++; }
      }
      if(n == 0) return 0;
      MqlDateTime d2; TimeToStruct(iTime(m_sym, m_tf, 2), d2);
      if(d2.hour < m_p.or_start + m_p.or_hours) return 0;          // bar[2] still inside the range window
      double c1 = iClose(m_sym, m_tf, 1), c2 = iClose(m_sym, m_tf, 2);
      if(c1 > hi && c2 <= hi) return 1;
      if(c1 < lo && c2 >= lo) return -1;
      return 0;
   }
};

//--- close crosses outside EMA +/- mult*ATR (trend breakout)
class CSigKeltner : public CQBSignal
{
   int m_ma, m_atr;
public:
   bool Init(const string sym, const ENUM_TIMEFRAMES tf, const QBSignalParams &p)
   {
      CQBSignal::Init(sym, tf, p);
      m_ma  = iMA(sym, tf, p.kc_period, 0, MODE_EMA, PRICE_CLOSE);
      m_atr = iATR(sym, tf, p.kc_period);
      return m_ma != INVALID_HANDLE && m_atr != INVALID_HANDLE;
   }
   int Direction()
   {
      double ma[], at[];
      if(!Buf(m_ma, 0, 1, 2, ma) || !Buf(m_atr, 0, 1, 2, at)) return 0;
      double c1 = iClose(m_sym, m_tf, 1), c2 = iClose(m_sym, m_tf, 2);
      double up1 = ma[0] + m_p.kc_mult * at[0], up2 = ma[1] + m_p.kc_mult * at[1];
      double dn1 = ma[0] - m_p.kc_mult * at[0], dn2 = ma[1] - m_p.kc_mult * at[1];
      if(c1 > up1 && c2 <= up2) return 1;
      if(c1 < dn1 && c2 >= dn2) return -1;
      return 0;
   }
   ~CSigKeltner() { IndicatorRelease(m_ma); IndicatorRelease(m_atr); }
};

//--- at a fixed server hour, trade in the direction of the last `lookback` bars
class CSigHourMomentum : public CQBSignal
{
public:
   int Direction()
   {
      MqlDateTime d0; TimeToStruct(iTime(m_sym, m_tf, 0), d0);
      if(d0.hour != m_p.entry_hour || d0.min != 0) return 0;
      double c1 = iClose(m_sym, m_tf, 1), cn = iClose(m_sym, m_tf, 1 + m_p.lookback);
      if(cn <= 0) return 0;
      return c1 > cn ? 1 : (c1 < cn ? -1 : 0);
   }
};

CQBSignal *QB_CreateSignal(const ENUM_QB_FAMILY fam)
{
   switch(fam)
   {
      case QB_DONCHIAN:      return new CSigDonchian();
      case QB_EMA_PULLBACK:  return new CSigEmaPullback();
      case QB_RSI_REVERSION: return new CSigRsiReversion();
      case QB_BB_REVERSION:  return new CSigBbReversion();
      case QB_ORB:           return new CSigOrb();
      case QB_KELTNER:       return new CSigKeltner();
      case QB_HOUR_MOMENTUM: return new CSigHourMomentum();
   }
   return NULL;
}
