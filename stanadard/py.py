import sqlite3
import os
import json
import re
from pathlib import Path

# ============================================================
# Fastener Standards Database Manager
# Handles schema initialization, FTS5 indexing, and data import
# ============================================================

DB_PATH = Path("fasteners.db")
DATA_DIR = Path("stanadard") # Path to the standards data directory

SCHEMA = """
-- Core settings
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
    overview      TEXT,                    -- # Standard Overview section
    cross_refs_raw TEXT,                   -- # Cross References section
    withdrawal_note TEXT,                  -- # Withdrawal Note section
    notes         TEXT
);

-- ------------------------------------------------------------
-- Equivalents / cross-references
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
-- Surface Treatments & Coatings
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS surface_treatments (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    standard_id     TEXT NOT NULL REFERENCES standards(id),
    code            TEXT,                  -- e.g. "01" (GOST) or "A2P" (ISO)
    description     TEXT NOT NULL,
    process         TEXT,                  -- electroplate | HDG | phosphate
    notes           TEXT
);

-- ------------------------------------------------------------
-- Tightening Torque Guidelines
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS tightening_torque (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    standard_id     TEXT NOT NULL REFERENCES standards(id),
    thread_size     TEXT NOT NULL,         -- e.g. "M10"
    property_class  TEXT NOT NULL,
    torque_nm       REAL NOT NULL,
    preload_kn      REAL,
    friction_coef   REAL DEFAULT 0.14,     -- default k-factor
    notes           TEXT
);

-- ------------------------------------------------------------
-- Property list (flexible attributes)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS properties (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    standard_id     TEXT NOT NULL REFERENCES standards(id),
    key             TEXT NOT NULL,
    value           TEXT NOT NULL
);

-- ------------------------------------------------------------
-- Engineering warnings / safety notes
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS warnings (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    standard_id     TEXT NOT NULL REFERENCES standards(id),
    severity        TEXT NOT NULL DEFAULT 'info',  -- critical | warning | info
    code            TEXT,                          -- e.g. "SINGLE_USE", "TEMP_LIMIT"
    message         TEXT NOT NULL
);

-- ------------------------------------------------------------
-- WAF (Width Across Flats) conflict table
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS waf_conflicts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    standard_a      TEXT NOT NULL,
    standard_b      TEXT NOT NULL,
    thread_size     TEXT NOT NULL,
    waf_a_mm        REAL NOT NULL,
    waf_b_mm        REAL NOT NULL,
    notes           TEXT
);

-- ------------------------------------------------------------
-- FTS5 Full-Text Search
-- ------------------------------------------------------------
CREATE VIRTUAL TABLE IF NOT EXISTS standards_fts USING fts5(
    standard_no,
    title,
    body,
    category,
    sub_category,
    overview,
    withdrawal_note,
    notes,
    content='standards',
    content_rowid='rowid'
);

-- FTS Triggers
CREATE TRIGGER IF NOT EXISTS standards_ai AFTER INSERT ON standards BEGIN
    INSERT INTO standards_fts(rowid, standard_no, title, body, category, sub_category, overview, withdrawal_note, notes)
    VALUES (new.rowid, new.standard_no, new.title, new.body, new.category, new.sub_category, new.overview, new.withdrawal_note, new.notes);
END;

CREATE TRIGGER IF NOT EXISTS standards_ad AFTER DELETE ON standards BEGIN
    INSERT INTO standards_fts(standards_fts, rowid, standard_no, title, body, category, sub_category, overview, withdrawal_note, notes)
    VALUES ('delete', old.rowid, old.standard_no, old.title, old.body, old.category, old.sub_category, old.overview, old.withdrawal_note, old.notes);
END;

CREATE TRIGGER IF NOT EXISTS standards_au AFTER UPDATE ON standards BEGIN
    INSERT INTO standards_fts(standards_fts, rowid, standard_no, title, body, category, sub_category, overview, withdrawal_note, notes)
    VALUES ('delete', old.rowid, old.standard_no, old.title, old.body, old.category, old.sub_category, old.overview, old.withdrawal_note, old.notes);
    INSERT INTO standards_fts(rowid, standard_no, title, body, category, sub_category, overview, withdrawal_note, notes)
    VALUES (new.rowid, new.standard_no, new.title, new.body, new.category, new.sub_category, new.overview, new.withdrawal_note, new.notes);
END;

-- Indexes
CREATE INDEX IF NOT EXISTS idx_standards_body     ON standards(body);
CREATE INDEX IF NOT EXISTS idx_standards_category ON standards(category);
CREATE INDEX IF NOT EXISTS idx_equivalents_source ON equivalents(source_id);
CREATE INDEX IF NOT EXISTS idx_properties_key      ON properties(standard_id, key);

-- Seed: WAF conflict data
INSERT OR IGNORE INTO waf_conflicts (standard_a, standard_b, thread_size, waf_a_mm, waf_b_mm, notes) VALUES
    ('DIN 931', 'ISO 4014', 'M10', 17.0, 16.0, 'DIN 931 uses 17mm WAF; ISO 4014 uses 16mm.'),
    ('DIN 931', 'ISO 4014', 'M12', 19.0, 18.0, 'DIN 931 uses 19mm WAF; ISO 4014 uses 18mm.'),
    ('DIN 931', 'ISO 4014', 'M14', 22.0, 21.0, 'DIN 931 uses 22mm WAF; ISO 4014 uses 21mm.'),
    ('DIN 931', 'ISO 4014', 'M22', 32.0, 34.0, 'DIN 931 uses 32mm WAF; ISO 4014 uses 34mm.');
"""

def extract_section(content, section_name):
    """Extracts content under a specific markdown header."""
    pattern = rf"# {section_name}\s*(.*?)(?=\n# |\Z)"
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else None

def init_db():
    """Initializes the database schema."""
    print(f"Connecting to {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    try:
        # Drop existing tables to apply new schema correctly
        conn.execute("DROP TABLE IF EXISTS standards_fts;")
        conn.execute("DROP TABLE IF EXISTS standards;")
        conn.executescript(SCHEMA)
        conn.commit()
        print("Schema applied successfully.")
    except sqlite3.Error as e:
        print(f"SQL Error: {e}")
    finally:
        conn.close()

def import_from_json():
    """Imports data from index.json and associated markdown files."""
    json_path = DATA_DIR / "standards" / "index.json"
    if not json_path.exists():
        print(f"Error: {json_path} not found.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print(f"Importing {len(data)} standards with documentation...")
    
    for item in data:
        std_no = item.get("standard", "")
        std_id = std_no.lower().replace(" ", "_").replace("-", "_").replace(".", "_")
        rel_path = item.get("path", "")
        full_path = DATA_DIR / rel_path
        
        overview = None
        cross_refs = None
        withdrawal = None
        
        if full_path.exists():
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                overview = extract_section(content, "Standard Overview")
                cross_refs = extract_section(content, "Cross References")
                withdrawal = extract_section(content, "Withdrawal Note")

        try:
            cursor.execute("""
                INSERT OR REPLACE INTO standards (
                    id, standard_no, title, body, country, category, sub_category, 
                    path, overview, cross_refs_raw, withdrawal_note
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                std_id,
                std_no,
                item.get("title", "Untitled"),
                item.get("body", "UNKNOWN"),
                item.get("country", "Unknown"),
                item.get("category", "fastener"),
                item.get("sub_category", ""),
                rel_path,
                overview,
                cross_refs,
                withdrawal
            ))

            # Import equivalents
            eqs = item.get("equivalents", {})
            for body, targets in eqs.items():
                if isinstance(targets, list):
                    for target in targets:
                        cursor.execute("""
                            INSERT OR IGNORE INTO equivalents (source_id, target_standard, target_body)
                            VALUES (?, ?, ?)
                        """, (std_id, target, body.upper()))

        except sqlite3.Error as e:
            print(f"Error importing {std_no}: {e}")

    conn.commit()
    conn.close()
    print("Import complete.")

def search(query):
    """Performs a full-text search on the standards."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    sql = """
        SELECT standard_no, title, body, category, rank, overview
        FROM standards_fts 
        WHERE standards_fts MATCH ? 
        ORDER BY rank
    """
    
    print(f"Searching for: {query}")
    for row in cursor.execute(sql, (query,)):
        print(f"[{row[2]}] {row[0]}: {row[1]}")
        if row[5]:
            print(f"   Overview: {row[5][:100]}...")
    
    conn.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python py.py [init | import | search <query>]")
    elif sys.argv[1] == "init":
        init_db()
    elif sys.argv[1] == "import":
        import_from_json()
    elif sys.argv[1] == "search" and len(sys.argv) > 2:
        search(" ".join(sys.argv[2:]))
    else:
        if not DB_PATH.exists():
            init_db()
            import_from_json()
        else:
            print("Database already exists. Use 'python py.py search <query>' to test.")