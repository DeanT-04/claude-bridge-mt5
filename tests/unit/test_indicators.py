"""Our numba indicators vs the independent `ta` library (after warm-up where seeding differs)."""

import numpy as np
import pandas as pd
import pytest
from ta.momentum import RSIIndicator
from ta.trend import MACD, ADXIndicator, EMAIndicator, SMAIndicator
from ta.volatility import AverageTrueRange, BollingerBands, DonchianChannel

from propquant.strategies import indicators as ind

RNG = np.random.default_rng(42)
N = 3000
CLOSE = 100 + np.cumsum(RNG.normal(0, 1, N))
OPEN = np.r_[100, CLOSE[:-1]]
HIGH = np.maximum(OPEN, CLOSE) + RNG.uniform(0, 1, N)
LOW = np.minimum(OPEN, CLOSE) - RNG.uniform(0, 1, N)
C, H, L = pd.Series(CLOSE), pd.Series(HIGH), pd.Series(LOW)
TAIL = slice(1500, None)  # exponential seeds differ; compare once they have decayed


def close_to(a, b, rel=1e-6):
    a, b = np.asarray(a)[TAIL], np.asarray(b)[TAIL]
    np.testing.assert_allclose(a, b, rtol=rel, atol=1e-8)


def test_sma_exact() -> None:
    np.testing.assert_allclose(
        ind.sma(CLOSE, 20)[19:], SMAIndicator(C, 20).sma_indicator().to_numpy()[19:]
    )


def test_ema() -> None:
    close_to(ind.ema(CLOSE, 20), EMAIndicator(C, 20).ema_indicator())


def test_rsi() -> None:
    close_to(ind.rsi(CLOSE, 14), RSIIndicator(C, 14).rsi())


def test_atr() -> None:
    close_to(ind.atr(HIGH, LOW, CLOSE, 14), AverageTrueRange(H, L, C, 14).average_true_range())


def test_bollinger_exact() -> None:
    lo, _mid, hi = ind.bollinger(CLOSE, 20, 2.0)
    bb = BollingerBands(C, 20, 2)
    np.testing.assert_allclose(hi[19:], bb.bollinger_hband().to_numpy()[19:])
    np.testing.assert_allclose(lo[19:], bb.bollinger_lband().to_numpy()[19:])


def test_donchian_exact() -> None:
    up, dn = ind.donchian(HIGH, LOW, 20)
    dc = DonchianChannel(H, L, C, 20)
    np.testing.assert_allclose(up[19:], dc.donchian_channel_hband().to_numpy()[19:])
    np.testing.assert_allclose(dn[19:], dc.donchian_channel_lband().to_numpy()[19:])


def test_macd() -> None:
    line, sig, _hist = ind.macd(CLOSE)
    m = MACD(C)
    close_to(line, m.macd())
    close_to(sig, m.macd_signal(), rel=1e-4)


def test_adx() -> None:
    close_to(ind.adx(HIGH, LOW, CLOSE, 14), ADXIndicator(H, L, C, 14).adx(), rel=1e-4)


def test_efficiency_ratio_extremes() -> None:
    line = np.arange(50, dtype=float)
    assert ind.efficiency_ratio(line, 10)[-1] == pytest.approx(1.0)
    zigzag = np.tile([0.0, 1.0], 25)
    assert ind.efficiency_ratio(zigzag, 10)[-1] == pytest.approx(0.0)


def test_supertrend_flips_with_trend() -> None:
    up = np.linspace(100, 200, 200)
    down = np.linspace(200, 100, 200)
    c = np.r_[up, down]
    _, d = ind.supertrend(c + 0.5, c - 0.5, c, 10, 3.0)
    assert d[150] == 1 and d[-1] == -1


def test_indicators_are_causal() -> None:
    """Changing future bars never changes past indicator values."""
    t = 2000
    h2, l2, c2 = HIGH.copy(), LOW.copy(), CLOSE.copy()
    c2[t + 1 :] += 50
    h2[t + 1 :] += 50
    l2[t + 1 :] += 50
    pairs = [
        (ind.ema(CLOSE, 20), ind.ema(c2, 20)),
        (ind.rsi(CLOSE, 14), ind.rsi(c2, 14)),
        (ind.atr(HIGH, LOW, CLOSE, 14), ind.atr(h2, l2, c2, 14)),
        (ind.adx(HIGH, LOW, CLOSE, 14), ind.adx(h2, l2, c2, 14)),
        (ind.supertrend(HIGH, LOW, CLOSE, 10, 3.0)[1], ind.supertrend(h2, l2, c2, 10, 3.0)[1]),
        (ind.macd(CLOSE)[1], ind.macd(c2)[1]),
        (ind.efficiency_ratio(CLOSE, 10), ind.efficiency_ratio(c2, 10)),
    ]
    for a, b in pairs:
        np.testing.assert_array_equal(a[: t + 1], b[: t + 1])
