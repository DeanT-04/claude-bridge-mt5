# Plan: prop-firm pipeline

**Goal:** find strategies with the highest probability of passing 1-step / 2-step prop-firm
challenges (FTMO, FundedNext, FundingPips, The5ers, FXIFY), then run and manage those challenges
automatically. The personal small account and instant-funding programs are shelved.

The previous milestones (M1–M7) built the foundations: bridge, tester automation, research
engine and gauntlet, strategy families, generated and ML strategies, `QB_Host` deployment, and
prop rules. The phases below build on them.

## P1 — Prop core ✅ (2026-09-25)
- ✅ The gauntlet's `prop` stage is a **gate** (`gauntlet.yaml: prop`): best program P(pass) ≥ 0.6
  and lift ≥ 0.2 over the edge-removed (de-meaned) baseline, on walk-forward OOS trades, before
  the holdout is spent. OOS trades are stored per rule variant (`oos_trades`).
- ✅ **Leaderboard** (`prop_leaderboard`, `research.py leaderboard`): strategy/portfolio × program
  × size with P(pass), lift, best risk, median days, fee, cost per pass.
- ✅ **Combiner** (`prop_combine`, `research.py combine`): greedy, correlation-filtered,
  inverse-vol weights, risk capped by `max_open_risk_pct`; stored in `prop_portfolios`.
  `portfolio_allocation`, `prop_simulate` and `prop_rank` now use WF OOS trades.
- ✅ Weekend-flat and news-blackout rules in the engine (news calendar history from
  `QB_ExportCalendar`); the prop simulator is vectorised (~13× faster).
- ✅ Research resumed: queue topped up to the 61-symbol researchable universe (rule families,
  genetic, ML) and running under the prop gate.
- Follow-ups: run `combine` once survivors exist; tune the gate thresholds on real survivors.

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
  windows (calendar), Friday flattening (also before an earlier market close: the engine flattens
  at the last bar before the cutoff, while QB_Host only acts on ticks inside the window).
- Challenge dashboard / chat summaries per account.

## P5 — Funded stage
- Separate funded-account sizing (payout- and consistency-oriented, e.g. FundingPips 35%,
  FXIFY 25% funded consistency rules), scaling plans, payout tracking.

## Standing constraints
- Demo forward test (BlackBull demo, USD 10,000) before any prop account.
- Prop accounts need the user to log in, set `account.enabled_targets`, pass `prop_preflight`,
  and approve every `apply_deployment`.
- FXIFY needs written EA approval (`terminals.<name>.ea_approved`).
