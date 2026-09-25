"""One-way mirror of the Obsidian vault into the repo (docs/vault) as a git-tracked backup."""

import shutil
from dataclasses import dataclass, field
from pathlib import Path

# Obsidian UI state and trash are per-machine noise, not knowledge.
EXCLUDED_DIRS = frozenset({".obsidian", ".trash"})


@dataclass
class SyncResult:
    copied: list[Path] = field(default_factory=list)
    deleted: list[Path] = field(default_factory=list)
    unchanged: int = 0


def _vault_files(root: Path) -> set[Path]:
    return {
        p.relative_to(root)
        for p in root.rglob("*")
        if p.is_file() and not EXCLUDED_DIRS.intersection(p.relative_to(root).parts)
    }


def _same(a: Path, b: Path) -> bool:
    return a.stat().st_size == b.stat().st_size and a.read_bytes() == b.read_bytes()


def mirror(src: Path, dst: Path) -> SyncResult:
    """Make ``dst`` an exact copy of ``src`` (minus excluded dirs). ``src`` is never modified."""
    if not src.is_dir():
        raise FileNotFoundError(f"vault not found: {src}")
    dst.mkdir(parents=True, exist_ok=True)
    result = SyncResult()

    src_files = _vault_files(src)
    for rel in sorted(src_files):
        target = dst / rel
        if target.exists() and _same(src / rel, target):
            result.unchanged += 1
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src / rel, target)
        result.copied.append(rel)

    for rel in sorted(_vault_files(dst) - src_files):
        (dst / rel).unlink()
        result.deleted.append(rel)
    for d in sorted((p for p in dst.rglob("*") if p.is_dir()), reverse=True):
        if not any(d.iterdir()):
            d.rmdir()
    return result
