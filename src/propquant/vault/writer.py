"""Write generated notes and evidence images into the vault."""

from pathlib import Path

from propquant import paths


def attachments_dir() -> Path:
    d = paths.vault_dir() / "attachments"
    d.mkdir(parents=True, exist_ok=True)
    return d


def write_note(rel_path: str, body: str) -> Path:
    """Write (or regenerate) a machine-generated note. Human notes should not use this."""
    p = paths.vault_dir() / rel_path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def md_table(rows: list[dict], cols: list[str] | None = None) -> str:
    if not rows:
        return "_none_"
    cols = cols or list(rows[0])

    def fmt(v) -> str:
        if isinstance(v, float):
            return f"{v:.4f}" if abs(v) < 10 else f"{v:,.1f}"
        return str(v)

    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    out += ["| " + " | ".join(fmt(r[c]) for c in cols) + " |" for r in rows]
    return "\n".join(out)
