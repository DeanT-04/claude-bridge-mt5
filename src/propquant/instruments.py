"""Instrument specs loaded from config/instruments.yaml."""

from functools import cache
from pathlib import Path

import yaml
from pydantic import BaseModel

from propquant.paths import CONFIG_DIR


class Micro(BaseModel):
    symbol: str
    point_value: float


class Feed(BaseModel):
    source: str
    instrument: str | None = None
    ticker: str | None = None


class Instrument(BaseModel):
    symbol: str
    name: str
    tick_size: float
    point_value: float
    micro: Micro
    proxy: Feed
    futures: Feed


@cache
def load_instruments(path: Path = CONFIG_DIR / "instruments.yaml") -> dict[str, Instrument]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))["instruments"]
    return {sym: Instrument(symbol=sym, **spec) for sym, spec in raw.items()}


def get(symbol: str) -> Instrument:
    try:
        return load_instruments()[symbol]
    except KeyError:
        raise KeyError(f"unknown instrument {symbol!r}") from None
