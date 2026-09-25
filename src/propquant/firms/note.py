"""Render a firm's verified rules into its vault note (Firms/<Name>.md)."""

from propquant.firms.base import load_firm
from propquant.vault import writer


def write(firm: str) -> str:
    f = load_firm(firm)
    lines = [
        "---",
        "type: firm",
        f"firm: {f.firm}",
        f"verified_on: {f.verified_on}",
        "---",
        f"# {f.name}",
        "",
        f"Rules verified **{f.verified_on}** from the firm's own pages (Internet Archive captures;",
        f"the live site blocks automated readers). Platform modelled: **{f.platform}**.",
        f"Source of truth: `config/firms/{f.firm}.yaml`.",
        "",
    ]
    for plan, body in f.plans.items():
        ev, pa = body["eval"], body["pa"]
        lines += [f"## {plan.upper()} plan", "", "### Evaluation", ""]
        rows = [{"size": k, **v} for k, v in ev["sizes"].items()]
        lines += [writer.md_table(rows), ""]
        lines += [
            f"- Drawdown trails: **{ev['trail']}**; stops trailing at the {ev['trail_stops_at']}"
            " balance",
            f"- Access: {ev['access_calendar_days']} calendar days; min trading days:"
            f" {ev['min_trading_days']}; DLL pauses the day: {ev['dll_pauses_day']}",
            "",
            "### Performance account",
            "",
            f"- Drawdown trails **{pa['trail']}**, locks at start + $100",
            f"- Payouts: {pa['payout']}",
            f"- Min profit for a qualifying day: {pa['min_daily_profit']}",
            f"- Activation fee: {pa['activation_fee']}",
            "",
        ]
        rows = [{"size": k, **{f"#{i + 1}": c for i, c in enumerate(v)}}
                for k, v in pa["payout_caps"].items()]  # fmt: skip
        lines += ["Payout caps:", "", writer.md_table(rows), ""]
    lines += ["## PA scaling tiers", ""]
    for size, tiers in f.pa_tiers.items():
        lines += [f"**{size}**", "", writer.md_table(tiers), ""]
    lines += ["## Commissions (per side)", "", str(f.commissions_per_side), ""]
    lines += ["## Open questions / modelling assumptions", ""]
    lines += [f"- {q}" for q in f.open_questions]
    lines += ["", "## Sources", ""]
    lines += [f"- `{k}`: {s.url} (capture {s.capture}) {s.note}" for k, s in f.sources.items()]
    path = writer.write_note(f"Firms/{f.name}.md", "\n".join(lines) + "\n")
    return str(path)
