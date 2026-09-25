"""The strategy catalogue: every planned (strategy, instrument, firm) test.

"x% of all strategies tested" is measured against this list. It is generated from what is
registered (every pre-registrable strategy on NQ and ES under Apex) plus the planned P7
entries (portfolios and CFD-firm versions), so the denominator is explicit and inspectable.
"""

from propquant.strategies.base import REGISTRY, get

SYMBOLS = ("NQ", "ES")
PLANNED_P7 = [
    # portfolios of families with real timing, and the CFD firms (FTMO, Blueberry Funded)
    {"key": "portfolio_timing@NQ", "stage": "P7 portfolio"},
    {"key": "portfolio_timing@NQ+ES", "stage": "P7 portfolio"},
    {"key": "portfolio_best@NQ+ES", "stage": "P7 portfolio"},
    {"key": "ftmo:best", "stage": "P7 FTMO"},
    {"key": "blueberry:best", "stage": "P7 Blueberry"},
]


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
