import random

import numpy as np
import pytest

from registry import db
from research import genetic
from research import indicators as ind
from research.engine import Costs
from research.strategies import generic as G
from tests.test_rules import random_bars


def genome(**kw):
    g = {"InpTrig": 0, "InpTrigP1": 20, "InpTrigP2": 0.0, "InpInvert": 0, "InpF1": 0, "InpF1P1": 0,
         "InpF1P2": 0.0, "InpF2": 0, "InpF2P1": 0, "InpF2P2": 0.0, "InpSlAtr": 2.0, "InpTpAtr": 3.0,
         "InpMaxBars": 24, "InpSessionStart": 0, "InpSessionEnd": 24, "InpAtrPeriod": 14}
    g.update(kw)
    return G.canonical(g)


def test_ema_cross_trigger_matches_naive():
    b = random_bars(1500, seed=4)
    d = G.trigger(b, 0, 20, 0.0)
    e = ind.ema(b["close"], 20)
    c = b["close"]
    for i in range(2, len(b)):
        exp = 1 if (c[i-1] > e[i-1] and c[i-2] <= e[i-2]) else (-1 if (c[i-1] < e[i-1] and c[i-2] >= e[i-2]) else 0)
        assert d[i] == exp, i


def test_momentum_trigger_matches_naive():
    b = random_bars(800, seed=5)
    d = G.trigger(b, 5, 4, 1.0)
    a = ind.atr_sma(b, 14)
    c = b["close"]
    for i in range(8, len(b)):
        if not np.isfinite(a[i-2]):
            continue
        m1, m2 = c[i-1] - c[i-5], c[i-2] - c[i-6]
        exp = 1 if (m1 > a[i-1] and m2 <= a[i-2]) else (-1 if (m1 < -a[i-1] and m2 >= -a[i-2]) else 0)
        assert d[i] == exp, i


def test_invert_and_trend_filter():
    b = random_bars(2000, seed=6)
    base = G.direction(b, G.params_of(genome())[1])
    inv = G.direction(b, G.params_of(genome(InpInvert=1))[1])
    assert np.array_equal(inv, -base)
    filt = G.direction(b, G.params_of(genome(InpF1=1, InpF1P1=100))[1])
    e1 = np.concatenate(([np.nan], ind.ema(b["close"], 100)[:-1]))
    c1 = np.concatenate(([np.nan], b["close"][:-1]))
    longs = np.flatnonzero(filt > 0)
    assert len(longs) and np.all(c1[longs] > e1[longs])
    assert set(np.flatnonzero(filt)) <= set(np.flatnonzero(base))


def test_canonical_hash_ignores_unused_settings():
    a = genome(InpTrig=1, InpTrigP1=20, InpTrigP2=2.5)
    b = genome(InpTrig=1, InpTrigP1=20, InpTrigP2=1.0)
    assert G.genome_id(a) == G.genome_id(b)
    assert G.genome_id(a) != G.genome_id(genome(InpTrig=1, InpTrigP1=30))


def test_family_grid_is_local_and_backtests():
    g = genome(InpTrig=4, InpTrigP1=20, InpTrigP2=1.5, InpF1=3, InpF1P1=100, InpF1P2=1.2)
    fam = G.make_family(g)
    grid = fam.grid_params()
    assert 1 < len(grid) <= 3 ** 7 and fam.trial_key == "generic"
    p = G.params_of(g)[1]
    assert p in set(grid)
    assert isinstance(fam.backtest(random_bars(3000), p, Costs(point=0.01)), list)


def test_genetic_operators_keep_genomes_valid():
    rng = random.Random(1)
    for _ in range(300):
        a, b = genetic.random_genome(rng), genetic.random_genome(rng)
        c = genetic.mutate(genetic.crossover(a, b, rng), rng)
        assert c["InpTrigP1"] in G.TRIG_P1[c["InpTrig"]]
        for k in ("F1", "F2"):
            f = c[f"Inp{k}"]
            assert (f == 0 and c[f"Inp{k}P1"] == 0) or c[f"Inp{k}P1"] in G.FILT_P1[f]
        assert c == G.canonical(c)


def test_evolve_logs_every_evaluation(tmp_path):
    con = db.connect(tmp_path / "r.sqlite")
    b = random_bars(24 * 900, seed=7)
    picks = genetic.evolve("TEST", "H1", b, {"name": "TEST", "point": 0.01, "spread": 2}, population=12,
                           generations=3, min_fitness=-99, seed=3, con=con, progress=lambda *_: None)
    n_trials = con.execute("SELECT COUNT(*) FROM trials WHERE family='generic'").fetchone()[0]
    assert n_trials >= 12 and 1 <= len(picks) <= 5
    assert db.get_genome(con, picks[0]["family"]) is not None
