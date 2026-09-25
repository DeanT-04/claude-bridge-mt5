"""Every regime filter's value for a session must depend only on data from before it is known
(before the session for pre-session filters, before 09:29 for overnight filters)."""

from datetime import date, timedelta

import numpy as np
import pytest

from propquant.engine.backtest import MarketData
from propquant.gauntlet import config
from propquant.strategies.filters import FILTERS, mask

# a coarse session (every 15 min) keeps 300 sessions small; includes evening + RTH bars
MINUTES = np.r_[np.arange(1080, 1440, 15), np.arange(0, 960, 15), 959].astype(np.int64)


def md_300(seed: int) -> MarketData:
    rng = np.random.default_rng(seed)
    days, d = [], date(2019, 1, 2)
    while len(days) < 300:
        if d.weekday() < 5:
            days.append(d)
        d += timedelta(days=1)
    m, k = len(MINUTES), len(days)
    rth = (MINUTES >= 570) & (MINUTES < 1080)
    vol = np.tile(np.where(rth, 12.0, 1.5), k)  # calm overnight, active cash session
    close = 7000 + np.cumsum(rng.normal(0, 1, m * k) * vol)
    open_ = np.r_[7000, close[:-1]]
    return MarketData(
        "T", np.arange(m * k), open_, np.maximum(open_, close) + rng.uniform(0, 3, m * k),
        np.minimum(open_, close) - rng.uniform(0, 3, m * k), close, np.ones(m * k),
        np.tile(MINUTES, k), np.repeat(np.arange(k), m).astype(np.int64),
        np.append(np.arange(k) * m, k * m).astype(np.int64),
        np.array([config.day_number(x) for x in days], dtype=np.int64),
    )  # fmt: skip


def shocked(md: MarketData, first_bar: int) -> MarketData:
    m = MarketData(**{k: (v.copy() if isinstance(v, np.ndarray) else v)
                      for k, v in md.__dict__.items()})  # fmt: skip
    for f in ("open", "high", "low", "close"):
        getattr(m, f)[first_bar:] *= 1.3
    return m


@pytest.mark.parametrize("name", sorted(FILTERS))
def test_filter_is_known_when_it_claims(name: str) -> None:
    md = md_300(1)
    base = mask(md, name)
    assert base.any(), f"{name} never true on 300 sessions: test would be vacuous"
    for s in (200, 250, 290):
        start = md.sess_start[s]
        if FILTERS[name].known != "pre-session":
            start += int(np.flatnonzero(MINUTES == 555)[0]) + 1  # after the 09:15 bar
        after = mask(shocked(md, start), name)
        # pre-session filters: sessions <= s unchanged; 09:29 filters: sessions < s unchanged
        upto = s + 1 if FILTERS[name].known == "pre-session" else s
        np.testing.assert_array_equal(base[:upto], after[:upto])
