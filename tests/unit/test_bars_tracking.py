from datetime import UTC, datetime, timedelta

import numpy as np
import polars as pl
import pytest

from propquant.data.bars import clean, mid_bars, quality_report, resample, with_session
from propquant.data.tracking import (
    fidelity,
    intrabar_order_agreement,
    outlier_mask,
    session_extreme_agreement,
)


def random_walk_1m(start: datetime, n: int, seed: int, px0: float = 18000.0) -> pl.DataFrame:
    rng = np.random.default_rng(seed)
    close = px0 * np.exp(np.cumsum(rng.normal(0, 3e-4, n)))
    open_ = np.concatenate([[px0], close[:-1]])
    wick = np.abs(rng.normal(0, 2e-4, n)) * close
    return pl.DataFrame(
        {
            "ts": [start + timedelta(minutes=i) for i in range(n)],
            "open": open_,
            "high": np.maximum(open_, close) + wick,
            "low": np.minimum(open_, close) - wick,
            "close": close,
            "volume": np.ones(n),
        }
    ).with_columns(pl.col("ts").cast(pl.Datetime("ms", "UTC")))


START = datetime(2024, 6, 10, 13, 30, tzinfo=UTC)  # 09:30 ET


def test_session_rolls_at_18_et() -> None:
    ts = [datetime(2024, 6, 10, 21, 59, tzinfo=UTC), datetime(2024, 6, 10, 22, 0, tzinfo=UTC)]
    df = pl.DataFrame({"ts": ts}).with_columns(pl.col("ts").cast(pl.Datetime("ms", "UTC")))
    s = with_session(df)["session"].to_list()  # 17:59 ET and 18:00 ET (EDT)
    assert str(s[0]) == "2024-06-10" and str(s[1]) == "2024-06-11"


def test_mid_bars_and_spread() -> None:
    bid = random_walk_1m(START, 30, 1)
    ask = bid.with_columns([pl.col(c) + 0.5 for c in ("open", "high", "low", "close")])
    m = mid_bars(bid, ask)
    assert m.height == 30
    np.testing.assert_allclose(m["spread"].to_numpy(), 0.5)
    np.testing.assert_allclose(m["close"].to_numpy(), bid["close"].to_numpy() + 0.25)


def test_resample_ohlc_and_quality() -> None:
    b = mid_bars(random_walk_1m(START, 60, 2), random_walk_1m(START, 60, 2))
    r = resample(b, "15m")
    assert r.height == 4
    first = b.head(15)
    assert r["open"][0] == first["open"][0]
    assert r["high"][0] == first["high"].max()
    assert r["low"][0] == first["low"].min()
    assert r["close"][0] == first["close"][-1]
    assert r["n_1m"].to_list() == [15, 15, 15, 15]
    q = quality_report(b)
    assert q["duplicate_ts"] == 0 and q["ohlc_violations"] == 0


def test_fidelity_identical_feeds_is_perfect() -> None:
    p = random_walk_1m(START, 390, 3)
    f = fidelity(p, p, "1m", 1)
    assert f.ret_corr == pytest.approx(1.0)
    assert f.range_corr == pytest.approx(1.0)
    assert f.tracking_err_bps == pytest.approx(0.0, abs=1e-9)
    assert f.excluded_outliers == 0


def test_fidelity_detects_unrelated_feeds() -> None:
    f = fidelity(random_walk_1m(START, 390, 4), random_walk_1m(START, 390, 5), "1m", 1)
    assert abs(f.ret_corr) < 0.2


def test_roll_jump_is_excluded() -> None:
    rng = np.random.default_rng(6)
    rp = rng.normal(0, 1e-3, 500)
    rf = rp + rng.normal(0, 1e-5, 500)
    rf[250] += 0.015  # a futures roll gap
    assert outlier_mask(rp, rf).sum() == 1


def test_extreme_and_order_agreement_identical() -> None:
    p = random_walk_1m(START, 390, 7)
    ext = session_extreme_agreement(p, p)
    assert ext["sessions"] == 1 and ext["high_agree"] == 1.0 and ext["low_agree"] == 1.0
    assert intrabar_order_agreement(p, p)["order_agree"] == 1.0


def test_clean_drops_weekend_and_thin_sessions() -> None:
    fri = random_walk_1m(datetime(2024, 6, 14, 13, 30, tzinfo=UTC), 100, 8)  # Friday RTH
    sat = random_walk_1m(datetime(2024, 6, 15, 13, 30, tzinfo=UTC), 100, 9)  # Saturday: never CME
    thin = random_walk_1m(datetime(2024, 6, 17, 13, 30, tzinfo=UTC), 10, 10)  # 10-bar session
    b = mid_bars(*(2 * [pl.concat([fri, sat, thin])]))
    out, dropped = clean(b)
    assert out.height == 100
    assert dropped == {"dropped_weekend_bars": 100, "dropped_thin_sessions": 1,
                       "dropped_thin_bars": 10}  # fmt: skip
