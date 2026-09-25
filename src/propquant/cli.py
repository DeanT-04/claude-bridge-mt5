"""Command-line entry point: `uv run propquant --help`."""

import sys

import typer
from rich.console import Console

from propquant import paths
from propquant.vault.skeleton import init_vault
from propquant.vault.sync import mirror

app = typer.Typer(no_args_is_help=True, help="Prop Quant Lab research pipeline.")
vault_app = typer.Typer(no_args_is_help=True, help="Obsidian knowledge base.")
app.add_typer(vault_app, name="vault")
# Windows consoles default to cp1252; research titles contain emoji and other symbols.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")
console = Console()


@vault_app.command("init")
def vault_init() -> None:
    """Create the vault folders, Home dashboard and note templates (never overwrites)."""
    root = paths.vault_dir()
    created = init_vault(root)
    console.print(f"Vault: {root}  ({len(created)} files created)")


@vault_app.command("sync")
def vault_sync() -> None:
    """Mirror the vault into docs/vault for the git backup."""
    res = mirror(paths.vault_dir(), paths.DOCS_VAULT_DIR)
    console.print(
        f"copied {len(res.copied)}, deleted {len(res.deleted)}, unchanged {res.unchanged}"
    )


data_app = typer.Typer(no_args_is_help=True, help="Market data: download, build bars, check.")
app.add_typer(data_app, name="data")


@data_app.command("fetch")
def data_fetch(
    symbol: str = typer.Option(..., help="Instrument symbol, e.g. NQ"),
    start: str = typer.Option("2012-01-01", "--from", help="UTC start date YYYY-MM-DD"),
    pause: float = typer.Option(1.0, help="Seconds between requests (be polite)"),
) -> None:
    """Download Dukascopy bid+ask 1-minute proxy bars (resumable)."""
    from datetime import UTC, datetime

    from propquant import instruments
    from propquant.data import dukascopy

    inst = instruments.get(symbol)
    begin = datetime.fromisoformat(start).replace(tzinfo=UTC)
    for side in dukascopy.SIDES:

        def show(ts, n, side=side):
            console.print(f"{symbol} {side}: {ts:%Y-%m-%d %H:%M}  (+{n:,} bars)")

        n = dukascopy.download(
            symbol, inst.proxy.instrument, side, begin, pause=pause, progress=show
        )
        console.print(f"[bold]{symbol} {side}: {n:,} new bars[/bold]")


@data_app.command("build")
def data_build(symbol: str = typer.Option(..., help="Instrument symbol, e.g. NQ")) -> None:
    """Build mid-price 1m bars (+5m/15m/1h) from raw proxy quotes and write a quality report."""
    from datetime import date

    from propquant.data import bars, dukascopy, store
    from propquant.vault import writer

    raw = bars.mid_bars(dukascopy.load_raw(symbol, "bid"), dukascopy.load_raw(symbol, "ask"))
    one, dropped = bars.clean(raw)
    store.write_parquet(one, store.bars_path(symbol, "1m"))
    for tf in ("5m", "15m", "1h"):
        store.write_parquet(bars.resample(one, tf), store.bars_path(symbol, tf))
    q = bars.quality_report(one) | dropped | {"data_hash": store.frame_hash(one)}
    rows = [{"check": k, "value": v} for k, v in q.items()]
    writer.write_note(
        f"Reports/Data-quality-{symbol}.md",
        f"---\ntype: report\nkind: data-quality\nsymbol: {symbol}\n"
        f"generated: {date.today().isoformat()}\n---\n# Data quality: {symbol} proxy 1m bars\n\n"
        f"{writer.md_table(rows)}\n\nReproduce: `uv run propquant data build --symbol {symbol}`\n",
    )
    for r in rows:
        console.print(f"{r['check']:>28}: {r['value']}")


@data_app.command("collect")
def data_collect(symbol: str = typer.Option(..., help="Instrument symbol, e.g. NQ")) -> None:
    """Fetch real futures bars from Yahoo (1m/5m/1h) and merge them into storage."""
    from propquant import instruments
    from propquant.data import yfin

    ticker = instruments.get(symbol).futures.ticker
    for interval in yfin.PERIODS:
        new, total = yfin.collect(symbol, ticker, interval)
        console.print(f"{symbol} {interval}: +{new:,} bars (total {total:,})")


@data_app.command("tracking")
def data_tracking(symbol: str = typer.Option(..., help="Instrument symbol, e.g. NQ")) -> None:
    """Measure proxy-vs-futures fidelity; writes charts + a vault report."""
    from propquant.reports import fidelity

    res = fidelity.run(symbol)
    for r in res["timeframes"]:
        console.print(
            f"{r['timeframe']:>3}: ret_corr={r['ret_corr']:.3f} range_corr={r['range_corr']:.3f} "
            f"up={r['up_exc_corr']:.3f} down={r['down_exc_corr']:.3f} n={r['n']:,} "
            f"excluded={r['excluded_outliers']} usable={r['usable']}"
        )
    console.print(res["extremes"], res["intrabar"])


firms_app = typer.Typer(no_args_is_help=True, help="Prop-firm rules.")
app.add_typer(firms_app, name="firms")


@firms_app.command("note")
def firms_note(firm: str = typer.Argument("apex")) -> None:
    """Write the firm's verified rules into the vault."""
    from propquant.firms import note

    console.print(note.write(firm))


gauntlet_app = typer.Typer(no_args_is_help=True, help="Run strategies through the gauntlet.")
app.add_typer(gauntlet_app, name="gauntlet")


@gauntlet_app.command("run")
def gauntlet_run(
    strategy: str = typer.Argument(..., help="Registered strategy name"),
    symbol: str = typer.Option("NQ"),
    force_holdout: bool = typer.Option(False, help="Re-open the holdout (logged as forced)"),
) -> None:
    """Walk-forward -> challenge Monte Carlo -> stats -> holdout -> verdict + vault note."""
    from propquant.gauntlet import run as grun
    from propquant.reports import strategy as report

    res = grun.run(strategy, symbol, force_holdout=force_holdout, progress=console.print)
    for ck in res.checks:
        r = ck.row()
        console.print(f"  {r['result']:>4}  {r['gate']:<34} {r['value']:>10.3f}  {r['needs']}")
    console.print(f"[bold]{strategy}: {res.verdict.upper()}[/bold]  (run {res.run_id})")
    console.print(report.write(res))
    from propquant.vault import leaderboard

    leaderboard.update()


@vault_app.command("leaderboard")
def vault_leaderboard() -> None:
    """Rebuild the Home.md leaderboard from the trial registry."""
    from propquant.vault import leaderboard

    leaderboard.update()


research_app = typer.Typer(no_args_is_help=True, help="Autonomous research ingestion.")
app.add_typer(research_app, name="research")


@research_app.command("collect")
def research_collect(
    source: str = typer.Option("all", help="youtube | papers | sites | all"),
    limit: int = typer.Option(40, help="Max new items per source"),
) -> None:
    """Discover and store new videos/papers/articles (no URLs needed)."""
    from propquant.research import papers, sites, youtube
    from propquant.research.inbox import Inbox

    inbox = Inbox()
    try:
        runs = {
            "youtube": lambda: youtube.collect(inbox, limit, console.print),
            "papers": lambda: papers.collect(inbox, console.print),
            "sites": lambda: sites.collect(inbox, console.print, limit),
        }
        for name, fn in runs.items():
            if source in (name, "all"):
                console.print(f"[bold]{name}[/bold]")
                console.print(f"{name}: +{fn()} new")
        for row in inbox.counts():
            console.print(f"  {row[0]:<22} {row[1]:<11} {row[2]}")
    finally:
        inbox.close()


@research_app.command("inbox")
def research_inbox(
    status: str = typer.Option("new"), kind: str = typer.Option(None), limit: int = 30
) -> None:
    """List inbox items."""
    from propquant.research.inbox import Inbox

    inbox = Inbox()
    try:
        for r in inbox.listing(status, kind, limit):
            console.print(f"{r[0]:<48} {r[4]:>7,} chars  {r[3][:70]}")
    finally:
        inbox.close()
