"""Regime-filtered variants of the families that showed real timing in batch 1
(beat 98-99.9% of random-entry runs but lacked edge). One variant per (family, filter)."""

from propquant.strategies.families.intraday import (
    InitialBalanceBreakout,
    LateDayTrend,
    OpeningRangeBreakout,
)
from propquant.strategies.filters import FILTERS, filtered

BASES = (LateDayTrend, OpeningRangeBreakout, InitialBalanceBreakout)
VARIANTS = [filtered(b, f) for b in BASES for f in FILTERS]
