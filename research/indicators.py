"""Indicators replicating MT5's built-ins exactly (so Python/MT5 parity holds)."""
from __future__ import annotations

import numpy as np
from scipy.signal import lfilter

from .engine import atr_sma  # noqa: F401  (re-export: iATR = SMA of true range)


def ema(x: np.ndarray, period: int) -> np.ndarray:
    """iMA(MODE_EMA): seeded with the first price, then a*x + (1-a)*prev."""
    a = 2.0 / (period + 1)
    x = x.astype(float)
    y, _ = lfilter([a], [1, -(1 - a)], x, zi=[(1 - a) * x[0]])
    return y


def sma(x: np.ndarray, period: int) -> np.ndarray:
    out = np.full(len(x), np.nan)
    if len(x) >= period:
        cs = np.cumsum(np.concatenate(([0.0], x.astype(float))))
        out[period - 1:] = (cs[period:] - cs[:-period]) / period
    return out


def rsi(x: np.ndarray, period: int) -> np.ndarray:
    """iRSI: Wilder smoothing seeded with the simple average of the first `period` changes."""
    n = len(x)
    out = np.full(n, np.nan)
    if n <= period:
        return out
    d = np.diff(x.astype(float))
    gain, loss = np.maximum(d, 0), np.maximum(-d, 0)
    a = 1.0 / period
    g0, l0 = gain[:period].mean(), loss[:period].mean()

    def smooth(v, seed):
        rest = v[period:]
        y, _ = lfilter([a], [1, -(1 - a)], rest, zi=[(1 - a) * seed])
        return np.concatenate(([seed], y))

    ag, al = smooth(gain, g0), smooth(loss, l0)      # aligned to x[period:]
    with np.errstate(divide="ignore", invalid="ignore"):
        r = np.where(al == 0, np.where(ag == 0, 50.0, 100.0), 100 - 100 / (1 + ag / al))
    out[period:] = r
    return out


def bands(x: np.ndarray, period: int, dev: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """iBands: SMA middle, population standard deviation."""
    mid = sma(x, period)
    out_sd = np.full(len(x), np.nan)
    if len(x) >= period:
        w = np.lib.stride_tricks.sliding_window_view(x.astype(float), period)
        out_sd[period - 1:] = np.sqrt(((w - mid[period - 1:, None]) ** 2).mean(axis=1))
    return mid, mid + dev * out_sd, mid - dev * out_sd
