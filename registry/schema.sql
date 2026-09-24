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
