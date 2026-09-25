CREATE TABLE IF NOT EXISTS trials (
    id          INTEGER PRIMARY KEY,
    family      TEXT NOT NULL,      -- strategy template, e.g. donchian
    symbol      TEXT NOT NULL,
    timeframe   TEXT NOT NULL,
    params      TEXT NOT NULL,      -- JSON
    sr_trade    REAL,               -- per-trade Sharpe on the evaluated segment
    trades      INTEGER,
    created     TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS trials_key ON trials(family, symbol, timeframe);

CREATE TABLE IF NOT EXISTS runs (
    id          INTEGER PRIMARY KEY,
    engine      TEXT NOT NULL,      -- py | mt5
    tag         TEXT,
    family      TEXT,
    symbol      TEXT,
    timeframe   TEXT,
    params      TEXT,
    metrics     TEXT,               -- JSON
    trades      TEXT,               -- JSON list (mt5 trade CSV rows or py trades)
    created     TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS gauntlets (
    id          INTEGER PRIMARY KEY,
    candidate   TEXT NOT NULL,      -- hash(family, symbol, timeframe, params)
    family      TEXT, symbol TEXT, timeframe TEXT, params TEXT,
    verdict     TEXT NOT NULL,      -- pass | fail
    stages      TEXT NOT NULL,      -- JSON: stage -> {pass, metrics}
    created     TEXT NOT NULL DEFAULT (datetime('now'))
);

-- A candidate may look at the holdout exactly once.
CREATE TABLE IF NOT EXISTS holdout_uses (
    candidate   TEXT PRIMARY KEY,
    result      TEXT,
    used        TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS universe (
    symbol          TEXT PRIMARY KEY,
    grp             TEXT,
    researchable    INTEGER,
    small_account   INTEGER,
    metrics         TEXT,           -- JSON from research.universe.scan
    updated         TEXT
);

-- Research queue: python gauntlets run in parallel; MT5 confirmation runs serially after.
CREATE TABLE IF NOT EXISTS jobs (
    id          INTEGER PRIMARY KEY,
    family      TEXT NOT NULL,
    symbol      TEXT NOT NULL,
    timeframe   TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'queued',   -- queued | running | done | error
    gauntlet_id INTEGER,
    verdict     TEXT,
    error       TEXT,
    created     TEXT NOT NULL DEFAULT (datetime('now')),
    started     TEXT,
    finished    TEXT
);

-- Portfolio configs proposed to / applied on a terminal (target = demo | live).
CREATE TABLE IF NOT EXISTS deployments (
    id          INTEGER PRIMARY KEY,
    target      TEXT NOT NULL,
    version     INTEGER NOT NULL,
    sha256      TEXT NOT NULL,
    config      TEXT NOT NULL,
    sleeves     TEXT NOT NULL,      -- JSON
    status      TEXT NOT NULL,      -- proposed | applied | superseded | rejected | kill
    note        TEXT,
    created     TEXT NOT NULL DEFAULT (datetime('now')),
    applied     TEXT
);

-- Generated strategy genomes (M4); family name = 'gen_' || id.
CREATE TABLE IF NOT EXISTS genomes (
    id          TEXT PRIMARY KEY,
    genome      TEXT NOT NULL,      -- JSON (canonical)
    description TEXT,
    symbol      TEXT,               -- where it was discovered
    timeframe   TEXT,
    fitness     REAL,
    created     TEXT NOT NULL DEFAULT (datetime('now'))
);
