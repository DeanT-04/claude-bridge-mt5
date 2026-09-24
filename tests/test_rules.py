import numpy as np
import pytest

from research import indicators as ind
from research.strategies import FAMILIES
from research.strategies.rules import FAMILIES as RULES

DT = [("time", "<i8"), ("open", "<f8"), ("high", "<f8"), ("low", "<f8"), ("close", "<f8"),
      ("tick_volume", "<u8"), ("spread", "<i4"), ("real_volume", "<u8")]


def random_bars(n=3000, seed=0, step=3600):
    rng = np.random.default_rng(seed)
    c = 100 + np.cumsum(rng.normal(0, 0.5, n))
    o = np.concatenate(([c[0]], c[:-1]))
    b = np.zeros(n, dtype=DT)
    b["time"] = 1_700_000_000 - (1_700_000_000 % 86400) + np.arange(n) * step
    b["open"], b["close"] = o, c
    b["high"] = np.maximum(o, c) + rng.random(n) * 0.3
    b["low"] = np.minimum(o, c) - rng.random(n) * 0.3
    b["spread"] = 2
    return b


def test_ema_matches_recursion():
    x = random_bars(300)["close"]
    e = ind.ema(x, 10)
    a, y = 2 / 11, x[0]
    for i in range(1, 300):
        y = a * x[i] + (1 - a) * y
    assert e[-1] == pytest.approx(y) and e[0] == x[0]


def test_rsi_matches_wilder_loop():
    x = random_bars(300)["close"]
    r = ind.rsi(x, 14)
    d = np.diff(x)
    ag = np.maximum(d[:14], 0).mean(); al = np.maximum(-d[:14], 0).mean()
    exp = [100 - 100 / (1 + ag / al)]
    for k in range(14, len(d)):
        ag = (ag * 13 + max(d[k], 0)) / 14
        al = (al * 13 + max(-d[k], 0)) / 14
        exp.append(100 - 100 / (1 + ag / al))
    assert np.isnan(r[13]) and r[14:] == pytest.approx(np.array(exp))


def test_bands_population_std():
    x = random_bars(100)["close"]
    mid, up, lo = ind.bands(x, 20, 2.0)
    w = x[80:100]
    assert mid[99] == pytest.approx(w.mean()) and up[99] == pytest.approx(w.mean() + 2 * w.std(ddof=0))


def test_orb_matches_naive():
    b = random_bars(24 * 60)
    fam = RULES["orb"]
    p = fam.Params(InpOrStart=8, InpOrHours=2)
    d = fam.direction(b, p)
    hour = (b["time"] // 3600) % 24
    day = b["time"] // 86400
    for i in range(2, len(b)):
        b1, b2 = i - 1, i - 2
        exp = 0
        if hour[b1] >= 10 and hour[b2] >= 10:
            m = (day == day[b1]) & (hour >= 8) & (hour < 10)
            if m.any():
                rh, rl = b["high"][m].max(), b["low"][m].min()
                c1, c2 = b["close"][b1], b["close"][b2]
                exp = 1 if (c1 > rh and c2 <= rh) else (-1 if (c1 < rl and c2 >= rl) else 0)
        assert d[i] == exp, i


def test_hour_momentum_only_fires_at_hour():
    b = random_bars(24 * 30)
    fam = RULES["hour_momentum"]
    d = fam.direction(b, fam.Params(InpEntryHour=10, InpLookback=4))
    hours = ((b["time"] // 3600) % 24)[d != 0]
    assert len(hours) > 20 and set(hours) == {10}


@pytest.mark.parametrize("name", list(FAMILIES))
def test_every_family_backtests_and_grids(name):
    from research.engine import Costs
    fam = FAMILIES[name]
    b = random_bars(4000, seed=3)
    grid = fam.grid_params()
    assert 100 <= len(grid) <= 3000
    p = grid[len(grid) // 2]
    trades = fam.backtest(b, p, Costs(point=0.01))
    assert isinstance(trades, list)
    for q in fam.neighbours(p):
        assert q in set(grid)
