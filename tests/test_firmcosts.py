import pytest

from research import firmcosts

EURUSD = {"name": "EURUSD", "group": "Forex", "point": 1e-05, "spread": 11, "tick_value": 1.0,
          "tick_size": 1e-05, "bid": 1.1}
XAUUSD = {"name": "XAUUSD", "group": "Commodities", "point": 0.01, "spread": 22, "tick_value": 1.0,
          "tick_size": 0.01, "bid": 4000.0}
NAS100 = {"name": "NAS100", "group": "Indices", "point": 0.1, "spread": 12, "tick_value": 0.1,
          "tick_size": 0.1, "bid": 25000.0}


def test_symbol_normalisation():
    assert firmcosts.normalize("EUR/USD") == "EURUSD"
    assert firmcosts.normalize("US100.cash") == "NAS100" and firmcosts.normalize("NDX100") == "NAS100"
    assert firmcosts.normalize("UKOUSD") == "BRENT" and firmcosts.normalize("JP225.cash") == "JPN225"


def test_asset_classes_and_blackbull_only_products():
    assert firmcosts.asset_class("XAUUSD", XAUUSD) == "Metals"
    assert firmcosts.asset_class("WTI", {"group": "Commodities"}) == "Energies"
    assert firmcosts.asset_class("US500.f", {"group": "Futures"}) is None
    assert firmcosts.asset_class("XAUUSDp", {"group": "Commodities"}) is None


def test_offered_lists():
    assert firmcosts.offered("FTMO", "EURUSD", EURUSD) and firmcosts.offered("FundingPips", "NAS100", NAS100)
    assert not firmcosts.offered("FundingPips", "USDZAR", {"group": "Forex"})
    assert firmcosts.offered("FXIFY", "EURUSD", EURUSD)           # unpublished list -> common set


def test_commission_conversion():
    c = firmcosts.costs("FTMO", "EURUSD", EURUSD)                  # $5 per lot at $1 per point per lot
    assert c.commission_price == pytest.approx(5 * 1e-05) and c.commission_rate == 0
    fn = firmcosts.costs("FundedNext", "EURUSD", EURUSD)           # $5 per side
    assert fn.commission_price == pytest.approx(10 * 1e-05)
    g = firmcosts.costs("FTMO", "XAUUSD", XAUUSD)
    assert g.commission_rate == pytest.approx(0.0014 / 100) and g.commission_price == 0
    assert firmcosts.costs("FTMO", "NAS100", NAS100).commission_price == 0


def test_spread_ratio_sources():
    r, src = firmcosts.spread_ratio("FTMO", "EURUSD", "Forex")
    assert 0.05 <= r < 1 and "snapshot" in src
    _, src2 = firmcosts.spread_ratio("FundingPips", "EURUSD", "Forex")
    assert "raw-spread" in src2
    assert firmcosts.spread_ratio("The5ers", "NAS100", "Indices")[0] == 1.0


def test_percent_commission_charged_in_engine():
    from research.engine import Costs, simulate
    from tests.test_engine import mk, sig
    b = mk([(100, 100, 100, 100), (100, 103, 99.5, 102), (102, 107, 101, 106)])
    free = simulate(b, *sig(3, 1, 1, 2.0, 5.0), max_bars=10, costs=Costs(point=0.01))
    paid = simulate(b, *sig(3, 1, 1, 2.0, 5.0), max_bars=10, costs=Costs(point=0.01, commission_rate=0.01))
    assert free[0].r - paid[0].r == pytest.approx(100 * 0.01 / 2.0)
