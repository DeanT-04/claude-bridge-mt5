from pathlib import Path

import pytest

from propquant.vault.skeleton import FOLDERS, init_vault
from propquant.vault.sync import mirror


def test_init_creates_skeleton(tmp_path: Path) -> None:
    created = init_vault(tmp_path)
    for folder in FOLDERS:
        assert (tmp_path / folder).is_dir()
    assert (tmp_path / "Home.md").exists()
    assert (tmp_path / "_templates" / "Idea.md").exists()
    assert len(created) >= 6


def test_init_never_overwrites(tmp_path: Path) -> None:
    init_vault(tmp_path)
    home = tmp_path / "Home.md"
    home.write_text("my edits", encoding="utf-8")
    assert init_vault(tmp_path) == []
    assert home.read_text(encoding="utf-8") == "my edits"


def _write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def test_mirror_copies_updates_and_deletes(tmp_path: Path) -> None:
    src, dst = tmp_path / "vault", tmp_path / "backup"
    _write(src / "Home.md", "a")
    _write(src / "Ideas" / "orb.md", "b")
    _write(src / ".obsidian" / "workspace.json", "ui")

    res = mirror(src, dst)
    assert sorted(map(str, res.copied)) == sorted(["Home.md", str(Path("Ideas/orb.md"))])
    assert not (dst / ".obsidian").exists()

    # unchanged second run
    res = mirror(src, dst)
    assert res.copied == [] and res.unchanged == 2

    # edit + delete propagate; source untouched
    _write(src / "Home.md", "a2")
    (src / "Ideas" / "orb.md").unlink()
    res = mirror(src, dst)
    assert (dst / "Home.md").read_text(encoding="utf-8") == "a2"
    assert not (dst / "Ideas").exists()
    assert (src / ".obsidian" / "workspace.json").exists()


def test_mirror_missing_vault(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        mirror(tmp_path / "nope", tmp_path / "dst")
