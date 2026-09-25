"""Genetic search over QB_GENERIC genomes.

Fitness is measured on pre-holdout data only, as the worse of the two halves' Sharpe (a genome
must work in both), minus a small penalty per filter. Every evaluated genome is logged to the
shared 'generic' trial pool, so the gauntlet's Deflated Sharpe sees the true search size.
The best distinct genomes are saved and handed to the full gauntlet.
"""
from __future__ import annotations

import math
import random
import zlib

import numpy as np

from bridge import config
from registry import db

from . import stats
from .engine import simulate
from .gauntlet import _month_ts, costs_for
from .strategies import generic as G

MIN_TRADES_PER_HALF = 40
FILTER_PENALTY = 0.1
TRIAL_KEY = "generic"


def random_genome(rng: random.Random) -> dict:
    t = rng.randrange(len(G.TRIGGERS))
    g = {"InpTrig": t, "InpTrigP1": rng.choice(G.TRIG_P1[t]),
         "InpTrigP2": rng.choice(G.TRIG_P2[t]) if t in G.TRIG_P2 else 0.0,
         "InpInvert": int(rng.random() < 0.3)}
    for k, prob in (("F1", 0.5), ("F2", 0.2)):
        _set_filter(g, k, rng.randrange(1, len(G.FILTERS)) if rng.random() < prob else 0, rng)
    g.update({"InpSlAtr": rng.choice(G.SL), "InpTpAtr": rng.choice(G.TP), "InpMaxBars": rng.choice(G.MAX_BARS),
              "InpAtrPeriod": 14})
    g["InpSessionStart"], g["InpSessionEnd"] = rng.choice(G.SESSIONS)
    return G.canonical(g)


def _set_filter(g: dict, k: str, f: int, rng: random.Random) -> None:
    g[f"Inp{k}"] = f
    g[f"Inp{k}P1"] = rng.choice(G.FILT_P1[f]) if f else 0
    g[f"Inp{k}P2"] = rng.choice(G.FILT_P2[f]) if f in G.FILT_P2 else 0.0


def _step(values: list, v, rng: random.Random):
    if v not in values:
        return rng.choice(values)
    i = values.index(v) + rng.choice((-1, 1))
    return values[min(max(i, 0), len(values) - 1)]


def mutate(g: dict, rng: random.Random) -> dict:
    g = dict(g)
    for _ in range(rng.choice((1, 1, 2))):
        what = rng.choice(["trig", "tp1", "tp2", "invert", "f1", "f2", "fp", "sl", "tp", "bars", "session"])
        t = g["InpTrig"]
        if what == "trig":
            t = rng.randrange(len(G.TRIGGERS))
            g.update({"InpTrig": t, "InpTrigP1": rng.choice(G.TRIG_P1[t]),
                      "InpTrigP2": rng.choice(G.TRIG_P2[t]) if t in G.TRIG_P2 else 0.0})
        elif what == "tp1":
            g["InpTrigP1"] = _step(G.TRIG_P1[t], g["InpTrigP1"], rng)
        elif what == "tp2" and t in G.TRIG_P2:
            g["InpTrigP2"] = _step(G.TRIG_P2[t], g["InpTrigP2"], rng)
        elif what == "invert":
            g["InpInvert"] ^= 1
        elif what in ("f1", "f2"):
            k = what.upper()
            _set_filter(g, k, rng.randrange(len(G.FILTERS)), rng)
        elif what == "fp":
            k = rng.choice(("F1", "F2"))
            f = g[f"Inp{k}"]
            if f:
                g[f"Inp{k}P1"] = _step(G.FILT_P1[f], g[f"Inp{k}P1"], rng)
                if f in G.FILT_P2:
                    g[f"Inp{k}P2"] = _step(G.FILT_P2[f], g[f"Inp{k}P2"], rng)
        elif what == "sl":
            g["InpSlAtr"] = _step(G.SL, g["InpSlAtr"], rng)
        elif what == "tp":
            g["InpTpAtr"] = _step(G.TP, g["InpTpAtr"], rng)
        elif what == "bars":
            g["InpMaxBars"] = _step(G.MAX_BARS, g["InpMaxBars"], rng)
        elif what == "session":
            g["InpSessionStart"], g["InpSessionEnd"] = rng.choice(G.SESSIONS)
    return G.canonical(g)


BLOCKS = [("InpTrig", "InpTrigP1", "InpTrigP2", "InpInvert"), ("InpF1", "InpF1P1", "InpF1P2"),
          ("InpF2", "InpF2P1", "InpF2P2"), ("InpSlAtr", "InpTpAtr", "InpMaxBars"),
          ("InpSessionStart", "InpSessionEnd")]


def crossover(a: dict, b: dict, rng: random.Random) -> dict:
    """Uniform crossover over whole building blocks (keeps each block self-consistent)."""
    child = dict(a)
    for block in BLOCKS:
        if rng.random() < 0.5:
            child.update({k: b[k] for k in block})
    return G.canonical(child)


class Evaluator:
    def __init__(self, bars: np.ndarray, spec: dict):
        self.bars = bars
        self.costs = costs_for(spec)
        t = bars["time"]
        hold = _month_ts(int(t[-1]), -config.settings()["research"]["holdout_months"])
        self.end = int(np.searchsorted(t, hold))
        self.mid = self.end // 2
        self.spans = [max((t[self.mid - 1] - t[0]) / 86400, 1), max((t[self.end - 1] - t[self.mid]) / 86400, 1)]
        self.log: list[tuple[dict, float, int]] = []
        self.seen: dict[str, float] = {}

    def fitness(self, g: dict) -> float:
        gid = G.genome_id(g)
        if gid in self.seen:
            return self.seen[gid]
        fam, p = G.params_of(g)
        d, sl, tp = fam.signals(self.bars, p)
        sharpes, n_total, all_r = [], 0, []
        for (a, b), span in zip(((0, self.mid), (self.mid, self.end)), self.spans):
            tr = simulate(self.bars, d, sl, tp, p.InpMaxBars, self.costs, a, b)
            n_total += len(tr)
            all_r += [x.r for x in tr]
            sharpes.append(stats.metrics(tr, span_days=span)["sharpe"] if len(tr) >= MIN_TRADES_PER_HALF
                           else -math.inf)
        n_filters = int(g["InpF1"] > 0) + int(g["InpF2"] > 0)
        fit = min(sharpes) - FILTER_PENALTY * n_filters
        self.log.append((g, stats.trade_sharpe(np.array(all_r)), n_total))
        self.seen[gid] = fit
        return fit


def evolve(symbol: str, timeframe: str, bars: np.ndarray, spec: dict, population: int = 80,
           generations: int = 40, elite: int = 4, top_k: int = 5, min_fitness: float = 0.5,
           seed: int | None = None, con=None, progress=print) -> list[dict]:
    """Run the GA; save and return up to top_k distinct genomes with fitness >= min_fitness."""
    rng = random.Random(seed if seed is not None else zlib.crc32(f"{symbol}:{timeframe}".encode()))
    ev = Evaluator(bars, spec)
    pop = [random_genome(rng) for _ in range(population)]
    for gen in range(generations):
        scored = sorted(((ev.fitness(g), g) for g in pop), key=lambda x: x[0], reverse=True)
        if gen % 5 == 0 or gen == generations - 1:
            progress(f"  gen {gen}: best {scored[0][0]:.2f} {G.describe(scored[0][1])}")
        nxt = [g for _, g in scored[:elite]]

        def pick():
            a, b = rng.sample(scored, 2), rng.sample(scored, 2)
            return max(a, key=lambda x: x[0])[1], max(b, key=lambda x: x[0])[1]

        while len(nxt) < population:
            p1, p2 = pick()
            child = crossover(p1, p2, rng) if rng.random() < 0.7 else dict(p1)
            if rng.random() < 0.6:
                child = mutate(child, rng)
            nxt.append(child)
        pop = nxt

    con = con or db.connect()
    db.log_trials(con, TRIAL_KEY, symbol, timeframe, ev.log)
    best = sorted(((f, gid) for gid, f in ev.seen.items() if f >= min_fitness), reverse=True)
    by_id = {G.genome_id(g): g for g, _, _ in ev.log}
    out, structures = [], set()
    for f, gid in best:
        g = by_id[gid]
        struct = (g["InpTrig"], g["InpInvert"], g["InpF1"], g["InpF2"])   # keep the picks diverse
        if struct in structures:
            continue
        structures.add(struct)
        fam_name = f"gen_{gid}"
        db.save_genome(con, fam_name, g, G.describe(g), symbol, timeframe, f)
        out.append({"family": fam_name, "fitness": f, "description": G.describe(g)})
        if len(out) >= top_k:
            break
    progress(f"  evaluated {len(ev.seen)} genomes; {len(out)} saved for the gauntlet")
    return out
