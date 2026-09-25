"""Pre-register batch 3: regime-filtered variants + indicator templates + inbox-derived ideas.

Run once (notes are write-once): `uv run python scripts/preregister_batch3.py`.
"""

from propquant.strategies.base import REGISTRY, get
from propquant.strategies.filters import FILTERS
from propquant.vault import ideas

get("orb")  # registers everything
BOTH = ("NQ", "ES")
FAIL = ("More trials make the Deflated Sharpe stricter; a filter that only removes days also "
        "removes sample size; regime labels can flip around their thresholds.")  # fmt: skip

TEMPLATES = {
    "ema_cross": (
        "Fast/slow EMA crossovers on intraday bars catch the start of intraday "
        "trends often enough that ATR-bracketed trades have positive expectancy.",
        "Intraday trends persist as institutions split large orders over hours; a "
        "cross marks the shift of short-term order flow.",
        "Long when EMA(fast) crosses above EMA(slow), short on the opposite cross; "
        "entries 09:35-15:00 ET, up to 3 per day; stop `sl_atr` x ATR14, target "
        "`tp_atr` x ATR14 (ATR on the strategy's bars); flat at 15:55.",
    ),
    "donchian_break": (
        "Closes beyond the prior n-bar high/low (Turtle-style Donchian breaks) "
        "continue far enough intraday to pay for the losers.",
        "Breaking a range triggers resting stops and momentum algos.",
        "Long when the close exceeds the highest high of the previous `n` bars, "
        "short below the lowest low; ATR bracket; 09:35-15:00; flat 15:55.",
    ),
    "bb_squeeze": (
        "After Bollinger bandwidth compresses to its lowest quantile, the first "
        "close outside the bands starts a directional expansion.",
        "Volatility is mean-reverting and clusters: compression precedes expansion.",
        "Squeeze = previous bar's BB(20,2) width in the lowest `q` of the last 100 "
        "bars; enter in the direction of the first close outside a band; ATR "
        "bracket; 09:35-15:00; flat 15:55.",
    ),
    "rsi2_pullback": (
        "Connors RSI(2): short, sharp pullbacks inside an intraday trend revert "
        "in the trend's direction.",
        "Liquidity-providing flows absorb over-extended moves against the prevailing trend.",
        "Long when close > EMA(`trend`) and RSI(2) < `lo`; short when close < EMA "
        "and RSI(2) > 100-`lo`; ATR bracket; 09:35-15:00; flat 15:55.",
    ),
    "keltner_fade": (
        "In low-ADX (range-bound) conditions, closes outside the Keltner channel "
        "revert to its middle.",
        "Without a trend, excursions are noise that market makers fade.",
        "When ADX14 < `adx_max`: fade a close outside Keltner(20, `k` x ATR), "
        "target the channel middle, stop `sl_atr` x ATR; 09:35-15:00; flat 15:55.",
    ),
    "supertrend": (
        "Supertrend(10, mult) direction flips on intraday bars mark tradeable trend changes.",
        "An ATR-based trailing regime line filters noise from genuine trend changes.",
        "Enter on a direction flip (optionally only with the 200-EMA trend), exit on "
        "the opposite flip or an ATR stop; 09:35-15:00; flat 15:55.",
    ),
    "macd_trend": (
        "MACD histogram zero-crosses aligned with the 200-EMA trend capture "
        "intraday momentum bursts.",
        "Momentum acceleration after consolidation, in the direction of the larger trend.",
        "Enter when the MACD(12,26,9) histogram crosses zero (optionally only with "
        "the 200-EMA trend); ATR bracket; 09:35-15:00; flat 15:55.",
    ),
}


def params_table(cls) -> dict:
    return {k: (v, "pre-set grid") for k, v in cls.param_space.items()}


made = 0
for name, cls in sorted(REGISTRY.items()):
    if ideas.path(name).exists() or not cls.needs_idea_note:
        continue
    base = getattr(cls, "base_strategy", None)
    if base:
        f = FILTERS[cls.filter_name]
        ideas.write(
            name, cls.family,
            hypothesis=f"The real timing edge of [[{base}]] (beat 98-99.9% of random entries "
                       f"in batch 1) is concentrated in one regime: {f.rationale}",
            mechanism=f"Same mechanism as [[{base}]]; the filter `{f.name}` (known "
                      f"{f.known}) keeps only sessions where that mechanism should be strongest.",
            rules=f"Exactly [[{base}]]'s rules and grid; new positions only on sessions where "
                  f"`{f.name}` is true. Filter defined in `strategies/filters.py`.",
            params=params_table(cls), failure_modes=FAIL,
            sources=["Lesson: Batch 1 - classic intraday families have timing but not enough "
                     "edge", f"Base idea: {base}"], instruments=BOTH,
        )  # fmt: skip
    else:
        tmpl = cls.family
        if tmpl not in TEMPLATES:
            continue
        hyp, mech, rules = TEMPLATES[tmpl]
        ideas.write(
            name, tmpl, hypothesis=f"[{cls.timeframe} bars] {hyp}", mechanism=mech, rules=rules,
            params=params_table(cls), failure_modes=FAIL + " Classic indicator rules are "
            "widely known and may be arbitraged.",
            sources=["Classic technical analysis (Donchian/Turtles, Bollinger, Connors, "
                     "Appel MACD, Wilder ADX)"], instruments=BOTH,
        )  # fmt: skip
    made += 1

INBOX = {
    "twap_reversion": dict(
        family="twap_reversion",
        hypothesis="Stretches of k x ATR away from the session average price revert toward it "
                   "during the middle of the day.",
        mechanism="VWAP/TWAP is an execution benchmark; algos trading against it pull price "
                  "back. The proxy has no real volume, so TWAP stands in for VWAP.",
        rules="From `start` to 15:00, fade a close >= `k` x ATR14(daily) from the session TWAP "
              "(since 09:30); target TWAP; stop `sl_mult` x k x ATR; up to 2 per day; flat 15:55.",
        sources=["YouTube inbox: several VWAP mean-reversion videos (e.g. 'Master VWAP Trading "
                 "Strategy', 'My Exact Mean Reversion Trading Framework (NQ)')"]),
    "nr_breakout": dict(
        family="narrow_range",
        hypothesis="After the narrowest daily range of the last 4/7 days (NR4/NR7), the next "
                   "day's break of that range extends.",
        mechanism="Volatility contraction precedes expansion (Crabel).",
        rules="If yesterday's RTH range was the narrowest of the last `nr` days: OCO stops at "
              "yesterday's high/low from 09:30 to 12:00; stop `sl_frac` x that range; target "
              "`tp_mult` x range; flat 15:55.",
        sources=["Oxford Strat inbox article: 'Price Breakout with NR7'", "Crabel (1990)"]),
    "pd_sweep": dict(
        family="liquidity_sweep",
        hypothesis="A run of yesterday's high (low) that closes back inside on a 1m bar is a "
                   "failed breakout that reverses toward the middle of yesterday's range.",
        mechanism="ICT/SMC 'liquidity sweep': stops above obvious highs get taken, then price "
                  "returns once that liquidity is absorbed.",
        rules="09:30 to `end`: short when a bar's high > yesterday's RTH high and it closes "
              "below it (long mirror at the low); stop beyond the sweep extreme + `buf` x "
              "ATR14(daily); target `tp_frac` x yesterday's range; 1 per day; flat 15:55.",
        sources=["YouTube inbox: SMC/ICT sweep videos (e.g. 'Copy This 5 Rule SMC Trading "
                 "Strategy (Backtested Results)')"]),
    "ib_twap": dict(
        family="initial_balance",
        hypothesis="Initial-balance breakouts in the direction of price vs the session average "
                   "(VWAP side) at 10:30 are the profitable half of IB breaks.",
        mechanism="Price above VWAP at the end of the IB signals buyers in control; breaks with "
                  "that flow extend.",
        rules="IB = 09:30-10:30 range; at 10:30 take the side of close vs session TWAP; single "
              "stop order at IB high (long) or low (short) until 14:00; stop `sl_frac` x IB; "
              "target `tp_mult` x IB; flat 15:55.",
        sources=["YouTube inbox: 'How I Used Initial Balance & VWAP to Get 7 Payouts in 10 Days'"]),
}  # fmt: skip
for name, d in INBOX.items():
    if ideas.path(name).exists():
        continue
    cls = REGISTRY[name]
    ideas.write(name, d["family"], hypothesis=d["hypothesis"], mechanism=d["mechanism"],
                rules=d["rules"], params=params_table(cls), failure_modes=FAIL,
                sources=d["sources"], instruments=BOTH)  # fmt: skip
    made += 1

print(f"pre-registered {made} ideas")
