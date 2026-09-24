"""Strategy families. Each module exposes: EXPERT, Params, GRID, signals, backtest, grid_params, neighbours."""
from . import donchian

FAMILIES = {"donchian": donchian}
