import polars as pl

from propquant.data.dukascopy import MINUTE_MS, missing_segments, parse_jsonp, rows_to_frame

SAMPLE = (
    "_callbacks____1([[1715347800000,18176.008,18176.289,18159.508,18161.631,0.03212],"
    "[1715347860000,18161.087,18185.999,18160.41,18184.987,0.03086]]);"
)


def test_parse_jsonp_rows() -> None:
    rows = parse_jsonp(SAMPLE)
    assert len(rows) == 2
    assert rows[0][0] == 1715347800000


def test_parse_jsonp_empty() -> None:
    assert parse_jsonp("_callbacks____1([null]);") == []


def test_rows_to_frame_columns_and_utc() -> None:
    df = rows_to_frame(parse_jsonp(SAMPLE))
    assert df.columns == ["ts", "open", "high", "low", "close", "volume"]
    assert df["ts"].dtype == pl.Datetime("ms", "UTC")
    assert str(df["ts"][0]) == "2024-05-10 13:30:00+00:00"
    assert df["high"][1] == 18185.999
    assert rows_to_frame([]).is_empty()


def test_missing_segments_fresh() -> None:
    assert missing_segments(0, 100 * MINUTE_MS, None) == [(0, 100 * MINUTE_MS)]


def test_missing_segments_backfills_before_and_extends_after() -> None:
    m = MINUTE_MS
    segs = missing_segments(0, 100 * m, (40 * m, 60 * m))
    assert segs == [(0, 40 * m), (61 * m, 100 * m)]


def test_missing_segments_fully_covered() -> None:
    m = MINUTE_MS
    assert missing_segments(10 * m, 50 * m, (0, 60 * m)) == []
