"""Strategy interface and registry.

A strategy turns bars into `Orders` using only information available at each bar's close.
`param_space` lists the small, pre-registered grid the walk-forward optimiser may search; every
point it evaluates is counted as a trial.
"""

from abc import ABC, abstractmethod
from typing import ClassVar

import numpy as np

from propquant.engine.backtest import MarketData, Orders

REGISTRY: dict[str, type["Strategy"]] = {}


class Strategy(ABC):
    name: ClassVar[str]
    family: ClassVar[str]
    idea: ClassVar[str] = ""  # vault note (Ideas/...) holding the pre-registered hypothesis
    param_space: ClassVar[dict[str, list]] = {}
    defaults: ClassVar[dict] = {}
    max_trades_per_session: ClassVar[int] = 1_000_000
    needs_idea_note: ClassVar[bool] = True  # pre-registration is enforced by the gauntlet

    def __init__(self, **params) -> None:
        unknown = set(params) - set(self.defaults)
        if unknown:
            raise ValueError(f"{self.name}: unknown params {sorted(unknown)}")
        self.params = {**self.defaults, **params}

    def __init_subclass__(cls, **kw) -> None:
        super().__init_subclass__(**kw)
        if not getattr(cls, "__abstractmethods__", None):
            REGISTRY[cls.name] = cls

    @abstractmethod
    def orders(self, md: MarketData) -> Orders: ...

    def backtest(self, md: MarketData, costs):
        from propquant.engine import backtest

        return backtest.run(md, self.orders(md), costs, max_per_session=self.max_trades_per_session)

    def __repr__(self) -> str:
        return f"{self.name}({self.params})"


def session_bar_index(md: MarketData) -> np.ndarray:
    """0-based position of each bar inside its session."""
    return np.arange(md.n) - md.sess_start[md.sess]


def get(name: str) -> type[Strategy]:
    import propquant.strategies.families  # noqa: F401  (registers everything)

    return REGISTRY[name]
