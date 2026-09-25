"""Proxy-fidelity evidence: charts + vault note comparing proxy bars with real futures."""

from dataclasses import asdict
from datetime import date

import matplotlib.pyplot as plt
import numpy as np
import polars as pl

from propquant.data import store, yfin
from propquant.data.bars import TZ
from propquant.data.tracking import (
    align,
    fidelity,
    intrabar_order_agreement,
    outlier_mask,
    session_extreme_agreement,
)
from propquant.reports import style
from propquant.vault import writer

TIMEFRAMES = (("1m", 1), ("5m", 5), ("1h", 60))

# Bar-level thresholds for calling a timeframe "usable" for backtests. Set before looking at
# results; intentionally strict because stops/targets are filled from these highs/lows.
USABLE = {"ret_corr": 0.95, "range_corr": 0.85, "up_exc_corr": 0.85, "down_exc_corr": 0.85}


def _proxy_at(symbol: str, tf: str) -> pl.DataFrame:
    return pl.read_parquet(store.bars_path(symbol, tf))


def run(symbol: str) -> dict:
    style.apply()
    results, aligned = [], {}
    for tf, minutes in TIMEFRAMES:
        proxy, fut = _proxy_at(symbol, tf), yfin.load(symbol, tf)
        fid = fidelity(proxy, fut, tf, minutes)
        verdict = all(getattr(fid, k) >= v for k, v in USABLE.items())
        results.append({**asdict(fid), "usable": "yes" if verdict else "NO"})
        aligned[tf] = align(proxy, fut, minutes).drop_nulls(["rp", "rf"])

    p1, f1 = _proxy_at(symbol, "1m"), yfin.load(symbol, "1m")
    extremes = session_extreme_agreement(p1, f1)
    order = intrabar_order_agreement(p1, f1, "15m")

    slug = f"proxy-fidelity-{symbol}"
    _scatter(aligned, results, f"{slug}-scatter.png")
    _rolling(aligned["1h"], f"{slug}-rolling.png")
    _overlay(p1, f1, f"{slug}-overlay.png")
    _write_note(symbol, slug, results, extremes, order)
    return {"timeframes": results, "extremes": extremes, "intrabar": order}


def _scatter(aligned: dict[str, pl.DataFrame], results: list[dict], name: str) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for ax, (tf, _), res in zip(axes, TIMEFRAMES, results, strict=True):
        a = aligned[tf]
        rp, rf = a["rp"].to_numpy() * 1e4, a["rf"].to_numpy() * 1e4
        bad = outlier_mask(rp, rf)
        ax.scatter(rp[~bad], rf[~bad], s=3, alpha=0.35, color=style.SERIES[0], linewidths=0)
        lim = np.percentile(np.abs(np.concatenate([rp, rf])), 99.5)
        ax.plot([-lim, lim], [-lim, lim], color=style.NEUTRAL, lw=1, ls="--")
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_title(f"{tf} returns  (r = {res['ret_corr']:.3f}, n = {res['n']:,})")
        ax.set_xlabel("proxy return (bps)")
        ax.set_ylabel("futures return (bps)")
    fig.suptitle("Proxy vs real futures bar returns (dashed = perfect tracking)", x=0.01, ha="left")
    style.save(fig, writer.attachments_dir() / name)


def _rolling(a1h: pl.DataFrame, name: str) -> None:
    bad = outlier_mask(a1h["rp"].to_numpy(), a1h["rf"].to_numpy())
    daily = (
        a1h.filter(pl.Series(~bad))
        .with_columns(week=pl.col("ts").dt.convert_time_zone(TZ).dt.truncate("1w"))
        .group_by("week")
        .agg(r=pl.corr("rp", "rf"), n=pl.len())
        .filter(pl.col("n") >= 20)
        .sort("week")
    )
    fig, ax = plt.subplots(figsize=(12, 3.2))
    ax.plot(daily["week"].to_list(), daily["r"].to_numpy(), color=style.SERIES[0])
    ax.axhline(USABLE["ret_corr"], color=style.NEUTRAL, lw=1, ls="--")
    ax.set_ylim(min(0.8, float(daily["r"].min() or 0.8)), 1.0)
    ax.set_title("Weekly correlation of 1h returns, proxy vs futures (dashed = usable threshold)")
    ax.set_ylabel("correlation")
    style.save(fig, writer.attachments_dir() / name)


def _overlay(p1: pl.DataFrame, f1: pl.DataFrame, name: str) -> None:
    common = p1.select("ts").join(f1.select("ts"), on="ts")
    et = pl.col("ts").dt.convert_time_zone(TZ)
    days = (
        common.with_columns(d=et.dt.date(), h=et.dt.hour())
        .filter(pl.col("h").is_between(9, 15))
        .group_by("d")
        .len()
        .filter(pl.col("len") > 300)
        .sort("d")
    )
    if days.is_empty():
        return
    day: date = days["d"][-1]
    fig, ax = plt.subplots(figsize=(12, 3.6))
    for df, label, color in ((f1, "futures", style.SERIES[0]), (p1, "proxy", style.SERIES[1])):
        d = df.join(common, on="ts").filter(
            (et.dt.date() == day) & (et.dt.hour() * 60 + et.dt.minute()).is_between(570, 959)
        )
        px = d["close"].to_numpy()
        ax.plot(
            d["ts"].dt.convert_time_zone(TZ).to_list(),
            (px / px[0] - 1) * 1e4,
            label=label,
            color=color,
            lw=1.3,
        )
    ax.set_title(f"Regular session {day}: 1m closes indexed to the open (bps)")
    ax.set_ylabel("bps from open")
    ax.legend(loc="upper left")
    style.save(fig, writer.attachments_dir() / name)


def _write_note(symbol: str, slug: str, results, extremes, order) -> None:
    cols = [
        "timeframe",
        "n",
        "excluded_outliers",
        "ret_corr",
        "beta",
        "sign_agree",
        "range_corr",
        "up_exc_corr",
        "down_exc_corr",
        "tracking_err_bps",
        "fut_ret_std_bps",
        "usable",
    ]
    body = f"""---
type: report
kind: proxy-fidelity
symbol: {symbol}
generated: {date.today().isoformat()}
---
# Proxy fidelity: {symbol}

The Dukascopy index CFD (mid of bid/ask) compared with real CME futures from Yahoo, on
overlapping bar-open timestamps. Futures roll gaps are excluded as outliers and counted.
A timeframe is **usable** only if every one of these holds (fixed before the run):
{", ".join(f"`{k} >= {v}`" for k, v in USABLE.items())}.

## Bar-level fidelity
{writer.md_table(results, cols)}

## Timing fidelity (1m, regular session 09:30-16:00 ET)
- Sessions compared: **{extremes["sessions"]}**
- Session high at the same time (±5 min): **{extremes["high_agree"]:.1%}**
- Session low at the same time (±5 min): **{extremes["low_agree"]:.1%}**
- Within 15m bars, same high-before-low order: **{order["order_agree"]:.1%}**
  ({order["bars"]:,} bars)

## Evidence
![[{slug}-scatter.png]]
![[{slug}-rolling.png]]
![[{slug}-overlay.png]]

## Known differences
- The proxy tracks the cash index, futures carry a basis, so price levels differ. Only returns
  and shapes are compared.
- The proxy has no bars 16:15-17:00 ET (the futures still trade). Strategies can't use that window.
- Proxy volume is a tick-activity count, not contracts. Volume-based rules need care.

Reproduce: `uv run propquant data tracking --symbol {symbol}`
"""
    writer.write_note(f"Reports/Proxy-fidelity-{symbol}.md", body)
