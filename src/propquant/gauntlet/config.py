"""Load the pre-registered research protocol (config/research.yaml)."""

from datetime import date
from functools import cache

import yaml

from propquant.paths import CONFIG_DIR


@cache
def load() -> dict:
    return yaml.safe_load((CONFIG_DIR / "research.yaml").read_text(encoding="utf-8"))


def day_number(d: date) -> int:
    return (d - date(1970, 1, 1)).days
