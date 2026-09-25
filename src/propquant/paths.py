"""Filesystem locations. Override with environment variables when needed."""

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = REPO_ROOT / "config"
DATA_DIR = Path(os.environ.get("PROPQUANT_DATA", REPO_ROOT / "data"))
DOCS_VAULT_DIR = REPO_ROOT / "docs" / "vault"


def vault_dir() -> Path:
    """Obsidian vault (source of truth for the knowledge base)."""
    default = Path.home() / "Documents" / "prop-quant-vault"
    return Path(os.environ.get("PROPQUANT_VAULT", default))
