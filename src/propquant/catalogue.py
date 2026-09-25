"""The strategy catalogue: every planned (strategy, instrument, firm) test.

"x% of all strategies tested" is measured against this list. It is generated from what is
registered (every pre-registrable strategy on NQ and ES under Apex) plus the planned P7
entries (portfolios and CFD-firm versions), so the denominator is explicit and inspectable.
"""

from propquant.strategies.base import REGISTRY, get

SYMBOLS = ("NQ", "ES")
TIMING_FAMILIES = ("late_trend", "orb", "ib_breakout", "macd_trend_5m", "donchian_break_15m",
                   "donchian_break_5m", "supertrend_5m", "ib_twap")  # fmt: skip
PLANNED_P7 = (
    # the timing portfolio, and CFD-firm transfers of the families with real timing
    [{"key": "portfolio_timing", "stage": "P7 portfolio"}]
    + [{"key": f"ftmo:{n}", "stage": "P7 FTMO"} for n in TIMING_FAMILIES]
    + [{"key": f"blueberry:{n}", "stage": "P7 Blueberry"} for n in TIMING_FAMILIES]
)


def catalogue() -> list[dict]:
    get("orb")  # registers every family
    out = []
    for name, cls in sorted(REGISTRY.items()):
        if not cls.needs_idea_note:
            continue
        for sym in SYMBOLS:
            out.append({"key": name if sym == "NQ" else f"{name}@{sym}", "strategy": name,
                        "symbol": sym, "family": cls.family, "stage": "P6"})  # fmt: skip
    out += [{"strategy": e["key"], "symbol": "", "family": "", **e} for e in PLANNED_P7]
    return out
