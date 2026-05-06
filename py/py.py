-- ============================================================
-- Fastener Standards Cross-Reference Database
-- Schema v1.0
-- ============================================================

PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;
PRAGMA encoding = 'UTF-8';

-- ------------------------------------------------------------
-- Core standards table
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS standards (
    id            TEXT PRIMARY KEY,        -- e.g. "gost_7798_70"
    standard_no   TEXT NOT NULL UNIQUE,    -- e.g. "GOST 7798-70"
    title         TEXT NOT NULL,
    body          TEXT NOT NULL,           -- GOST | ISO | DIN | BIS
    country       TEXT NOT NULL,
    domain        TEXT NOT NULL DEFAULT 'fasteners',
    subdomain     TEXT,                    -- bolts | nuts | washers | ...
    category      TEXT NOT NULL,           -- bolt | nut | washer | ...
    sub_category  TEXT,
    status        TEXT NOT NULL DEFAULT 'active',   -- active | withdrawn
    replaced_by   TEXT,
    confidence    TEXT NOT NULL DEFAULT 'high',     -- high | medium | low | flag
    thread_range  TEXT,
    doc_version   TEXT,
    last_updated  TEXT,
    path          TEXT,                    -- relative path to .md file
    notes         TEXT
);

-- ------------------------------------------------------------
-- Equivalents / cross-references
-- One row per directed relationship
-- relation_type: identical | equivalent | similar | predecessor
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS equivalents (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id       TEXT NOT NULL REFERENCES standards(id),
    target_standard TEXT NOT NULL,         -- e.g. "ISO 4032"
    target_body     TEXT NOT NULL,         -- GOST | ISO | DIN | BIS | ASTM
    relation_type   TEXT NOT NULL DEFAULT 'equivalent',
    confidence      TEXT NOT NULL DEFAULT 'high',
    notes           TEXT
);

-- ------------------------------------------------------------
-- Mechanical properties
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS mechanical_properties (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    standard_id     TEXT NOT NULL REFERENCES standards(id),
    property_class  TEXT NOT NULL,         -- e.g. "8.8", "A2-70"
    tensile_min_mpa INTEGER,
    yield_min_mpa   INTEGER,
    hardness_min_hv INTEGER,
    hardness_max_hv INTEGER,
    notes           TEXT
);

-- ------------------------------------------------------------
-- Property list (thread_range, grade, coating, temp limit etc.)
-- Key-value store for flexible attributes
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS properties (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    standard_id     TEXT NOT NULL REFERENCES standards(id),
    key             TEXT NOT NULL,
    value           TEXT NOT NULL
);

-- ------------------------------------------------------------
-- Engineering warnings / reliability notes
-- Surfaced prominently in the UI
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS warnings (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    standard_id     TEXT NOT NULL REFERENCES standards(id),
    severity        TEXT NOT NULL DEFAULT 'info',  -- critical | warning | info
    code            TEXT,                           -- e.g. "SINGLE_USE", "NO_HDG", "WAF_DIFF"
    message         TEXT NOT NULL
);

-- ------------------------------------------------------------
-- WAF (Width Across Flats) conflict table
-- Used by compare engine
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS waf_conflicts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    standard_a      TEXT NOT NULL,
    standard_b      TEXT NOT NULL,
    thread_size     TEXT NOT NULL,         -- e.g. "M10"
    waf_a_mm        REAL NOT NULL,
    waf_b_mm        REAL NOT NULL,
    notes           TEXT
);

-- ------------------------------------------------------------
-- Aliases — common names, trade names, legacy refs
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS aliases (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    standard_id     TEXT NOT NULL REFERENCES standards(id),
    alias           TEXT NOT NULL
);

-- ------------------------------------------------------------
-- Tags — for semantic search and filtering
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS tags (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    standard_id     TEXT NOT NULL REFERENCES standards(id),
    tag             TEXT NOT NULL
);

-- ------------------------------------------------------------
-- FTS5 full-text search virtual table
-- Covers everything a user might type
-- ------------------------------------------------------------
CREATE VIRTUAL TABLE IF NOT EXISTS standards_fts USING fts5(
    standard_no,
    title,
    body,
    category,
    sub_category,
    notes,
    content='standards',
    content_rowid='rowid'
);

-- FTS triggers to keep index in sync
CREATE TRIGGER IF NOT EXISTS standards_ai AFTER INSERT ON standards BEGIN
    INSERT INTO standards_fts(rowid, standard_no, title, body, category, sub_category, notes)
    VALUES (new.rowid, new.standard_no, new.title, new.body, new.category, new.sub_category, new.notes);
END;

CREATE TRIGGER IF NOT EXISTS standards_ad AFTER DELETE ON standards BEGIN
    INSERT INTO standards_fts(standards_fts, rowid, standard_no, title, body, category, sub_category, notes)
    VALUES ('delete', old.rowid, old.standard_no, old.title, old.body, old.category, old.sub_category, old.notes);
END;

CREATE TRIGGER IF NOT EXISTS standards_au AFTER UPDATE ON standards BEGIN
    INSERT INTO standards_fts(standards_fts, rowid, standard_no, title, body, category, sub_category, notes)
    VALUES ('delete', old.rowid, old.standard_no, old.title, old.body, old.category, old.sub_category, old.notes);
    INSERT INTO standards_fts(rowid, standard_no, title, body, category, sub_category, notes)
    VALUES (new.rowid, new.standard_no, new.title, new.body, new.category, new.sub_category, new.notes);
END;

-- ------------------------------------------------------------
-- Indexes
-- ------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_standards_body     ON standards(body);
CREATE INDEX IF NOT EXISTS idx_standards_category ON standards(category);
CREATE INDEX IF NOT EXISTS idx_standards_status   ON standards(status);
CREATE INDEX IF NOT EXISTS idx_equivalents_source ON equivalents(source_id);
CREATE INDEX IF NOT EXISTS idx_equivalents_target ON equivalents(target_standard);
CREATE INDEX IF NOT EXISTS idx_tags_tag            ON tags(tag);
CREATE INDEX IF NOT EXISTS idx_aliases_alias       ON aliases(alias);
CREATE INDEX IF NOT EXISTS idx_properties_key      ON properties(standard_id, key);

-- ------------------------------------------------------------
-- Seed: WAF conflict data (DIN 931 vs ISO 4014)
-- ------------------------------------------------------------
INSERT OR IGNORE INTO waf_conflicts (standard_a, standard_b, thread_size, waf_a_mm, waf_b_mm, notes) VALUES
    ('DIN 931', 'ISO 4014', 'M10', 17.0, 16.0, 'DIN 931 uses 17mm WAF; ISO 4014 uses 16mm. Verify spanner compatibility.'),
    ('DIN 931', 'ISO 4014', 'M12', 19.0, 18.0, 'DIN 931 uses 19mm WAF; ISO 4014 uses 18mm. Verify spanner compatibility.'),
    ('DIN 931', 'ISO 4014', 'M14', 22.0, 21.0, 'DIN 931 uses 22mm WAF; ISO 4014 uses 21mm. Verify spanner compatibility.'),
    ('DIN 931', 'ISO 4014', 'M22', 32.0, 34.0, 'DIN 931 uses 32mm WAF; ISO 4014 uses 34mm. Verify spanner compatibility.');