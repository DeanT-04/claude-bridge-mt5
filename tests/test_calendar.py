import numpy as np

from research import calendar


def test_currencies_from_spec_name_and_index_map():
    assert calendar.currencies("EURUSD") == {"EUR", "USD"}
    assert calendar.currencies("XAUUSD") == {"USD"}
    assert calendar.currencies("GER40") == {"EUR"} and calendar.currencies("NAS100") == {"USD"}
    assert calendar.currencies("BTCUSD", {"currency_profit": "USD"}) == {"USD"}


def test_news_mask_matches_symbol_currencies_within_window(monkeypatch):
    ev = {"time": np.array([10_000, 50_000], dtype=np.int64), "currency": np.array(["USD", "JPY"])}
    monkeypatch.setattr(calendar, "load", lambda: ev)
    t = np.array([9_000, 9_700, 10_300, 10_301, 50_000])
    assert calendar.news_mask(t, "EURUSD", 5).tolist() == [False, True, True, False, False]
    assert calendar.news_mask(t, "USDJPY", 5).tolist() == [False, True, True, False, True]
    assert not calendar.news_mask(t, "EURUSD", 0).any()
