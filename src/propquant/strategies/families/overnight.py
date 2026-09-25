"""Overnight families: positions inside the CME session between the 18:00 open and the cash open.

Holding 18:00 -> 09:30 is intraday for CME (the session runs 18:00-17:00), so it complies with
Apex's end-of-day handling. Clock minutes: 18:00 = 1080, 09:30 = 570.
"""

import numpy as np

from propquant.engine import core
from propquant.engine.backtest import MarketData, Orders
from propquant.strategies import features as F
from propquant.strategies.base import Strategy


class OvernightDrift(Strategy):
    """Long the overnight session; optionally only after an up/down regular session."""

    name = "overnight_drift"
    family = "overnight"
    max_trades_per_session = 1
    defaults = {"entry": 1081, "exit": 570, "after": "any", "sl_pct": np.nan}
    param_space = {"entry": [1081, 1140], "exit": [570, 540], "after": ["any", "down", "up"],
                   "sl_pct": [np.nan, 0.01]}  # fmt: skip

    def orders(self, md: MarketData) -> Orders:
        p = self.params
        d = F.rth_daily(md)
        # the previous regular session (known since 16:00 yesterday = before this session opens)
        prev_ret = F.prev(d["close"] / d["open"] - 1)
        ok = np.ones_like(prev_ret, dtype=bool)
        if p["after"] == "down":
            ok = prev_ret < 0
        elif p["after"] == "up":
            ok = prev_ret > 0
        o = Orders.empty(md.n)
        go = (md.minute == p["entry"] - 1) & F.to_bars(md, ok)
        o.order_type[go] = core.MARKET
        o.order_dir[go] = 1
        if np.isfinite(p["sl_pct"]):
            o.sl_pts[go] = md.close[go] * p["sl_pct"]
        o.exit_sig |= md.minute == p["exit"] - 1
        return o
