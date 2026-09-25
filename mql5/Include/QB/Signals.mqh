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
   QB_GENERIC       = 7,   // M4: trigger + filters encoded as parameters
   QB_ML            = 8,   // M5: ONNX model probability vs threshold
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
   // generic (QB_GENERIC): see CSigGeneric
   int    trig, trig_p1; double trig_p2; int invert;
   int    f1, f1_p1; double f1_p2;
   int    f2, f2_p1; double f2_p2;
   // ML (QB_ML): see CSigML
   double ml_thr; string ml_model;
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

//--- QB_GENERIC: one trigger (optionally inverted) gated by up to two filters.
//    Twin: research/strategies/generic.py. Triggers fire on a cross between bars [2] and [1].
//    trig: 0 EMA cross (p1 period)         1 Donchian breakout (p1 channel)
//          2 RSI level cross (p1, p2 = L; long crosses up through L, short down through 100-L)
//          3 Bollinger breakout (p1, p2 dev) 4 Keltner breakout (p1, p2 mult)
//          5 momentum: c1-c[1+p1] crosses p2*ATR14 (mirror for short)
//    filters: 0 none  1 close on trend side of EMA(p1)  2 EMA(p1) slope over 5 bars agrees
//             3 ATR14/ATR(p1) > p2 (high vol)  4 ATR14/ATR(p1) < p2 (low vol)
//             5 RSI(p1) on the trade's side of 50
class CSigGeneric : public CQBSignal
{
   int m_t1, m_t2, m_atr14;          // trigger handles
   int m_fh[2][2];                   // filter handles
   int m_ft[2], m_fp1[2]; double m_fp2[2];

   bool MakeFilter(const int k)
   {
      m_fh[k][0] = INVALID_HANDLE; m_fh[k][1] = INVALID_HANDLE;
      switch(m_ft[k])
      {
         case 1: case 2: m_fh[k][0] = iMA(m_sym, m_tf, m_fp1[k], 0, MODE_EMA, PRICE_CLOSE); break;
         case 3: case 4: m_fh[k][0] = iATR(m_sym, m_tf, 14); m_fh[k][1] = iATR(m_sym, m_tf, m_fp1[k]);
                         if(m_fh[k][1] == INVALID_HANDLE) return false; break;
         case 5: m_fh[k][0] = iRSI(m_sym, m_tf, m_fp1[k], PRICE_CLOSE); break;
         default: return true;
      }
      return m_fh[k][0] != INVALID_HANDLE;
   }

   bool FilterOk(const int k, const int d)
   {
      double a[], b[];
      double c1 = iClose(m_sym, m_tf, 1);
      switch(m_ft[k])
      {
         case 0: return true;
         case 1: if(!Buf(m_fh[k][0], 0, 1, 1, a)) return false; return d > 0 ? c1 > a[0] : c1 < a[0];
         case 2: if(!Buf(m_fh[k][0], 0, 1, 6, a)) return false;              // a[0]=bar1, a[5]=bar6
                 return d > 0 ? a[0] > a[5] : a[0] < a[5];
         case 3: case 4:
                 if(!Buf(m_fh[k][0], 0, 1, 1, a) || !Buf(m_fh[k][1], 0, 1, 1, b) || b[0] <= 0) return false;
                 return m_ft[k] == 3 ? a[0] / b[0] > m_fp2[k] : a[0] / b[0] < m_fp2[k];
         case 5: if(!Buf(m_fh[k][0], 0, 1, 1, a)) return false; return d > 0 ? a[0] > 50 : a[0] < 50;
      }
      return false;
   }

   int Trigger()
   {
      double c1 = iClose(m_sym, m_tf, 1), c2 = iClose(m_sym, m_tf, 2);
      double x[], y[], z[];
      switch(m_p.trig)
      {
         case 0:
            if(!Buf(m_t1, 0, 1, 2, x)) return 0;
            if(c1 > x[0] && c2 <= x[1]) return 1;
            if(c1 < x[0] && c2 >= x[1]) return -1;
            return 0;
         case 1:
         {
            int hh = iHighest(m_sym, m_tf, MODE_HIGH, m_p.trig_p1, 2), ll = iLowest(m_sym, m_tf, MODE_LOW, m_p.trig_p1, 2);
            if(hh < 0 || ll < 0) return 0;
            if(c1 > iHigh(m_sym, m_tf, hh)) return 1;
            if(c1 < iLow(m_sym, m_tf, ll)) return -1;
            return 0;
         }
         case 2:
         {
            if(!Buf(m_t1, 0, 1, 2, x)) return 0;
            double lo = m_p.trig_p2, hi = 100.0 - m_p.trig_p2;
            if(x[1] < lo && x[0] >= lo) return 1;
            if(x[1] > hi && x[0] <= hi) return -1;
            return 0;
         }
         case 3:
            if(!Buf(m_t1, 1, 1, 2, x) || !Buf(m_t1, 2, 1, 2, y)) return 0;
            if(c1 > x[0] && c2 <= x[1]) return 1;
            if(c1 < y[0] && c2 >= y[1]) return -1;
            return 0;
         case 4:
         {
            if(!Buf(m_t1, 0, 1, 2, x) || !Buf(m_t2, 0, 1, 2, y)) return 0;
            double u1 = x[0] + m_p.trig_p2 * y[0], u2 = x[1] + m_p.trig_p2 * y[1];
            double l1 = x[0] - m_p.trig_p2 * y[0], l2 = x[1] - m_p.trig_p2 * y[1];
            if(c1 > u1 && c2 <= u2) return 1;
            if(c1 < l1 && c2 >= l2) return -1;
            return 0;
         }
         case 5:
         {
            if(!Buf(m_atr14, 0, 1, 2, z)) return 0;
            double m1 = c1 - iClose(m_sym, m_tf, 1 + m_p.trig_p1), m2 = c2 - iClose(m_sym, m_tf, 2 + m_p.trig_p1);
            double t1 = m_p.trig_p2 * z[0], t2 = m_p.trig_p2 * z[1];
            if(m1 > t1 && m2 <= t2) return 1;
            if(m1 < -t1 && m2 >= -t2) return -1;
            return 0;
         }
      }
      return 0;
   }

public:
   CSigGeneric() : m_t1(INVALID_HANDLE), m_t2(INVALID_HANDLE), m_atr14(INVALID_HANDLE)
   { for(int k = 0; k < 2; k++) { m_fh[k][0] = INVALID_HANDLE; m_fh[k][1] = INVALID_HANDLE; } }

   bool Init(const string sym, const ENUM_TIMEFRAMES tf, const QBSignalParams &p)
   {
      CQBSignal::Init(sym, tf, p);
      switch(p.trig)
      {
         case 0: m_t1 = iMA(sym, tf, p.trig_p1, 0, MODE_EMA, PRICE_CLOSE); break;
         case 1: m_t1 = 0; break;                                      // no handle needed
         case 2: m_t1 = iRSI(sym, tf, p.trig_p1, PRICE_CLOSE); break;
         case 3: m_t1 = iBands(sym, tf, p.trig_p1, 0, p.trig_p2, PRICE_CLOSE); break;
         case 4: m_t1 = iMA(sym, tf, p.trig_p1, 0, MODE_EMA, PRICE_CLOSE); m_t2 = iATR(sym, tf, p.trig_p1);
                 if(m_t2 == INVALID_HANDLE) return false; break;
         case 5: m_t1 = 0; m_atr14 = iATR(sym, tf, 14); if(m_atr14 == INVALID_HANDLE) return false; break;
         default: return false;
      }
      if(m_t1 == INVALID_HANDLE) return false;
      m_ft[0] = p.f1; m_fp1[0] = p.f1_p1; m_fp2[0] = p.f1_p2;
      m_ft[1] = p.f2; m_fp1[1] = p.f2_p1; m_fp2[1] = p.f2_p2;
      return MakeFilter(0) && MakeFilter(1);
   }

   int Direction()
   {
      int d = Trigger();
      if(d == 0) return 0;
      if(m_p.invert != 0) d = -d;
      if(!FilterOk(0, d) || !FilterOk(1, d)) return 0;
      return d;
   }

   ~CSigGeneric()
   {
      if(m_t1 > 0) IndicatorRelease(m_t1);
      if(m_t2 != INVALID_HANDLE) IndicatorRelease(m_t2);
      if(m_atr14 != INVALID_HANDLE) IndicatorRelease(m_atr14);
      for(int k = 0; k < 2; k++) for(int j = 0; j < 2; j++) if(m_fh[k][j] != INVALID_HANDLE) IndicatorRelease(m_fh[k][j]);
   }
};

//--- QB_ML: 12 features of closed bar [1] -> ONNX classifier -> P(long wins).
//    Twin: research/ml.py (FEATURES order = model input order). Long if p > thr,
//    short if p < 1 - thr. Model file: Common\Files\QB\models\<ml_model>.
class CSigML : public CQBSignal
{
   long m_onnx;
   int  m_e20, m_e100, m_rsi, m_a14, m_a100;
public:
   CSigML() : m_onnx(INVALID_HANDLE), m_e20(INVALID_HANDLE), m_e100(INVALID_HANDLE), m_rsi(INVALID_HANDLE),
              m_a14(INVALID_HANDLE), m_a100(INVALID_HANDLE) {}

   bool Init(const string sym, const ENUM_TIMEFRAMES tf, const QBSignalParams &p)
   {
      CQBSignal::Init(sym, tf, p);
      m_onnx = OnnxCreate("QB\\models\\" + p.ml_model, ONNX_COMMON_FOLDER);
      if(m_onnx == INVALID_HANDLE) { Print("QB ML: cannot load model ", p.ml_model, " err=", GetLastError()); return false; }
      ulong in_shape[] = {1, 12};
      ulong lab_shape[] = {1};
      ulong prob_shape[] = {1, 2};
      if(!OnnxSetInputShape(m_onnx, 0, in_shape) || !OnnxSetOutputShape(m_onnx, 0, lab_shape) ||
         !OnnxSetOutputShape(m_onnx, 1, prob_shape))
      { Print("QB ML: shape setup failed err=", GetLastError()); return false; }
      m_e20 = iMA(sym, tf, 20, 0, MODE_EMA, PRICE_CLOSE);
      m_e100 = iMA(sym, tf, 100, 0, MODE_EMA, PRICE_CLOSE);
      m_rsi = iRSI(sym, tf, 14, PRICE_CLOSE);
      m_a14 = iATR(sym, tf, 14);
      m_a100 = iATR(sym, tf, 100);
      return m_e20 != INVALID_HANDLE && m_e100 != INVALID_HANDLE && m_rsi != INVALID_HANDLE &&
             m_a14 != INVALID_HANDLE && m_a100 != INVALID_HANDLE;
   }

   int Direction()
   {
      double e20[], e100[], r[], a14[], a100[];
      if(!Buf(m_e20, 0, 1, 1, e20) || !Buf(m_e100, 0, 1, 1, e100) || !Buf(m_rsi, 0, 1, 1, r) ||
         !Buf(m_a14, 0, 1, 1, a14) || !Buf(m_a100, 0, 1, 1, a100)) return 0;
      double atr = a14[0];
      if(atr <= 0 || a100[0] <= 0) return 0;
      double c1 = iClose(m_sym, m_tf, 1), h1 = iHigh(m_sym, m_tf, 1), l1 = iLow(m_sym, m_tf, 1);
      int hh = iHighest(m_sym, m_tf, MODE_HIGH, 20, 1), ll = iLowest(m_sym, m_tf, MODE_LOW, 20, 1);
      if(hh < 0 || ll < 0) return 0;
      double H = iHigh(m_sym, m_tf, hh), L = iLow(m_sym, m_tf, ll);
      if(H <= L) return 0;
      MqlDateTime d0; TimeToStruct(iTime(m_sym, m_tf, 0), d0);

      matrixf x(1, 12);
      int lags[] = {1, 4, 12, 24};
      for(int k = 0; k < 4; k++)
      {
         double cn = iClose(m_sym, m_tf, 1 + lags[k]);
         if(cn <= 0) return 0;
         x[0][k] = (float)((c1 - cn) / atr);
      }
      x[0][4]  = (float)((c1 - e20[0]) / atr);
      x[0][5]  = (float)((c1 - e100[0]) / atr);
      x[0][6]  = (float)(r[0] / 100.0);
      x[0][7]  = (float)(atr / a100[0]);
      x[0][8]  = (float)((h1 - l1) / atr);
      x[0][9]  = (float)MathSin(2 * M_PI * d0.hour / 24.0);
      x[0][10] = (float)MathCos(2 * M_PI * d0.hour / 24.0);
      x[0][11] = (float)((c1 - L) / (H - L));

      long label[1];
      matrixf prob(1, 2);
      if(!OnnxRun(m_onnx, ONNX_NO_CONVERSION, x, label, prob)) { Print("QB ML: OnnxRun failed err=", GetLastError()); return 0; }
      double p = prob[0][1];
      if(p > m_p.ml_thr) return 1;
      if(p < 1.0 - m_p.ml_thr) return -1;
      return 0;
   }

   ~CSigML()
   {
      if(m_onnx != INVALID_HANDLE) OnnxRelease(m_onnx);
      int hs[] = {m_e20, m_e100, m_rsi, m_a14, m_a100};
      for(int i = 0; i < 5; i++) if(hs[i] != INVALID_HANDLE) IndicatorRelease(hs[i]);
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
      case QB_GENERIC:       return new CSigGeneric();
      case QB_ML:            return new CSigML();
   }
   return NULL;
}
