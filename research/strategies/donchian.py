"""Python twin of mql5/Experts/QB/QB_Donchian.mq5 — keep the rules in sync."""
from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np

from ..engine import Costs, atr_sma, server_hour, simulate

EXPERT = "QB\\QB_Donchian.ex5"
fid = 0   # ENUM_QB_FAMILY value in Signals.mqh (QB_Host runs it as a sleeve)


@dataclass(frozen=True)
class Params:
    InpChannel: int = 20
    InpAtrPeriod: int = 14
    InpSlAtr: float = 2.0
    InpTpAtr: float = 3.0
    InpMaxBars: int = 48
    InpSessionStart: int = 7
    InpSessionEnd: int = 20

    def dict(self) -> dict:
        return asdict(self)


# Optimisation grid: (start, step, stop) per parameter. Session is fixed per run for now.
GRID = {
    "InpChannel": (10, 5, 60),
    "InpSlAtr": (1.0, 0.5, 3.0),
    "InpTpAtr": (1.0, 0.5, 5.0),
    "InpMaxBars": (12, 12, 72),
}


def signals(bars: np.ndarray, p: Params):
    """Entry arrays aligned so index i means 'enter at the open of bar i'."""
    n = len(bars)
    h, l, c = bars["high"], bars["low"], bars["close"]
    N = p.InpChannel
    atr = atr_sma(bars, p.InpAtrPeriod)
    hour = server_hour(bars)
    in_sess = (hour >= p.InpSessionStart) & (hour < p.InpSessionEnd) if p.InpSessionStart <= p.InpSessionEnd \
        else (hour >= p.InpSessionStart) | (hour < p.InpSessionEnd)

    direction = np.zeros(n, dtype=np.int8)
    sl = np.zeros(n)
    tp = np.zeros(n)
    if n < N + 3:
        return direction, sl, tp
    # upper[i] = max high over bars i-N-1 .. i-2 (the EA's iHighest(..., N, 2) at bar i)
    win_h = np.lib.stride_tricks.sliding_window_view(h, N).max(axis=1)   # win_h[k] = max h[k..k+N-1]
    win_l = np.lib.stride_tricks.sliding_window_view(l, N).min(axis=1)
    idx = np.arange(N + 1, n)
    upper = win_h[idx - N - 1]
    lower = win_l[idx - N - 1]
    c1 = c[idx - 1]
    a1 = atr[idx - 1]
    d = np.where(c1 > upper, 1, np.where(c1 < lower, -1, 0))
    ok = in_sess[idx] & np.isfinite(a1) & (a1 > 0)
    d = np.where(ok, d, 0)
    direction[idx] = d
    sl[idx] = np.where(ok, p.InpSlAtr * a1, 0)
    tp[idx] = np.where(ok, p.InpTpAtr * a1, 0)
    return direction, sl, tp


def backtest(bars: np.ndarray, p: Params, costs: Costs, start: int = 0, end: int | None = None):
    d, sl, tp = signals(bars, p)
    return simulate(bars, d, sl, tp, p.InpMaxBars, costs, start, end)


def grid_params(base: Params | None = None) -> list[Params]:
    base = base or Params()
    axes = {k: np.round(np.arange(a, c + b / 2, b), 6) for k, (a, b, c) in GRID.items()}
    keys = list(axes)
    mesh = np.array(np.meshgrid(*axes.values(), indexing="ij")).reshape(len(keys), -1).T
    out = []
    for row in mesh:
        kw = {k: (int(v) if isinstance(getattr(base, k), int) else float(v)) for k, v in zip(keys, row)}
        out.append(Params(**{**base.dict(), **kw}))
    return out


def neighbours(p: Params) -> list[Params]:
    """Params one grid step away on each optimised axis."""
    out = []
    for k, (a, b, c) in GRID.items():
        for s in (-b, b):
            v = getattr(p, k) + s
            if a - 1e-9 <= v <= c + 1e-9:
                v = int(v) if isinstance(getattr(p, k), int) else float(v)
                out.append(Params(**{**p.dict(), k: v}))
    return out
