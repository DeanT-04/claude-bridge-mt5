"""Technical indicators (numba). Every value at index i uses data up to and including bar i,
i.e. it is known at the CLOSE of bar i. Warm-up values are NaN.

Definitions follow the common references (Wilder smoothing for RSI/ATR/ADX) and are checked
against the independent `ta` library in tests/unit/test_indicators.py.
"""

import numpy as np
from numba import njit


@njit(cache=True)
def sma(x, n):
    out = np.full(len(x), np.nan)
    s = 0.0
    for i in range(len(x)):
        s += x[i]
        if i >= n:
            s -= x[i - n]
        if i >= n - 1:
            out[i] = s / n
    return out


@njit(cache=True)
def ema(x, n):
    """EMA with alpha = 2/(n+1), seeded with the SMA of the first n values."""
    out = np.full(len(x), np.nan)
    if len(x) < n:
        return out
    a = 2.0 / (n + 1)
    v = x[:n].mean()
    out[n - 1] = v
    for i in range(n, len(x)):
        v = a * x[i] + (1 - a) * v
        out[i] = v
    return out


@njit(cache=True)
def wilder(x, n):
    """Wilder's smoothing (RMA): alpha = 1/n, seeded with the SMA of the first n values."""
    out = np.full(len(x), np.nan)
    if len(x) < n:
        return out
    v = x[:n].mean()
    out[n - 1] = v
    for i in range(n, len(x)):
        v = (v * (n - 1) + x[i]) / n
        out[i] = v
    return out


@njit(cache=True)
def rolling_std(x, n):
    out = np.full(len(x), np.nan)
    for i in range(n - 1, len(x)):
        out[i] = np.std(x[i - n + 1 : i + 1])
    return out


@njit(cache=True)
def rolling_max(x, n):
    out = np.full(len(x), np.nan)
    for i in range(n - 1, len(x)):
        out[i] = x[i - n + 1 : i + 1].max()
    return out


@njit(cache=True)
def rolling_min(x, n):
    out = np.full(len(x), np.nan)
    for i in range(n - 1, len(x)):
        out[i] = x[i - n + 1 : i + 1].min()
    return out


@njit(cache=True)
def true_range(high, low, close):
    tr = np.empty(len(high))
    tr[0] = high[0] - low[0]
    for i in range(1, len(high)):
        tr[i] = max(high[i] - low[i], abs(high[i] - close[i - 1]), abs(low[i] - close[i - 1]))
    return tr


@njit(cache=True)
def atr(high, low, close, n):
    return wilder(true_range(high, low, close), n)


@njit(cache=True)
def rsi(close, n):
    """Wilder RSI."""
    k = len(close)
    out = np.full(k, np.nan)
    if k <= n:
        return out
    gain = np.zeros(k)
    loss = np.zeros(k)
    for i in range(1, k):
        d = close[i] - close[i - 1]
        gain[i] = max(d, 0.0)
        loss[i] = max(-d, 0.0)
    ag = gain[1 : n + 1].mean()
    al = loss[1 : n + 1].mean()
    out[n] = 100.0 if al == 0 else 100.0 - 100.0 / (1 + ag / al)
    for i in range(n + 1, k):
        ag = (ag * (n - 1) + gain[i]) / n
        al = (al * (n - 1) + loss[i]) / n
        out[i] = 100.0 if al == 0 else 100.0 - 100.0 / (1 + ag / al)
    return out


def bollinger(close, n, k):
    mid = sma(close, n)
    sd = rolling_std(close, n)
    return mid - k * sd, mid, mid + k * sd


def keltner(high, low, close, n, k):
    mid = ema(close, n)
    a = atr(high, low, close, n)
    return mid - k * a, mid, mid + k * a


def donchian(high, low, n):
    """Upper/lower channel over the last n bars INCLUDING the current one."""
    return rolling_max(high, n), rolling_min(low, n)


def macd(close, fast=12, slow=26, signal=9):
    line = ema(close, fast) - ema(close, slow)
    valid = ~np.isnan(line)
    sig = np.full(len(close), np.nan)
    if valid.sum() >= signal:
        first = int(np.argmax(valid))
        sig[first:] = ema(line[first:], signal)
    return line, sig, line - sig


@njit(cache=True)
def adx(high, low, close, n):
    """Wilder ADX."""
    k = len(close)
    plus = np.zeros(k)
    minus = np.zeros(k)
    for i in range(1, k):
        up = high[i] - high[i - 1]
        dn = low[i - 1] - low[i]
        plus[i] = up if (up > dn and up > 0) else 0.0
        minus[i] = dn if (dn > up and dn > 0) else 0.0
    tr = true_range(high, low, close)
    atr_ = wilder(tr[1:], n)
    pdi = 100 * wilder(plus[1:], n) / atr_
    mdi = 100 * wilder(minus[1:], n) / atr_
    dx = 100 * np.abs(pdi - mdi) / (pdi + mdi)
    out = np.full(k, np.nan)
    start = n - 1
    valid = dx[start:]
    if len(valid) >= n:
        a = wilder(valid, n)
        out[1 + start :] = a
    return out


@njit(cache=True)
def supertrend(high, low, close, n, mult):
    """Returns (line, direction) with direction +1 (up) / -1 (down)."""
    k = len(close)
    a = atr(high, low, close, n)
    line = np.full(k, np.nan)
    dirn = np.zeros(k)
    ub = np.nan
    lb = np.nan
    d = 1.0
    for i in range(k):
        if np.isnan(a[i]):
            continue
        mid = (high[i] + low[i]) / 2
        bu, bl = mid + mult * a[i], mid - mult * a[i]
        if np.isnan(ub):
            ub, lb = bu, bl
        else:
            ub = bu if (bu < ub or close[i - 1] > ub) else ub
            lb = bl if (bl > lb or close[i - 1] < lb) else lb
        if d == 1.0 and close[i] < lb:
            d = -1.0
        elif d == -1.0 and close[i] > ub:
            d = 1.0
        dirn[i] = d
        line[i] = lb if d == 1.0 else ub
    return line, dirn


@njit(cache=True)
def efficiency_ratio(close, n):
    """Kaufman: |net change| / sum of |changes| over n bars (1 = straight line, 0 = noise)."""
    out = np.full(len(close), np.nan)
    for i in range(n, len(close)):
        net = abs(close[i] - close[i - n])
        path = 0.0
        for j in range(i - n + 1, i + 1):
            path += abs(close[j] - close[j - 1])
        out[i] = net / path if path > 0 else 0.0
    return out


def zscore(x, n):
    return (x - sma(x, n)) / rolling_std(x, n)


def cross_up(a, b):
    """True on the bar where a crosses above b (known at that bar's close)."""
    out = np.zeros(len(a), dtype=bool)
    out[1:] = (a[1:] > b[1:]) & (a[:-1] <= b[:-1])
    return out


def cross_down(a, b):
    return cross_up(b, a)
