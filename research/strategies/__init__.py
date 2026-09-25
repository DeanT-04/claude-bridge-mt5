"""Strategy families. Each exposes: EXPERT, fid, Params, GRID, signals, backtest, grid_params, neighbours.

Fixed families live in FAMILIES; generated ones ("gen_<hash>") are rebuilt from the genome
stored in the registry, so any process (queue workers, deploy, monitor) can resolve them.
"""
from . import donchian, rules

FAMILIES = {"donchian": donchian, **rules.FAMILIES}
_generated: dict = {}


def get_family(name: str):
    if name in FAMILIES:
        return FAMILIES[name]
    if name.startswith("gen_"):
        if name not in _generated:
            from registry import db
            from . import generic
            g = db.get_genome(db.connect(), name)
            if g is None:
                raise KeyError(f"unknown generated family {name!r}")
            _generated[name] = generic.make_family(g)
        return _generated[name]
    raise KeyError(f"unknown family {name!r}")


def is_known(name: str) -> bool:
    try:
        get_family(name)
        return True
    except KeyError:
        return False
