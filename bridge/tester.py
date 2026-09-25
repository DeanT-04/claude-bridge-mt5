"""Strategy Tester automation: build job .ini, run the portable tester copy, parse outputs."""
from __future__ import annotations

import csv
import re
import subprocess
import time
import uuid
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

from lxml import etree, html

from . import config

MODEL = {"every_tick": 0, "ohlc_m1": 1, "open_prices": 2, "math": 3, "real_ticks": 4}
OPT_MODE = {"none": 0, "slow": 1, "genetic": 2, "all_symbols": 3}
# 0 balance, 1 PF, 2 expected payoff, 3 DD, 4 recovery factor, 5 Sharpe, 6 custom (OnTester), 7 complex
CRITERION = {"balance": 0, "profit_factor": 1, "payoff": 2, "drawdown": 3, "recovery": 4,
             "sharpe": 5, "custom": 6, "complex": 7}


@dataclass
class Param:
    value: float | int | str | bool
    start: float | None = None
    step: float | None = None
    stop: float | None = None

    @property
    def optimise(self) -> bool:
        return self.start is not None and self.step is not None and self.stop is not None

    def ini(self) -> str:
        v = _fmt(self.value)
        if isinstance(self.value, str):
            return v           # string inputs are taken literally; the range syntax would corrupt them
        if self.optimise:
            return f"{v}||{_fmt(self.start)}||{_fmt(self.step)}||{_fmt(self.stop)}||Y"
        return f"{v}||{v}||0||{v}||N"


@dataclass
class Job:
    expert: str                     # e.g. "QB\\QB_Donchian.ex5" relative to MQL5\Experts
    symbol: str
    period: str                     # M15/H1/...
    date_from: date
    date_to: date
    params: dict[str, Param] = field(default_factory=dict)
    model: str = "ohlc_m1"
    optimisation: str = "none"
    criterion: str = "custom"
    forward_date: date | None = None   # MT5's built-in forward split (ForwardMode=4)
    spread: int | None = None          # fixed spread in points; None = current/historical
    delay_ms: int = 0                  # ExecutionMode latency
    tag: str = field(default_factory=lambda: uuid.uuid4().hex[:12])

    deposit: float | None = None       # in tester currency; default = target deposit converted
    currency: str | None = None

    def ini_text(self) -> str:
        acc = config.settings()["account"]
        currency = self.currency or config.settings()["tester"].get("currency", acc["currency"])
        deposit = self.deposit if self.deposit is not None else tester_deposit(currency)
        lines = ["[Tester]",
                 f"Expert={self.expert}",
                 f"Symbol={self.symbol}",
                 f"Period={self.period}",
                 f"Model={MODEL[self.model]}",
                 f"ExecutionMode={self.delay_ms}",
                 f"Optimization={OPT_MODE[self.optimisation]}",
                 f"OptimizationCriterion={CRITERION[self.criterion]}",
                 f"FromDate={self.date_from:%Y.%m.%d}",
                 f"ToDate={self.date_to:%Y.%m.%d}",
                 f"Deposit={deposit:g}",
                 f"Currency={currency}",
                 f"Leverage=1:{acc['leverage']}",
                 f"Report={self.report_rel}",
                 "ReplaceReport=1",
                 "ShutdownTerminal=1",
                 "Visual=0",
                 "UseLocal=1",
                 "UseRemote=0",
                 "UseCloud=0"]
        if self.forward_date:
            lines += ["ForwardMode=4", f"ForwardDate={self.forward_date:%Y.%m.%d}"]
        else:
            lines.append("ForwardMode=0")
        if self.spread is not None:
            lines.append(f"Spread={self.spread}")
        # The tester silently reuses the previous run's value for any input left out, so always
        # write every input: explicit params first, then the defaults declared in the source.
        params = {k: Param(v) for k, v in ea_input_defaults(self.expert).items()}
        params.update(self.params)
        params["InpRunTag"] = self.params.get("InpRunTag", Param(self.tag))
        lines.append("[TesterInputs]")
        lines += [f"{k}={p.ini()}" for k, p in params.items()]
        return "\r\n".join(lines) + "\r\n"

    @property
    def report_rel(self) -> str:
        return f"reports\\{self.tag}"


_INPUT_RE = re.compile(r"^\s*input\s+(\w+)\s+(\w+)\s*=\s*([^;]+);", re.M)
_INCLUDE_RE = re.compile(r'^\s*#include\s+<(QB\\[^>]+)>', re.M)


def ea_input_defaults(expert: str) -> dict:
    """Default values of every `input` in an EA and the QB headers it includes.
    expert: 'QB\\QB_Rules.ex5' (relative to MQL5\\Experts). Enum defaults resolve to their values."""
    src_root = config.ROOT / "mql5"
    src = src_root / "Experts" / expert.replace(".ex5", ".mq5")
    if not src.exists():
        return {}
    texts, seen, todo = [], set(), [src]
    while todo:
        f = todo.pop()
        if f in seen or not f.exists():
            continue
        seen.add(f)
        t = f.read_text(encoding="utf-8", errors="replace")
        texts.append(t)
        todo += [src_root / "Include" / m for m in _INCLUDE_RE.findall(t)]
    enums = {}
    for t in texts:
        for name, val in re.findall(r"^\s*(QB_\w+)\s*=\s*(\d+)\s*,", t, re.M):
            enums[name] = int(val)
    out = {}
    for t in texts:
        for typ, name, raw in _INPUT_RE.findall(t):
            raw = raw.split("//")[0].strip()
            if typ == "string":
                out[name] = raw.strip('"')
            elif typ in ("double", "float"):
                out[name] = float(raw)
            elif typ == "bool":
                out[name] = raw == "true"
            elif raw in enums:
                out[name] = enums[raw]
            else:
                try:
                    out[name] = int(raw)
                except ValueError:
                    continue
    return out


def tester_deposit(currency: str) -> float:
    """Target account deposit expressed in the tester currency (rounded to whole units)."""
    acc = config.settings()["account"]
    if currency == acc["currency"]:
        return float(acc["deposit"])
    from . import mt5_client
    for sym, invert in ((acc["currency"] + currency, False), (currency + acc["currency"], True)):
        try:
            px = mt5_client.symbol_spec(sym)["bid"]
        except Exception:
            continue
        if px:
            return float(round(acc["deposit"] * (1 / px if invert else px)))
    raise RuntimeError(f"no rate to convert {acc['currency']} deposit to {currency}")


@dataclass
class Result:
    job: Job
    ok: bool
    seconds: float
    summary: dict
    trades: list[dict]
    passes: list[dict]            # optimisation passes (in-sample)
    forward_passes: list[dict]    # optimisation passes on the forward segment
    error: str = ""


def run(job: Job, timeout: int | None = None) -> Result:
    tdir = config.tester_dir()
    if not (tdir / "MQL5").exists():
        raise RuntimeError("tester copy not initialised: launch runtime\\tester\\terminal64.exe /portable "
                           "once and log into the demo account")
    ini = config.reports_dir() / f"{job.tag}.ini"
    # MT5 reads config files as UTF-16LE with BOM most reliably.
    ini.write_text(job.ini_text(), encoding="utf-16")
    (tdir / "reports").mkdir(exist_ok=True)
    trades_csv = config.common_files() / "QB" / f"trades_{job.tag}.csv"
    trades_csv.unlink(missing_ok=True)

    t0 = time.time()
    timeout = timeout or config.settings()["tester"]["timeout_sec"]
    try:
        subprocess.run([str(tdir / "terminal64.exe"), "/portable", f"/config:{ini}"],
                       timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        _kill_tester(tdir)
        return Result(job, False, time.time() - t0, {}, [], [], [], error=f"timeout after {timeout}s")
    secs = time.time() - t0

    base = tdir / job.report_rel
    summary = parse_report(_first_existing(base, [".htm", ".html"]))
    passes = parse_opt_xml(_first_existing(base, [".xml"]))
    fwd = parse_opt_xml(_first_existing(Path(str(base) + ".forward"), [".xml"]))
    trades = parse_trades(trades_csv)
    # A report of zeros (bars == 0) means the test aborted, e.g. missing history.
    ok = bool(passes) or bool(summary.get("bars"))
    err = "" if ok else (_tester_errors(tdir, t0) or "no report produced")
    return Result(job, ok, secs, summary, trades, passes, fwd, error=err)


def _tester_errors(tdir: Path, since: float) -> str:
    """Error/stop lines from today's tester log written after `since`."""
    logs = sorted((tdir / "Tester" / "logs").glob("*.log"), key=lambda p: p.stat().st_mtime)
    if not logs or logs[-1].stat().st_mtime < since:
        return ""
    lines = _decode(logs[-1]).splitlines()
    t0 = time.strftime("%H:%M:%S", time.localtime(since))
    bad = [ln.split("\t", 3)[-1] for ln in lines
           if re.search(r"error|stop testing|out of this range|failed|cannot", ln, re.I)
           and len(ln.split("\t")) > 2 and ln.split("\t")[2][:8] >= t0]
    return " | ".join(bad[-5:])


def _kill_tester(tdir: Path) -> None:
    exe = str(tdir / "terminal64.exe").replace("'", "''")
    subprocess.run(["powershell", "-NoProfile", "-Command",
                    f"Get-Process terminal64 -ErrorAction SilentlyContinue | "
                    f"Where-Object {{ $_.Path -eq '{exe}' }} | Stop-Process -Force"], check=False)


def _first_existing(base: Path, exts: list[str]) -> Path | None:
    for e in exts:
        p = base.with_name(base.name + e)
        if p.exists():
            return p
    return None


def _decode(p: Path) -> str:
    raw = p.read_bytes()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return raw.decode("utf-16")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("utf-16", errors="replace")


# --- report parsing --------------------------------------------------------------------

_SUMMARY_KEYS = {
    "Total Net Profit": "net_profit", "Gross Profit": "gross_profit", "Gross Loss": "gross_loss",
    "Profit Factor": "profit_factor", "Expected Payoff": "expected_payoff",
    "Recovery Factor": "recovery_factor", "Sharpe Ratio": "sharpe", "Total Trades": "trades",
    "Balance Drawdown Maximal": "balance_dd_max", "Equity Drawdown Maximal": "equity_dd_max",
    "Equity Drawdown Relative": "equity_dd_rel", "History Quality": "history_quality",
    "Initial Deposit": "deposit", "Bars": "bars", "OnTester result": "ontester",
}


def parse_report(p: Path | None) -> dict:
    """Pull headline stats from the single-test HTML report."""
    if p is None:
        return {}
    doc = html.fromstring(_decode(p))
    out: dict = {}
    for td in doc.iter("td"):
        label = (td.text_content() or "").strip().rstrip(":")
        key = _SUMMARY_KEYS.get(label)
        if not key or key in out:
            continue
        nxt = td.getnext()
        while nxt is not None and not (nxt.text_content() or "").strip():
            nxt = nxt.getnext()
        if nxt is not None:
            out[key] = _num(nxt.text_content())
    return out


def _num(s: str):
    s = s.strip()
    m = re.match(r"^\s*([-\d\s.,]+)\s*(?:\(([-\d.,\s]+)%\))?", s)
    if not m:
        return s
    first = m.group(1).replace(" ", "").replace(",", "")
    try:
        v = float(first)
    except ValueError:
        return s
    if m.group(2):
        pct = float(m.group(2).replace(" ", "").replace(",", ""))
        return {"value": v, "pct": pct}
    return v


def parse_opt_xml(p: Path | None) -> list[dict]:
    """Optimisation results are an Excel 2003 XML spreadsheet: header row then one row per pass."""
    if p is None:
        return []
    root = etree.fromstring(p.read_bytes())
    ns = {"ss": "urn:schemas-microsoft-com:office:spreadsheet"}
    rows = root.findall(".//ss:Worksheet/ss:Table/ss:Row", ns)
    if not rows:
        return []
    cells = lambda r: [(c.findtext("ss:Data", default="", namespaces=ns) or "").strip()
                       for c in r.findall("ss:Cell", ns)]
    header = cells(rows[0])
    out = []
    for r in rows[1:]:
        vals = cells(r)
        d = {}
        for k, v in zip(header, vals):
            try:
                d[k] = float(v)
            except ValueError:
                d[k] = v
        out.append(d)
    return out


def parse_trades(p: Path) -> list[dict]:
    if not p.exists():
        return []
    with p.open(newline="", encoding="cp1252") as f:
        rows = list(csv.DictReader(f))
    out = []
    for r in rows:
        out.append({
            "position_id": int(r["position_id"]), "symbol": r["symbol"],
            "direction": int(r["direction"]), "volume": float(r["volume"]),
            "open_time": datetime.strptime(r["open_time"], "%Y.%m.%d %H:%M:%S"),
            "open_price": float(r["open_price"]),
            "close_time": datetime.strptime(r["close_time"], "%Y.%m.%d %H:%M:%S"),
            "close_price": float(r["close_price"]), "sl": float(r["sl"]),
            "profit": float(r["profit"]), "commission": float(r["commission"]),
            "swap": float(r["swap"]),
        })
    return out


def _fmt(v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float):
        return f"{v:g}"
    return str(v)
