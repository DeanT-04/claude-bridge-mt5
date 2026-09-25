"""Approval-gated deployment of strategy sleeves to the QB_Host EA.

Flow: propose() renders the exact config text and stores it with its sha256; the user reviews
it in chat; apply() writes that exact text only if the sha matches and nothing changed since.
apply() is exposed as an MCP tool that must stay behind Claude Code's permission prompt.

kill() is deliberately NOT gated: stopping trading must always be one call away.
"""
from __future__ import annotations

import difflib
import hashlib
import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path

from registry import db

from . import config

TARGETS = ("demo", "live")


@dataclass
class Sleeve:
    id: int
    family: str
    symbol: str
    timeframe: str
    risk_pct: float
    params: dict
    gauntlet_id: int | None = None
    validated: bool = False          # passed the full gauntlet (incl. MT5 confirmation)
    max_spread: float = 0.0

    def line(self) -> str:
        from research.strategies import FAMILIES
        fid = FAMILIES[self.family].fid
        kv = {"id": self.id, "family": fid, "symbol": self.symbol, "tf": self.timeframe,
              "risk": f"{self.risk_pct:.4g}", "max_spread": f"{self.max_spread:g}"}
        kv.update({k: v for k, v in self.params.items() if k != "InpFamily"})
        return "sleeve=" + ";".join(f"{k}:{v}" for k, v in kv.items())


@dataclass
class Portfolio:
    target: str
    version: int = 0
    enabled: bool = False
    balance_scale: float = 1.0
    max_daily_loss_pct: float = 5
    max_total_dd_pct: float = 30
    max_open_risk_pct: float = 6
    reset_halt: int = 0
    sleeves: list[Sleeve] = field(default_factory=list)

    def render(self) -> str:
        head = [f"# QB_Host portfolio config ({self.target}). Written by bridge/deploy.py - do not hand-edit.",
                f"version={self.version}", f"account={self.target}", f"enabled={int(self.enabled)}",
                f"balance_scale={self.balance_scale:.6g}", f"max_daily_loss_pct={self.max_daily_loss_pct:g}",
                f"max_total_dd_pct={self.max_total_dd_pct:g}", f"max_open_risk_pct={self.max_open_risk_pct:g}",
                f"reset_halt={self.reset_halt}"]
        return "\n".join(head + [s.line() for s in sorted(self.sleeves, key=lambda s: s.id)]) + "\n"


# ------------------------------------------------------------------ files
def config_path(target: str) -> Path:
    _check_target(target)
    return config.common_files() / "QB" / f"portfolio_{target}.cfg"


def status_path(target: str) -> Path:
    return config.common_files() / "QB" / f"host_status_portfolio_{target}.json"


def _check_target(target: str) -> None:
    if target not in TARGETS:
        raise ValueError(f"target must be one of {TARGETS}")
    if target == "live" and not config.settings()["account"].get("live_enabled"):
        raise PermissionError("live deployment is disabled: set account.live_enabled: true in "
                              "config/settings.yaml yourself once a live account is logged in")


def current(target: str, con=None) -> Portfolio:
    """The last applied portfolio (from the registry), or an empty disabled one."""
    con = con or db.connect()
    r = con.execute("SELECT version, sleeves, config FROM deployments WHERE target=? AND status IN "
                    "('applied','kill') ORDER BY id DESC LIMIT 1", (target,)).fetchone()
    lim = config.settings()["deployment"]
    if r is None:
        return Portfolio(target, max_daily_loss_pct=lim["max_daily_loss_pct"],
                         max_total_dd_pct=lim["max_total_dd_pct"], max_open_risk_pct=lim["max_open_risk_pct"])
    meta = json.loads(r["sleeves"])["portfolio"]
    p = Portfolio(**{k: v for k, v in meta.items() if k != "sleeves"})
    p.sleeves = [Sleeve(**s) for s in meta["sleeves"]]
    return p


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def _file_text(target: str) -> str:
    p = config_path(target)
    return p.read_text() if p.exists() else ""


# ------------------------------------------------------------------ sleeves from research
def sleeve_from_gauntlet(g: dict, sleeve_id: int, allow_unvalidated: bool) -> Sleeve:
    validated = g["verdict"] == "pass"
    if not validated and not allow_unvalidated:
        raise ValueError(f"gauntlet {g['id']} verdict is {g['verdict']!r}; pass allow_unvalidated=True "
                         "to forward-test it on demo anyway")
    params = g["params"] or {}
    if not params:
        raise ValueError(f"gauntlet {g['id']} has no final params (stopped at {next(iter(g['stages']))})")
    risk = (g["stages"].get("sizing_montecarlo", {}).get("risk") or 0) * 100
    if not validated or risk <= 0:
        risk = config.settings()["deployment"]["unvalidated_risk_pct"]
    return Sleeve(sleeve_id, g["family"], g["symbol"], g["timeframe"], round(risk, 4), params,
                  gauntlet_id=g["id"], validated=validated)


def demo_balance_scale(account: dict, rate_target_to_acct: float) -> float:
    """Scale demo equity so position sizes match the target account (e.g. £100 on a $1000 demo)."""
    target_in_acct = config.settings()["account"]["deposit"] * rate_target_to_acct
    return round(target_in_acct / account["equity"], 6) if account["equity"] > 0 else 1.0


# ------------------------------------------------------------------ propose / apply / kill
def propose(target: str, add_gauntlets: list[int] | None = None, remove_sleeves: list[int] | None = None,
            allow_unvalidated: bool = False, enabled: bool = True, limits: dict | None = None,
            balance_scale: float | None = None, reset_halt: bool = False, note: str = "",
            add_sleeves: list[Sleeve] | None = None, con=None) -> dict:
    _check_target(target)
    con = con or db.connect()
    if allow_unvalidated and target == "live":
        raise PermissionError("unvalidated sleeves may only run on demo")
    cur = current(target, con)
    new = Portfolio(**{**asdict(cur), "sleeves": []})
    new.sleeves = [s for s in cur.sleeves if s.id not in set(remove_sleeves or [])]
    next_id = max([s.id for s in cur.sleeves] + [0]) + 1
    for gid in add_gauntlets or []:
        g = db.gauntlet(con, gid)
        if g is None:
            raise ValueError(f"no gauntlet {gid}")
        key = (g["family"], g["symbol"], g["timeframe"])
        existing = next((s for s in new.sleeves if (s.family, s.symbol, s.timeframe) == key), None)
        sid = existing.id if existing else next_id
        if not existing:
            next_id += 1
        new.sleeves = [s for s in new.sleeves if s.id != sid] + [sleeve_from_gauntlet(g, sid, allow_unvalidated)]
    for s in add_sleeves or []:                  # e.g. promotion copies demo sleeves (keeping their ids)
        new.sleeves = [x for x in new.sleeves if x.id != s.id] + [s]
    for k, v in (limits or {}).items():
        if k not in ("max_daily_loss_pct", "max_total_dd_pct", "max_open_risk_pct"):
            raise ValueError(f"unknown limit {k}")
        setattr(new, k, float(v))
    if balance_scale is not None:
        new.balance_scale = balance_scale
    if target == "live" and any(not s.validated for s in new.sleeves):
        raise PermissionError("every live sleeve must have passed the gauntlet")
    new.enabled = enabled
    new.reset_halt = cur.reset_halt + (1 if reset_halt else 0)
    new.version = cur.version + 1
    text = new.render()
    sha = _sha(text)
    meta = {"portfolio": asdict(new), "base_version": cur.version, "base_sha": _sha(_file_text(target))}
    cur_text = _file_text(target)
    diff = "".join(difflib.unified_diff(cur_text.splitlines(True), text.splitlines(True),
                                        f"portfolio_{target}.cfg (current)", f"portfolio_{target}.cfg (proposed)"))
    pid = con.execute("INSERT INTO deployments(target, version, sha256, config, sleeves, status, note) "
                      "VALUES (?,?,?,?,?, 'proposed', ?)",
                      (target, new.version, sha, text, json.dumps(meta), note)).lastrowid
    con.commit()
    total_risk = sum(s.risk_pct for s in new.sleeves)
    return {"proposal_id": pid, "sha256": sha, "target": target, "version": new.version,
            "sleeves": [asdict(s) for s in new.sleeves], "sum_sleeve_risk_pct": total_risk,
            "unvalidated": [s.id for s in new.sleeves if not s.validated], "diff": diff, "config": text}


def apply(proposal_id: int, sha256: str, con=None) -> dict:
    """Write an approved proposal. Refuses if the sha differs or the file changed since proposing."""
    con = con or db.connect()
    r = con.execute("SELECT * FROM deployments WHERE id=?", (proposal_id,)).fetchone()
    if r is None or r["status"] != "proposed":
        raise ValueError(f"proposal {proposal_id} is not an open proposal")
    _check_target(r["target"])
    if r["sha256"] != sha256:
        raise ValueError("sha256 does not match the proposal the user reviewed")
    meta = json.loads(r["sleeves"])
    if _sha(_file_text(r["target"])) != meta["base_sha"]:
        raise RuntimeError("the live config changed since this proposal was made; propose again")
    _atomic_write(config_path(r["target"]), r["config"])
    con.execute("UPDATE deployments SET status='superseded' WHERE target=? AND status IN ('applied','kill')",
                (r["target"],))
    con.execute("UPDATE deployments SET status='rejected' WHERE target=? AND status='proposed' AND id<>?",
                (r["target"], proposal_id))
    con.execute("UPDATE deployments SET status='applied', applied=datetime('now') WHERE id=?", (proposal_id,))
    con.commit()
    return {"applied": proposal_id, "target": r["target"], "version": r["version"],
            "path": str(config_path(r["target"]))}


def kill(target: str, reason: str = "", con=None) -> dict:
    """Disable trading now: QB_Host closes every QB position and stops. No approval needed."""
    if target not in TARGETS:
        raise ValueError(f"target must be one of {TARGETS}")
    con = con or db.connect()
    cur = current(target, con)
    cur.enabled = False
    cur.version += 1
    text = cur.render()
    _atomic_write(config_path(target), text)
    con.execute("UPDATE deployments SET status='superseded' WHERE target=? AND status IN ('applied','kill')",
                (target,))
    con.execute("INSERT INTO deployments(target, version, sha256, config, sleeves, status, note, applied) "
                "VALUES (?,?,?,?,?, 'kill', ?, datetime('now'))",
                (target, cur.version, _sha(text), text, json.dumps({"portfolio": asdict(cur)}), reason))
    con.commit()
    return {"killed": target, "version": cur.version, "reason": reason}


def host_status(target: str) -> dict | None:
    p = status_path(target)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="cp1252"))
    except json.JSONDecodeError:
        return None          # host mid-write; caller may retry


def _atomic_write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(text, encoding="cp1252", newline="\r\n")
    os.replace(tmp, p)
