"""ML strategies: features, labels, walk-forward training and ONNX export.

Features are computed on the closed bar before the entry bar, from MT5 built-in indicators, and
must match CSigML in mql5/Include/QB/Signals.mqh exactly (FEATURES order = model input order).

Label: does a LONG trade entered at the bar's open, with a symmetric ATR stop/target
(label_k × ATR14[1]) and a time exit after label_bars, finish with R > 0? With symmetric exits one
model serves both sides: long if p > t, short if p < 1 - t.

Predictions are walk-forward: models retrain on an expanding window every `retrain_months`, with
the last `label_bars` bars before each cut purged so labels never see the future, plus a forced
cut at the holdout boundary. That last model is the one exported to ONNX.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass

import numpy as np

from bridge import config

from . import indicators as ind
from .engine import atr_sma, server_hour

FEATURES = ["ret1", "ret4", "ret12", "ret24", "dist_ema20", "dist_ema100", "rsi14", "atr_ratio",
            "range1", "hour_sin", "hour_cos", "chan_pos20"]
WARMUP = 120      # bars before features are trusted (EMA100 / ATR100 settle)


@dataclass(frozen=True)
class MLSpec:
    symbol: str
    timeframe: str
    model: str = "logreg"          # logreg | gbm
    label_k: float = 1.5           # stop = target = k × ATR14
    label_bars: int = 24           # time exit for labelling
    retrain_months: int = 6
    min_train_months: int = 24

    @property
    def id(self) -> str:
        return "ml_" + hashlib.sha1(json.dumps(asdict(self), sort_keys=True).encode()).hexdigest()[:10]


def register(symbol: str, timeframe: str, model: str = "logreg", label_k: float = 1.5,
             label_bars: int = 24, con=None) -> str:
    """Store an ML spec so its family ('ml_<hash>') resolves anywhere; returns the family name."""
    from registry import db
    spec = MLSpec(symbol, timeframe, model, label_k, label_bars)
    db.save_ml_spec(con or db.connect(), spec.id, asdict(spec))
    return spec.id


# ------------------------------------------------------------------ features / labels
def _lag(x, k=1):
    out = np.full(len(x), np.nan)
    out[k:] = x[:len(x) - k]
    return out


def features(b: np.ndarray) -> np.ndarray:
    """[n, 12] float32; row i describes closed bar i-1 (for an entry at bar i's open)."""
    c, h, l = b["close"].astype(float), b["high"].astype(float), b["low"].astype(float)
    a14, a100 = atr_sma(b, 14), atr_sma(b, 100)
    e20, e100 = ind.ema(c, 20), ind.ema(c, 100)
    r14 = ind.rsi(c, 14)
    n = len(b)
    with np.errstate(invalid="ignore", divide="ignore"):
        def ret(k):
            out = np.full(n, np.nan)
            out[k:] = c[k:] - c[:n - k]
            return out / a14
        hh = np.full(n, np.nan); ll = np.full(n, np.nan)
        if n >= 20:
            hh[19:] = np.lib.stride_tricks.sliding_window_view(h, 20).max(axis=1)
            ll[19:] = np.lib.stride_tricks.sliding_window_view(l, 20).min(axis=1)
        cols_on_bar = [ret(1), ret(4), ret(12), ret(24), (c - e20) / a14, (c - e100) / a14, r14 / 100.0,
                       a14 / a100, (h - l) / a14, None, None, (c - ll) / (hh - ll)]
    hour = server_hour(b).astype(float)            # hour of the ENTRY bar (bar 0)
    out = np.full((n, len(FEATURES)), np.nan)
    for j, col in enumerate(cols_on_bar):
        if col is not None:
            out[:, j] = _lag(col, 1)
    out[:, 9] = np.sin(2 * np.pi * hour / 24)
    out[:, 10] = np.cos(2 * np.pi * hour / 24)
    out[:WARMUP] = np.nan
    return out.astype(np.float32)


def labels(b: np.ndarray, k: float, bars: int, spread_points: float, point: float) -> np.ndarray:
    """1 if a long entered at bar i's open (ask) wins, 0 if it loses, NaN if not resolvable."""
    o, h, l, c = b["open"], b["high"], b["low"], b["close"]
    n = len(b)
    a1 = _lag(atr_sma(b, 14), 1)
    spr = np.maximum(b["spread"].astype(float), spread_points) * point
    entry = o + spr
    sl, tp = entry - k * a1, entry + k * a1
    y = np.full(n, np.nan)
    done = np.zeros(n, bool) | ~np.isfinite(a1)
    for j in range(bars):
        idx = np.arange(n - j)
        rows = idx[~done[: n - j]]
        if not len(rows):
            break
        hit_sl = l[rows + j] <= sl[rows]
        hit_tp = h[rows + j] >= tp[rows]
        y[rows[hit_sl]] = 0                                   # SL first when both in one bar
        y[rows[hit_tp & ~hit_sl]] = 1
        done[rows[hit_sl | hit_tp]] = True
    rows = np.flatnonzero(~done[: n - bars])
    y[rows] = (o[rows + bars] > entry[rows]).astype(float)    # time exit at the open
    return y


# ------------------------------------------------------------------ models
def make_model(kind: str):
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    if kind == "logreg":
        return make_pipeline(StandardScaler(), LogisticRegression(C=0.1, max_iter=1000))
    if kind == "gbm":
        return GradientBoostingClassifier(n_estimators=150, max_depth=3, learning_rate=0.05,
                                          subsample=0.7, min_samples_leaf=200, random_state=0)
    raise ValueError(kind)


def _month_ts(ts, m):
    from .gauntlet import _month_ts as f
    return f(ts, m)


def cut_points(t: np.ndarray, spec: MLSpec) -> list[int]:
    """Bar indices where a new model takes over (expanding-window retrains + holdout boundary)."""
    hold = int(np.searchsorted(t, _month_ts(int(t[-1]), -config.settings()["research"]["holdout_months"])))
    cuts, ts = [], _month_ts(int(t[0]), spec.min_train_months)
    while True:
        i = int(np.searchsorted(t, ts))
        if i >= hold:
            break
        cuts.append(i)
        ts = _month_ts(ts, spec.retrain_months)
    return sorted(set(cuts + [hold]))


def _fit(X, y, kind, upto: int, purge: int):
    m = np.isfinite(y[:upto - purge]) & np.all(np.isfinite(X[:upto - purge]), axis=1)
    if m.sum() < 500 or len(np.unique(y[:upto - purge][m])) < 2:
        return None
    model = make_model(kind)
    model.fit(X[:upto - purge][m], y[:upto - purge][m].astype(int))
    return model


def walk_forward_proba(b: np.ndarray, spec: MLSpec, spread_points: float, point: float):
    """(proba[n] with NaN before the first cut, final model fitted at the holdout boundary)."""
    X = features(b)
    y = labels(b, spec.label_k, spec.label_bars, spread_points, point)
    cuts = cut_points(b["time"], spec)
    p = np.full(len(b), np.nan)
    final = None
    for k, cut in enumerate(cuts):
        model = _fit(X, y, spec.model, cut, spec.label_bars)
        if model is None:
            continue
        nxt = cuts[k + 1] if k + 1 < len(cuts) else len(b)
        seg = X[cut:nxt]
        ok = np.all(np.isfinite(seg), axis=1)
        if ok.any():
            p[cut:nxt][ok] = model.predict_proba(seg[ok])[:, 1]
        final = model
    return p.astype(np.float32), final


def export_onnx(model, path) -> None:
    from skl2onnx import to_onnx
    est = model.steps[-1][1] if hasattr(model, "steps") else model
    onx = to_onnx(model, np.zeros((1, len(FEATURES)), np.float32), options={id(est): {"zipmap": False}},
                  target_opset=15)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(onx.SerializeToString())


def onnx_proba(path, X: np.ndarray) -> np.ndarray:
    import onnxruntime as ort
    s = ort.InferenceSession(str(path))
    ok = np.all(np.isfinite(X), axis=1)
    out = np.full(len(X), np.nan, np.float32)
    if ok.any():
        out[ok] = s.run(None, {s.get_inputs()[0].name: X[ok].astype(np.float32)})[1][:, 1]
    return out
