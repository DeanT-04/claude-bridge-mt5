"""Firm rule files -> a flat, validated ChallengeSpec the simulator can run.

A rule file without sources or a verification date is rejected: unverified rules would make
every downstream result meaningless.
"""

from datetime import date
from functools import cache
from pathlib import Path

import numpy as np
import yaml
from pydantic import BaseModel, field_validator

from propquant.paths import CONFIG_DIR

TRAIL_EOD, TRAIL_INTRADAY = 0, 1


class Source(BaseModel):
    url: str
    capture: str
    note: str = ""


class FirmFile(BaseModel):
    firm: str
    name: str
    verified_on: date
    platform: str
    sources: dict[str, Source]
    session: dict
    commissions_per_side: dict[str, float]
    plans: dict[str, dict]
    pa_tiers: dict[str, list[dict]]
    open_questions: list[str] = []

    @field_validator("sources")
    @classmethod
    def _need_sources(cls, v: dict[str, Source]) -> dict[str, Source]:
        if not v:
            raise ValueError("firm rules must cite at least one source")
        return v


class ChallengeSpec(BaseModel):
    """Everything the simulator needs for one firm/plan/size, in account currency (USD)."""

    firm: str
    plan: str
    size: str
    balance: float
    # evaluation
    target: float
    drawdown: float
    eval_dll: float  # 0 = none
    eval_max_micros: int
    eval_trail: int
    eval_trail_cap: float  # threshold never exceeds this (target balance for Rithmic)
    access_days: int
    eval_fee: float
    # performance account
    pa_trail: int
    pa_trail_cap: float  # start + 100
    activation_fee: float
    tier_profit_from: list[float]
    tier_max_micros: list[int]
    tier_dll: list[float]
    min_daily_profit: float
    payout_min_days: int
    payout_consistency: float
    payout_min_amount: float
    payout_caps: list[float]
    safety_net: float
    commission_micro_rt: float
    verified_on: date
    open_questions: list[str]

    def tiers(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        return (
            np.asarray(self.tier_profit_from, dtype=np.float64),
            np.asarray(self.tier_max_micros, dtype=np.int64),
            np.asarray(self.tier_dll, dtype=np.float64),
        )


@cache
def load_firm(firm: str, root: Path = CONFIG_DIR / "firms") -> FirmFile:
    return FirmFile(**yaml.safe_load((root / f"{firm}.yaml").read_text(encoding="utf-8")))


def challenge(firm: str, plan: str, size: str) -> ChallengeSpec:
    f = load_firm(firm)
    if plan not in f.plans:
        raise KeyError(f"{firm} has no plan {plan!r}; have {sorted(f.plans)}")
    ev, pa = f.plans[plan]["eval"], f.plans[plan]["pa"]
    if size not in ev["sizes"] or size not in f.pa_tiers or size not in pa["payout_caps"]:
        raise KeyError(f"{firm}/{plan}/{size} is not fully specified in the verified rules")
    s = ev["sizes"][size]
    micros = int(f.session["micros_per_contract"])
    trail = {"eod": TRAIL_EOD, "intraday": TRAIL_INTRADAY}
    if ev["trail_stops_at"] != "target" or pa["trail_stops_at"] != "start_plus_100":
        raise ValueError("unsupported trail stop rule")
    tiers = f.pa_tiers[size]
    return ChallengeSpec(
        firm=firm,
        plan=plan,
        size=size,
        balance=s["balance"],
        target=s["target"],
        drawdown=s["drawdown"],
        eval_dll=s["dll"] if ev["dll_pauses_day"] else 0.0,
        eval_max_micros=s["max_contracts"] * micros,
        eval_trail=trail[ev["trail"]],
        eval_trail_cap=s["balance"] + s["target"],
        access_days=ev["access_calendar_days"],
        eval_fee=s["price"],
        pa_trail=trail[pa["trail"]],
        pa_trail_cap=s["balance"] + 100,
        activation_fee=pa["activation_fee"][size],
        tier_profit_from=[t["profit_from"] for t in tiers],
        tier_max_micros=[t["max_contracts"] * micros for t in tiers],
        tier_dll=[t["dll"] for t in tiers],
        min_daily_profit=pa["min_daily_profit"][size],
        payout_min_days=pa["payout"]["min_days"],
        payout_consistency=pa["payout"]["consistency"],
        payout_min_amount=pa["payout"]["min_amount"],
        payout_caps=pa["payout_caps"][size],
        safety_net=s["balance"] + s["drawdown"] + 100,
        commission_micro_rt=2 * f.commissions_per_side["micro"],
        verified_on=f.verified_on,
        open_questions=f.open_questions,
    )
