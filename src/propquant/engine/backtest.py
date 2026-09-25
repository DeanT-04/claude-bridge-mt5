"""Glue between bar data, a strategy's orders, the numba engine and the challenge simulator."""

from dataclasses import dataclass, field

import numpy as np
import polars as pl

from propquant import instruments
from propquant.data import store
from propquant.data.bars import TZ
from propquant.engine import core

DEFAULT_FLAT_MINUTE = 16 * 60 + 10  # 16:10 ET: the proxy has no bars 16:15-17:00


@dataclass
class MarketData:
    """Numpy view of 1m bars. `minute` is minutes since midnight ET; `sess` a session index."""

    symbol: str
    ts: np.ndarray
    open: np.ndarray
    high: np.ndarray
    low: np.ndarray
    close: np.ndarray
    volume: np.ndarray
    minute: np.ndarray
    sess: np.ndarray
    sess_start: np.ndarray  # first bar of each session (+ final sentinel = n)
    sess_day: np.ndarray  # session date as days since 1970-01-01
    data_hash: str = ""

    @property
    def n(self) -> int:
        return len(self.open)

    @classmethod
    def from_frame(cls, symbol: str, df: pl.DataFrame, data_hash: str = "") -> "MarketData":
        et = pl.col("ts").dt.convert_time_zone(TZ)
        df = df.sort("ts").with_columns(
            minute=(et.dt.hour().cast(pl.Int32) * 60 + et.dt.minute().cast(pl.Int32)),
            sess=pl.col("session").rank("dense").cast(pl.Int64) - 1,
        )
        sess = df["sess"].to_numpy()
        starts = np.flatnonzero(np.diff(sess, prepend=-1) != 0)
        days = df["session"].cast(pl.Int64).to_numpy()[starts]
        return cls(
            symbol=symbol,
            ts=df["ts"].to_numpy(),
            open=df["open"].to_numpy().astype(np.float64),
            high=df["high"].to_numpy().astype(np.float64),
            low=df["low"].to_numpy().astype(np.float64),
            close=df["close"].to_numpy().astype(np.float64),
            volume=df["volume"].to_numpy().astype(np.float64),
            minute=df["minute"].to_numpy().astype(np.int64),
            sess=sess.astype(np.int64),
            sess_start=np.append(starts, len(sess)).astype(np.int64),
            sess_day=days.astype(np.int64),
            data_hash=data_hash,
        )

    @classmethod
    def load(cls, symbol: str, timeframe: str = "1m") -> "MarketData":
        df = pl.read_parquet(store.bars_path(symbol, timeframe))
        return cls.from_frame(symbol, df, store.frame_hash(df))

    def slice_sessions(self, first: int, last: int) -> "MarketData":
        """Sessions [first, last) as a new MarketData (for walk-forward folds)."""
        a, b = self.sess_start[first], self.sess_start[last]
        return MarketData(
            symbol=self.symbol,
            ts=self.ts[a:b],
            open=self.open[a:b],
            high=self.high[a:b],
            low=self.low[a:b],
            close=self.close[a:b],
            volume=self.volume[a:b],
            minute=self.minute[a:b],
            sess=self.sess[a:b] - first,
            sess_start=self.sess_start[first : last + 1] - a,
            sess_day=self.sess_day[first:last],
            data_hash=f"{self.data_hash}[{first}:{last}]",
        )


@dataclass
class Orders:
    """Order intents decided at the close of each bar; they act from the next bar."""

    order_type: np.ndarray
    order_dir: np.ndarray
    order_px: np.ndarray
    sl_pts: np.ndarray
    tp_pts: np.ndarray
    exit_sig: np.ndarray
    order_px2: np.ndarray  # sell-stop leg of an OCO bracket (order_dir 0)

    @classmethod
    def empty(cls, n: int) -> "Orders":
        return cls(
            order_type=np.zeros(n, np.int64),
            order_dir=np.zeros(n, np.int64),
            order_px=np.full(n, np.nan),
            order_px2=np.full(n, np.nan),
            sl_pts=np.full(n, np.nan),
            tp_pts=np.full(n, np.nan),
            exit_sig=np.zeros(n, np.bool_),
        )


@dataclass
class Costs:
    tick: float
    point_value: float  # per micro contract
    slip_ticks: float = 1.0
    commission_side: float = 0.51  # per micro, Apex/Rithmic (see config/firms/apex.yaml)

    @classmethod
    def micro(cls, symbol: str, slip_ticks: float = 1.0, commission_side: float = 0.51):
        inst = instruments.get(symbol)
        return cls(inst.tick_size, inst.micro.point_value, slip_ticks, commission_side)


TRADE_COLS = ("entry_i", "exit_i", "dir", "entry_px", "exit_px", "pnl", "reason")


@dataclass
class Result:
    d_close: np.ndarray
    d_low: np.ndarray
    d_high: np.ndarray
    trades: np.ndarray
    md: MarketData = field(repr=False)

    def sim_input(self) -> dict[str, np.ndarray]:
        return {
            "d_close": self.d_close,
            "d_low": self.d_low,
            "d_high": self.d_high,
            "sess_start": self.md.sess_start,
            "sess_day": self.md.sess_day,
        }

    def daily_pnl(self) -> np.ndarray:
        """Net P&L per session, USD per micro."""
        return np.add.reduceat(self.d_close, self.md.sess_start[:-1])

    def trades_frame(self) -> pl.DataFrame:
        df = pl.DataFrame(self.trades, schema=list(TRADE_COLS), orient="row")
        return df.with_columns(
            pl.col("entry_i", "exit_i", "dir", "reason").cast(pl.Int64),
        )


def run(md: MarketData, orders: Orders, costs: Costs, flat_minute: int = DEFAULT_FLAT_MINUTE,
        max_per_session: int = 1_000_000):  # fmt: skip
    d_close, d_low, d_high, trades = core.run(
        md.open, md.high, md.low, md.close, md.minute, md.sess,
        orders.order_type, orders.order_dir, orders.order_px, orders.order_px2, orders.sl_pts,
        orders.tp_pts,
        orders.exit_sig, flat_minute, costs.tick, costs.point_value, costs.slip_ticks,
        costs.commission_side, max_per_session,
    )  # fmt: skip
    return Result(d_close, d_low, d_high, trades, md)
