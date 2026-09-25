"""QB_GENERIC: strategies assembled from building blocks, expressed as parameters.

Python twin of CSigGeneric in mql5/Include/QB/Signals.mqh. A genome picks a trigger (with its
settings), an optional invert, up to two filters and the shared exits. Each genome becomes its
own Family ("gen_<hash>") whose optimisation grid is the genome's local neighbourhood, so it
runs through the unchanged gauntlet, MT5 tester (QB_Rules) and QB_Host.
"""
from __future__ import annotations

import hashlib
import json

import numpy as np

from .. import indicators as ind
from ..engine import atr_sma
from .rules import COMMON, Family

FID = 7
TRIGGERS = ["ema_cross", "donchian", "rsi_level", "bb_break", "keltner", "momentum"]
FILTERS = ["none", "trend_ema", "ema_slope", "vol_high", "vol_low", "rsi_side"]

# Discrete value lists per gene (mutation steps along these; the gauntlet grid is ±1 step).
TRIG_P1 = {0: [10, 20, 30, 50, 100, 200], 1: [10, 20, 30, 50, 80, 100], 2: [5, 7, 10, 14, 21, 30],
           3: [10, 20, 30, 40, 60], 4: [10, 20, 30, 50, 100], 5: [2, 4, 8, 12, 24, 48]}
TRIG_P2 = {2: [15.0, 20.0, 25.0, 30.0, 35.0, 40.0], 3: [1.5, 2.0, 2.5, 3.0],
           4: [0.5, 1.0, 1.5, 2.0, 2.5, 3.0], 5: [0.5, 1.0, 1.5, 2.0, 3.0]}
FILT_P1 = {1: [20, 50, 100, 200], 2: [20, 50, 100, 200], 3: [50, 100, 200], 4: [50, 100, 200],
           5: [7, 14, 21]}
FILT_P2 = {3: [0.8, 1.0, 1.2, 1.4], 4: [0.6, 0.8, 1.0, 1.2]}
SL = [0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0]
TP = [0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0]
MAX_BARS = [4, 8, 12, 24, 48, 96]
SESSIONS = [(0, 24), (9, 21), (2, 10), (8, 16), (14, 22)]

GENE_FIELDS = [("InpTrig", int, 0), ("InpTrigP1", int, 20), ("InpTrigP2", float, 2.0), ("InpInvert", int, 0),
               ("InpF1", int, 0), ("InpF1P1", int, 100), ("InpF1P2", float, 1.0),
               ("InpF2", int, 0), ("InpF2P1", int, 100), ("InpF2P2", float, 1.0)]

# ------------------------------------------------------------------ indicator cache
_cache: dict = {}


def _cached(bars, key, fn):
    # identity of the bar array: address alone could be reused after garbage collection
    k = (bars.ctypes.data, len(bars), int(bars["time"][0]), int(bars["time"][-1]), key)
    if k not in _cache:
        if len(_cache) > 512:
            _cache.clear()
        _cache[k] = fn()
    return _cache[k]


def _ema(b, n):
    return _cached(b, ("ema", n), lambda: ind.ema(b["close"], n))


def _atr(b, n):
    return _cached(b, ("atr", n), lambda: atr_sma(b, n))


def _rsi(b, n):
    return _cached(b, ("rsi", n), lambda: ind.rsi(b["close"], n))


def _bands(b, n, dev):
    return _cached(b, ("bb", n, dev), lambda: ind.bands(b["close"], n, dev))


def _lag(x, k):
    """x shifted so out[i] = x[i-k] (NaN for the first k)."""
    out = np.full(len(x), np.nan)
    out[k:] = x[:len(x) - k]
    return out


# ------------------------------------------------------------------ signal
def trigger(b, t: int, p1: int, p2: float) -> np.ndarray:
    """Direction for entry at bar i from closed bars i-1 (…1) and i-2 (…2)."""
    c = b["close"]
    c1, c2 = _lag(c, 1), _lag(c, 2)
    with np.errstate(invalid="ignore"):
        if t == 0:
            e = _ema(b, p1); e1, e2 = _lag(e, 1), _lag(e, 2)
            up, dn = (c1 > e1) & (c2 <= e2), (c1 < e1) & (c2 >= e2)
        elif t == 1:
            h, l = b["high"], b["low"]
            d = np.zeros(len(b), np.int8)
            if len(b) > p1 + 2:
                wh = np.lib.stride_tricks.sliding_window_view(h, p1).max(axis=1)
                wl = np.lib.stride_tricks.sliding_window_view(l, p1).min(axis=1)
                idx = np.arange(p1 + 1, len(b))
                cc = c[idx - 1]
                d[idx] = np.where(cc > wh[idx - p1 - 1], 1, np.where(cc < wl[idx - p1 - 1], -1, 0))
            return d
        elif t == 2:
            r = _rsi(b, p1); r1, r2 = _lag(r, 1), _lag(r, 2)
            up, dn = (r2 < p2) & (r1 >= p2), (r2 > 100 - p2) & (r1 <= 100 - p2)
        elif t == 3:
            _, u, lo = _bands(b, p1, p2)
            up = (c1 > _lag(u, 1)) & (c2 <= _lag(u, 2))
            dn = (c1 < _lag(lo, 1)) & (c2 >= _lag(lo, 2))
        elif t == 4:
            e, a = _ema(b, p1), _atr(b, p1)
            u, lo = e + p2 * a, e - p2 * a
            up = (c1 > _lag(u, 1)) & (c2 <= _lag(u, 2))
            dn = (c1 < _lag(lo, 1)) & (c2 >= _lag(lo, 2))
        elif t == 5:
            a = _atr(b, 14)
            m = c - _lag(c, p1)                                   # m[j] = c[j] - c[j-p1]
            m1, m2 = _lag(m, 1), _lag(m, 2)
            t1, t2 = p2 * _lag(a, 1), p2 * _lag(a, 2)
            up, dn = (m1 > t1) & (m2 <= t2), (m1 < -t1) & (m2 >= -t2)
        else:
            raise ValueError(f"unknown trigger {t}")
    return np.where(up, 1, np.where(dn, -1, 0)).astype(np.int8)


def filter_ok(b, f: int, p1: int, p2: float, d: np.ndarray) -> np.ndarray:
    if f == 0:
        return np.ones(len(b), bool)
    c1 = _lag(b["close"], 1)
    with np.errstate(invalid="ignore", divide="ignore"):
        if f == 1:
            e1 = _lag(_ema(b, p1), 1)
            return np.where(d > 0, c1 > e1, c1 < e1)
        if f == 2:
            e = _ema(b, p1)
            s = _lag(e, 1) - _lag(e, 6)
            return np.where(d > 0, s > 0, s < 0)
        if f in (3, 4):
            ratio = _lag(_atr(b, 14), 1) / _lag(_atr(b, p1), 1)
            return ratio > p2 if f == 3 else ratio < p2
        if f == 5:
            r1 = _lag(_rsi(b, p1), 1)
            return np.where(d > 0, r1 > 50, r1 < 50)
    raise ValueError(f"unknown filter {f}")


def direction(b, p) -> np.ndarray:
    d = trigger(b, p.InpTrig, p.InpTrigP1, p.InpTrigP2)
    if p.InpInvert:
        d = -d
    ok = filter_ok(b, p.InpF1, p.InpF1P1, p.InpF1P2, d) & filter_ok(b, p.InpF2, p.InpF2P1, p.InpF2P2, d)
    return np.where(ok, d, 0).astype(np.int8)


# ------------------------------------------------------------------ genomes -> families
def canonical(genome: dict) -> dict:
    """Zero out settings a genome doesn't use, so equivalent genomes hash the same."""
    g = dict(genome)
    if g["InpTrig"] not in TRIG_P2:
        g["InpTrigP2"] = 0.0
    for k in ("F1", "F2"):
        if g[f"Inp{k}"] == 0:
            g[f"Inp{k}P1"], g[f"Inp{k}P2"] = 0, 0.0
        elif g[f"Inp{k}"] not in FILT_P2:
            g[f"Inp{k}P2"] = 0.0
    return g


def genome_id(genome: dict) -> str:
    return hashlib.sha1(json.dumps(canonical(genome), sort_keys=True).encode()).hexdigest()[:10]


def describe(g: dict) -> str:
    t = TRIGGERS[g["InpTrig"]]
    s = f"{'inverted ' if g['InpInvert'] else ''}{t}({g['InpTrigP1']}" + \
        (f", {g['InpTrigP2']:g})" if g["InpTrig"] in TRIG_P2 else ")")
    for k in ("F1", "F2"):
        if g[f"Inp{k}"]:
            f = FILTERS[g[f"Inp{k}"]]
            s += f" + {f}({g[f'Inp{k}P1']}" + (f", {g[f'Inp{k}P2']:g})" if g[f"Inp{k}"] in FILT_P2 else ")")
    s += f" | SL {g['InpSlAtr']:g} TP {g['InpTpAtr']:g} ATR, {g['InpMaxBars']} bars, " \
         f"hours {g['InpSessionStart']}-{g['InpSessionEnd']}"
    return s


def _around(values: list, v) -> list:
    if v not in values:
        return [v]
    i = values.index(v)
    return values[max(0, i - 1): i + 2]


def local_grid(g: dict) -> dict:
    grid = {"InpTrigP1": _around(TRIG_P1[g["InpTrig"]], g["InpTrigP1"])}
    if g["InpTrig"] in TRIG_P2:
        grid["InpTrigP2"] = _around(TRIG_P2[g["InpTrig"]], g["InpTrigP2"])
    for k in ("F1", "F2"):
        f = g[f"Inp{k}"]
        if f:
            grid[f"Inp{k}P1"] = _around(FILT_P1[f], g[f"Inp{k}P1"])
            if f in FILT_P2:
                grid[f"Inp{k}P2"] = _around(FILT_P2[f], g[f"Inp{k}P2"])
    return grid


_families: dict[str, Family] = {}


def make_family(genome: dict) -> Family:
    """One Family (and Params type) per distinct genome, cached so Params compare equal."""
    g = canonical(genome)
    gid = genome_id(g)
    if gid not in _families:
        if len(_families) > 5000:
            _families.clear()
        _families[gid] = _build_family(g)
    return _families[gid]


def _build_family(g: dict) -> Family:
    fields = [(n, t, g.get(n, d)) for n, t, d in GENE_FIELDS]
    fam = Family(f"gen_{genome_id(g)}", FID, fields, local_grid(g), direction,
                 sessions=[(g["InpSessionStart"], g["InpSessionEnd"])])
    # Exits: neighbourhood of the genome's own values instead of the global rules grid.
    fam.GRID.update({"InpSlAtr": _around(SL, g["InpSlAtr"]), "InpTpAtr": _around(TP, g["InpTpAtr"]),
                     "InpMaxBars": _around(MAX_BARS, g["InpMaxBars"])})
    fam.trial_key = "generic"          # all generated strategies share one multiple-testing pool
    fam.genome = g
    return fam


def params_of(genome: dict):
    """The genome as its family's Params (exits and session included)."""
    fam = make_family(genome)
    keys = {n for n, _, _ in COMMON + GENE_FIELDS}
    return fam, fam.Params(**{k: v for k, v in canonical(genome).items() if k in keys})
