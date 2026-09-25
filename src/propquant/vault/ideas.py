"""Pre-registered hypotheses (vault Ideas/<strategy>.md).

The gauntlet refuses to test a strategy whose Idea note is missing. The note's content hash is
stored with every run, so a hypothesis edited after the fact is visible.
"""

import hashlib
from datetime import date

from propquant import paths
from propquant.vault import writer


class MissingIdea(RuntimeError):
    pass


def path(name: str):
    return paths.vault_dir() / "Ideas" / f"{name}.md"


def require(name: str) -> str:
    p = path(name)
    if not p.exists():
        raise MissingIdea(
            f"{name}: no pre-registered hypothesis at {p}. Write the Idea note first "
            "(hypothesis, mechanism, exact rules, fixed parameter ranges)."
        )
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def write(name: str, family: str, *, hypothesis: str, mechanism: str, rules: str,
          params: dict[str, tuple[list, str]], failure_modes: str, sources: list[str],
          instruments: tuple[str, ...] = ("NQ",)) -> str:  # fmt: skip
    """Create the Idea note. Refuses to overwrite: pre-registration is write-once."""
    p = path(name)
    if p.exists():
        raise FileExistsError(f"{p} already exists (pre-registrations are write-once)")
    rows = [{"param": k, "values": v, "why": why} for k, (v, why) in params.items()]
    src = "\n".join(f"- {s}" for s in sources) or "- Claude (original)"
    body = f"""---
type: idea
status: pre-registered
created: {date.today().isoformat()}
family: {family}
instruments: {list(instruments)}
strategy: {name}
---
# {name}

## Hypothesis
{hypothesis}

## Mechanism
{mechanism}

## Exact rules
{rules}

## Parameter ranges (fixed before testing)
{writer.md_table(rows)}

## Expected failure modes
{failure_modes}

## Sources
{src}
"""
    return str(writer.write_note(f"Ideas/{name}.md", body))
