"""Settings loader. Paths expand ${ENV} vars and resolve relative to the repo root."""
from __future__ import annotations

import os
import re
from functools import lru_cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"

_ENV = re.compile(r"\$\{(\w+)\}")


def _expand(value):
    if isinstance(value, str):
        return _ENV.sub(lambda m: os.environ.get(m.group(1), ""), value)
    if isinstance(value, dict):
        return {k: _expand(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_expand(v) for v in value]
    return value


@lru_cache
def settings() -> dict:
    return _expand(yaml.safe_load((CONFIG_DIR / "settings.yaml").read_text()))


@lru_cache
def gauntlet() -> dict:
    return yaml.safe_load((CONFIG_DIR / "gauntlet.yaml").read_text())


def path(p: str) -> Path:
    """Resolve a configured path; relative paths are relative to the repo root."""
    q = Path(p)
    return q if q.is_absolute() else ROOT / q


def terminal_exe() -> Path:
    return path(settings()["terminal"]["install_dir"]) / "terminal64.exe"


def tester_dir() -> Path:
    return path(settings()["tester"]["install_dir"])


def reports_dir() -> Path:
    d = path(settings()["paths"]["reports"])
    d.mkdir(parents=True, exist_ok=True)
    return d


def common_files() -> Path:
    return path(settings()["terminal"]["common_files"])
