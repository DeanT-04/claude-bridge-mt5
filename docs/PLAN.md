# Plan: prop-firm pipeline

**Goal:** find strategies with the highest probability of passing 1-step / 2-step prop-firm
challenges (FTMO, FundedNext, FundingPips, The5ers, FXIFY), then run and manage those challenges
automatically. The personal small account and instant-funding programs are shelved.

The previous milestones (M1–M7) built the foundations: bridge, tester automation, research
engine and gauntlet, strategy families, generated and ML strategies, `QB_Host` deployment, and
prop rules. The phases below build on them.

## P1 — Prop core
- Make the gauntlet's `prop` stage a **gate**: best P(pass) over the chosen programs ≥ a
  threshold in `gauntlet.yaml`. It already runs on walk-forward OOS trades.
- A **leaderboard** tool: strategy (or portfolio) × program × size, with P(pass), the risk that
  maximises it, median days, fee and cost per pass.
- Portfolio search for challenges: combine uncorrelated survivors and rank the combination
  (`prop_rank` exists; add an automatic combiner). Base `portfolio_allocation` on WF OOS trades,
  not the tuned params.
- Weekend-flat and news-blackout rules in the backtest engine, so firms with those rules are
  simulated faithfully. The best-day, min-profitable-days and trailing-lock rules are already
  simulated.
- Resume research: the queue still holds the stopped M4/M5 jobs (genetic + ML); rerun them
  under the prop stage, over the researchable universe (61 symbols, including gold and indices).

## P2 — Firm realism (no trial accounts: BlackBull data + verified published figures)
- Collect each firm's published spreads, commissions per lot and symbol lists from verified
  sources (firm help centres, reputable reviews) into `config/propfirms.yaml` costs.
- Per-firm cost stress in the gauntlet (commission + spread differences vs BlackBull).
- Re-verify every `verify:` item and fee in `config/propfirms.yaml`.

## P3 — Strategy sourcing
- Pipelines that turn research papers, YouTube transcripts and Instagram transcripts into
  strategy specs: extraction → structured spec → mapped to QB_GENERIC genomes or new families.
- Provenance kept per strategy; every sourced idea still goes through the full gauntlet.

## P4 — Challenge execution
- Phase tracking in `QB_Host`: know the phase target, **stop trading once the target and the
  minimum days are met**, then top up missing minimum trading days with tiny positions.
- Firm-specific guards: FTMO request limits, FundingPips same-direction re-entry rule, news
  windows (calendar), Friday flattening.
- Challenge dashboard / chat summaries per account.

## P5 — Funded stage
- Separate funded-account sizing (payout- and consistency-oriented, e.g. FundingPips 35%,
  FXIFY 25% funded consistency rules), scaling plans, payout tracking.

## Standing constraints
- Demo forward test (BlackBull demo, USD 10,000) before any prop account.
- Prop accounts need the user to log in, set `account.enabled_targets`, pass `prop_preflight`,
  and approve every `apply_deployment`.
- FXIFY needs written EA approval (`terminals.<name>.ea_approved`).
