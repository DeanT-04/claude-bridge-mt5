"""Create the Obsidian vault skeleton. Idempotent: never overwrites an existing note."""

from pathlib import Path

FOLDERS = (
    "Ideas",
    "Sources",
    "Strategies",
    "Graveyard",
    "Lessons",
    "Firms",
    "Reports",
    "attachments",
    "_templates",
)

HOME = """\
# Prop Quant Lab

Knowledge base for the prop-firm strategy research pipeline. Every discovery lives here:
winners, contenders, failures and lessons. **Read [[Lessons]] before designing anything new.**

## Rules
- **No faking.** Every number comes from a recorded run (data hash + git commit + seed).
- Hypotheses are pre-registered in `Ideas/` *before* testing. Every trial is counted.
- The holdout (2025-03-25 → 2026-09-25) is opened once per strategy and logged.

## Promotion gates (out-of-sample, ≥ 1,000 random-start challenge simulations)
| Gate | Threshold |
|---|---|
| **End-to-end payout rate** (eval bought → ≥ 1 payout) | **≥ 60%** |
| Evaluation pass rate | ≥ 85% |
| First payout, once funded | ≥ 70% |
| Days to pass | median ≤ 15, 90th pct ≤ 30 |
| Expected profit per attempt after fees | 5th-pct bootstrap > 0 |
| Statistics | DSR > 0.95, beats 95% random-entry, holdout consistent |

Verdicts: **Elite** (all gates) · **Contender** (misses only speed gates or narrowly)
· **Graveyard**.

## Leaderboard
<!-- AUTO:leaderboard:start -->
_No strategies tested yet._
<!-- AUTO:leaderboard:end -->

## Map
- `Ideas/`: pre-registered hypotheses
- `Sources/`: papers, videos, articles (our own summaries)
- `Strategies/`: one note per tested strategy, with evidence charts
- `Graveyard/`: rejected strategies and why they failed
- `Lessons/`: what we've learned across runs
- `Firms/`: verified firm rules with source URLs and dates
- `Reports/`: batch run summaries and data-quality reports
"""

LESSONS = """\
# Lessons

Index of cross-cutting lessons. One note per lesson in this folder; link it here.

- (none yet)
"""

TEMPLATES = {
    "Idea.md": """\
---
type: idea
status: pre-registered
created: {{date}}
source: ""
family: ""
instruments: []
---
# {{title}}

## Hypothesis
What inefficiency or behaviour is being exploited, and why should it persist?

## Mechanism
Who is on the other side of the trade, and why do they lose?

## Exact rules
Entry, exit, stop, target, filters, session. No ambiguity.

## Parameter ranges (fixed before testing)
| Param | Range | Why |
|---|---|---|

## Expected failure modes
""",
    "Source.md": """\
---
type: source
kind: video | paper | article
url: ""
author: ""
fetched: {{date}}
---
# {{title}}

## Summary (our own words)

## Testable ideas extracted

## Credibility notes
""",
    "Strategy.md": """\
---
type: strategy
verdict: elite | contender | graveyard
idea: ""
run_id: ""
data_hash: ""
commit: ""
seed: 0
---
# {{title}}

## Verdict

## Gate results

## Evidence

## Notes
""",
    "Lesson.md": """\
---
type: lesson
created: {{date}}
evidence: []
---
# {{title}}

## What we observed

## Why it matters

## How to apply it next time
""",
}


def init_vault(root: Path) -> list[Path]:
    """Create missing folders and notes under ``root``. Returns the files created."""
    created: list[Path] = []
    for folder in FOLDERS:
        (root / folder).mkdir(parents=True, exist_ok=True)

    files = {root / "Home.md": HOME, root / "Lessons" / "Lessons.md": LESSONS}
    files.update({root / "_templates" / name: body for name, body in TEMPLATES.items()})
    for path, body in files.items():
        if not path.exists():
            path.write_text(body, encoding="utf-8")
            created.append(path)
    return created
