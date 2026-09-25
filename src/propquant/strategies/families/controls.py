"""Control strategies. They exist to prove the gauntlet can't be fooled.

`control_random` has no edge by construction: it enters at random times in a random direction
with a fixed bracket. Its only expected result is losing the costs. If it ever gets promoted,
the gauntlet is broken.
"""

import numpy as np

from propquant.engine import core
from propquant.engine.backtest import MarketData, Orders
from propquant.strategies.base import Strategy


class RandomControl(Strategy):
    name = "control_random"
    family = "control"
    defaults = {"seed": 0, "p_entry": 0.004, "sl_pts": 20.0, "tp_pts": 20.0,
                "rth_only": True}  # fmt: skip
    param_space = {"seed": list(range(5))}

    def orders(self, md: MarketData) -> Orders:
        p = self.params
        rng = np.random.default_rng(p["seed"])
        o = Orders.empty(md.n)
        fire = rng.random(md.n) < p["p_entry"]
        if p["rth_only"]:
            fire &= (md.minute >= 9 * 60 + 30) & (md.minute < 15 * 60 + 30)
        o.order_type[fire] = core.MARKET
        o.order_dir[fire] = np.where(rng.random(md.n) < 0.5, 1, -1)[fire]
        o.sl_pts[fire] = p["sl_pts"]
        o.tp_pts[fire] = p["tp_pts"]
        return o
