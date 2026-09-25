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

## P2 — Firm realism ✅ (2026-09-25; no trial accounts: BlackBull data + the firms' own pages)
- ✅ Commissions, tradable symbols and leverage per firm in `config/firmcosts.yaml`, from firm
  pages only (FTMO's public symbols JSON, FundedNext's and FundingPips' rule pages, The5ers'
  asset page, FXIFY's FAQ).
- ✅ Spread ratios vs BlackBull from the firms' published live spread tables (FTMO, FundedNext),
  two snapshots each, in `config/spread_snapshots.jsonl`; `record_spread_snapshot` adds more.
- ✅ Per-firm costs and cost stress in the gauntlet (`firm_costs` stage); the prop gate evaluates
  each program on its own firm's trades and skips firms that don't list the symbol.
- ✅ Every rule and fee re-verified: The5ers split by size (50K/100K are 4%/8%) and Classic added;
  FXIFY Classic and Pro added, 5 min days; FTMO fees in EUR, 1-Step end-of-day trailing;
  FundingPips has no news or weekend limits in evaluation and a baseline daily limit; FundedNext
  EAs only up to 25K with a paid add-on. Simulator, host config and QB_Host support the new
  semantics (baseline daily limit, balance/end-of-day trailing, lock).
- Still open (`verify:` items): FundingPips 1-Step Flex fees, FundedNext 25K fee and EA add-on
  price, The5ers and FXIFY symbol lists and non-FX commissions, FXIFY Classic/Pro phase order.
- Follow-up: more spread snapshots in the London and New York sessions (the first two were taken
  in the Asian session), e.g. a scheduled browser task.

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
