"""Strategy families. Each exposes: EXPERT, Params, GRID, signals, backtest, grid_params, neighbours."""
from . import donchian, rules

FAMILIES = {"donchian": donchian, **rules.FAMILIES}
