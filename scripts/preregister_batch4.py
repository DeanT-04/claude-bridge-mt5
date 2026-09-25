"""Pre-register batch 4: inbox-derived ideas triaged from the research inbox (write-once)."""

from propquant.strategies.base import REGISTRY, get
from propquant.vault import ideas

get("orb")
PRIOR = ("Inbox evidence is weak overall: arXiv:2605.04004 (walk-forward MNQ with costs) found no "
         "plain OHLC intraday signal that survived, and a video coding 10 years of ORB variants "
         "found them flat or losing after costs. Prior is low.")  # fmt: skip
IDEAS = {
    "overnight_failure_fade": dict(
        family="overnight_failure",
        hyp="After a strong one-way overnight move (>= k x ATR, closing in the extreme c of the "
            "overnight range) that the first cash hour fails to extend, price washes back toward "
            "the prior close.",
        mech="Overnight moves are carried by weak, one-sided inventory. When the cash session "
             "cannot extend them, those holders liquidate (the 'overnight up, intraday down' "
             "reversal).",
        rules="Enter at the 10:30 close against the overnight move. Stop beyond max/min(ON, IB) "
              "extreme + 2 ticks. Target: prior RTH close. Flat 15:55. Optional: require the 10:30 "
              "close on the fading side of the IB mid.",
        src=["youtube:aBC6iKIbKgQ (Axia Futures, 'What Initial Balance Should You Use?')",
             "openalex:W2945479896 'Intraday Return Reversals: Korean ETF Market'"],
        cred="Educator mechanism without a backtest; supporting econometrics on another market."),
    "ib_failed_auction": dict(
        family="failed_auction",
        hyp="After 10:30, a B-minute block that pierces the IB extreme by >2 ticks but closes back "
            "inside marks a failed auction that rotates back into the IB.",
        mech="Market-profile failed auction: excursions outside first-hour value find no "
             "acceptance and are reversed.",
        rules="Enter at the next bar open toward the IB; stop 2 ticks beyond the extreme since "
              "10:30; target IB extreme + t x IBR inside; up to one trade per side per day; "
              "entries "
              "until 15:00; flat 15:55. Optional double sweep: the excursion also takes the "
              "overnight extreme.",
        src=["youtube:lOnEKIWj0S8 'Initial Balance Masterclass'",
             "youtube:gGrnIm9wpx0 'IB Indicator Day Trading Strategy'",
             "youtube:o_rVg1bAD9k 'How to use Initial Balance (TBM)'"],
        cred="Three independent educators, no statistics (a self-reported 85% win rate)."),
    "right_side_v": dict(
        family="capitulation_reversal",
        hyp="After a fast drop (60-minute high to low >= m x ATR14) between 10:00 and 14:30, "
            "buying the first 5-minute close above the prior 5-minute high has positive "
            "expectancy (long only).",
        mech="Sell-side liquidity shocks overshoot and are replenished; waiting for the turn "
             "avoids catching the falling knife.",
        rules="Long at the next open after the confirming 5m close; stop 2 ticks under the V "
              "low; target V low + f x (60-minute high - V low); time stop `hold` minutes; one "
              "trade per day; flat 15:55.",
        src=["arXiv:2511.06177 'Push-response anomalies in high-frequency S&P 500 price series'",
             "youtube:wtQIj6Apiq0 'Right Side of the V' (Breitstein)"],
        cred="Tick-level SPY asymmetry without costs; anecdotal trader method."),
    "opening_range_reversal": dict(
        family="opening_reversal",
        hyp="An early move against the 50-day trend of >= p x ATR (before 11:00) is reversed: a "
            "stop above the last completed 5-minute bar catches the turn.",
        mech="Early counter-trend moves are liquidity-seeking; the daily trend reasserts.",
        rules="Bias from the prior close vs its 50-day SMA (or off). Buy stop 1 tick above the "
              "last completed 5m high (sell mirror) until 11:30; stop 2 ticks beyond the session "
              "extreme; target a g fraction of the move back toward the open; one trade; flat "
              "15:55.",
        src=["youtube:8vufTzGZqiI 'The One Day Trading Strategy I Make A Living From'"],
        cred="Newsletter marketing with explicit rules; no backtest shown."),
    "wide_ib_rotation": dict(
        family="ib_rotation",
        hyp="On days whose IB is >= q x its 20-day median, the rest of the day rotates inside it: "
            "fading the IB extremes with limit orders pays.",
        mech="A wide first hour completes much of the day's business, so the afternoon ranges.",
        rules="From 10:30 to 14:30, a limit at the IB extreme nearer to price (sell the high / "
              "buy the low); stop s x IBR beyond it; target IB mid or 75% across; up to two "
              "trades; flat 15:55.",
        src=["youtube:aBC6iKIbKgQ (Axia)", "youtube:o_rVg1bAD9k (TBM)"],
        cred="Conceptual only; vendor statistics (one-sided IB breaks on ~85% of days) argue "
             "against it."),
    "session_range_sweep": dict(
        family="liquidity_sweep",
        hyp="A sweep beyond a pre-open range (03:00-09:29, the 8am hour, or London 02:00-05:00) "
            "that closes back inside during 09:30-11:30 reverses toward the range middle or far "
            "side.",
        mech="Stops cluster beyond obvious pre-open extremes and are run at the cash open.",
        rules="1m bar pierces the range by > 1 tick and closes back inside -> enter at next open "
              "against the sweep; stop 2 ticks beyond the sweep bar; target range mid or far side; "
              "exit by 12:00; skip ranges < 0.15 x ATR14; one trade per day.",
        src=["youtube:Lfa2pAZ4kUE 'I Backtested CRT... 9am CRT Model'",
             "youtube:E9MzEC_yNoM 'Easy Futures Day Trading Strategy (5 Minute Setups)'",
             "youtube:8PYgFVB0GHE 'My UPDATED Day Trading Strategy (2026)'"],
        cred="ICT/SMC marketing; hand-picked replays."),
}  # fmt: skip

made = 0
for name, d in IDEAS.items():
    if ideas.path(name).exists():
        continue
    cls = REGISTRY[name]
    ideas.write(
        name, d["family"], hypothesis=d["hyp"], mechanism=d["mech"], rules=d["rules"],
        params={k: (v, "triage grid (fixed before testing)") for k, v in cls.param_space.items()},
        failure_modes=f"{PRIOR} Source credibility: {d['cred']}",
        sources=d["src"] + ["Triage report: research inbox (batch 4)"], instruments=("NQ", "ES"),
    )  # fmt: skip
    made += 1
print(f"pre-registered {made}")
