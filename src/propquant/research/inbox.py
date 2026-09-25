"""Research inbox: every collected video/paper/article, deduplicated, with its text on disk.

Collected text is third-party material: it stays under data/ (gitignored). The vault only
ever receives our own summaries.
"""

import hashlib
import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from functools import cache
from pathlib import Path

import duckdb
import yaml

from propquant import paths

SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
    id VARCHAR PRIMARY KEY, kind VARCHAR, source VARCHAR, url VARCHAR, title VARCHAR,
    author VARCHAR, published VARCHAR, meta VARCHAR, query VARCHAR, fetched_at TIMESTAMP,
    text_file VARCHAR, chars INTEGER, status VARCHAR
);
"""
STATUSES = ("new", "read", "formalised", "rejected")


@cache
def sources_config() -> dict:
    return yaml.safe_load((paths.CONFIG_DIR / "research_sources.yaml").read_text("utf-8"))


@dataclass
class Item:
    id: str
    kind: str  # video | paper | article
    source: str
    url: str
    title: str
    author: str = ""
    published: str = ""
    query: str = ""
    meta: dict = field(default_factory=dict)


def clean(s: str) -> str:
    """Drop unencodable characters (lone surrogates from PDF extraction)."""
    return s.encode("utf-8", "replace").decode("utf-8")


class Inbox:
    def __init__(self, root: Path | None = None) -> None:
        self.root = root or paths.DATA_DIR / "research"
        (self.root / "text").mkdir(parents=True, exist_ok=True)
        self.con = duckdb.connect(str(self.root / "inbox.duckdb"))
        self.con.execute(SCHEMA)

    def close(self) -> None:
        self.con.close()

    def has(self, item_id: str) -> bool:
        return bool(self.con.execute("SELECT 1 FROM items WHERE id = ?", [item_id]).fetchone())

    def add(self, item: Item, text: str) -> bool:
        """Store an item and its text. Returns False if it was already there."""
        if self.has(item.id):
            return False
        text, item.title = clean(text), clean(item.title)
        name = hashlib.sha1(item.id.encode()).hexdigest()[:16] + ".txt"
        (self.root / "text" / name).write_text(text, encoding="utf-8")
        self.con.execute(
            "INSERT INTO items VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [item.id, item.kind, item.source, item.url, item.title, item.author,
             item.published, json.dumps(item.meta, default=str), item.query,
             datetime.now(UTC), name, len(text), "new"],
        )  # fmt: skip
        return True

    def text(self, item_id: str) -> str:
        row = self.con.execute("SELECT text_file FROM items WHERE id = ?", [item_id]).fetchone()
        if not row:
            raise KeyError(item_id)
        return (self.root / "text" / row[0]).read_text(encoding="utf-8")

    def set_status(self, item_id: str, status: str) -> None:
        if status not in STATUSES:
            raise ValueError(status)
        self.con.execute("UPDATE items SET status = ? WHERE id = ?", [status, item_id])

    def listing(self, status: str | None = "new", kind: str | None = None, limit: int = 50):
        q = "SELECT id, kind, source, title, chars, status, url FROM items WHERE 1=1"
        args: list = []
        if status:
            q += " AND status = ?"
            args.append(status)
        if kind:
            q += " AND kind = ?"
            args.append(kind)
        q += " ORDER BY fetched_at DESC LIMIT ?"
        args.append(limit)
        return self.con.execute(q, args).fetchall()

    def counts(self) -> list[tuple]:
        return self.con.execute(
            "SELECT source, status, count(*) FROM items GROUP BY 1, 2 ORDER BY 1, 2"
        ).fetchall()
