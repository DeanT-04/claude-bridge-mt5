"""Python twins of the QB_Rules signal families (mql5/Include/QB/Signals.mqh).

Every family shares QB_Rules' execution: entry at the open of bar i when the signal on
closed bars i-1/i-2 fires, SL/TP as ATR multiples of ATR[i-1], time exit, session filter.
"""
from __future__ import annotations

import itertools
from dataclasses import asdict, dataclass, field, make_dataclass

import numpy as np

from .. import indicators as ind
from ..engine import Costs, atr_sma, server_hour, simulate

EXPERT = "QB\\QB_Rules.ex5"

COMMON = [("InpAtrPeriod", int, 14), ("InpSlAtr", float, 2.0), ("InpTpAtr", float, 3.0),
          ("InpMaxBars", int, 24), ("InpSessionStart", int, 0), ("InpSessionEnd", int, 24)]

COMMON_GRID = {
    "InpSlAtr": [1.0, 1.5, 2.0, 3.0],
    "InpTpAtr": [1.0, 1.5, 2.0, 3.0, 4.0],
    "InpMaxBars": [6, 12, 24, 48],
}
FULL_DAY, EURO_US = (0, 24), (9, 21)       # server hours (BlackBull server ~ GMT+2/3)


# ---------------------------------------------------------------- direction functions
def _dir_ema_pullback(b, p):
    f, s = ind.ema(b["close"], p.InpFast), ind.ema(b["close"], p.InpSlow)
    h, l, c = b["high"], b["low"], b["close"]
    d = np.zeros(len(b), np.int8)
    f1, s1, h1, l1, c1 = f[:-1], s[:-1], h[:-1], l[:-1], c[:-1]
    d[1:] = np.where((f1 > s1) & (l1 <= f1) & (c1 > f1), 1,
                     np.where((f1 < s1) & (h1 >= f1) & (c1 < f1), -1, 0))
    return d


def _dir_rsi_reversion(b, p):
    r = ind.rsi(b["close"], p.InpRsiPeriod)
    d = np.zeros(len(b), np.int8)
    r1, r2 = r[1:-1], r[:-2]
    with np.errstate(invalid="ignore"):
        d[2:] = np.where((r2 < p.InpRsiLo) & (r1 >= p.InpRsiLo), 1,
                         np.where((r2 > p.InpRsiHi) & (r1 <= p.InpRsiHi), -1, 0))
    return d


def _dir_bb_reversion(b, p):
    _, up, lo = ind.bands(b["close"], p.InpBbPeriod, p.InpBbDev)
    c = b["close"]
    d = np.zeros(len(b), np.int8)
    c1, c2 = c[1:-1], c[:-2]
    with np.errstate(invalid="ignore"):
        d[2:] = np.where((c2 < lo[:-2]) & (c1 > lo[1:-1]), 1,
                         np.where((c2 > up[:-2]) & (c1 < up[1:-1]), -1, 0))
    return d


def _dir_orb(b, p):
    t, h, l, c = b["time"], b["high"], b["low"], b["close"]
    hour = server_hour(b)
    day = t // 86400
    uday, di = np.unique(day, return_inverse=True)
    end = p.InpOrStart + p.InpOrHours
    in_or = (hour >= p.InpOrStart) & (hour < end)
    hi = np.full(len(uday), -np.inf)
    lo = np.full(len(uday), np.inf)
    np.maximum.at(hi, di[in_or], h[in_or])
    np.minimum.at(lo, di[in_or], l[in_or])
    d = np.zeros(len(b), np.int8)
    i = np.arange(2, len(b))
    b1, b2 = i - 1, i - 2
    rh, rl = hi[di[b1]], lo[di[b1]]
    ok = (hour[b1] >= end) & (hour[b2] >= end) & np.isfinite(rh)
    d[2:] = np.where(ok & (c[b1] > rh) & (c[b2] <= rh), 1,
                     np.where(ok & (c[b1] < rl) & (c[b2] >= rl), -1, 0))
    return d


def _dir_keltner(b, p):
    m = ind.ema(b["close"], p.InpKcPeriod)
    a = atr_sma(b, p.InpKcPeriod)
    c = b["close"]
    up, dn = m + p.InpKcMult * a, m - p.InpKcMult * a
    d = np.zeros(len(b), np.int8)
    c1, c2 = c[1:-1], c[:-2]
    with np.errstate(invalid="ignore"):
        d[2:] = np.where((c1 > up[1:-1]) & (c2 <= up[:-2]), 1,
                         np.where((c1 < dn[1:-1]) & (c2 >= dn[:-2]), -1, 0))
    return d


def _dir_hour_momentum(b, p):
    t, c = b["time"], b["close"]
    hour, minute = server_hour(b), (t // 60) % 60
    L = p.InpLookback
    d = np.zeros(len(b), np.int8)
    if len(b) <= L + 1:
        return d
    i = np.arange(L + 1, len(b))
    c1, cn = c[i - 1], c[i - 1 - L]
    at = (hour[i] == p.InpEntryHour) & (minute[i] == 0)
    d[L + 1:] = np.where(at & (c1 > cn), 1, np.where(at & (c1 < cn), -1, 0))
    return d


# ---------------------------------------------------------------- family plumbing
@dataclass
class Family:
    name: str
    fid: int                       # ENUM_QB_FAMILY value
    fields: list                   # (name, type, default) family-specific
    grid: dict                     # axis -> values; "a,b" axes take tuples (categorical)
    direction: callable
    sessions: list = field(default_factory=lambda: [FULL_DAY, EURO_US])
    EXPERT: str = EXPERT

    def __post_init__(self):
        cls = make_dataclass(
            f"{self.name.title().replace('_', '')}Params",
            [(n, t, d) for n, t, d in COMMON + self.fields] + [("InpFamily", int, self.fid)],
            frozen=True, namespace={"dict": lambda s: asdict(s)})
        self.Params = cls
        self.GRID = {**self.grid, **COMMON_GRID}
        if self.sessions:
            self.GRID["InpSessionStart,InpSessionEnd"] = self.sessions

    def signals(self, bars: np.ndarray, p):
        d = self.direction(bars, p).astype(np.int8)
        atr = atr_sma(bars, p.InpAtrPeriod)
        a1 = np.concatenate(([np.nan], atr[:-1]))
        hour = server_hour(bars)
        s, e = p.InpSessionStart, p.InpSessionEnd
        sess = (hour >= s) & (hour < e) if s <= e else (hour >= s) | (hour < e)
        ok = sess & np.isfinite(a1) & (a1 > 0)
        d = np.where(ok, d, 0).astype(np.int8)
        sl = np.where(ok, p.InpSlAtr * np.nan_to_num(a1), 0.0)
        tp = np.where(ok, p.InpTpAtr * np.nan_to_num(a1), 0.0)
        return d, sl, tp

    def backtest(self, bars, p, costs: Costs, start=0, end=None):
        d, sl, tp = self.signals(bars, p)
        return simulate(bars, d, sl, tp, p.InpMaxBars, costs, start, end)

    def _expand(self, axis, value) -> dict:
        names = axis.split(",")
        vals = value if len(names) > 1 else (value,)
        return dict(zip(names, vals))

    def grid_params(self) -> list:
        axes = list(self.GRID)
        out = []
        for combo in itertools.product(*(self.GRID[a] for a in axes)):
            kw = {}
            for a, v in zip(axes, combo):
                kw.update(self._expand(a, v))
            out.append(self.Params(**kw))
        return out

    def neighbours(self, p) -> list:
        """One step along each numeric axis; categorical (tuple) axes are not perturbed."""
        out = []
        for a, vals in self.GRID.items():
            if "," in a:
                continue
            cur = getattr(p, a)
            if cur not in vals:
                continue
            k = vals.index(cur)
            for j in (k - 1, k + 1):
                if 0 <= j < len(vals):
                    out.append(self.Params(**{**p.dict(), a: vals[j]}))
        return out


FAMILIES = {
    "ema_pullback": Family("ema_pullback", 1,
                           [("InpFast", int, 20), ("InpSlow", int, 100)],
                           {"InpFast": [10, 20, 30], "InpSlow": [50, 100, 200]}, _dir_ema_pullback),
    "rsi_reversion": Family("rsi_reversion", 2,
                            [("InpRsiPeriod", int, 14), ("InpRsiLo", float, 30.0), ("InpRsiHi", float, 70.0)],
                            {"InpRsiPeriod": [7, 14],
                             "InpRsiLo,InpRsiHi": [(20.0, 80.0), (25.0, 75.0), (30.0, 70.0)]},
                            _dir_rsi_reversion),
    "bb_reversion": Family("bb_reversion", 3,
                           [("InpBbPeriod", int, 20), ("InpBbDev", float, 2.0)],
                           {"InpBbPeriod": [20, 40], "InpBbDev": [2.0, 2.5, 3.0]}, _dir_bb_reversion),
    "orb": Family("orb", 4,
                  [("InpOrStart", int, 8), ("InpOrHours", int, 2)],
                  {"InpOrStart": [1, 8, 9, 10, 15, 16], "InpOrHours": [1, 2, 3]}, _dir_orb,
                  sessions=[FULL_DAY]),
    "keltner": Family("keltner", 5,
                      [("InpKcPeriod", int, 20), ("InpKcMult", float, 1.5)],
                      {"InpKcPeriod": [20, 50], "InpKcMult": [1.0, 1.5, 2.0, 2.5]}, _dir_keltner),
    "hour_momentum": Family("hour_momentum", 6,
                            [("InpEntryHour", int, 10), ("InpLookback", int, 4)],
                            {"InpEntryHour": [2, 8, 10, 14, 16, 20], "InpLookback": [2, 6, 12]},
                            _dir_hour_momentum, sessions=[FULL_DAY]),
}
