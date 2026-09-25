"""Pre-register ES extensions of the original NQ-only ideas (write-once)."""

from propquant.vault import ideas

BASES = ("orb", "intraday_momentum", "gap_fade", "ib_breakout", "late_trend", "overnight_drift")
made = 0
for name in BASES:
    if ideas.path(f"{name}@ES").exists():
        continue
    ideas.write(
        f"{name}@ES", "instrument_extension",
        hypothesis=f"The pre-registered hypothesis of [[{name}]] also holds on ES "
                   "(E-mini S&P 500).",
        mechanism=f"Same mechanism as [[{name}]]; ES is the most liquid equity-index future and "
                  "less tech-concentrated than NQ.",
        rules=f"Identical rules and parameter grid to [[{name}]], run on ES proxy data.",
        params={"(same as base)": (["see base note"], "no new parameters")},
        failure_modes="ES trends less than NQ intraday; costs per point are larger relative "
                      "to its range.",
        sources=[f"Base idea: {name}"], instruments=("ES",),
    )  # fmt: skip
    made += 1
print(f"pre-registered {made} ES extensions")
