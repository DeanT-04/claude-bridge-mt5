"""Sync repo MQL5 sources into a terminal's MQL5 folder and compile with MetaEditor."""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

from . import config

SRC = config.ROOT / "mql5"
# Only these subtrees are ever written into a terminal, so the user's other EAs stay untouched.
OWNED = [Path("Include/QB"), Path("Experts/QB")]


def mql5_root(install_dir: Path | None = None) -> Path:
    """MQL5 folder of the portable tester copy (default) or a given portable install."""
    return (install_dir or config.tester_dir()) / "MQL5"


def sync(dest_mql5: Path | None = None) -> Path:
    dest = dest_mql5 or mql5_root()
    for sub in OWNED:
        src = SRC / sub
        if src.exists():
            shutil.copytree(src, dest / sub, dirs_exist_ok=True)
    return dest


def compile_expert(name: str, dest_mql5: Path | None = None) -> dict:
    """Compile Experts/QB/<name>.mq5. Returns {ok, errors, warnings, log, ex5}."""
    dest = sync(dest_mql5)
    src = dest / "Experts" / "QB" / f"{name}.mq5"
    if not src.exists():
        raise FileNotFoundError(src)
    log = src.with_suffix(".log")
    log.unlink(missing_ok=True)
    editor = config.tester_dir() / "MetaEditor64.exe"
    subprocess.run([str(editor), f"/compile:{src}", f"/inc:{dest}", f"/log:{log}"],
                   timeout=300, check=False)
    text = _read_log(log)
    m = re.search(r"(\d+) errors?, (\d+) warnings?", text)
    errors, warnings = (int(m.group(1)), int(m.group(2))) if m else (-1, -1)
    ex5 = src.with_suffix(".ex5")
    issues = [ln for ln in text.splitlines() if re.search(r"\b(error|warning)\b", ln, re.I)
              and not re.search(r"\d+ errors?, \d+ warnings?", ln)]
    return {"ok": errors == 0 and ex5.exists(), "errors": errors, "warnings": warnings,
            "issues": issues[:50], "ex5": str(ex5)}


def _read_log(p: Path) -> str:
    if not p.exists():
        return ""
    raw = p.read_bytes()
    for enc in ("utf-16", "utf-8", "cp1252"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1")
