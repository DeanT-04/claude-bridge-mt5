"""Turn measured results into gate checks and a verdict (rules fixed in config/research.yaml)."""

from dataclasses import dataclass

ELITE, CONTENDER, GRAVEYARD = "elite", "contender", "graveyard"


@dataclass
class Check:
    name: str
    value: float
    threshold: float
    op: str  # ">=", "<=", ">"
    kind: str  # "stat" | "commercial" | "speed"

    @property
    def passed(self) -> bool:
        v, t = self.value, self.threshold
        return {">=": v >= t, "<=": v <= t, ">": v > t}[self.op]

    def row(self) -> dict:
        return {
            "gate": self.name,
            "value": self.value,
            "needs": f"{self.op} {self.threshold:g}",
            "kind": self.kind,
            "result": "PASS" if self.passed else "FAIL",
        }


def checks(g: dict, *, oos_trades: int, dsr: float, re_pct: float, ch: dict,
           holdout_ok: bool) -> list[Check]:  # fmt: skip
    return [
        Check("OOS trades", oos_trades, g["min_oos_trades"], ">=", "stat"),
        Check("Deflated Sharpe", dsr, g["dsr"], ">=", "stat"),
        Check(
            "Beats random entry (percentile)", re_pct, g["random_entry_percentile"], ">=", "stat"
        ),
        Check("EV per attempt, 5th pct (USD)", ch["ev_p05"], g["ev_per_attempt_p05"], ">", "stat"),
        Check("Holdout consistent", float(holdout_ok), 1.0, ">=", "stat"),
        Check(
            "End-to-end payout rate",
            ch["end_to_end_payout"],
            g["end_to_end_payout"],
            ">=",
            "commercial",
        ),
        Check("Evaluation pass rate", ch["eval_pass"], g["eval_pass"], ">=", "commercial"),
        Check(
            "First payout once funded",
            ch["first_payout_given_pass"],
            g["first_payout_given_pass"],
            ">=",
            "commercial",
        ),
        Check(
            "Median sessions to pass",
            ch["median_sessions_to_pass"],
            g["median_sessions_to_pass"],
            "<=",
            "speed",
        ),
        Check(
            "90th pct sessions to pass",
            ch["p90_sessions_to_pass"],
            g["p90_sessions_to_pass"],
            "<=",
            "speed",
        ),
    ]


def decide(cs: list[Check], contender: dict, ch: dict) -> tuple[str, list[str]]:
    failed = [c.name for c in cs if not c.passed]
    if not failed:
        return ELITE, []
    stats_ok = all(c.passed for c in cs if c.kind == "stat")
    commercial_ok = all(c.passed for c in cs if c.kind == "commercial")
    near = (ch["end_to_end_payout"] >= contender["end_to_end_payout"]
            and ch["eval_pass"] >= contender["eval_pass"])  # fmt: skip
    if stats_ok and (commercial_ok or near):
        return CONTENDER, failed
    return GRAVEYARD, failed
