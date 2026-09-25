"""ML families (QB_ML): trade when the walk-forward model's probability clears a threshold.

direction(bars, p) uses walk-forward probabilities (no look-ahead). The final model (fitted at the
holdout boundary) is exported to Common\\Files\\QB\\models\\<id>.onnx for the MT5 tester and QB_Host.
"""
from __future__ import annotations

import numpy as np

from bridge import config

from .. import ml
from .rules import Family

FID = 8
THRESHOLDS = [0.52, 0.54, 0.56, 0.58, 0.60, 0.63, 0.66]


def model_path(family: str):
    return config.common_files() / "QB" / "models" / f"{family}.onnx"


class MLFamily(Family):
    """Family whose signal is a model probability; probabilities cached per bar array."""

    def __post_init__(self):
        super().__post_init__()
        self._proba: dict = {}

    def proba(self, bars: np.ndarray) -> np.ndarray:
        key = (bars.ctypes.data, len(bars), int(bars["time"][0]), int(bars["time"][-1]))
        if key not in self._proba:
            from .. import data
            spec = data.spec(self.spec.symbol)
            p, final = ml.walk_forward_proba(bars, self.spec, float(spec.get("spread", 0)), spec["point"])
            if final is not None and not model_path(self.name).exists():
                ml.export_onnx(final, model_path(self.name))
            self._proba = {key: p}                 # keep one: bar arrays are large
        return self._proba[key]


def _direction_for(fam_ref: dict):
    def direction(b, p):
        pr = fam_ref["fam"].proba(b)
        with np.errstate(invalid="ignore"):
            d = np.where(pr > p.InpMlThr, 1, np.where(pr < 1 - p.InpMlThr, -1, 0))
        return d.astype(np.int8)
    return direction


def make_family(spec: ml.MLSpec) -> MLFamily:
    ref: dict = {}
    k, bars = spec.label_k, spec.label_bars
    fam = MLFamily(spec.id, FID, [("InpMlThr", float, 0.56), ("InpMlModel", str, f"{spec.id}.onnx")],
                   {"InpMlThr": THRESHOLDS}, _direction_for(ref), sessions=[(0, 24)])
    ref["fam"] = fam
    fam.spec = spec
    fam.trial_key = f"ml_{spec.model}"
    # Exits stay close to what the model was trained to predict.
    fam.GRID.update({"InpSlAtr": [k], "InpTpAtr": sorted({k, round(k * 1.5, 2)}),
                     "InpMaxBars": sorted({max(bars // 2, 2), bars})})
    return fam
