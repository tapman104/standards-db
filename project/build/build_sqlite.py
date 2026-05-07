"""
build_sqlite.py  —  Load all YAML fastener records and write to SQLite DB.

Usage:
    cd project/build
    python build_sqlite.py

Output: project/build/sqlite/standards.db
"""
import sys, pathlib, sqlite3, json, yaml

ROOT     = pathlib.Path(__file__).resolve().parent.parent
YAML_DIR = ROOT / "data" / "yaml"
DB_PATH  = ROOT / "build" / "sqlite" / "standards.db"

# ─── DDL ──────────────────────────────────────────────────────────────────────

DDL_STANDARDS = """
CREATE TABLE IF NOT EXISTS standards (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    standard                TEXT NOT NULL,
    title                   TEXT,
    category                TEXT,
    sub_category            TEXT,
    body                    TEXT,
    country                 TEXT,
    status                  TEXT,
    replaced_by             TEXT,
    confidence              TEXT,
    thread_range            TEXT,
    thread_tolerance        TEXT,
    product_grade           TEXT,
    max_temperature_c       INTEGER,
    single_use              INTEGER,       -- 0/1 boolean
    -- dimensions
    head_type               TEXT,
    drive                   TEXT,
    waf_notes               TEXT,
    length_range            TEXT,
    tolerance_grade         TEXT,
    -- materials
    primary_materials       TEXT,          -- JSON array
    stainless_variants      TEXT,          -- JSON array
    materials_notes         TEXT,
    -- surface treatments
    surface_available       TEXT,          -- JSON array
    surface_prohibited      TEXT,          -- JSON array
    coating_codes           TEXT,          -- JSON object
    h_embrittlement_bake    TEXT,
    -- marking
    head_marking_required   INTEGER,       -- 0/1/NULL
    class_12_9_rule         TEXT,
    marking_notes           TEXT,
    -- testing
    proof_load_test         INTEGER,       -- 0/1/NULL
    prevailing_torque_cycles INTEGER,
    testing_standard_ref    TEXT,
    -- designation examples
    designation_gost        TEXT,
    designation_iso         TEXT,
    designation_din         TEXT,
    designation_indian      TEXT,
    -- arrays stored as JSON
    property_classes        TEXT,          -- JSON array
    reliability_notes       TEXT,          -- JSON array
    sources                 TEXT,          -- JSON array
    -- meta
    source_type             TEXT,
    legal_status            TEXT,
    doc_version             TEXT,
    last_updated            TEXT,
    -- housekeeping
    yaml_path               TEXT
);
"""

DDL_EQUIVALENTS = """
CREATE TABLE IF NOT EXISTS equivalents (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    standard_id     INTEGER NOT NULL REFERENCES standards(id),
    body            TEXT NOT NULL,    -- iso | din | gost | indian
    equivalent      TEXT NOT NULL
);
"""

DDL_MECH_PROPS = """
CREATE TABLE IF NOT EXISTS mechanical_properties (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    standard_id             INTEGER NOT NULL REFERENCES standards(id),
    property_class          TEXT,
    tensile_strength_mpa    INTEGER,
    yield_strength_mpa      INTEGER,
    hardness_min            TEXT,
    hardness_max            TEXT,
    proof_load_mpa          INTEGER
);
"""

DDL_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_std_body     ON standards(body);",
    "CREATE INDEX IF NOT EXISTS idx_std_category ON standards(category);",
    "CREATE INDEX IF NOT EXISTS idx_std_standard ON standards(standard);",
    "CREATE INDEX IF NOT EXISTS idx_eq_standard  ON equivalents(standard_id);",
    "CREATE INDEX IF NOT EXISTS idx_mp_standard  ON mechanical_properties(standard_id);",
]

# ─── helpers ──────────────────────────────────────────────────────────────────

def jdump(val):
    """Serialise a Python value to a JSON string; return None if not a useful container."""
    if val is None:
        return None
    if isinstance(val, (list, dict)):
        return json.dumps(val, ensure_ascii=False)
    return str(val)

def bool_int(val):
    if val is None:
        return None
    return 1 if val else 0

# ─── main ─────────────────────────────────────────────────────────────────────

def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()
        print(f"Removed existing DB at {DB_PATH}")

    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys = ON;")
    con.execute("PRAGMA journal_mode = WAL;")
    con.executescript(DDL_STANDARDS + DDL_EQUIVALENTS + DDL_MECH_PROPS)
    for idx in DDL_INDEXES:
        con.execute(idx)
    con.commit()

    files = sorted(YAML_DIR.rglob("*.yaml"))
    print(f"Loading {len(files)} YAML files …")

    inserted = 0
    errors   = []

    for f in files:
        try:
            with open(f, encoding="utf-8") as fh:
                d = yaml.safe_load(fh)
        except yaml.YAMLError as exc:
            errors.append(f"{f}: YAML error — {exc}")
            continue

        dim  = d.get("dimensions") or {}
        mat  = d.get("materials") or {}
        surf = d.get("surface_treatments") or {}
        mark = d.get("marking") or {}
        test = d.get("testing") or {}
        desig = d.get("designation_examples") or {}
        meta  = d.get("meta") or {}

        cur = con.execute("""
            INSERT INTO standards (
                standard, title, category, sub_category, body, country, status, replaced_by,
                confidence, thread_range, thread_tolerance, product_grade, max_temperature_c,
                single_use,
                head_type, drive, waf_notes, length_range, tolerance_grade,
                primary_materials, stainless_variants, materials_notes,
                surface_available, surface_prohibited, coating_codes, h_embrittlement_bake,
                head_marking_required, class_12_9_rule, marking_notes,
                proof_load_test, prevailing_torque_cycles, testing_standard_ref,
                designation_gost, designation_iso, designation_din, designation_indian,
                property_classes, reliability_notes, sources,
                source_type, legal_status, doc_version, last_updated,
                yaml_path
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            d.get("standard"),          d.get("title"),
            d.get("category"),          d.get("sub_category"),
            d.get("body"),              d.get("country"),
            d.get("status"),            d.get("replaced_by"),
            d.get("confidence"),        d.get("thread_range"),
            d.get("thread_tolerance"),  d.get("product_grade"),
            d.get("max_temperature_c"), bool_int(d.get("single_use")),
            dim.get("head_type"),       dim.get("drive"),
            dim.get("waf_notes"),       dim.get("length_range"),
            dim.get("tolerance_grade"),
            jdump(mat.get("primary")),  jdump(mat.get("stainless_variants")),
            mat.get("notes"),
            jdump(surf.get("available")), jdump(surf.get("prohibited")),
            jdump(surf.get("coating_codes")), surf.get("hydrogen_embrittlement_bake"),
            bool_int(mark.get("head_marking_required")),
            mark.get("class_12_9_rule"), mark.get("notes"),
            bool_int(test.get("proof_load_test")),
            test.get("prevailing_torque_cycles"), test.get("standard_reference"),
            desig.get("gost"),  desig.get("iso"),
            desig.get("din"),   desig.get("indian"),
            jdump(d.get("property_classes")),
            jdump(d.get("reliability_notes")),
            jdump(d.get("sources")),
            meta.get("source_type"),   meta.get("legal_status"),
            meta.get("doc_version"),   meta.get("last_updated"),
            f.relative_to(ROOT).as_posix(),
        ))
        std_id = cur.lastrowid

        # equivalents
        eq = d.get("equivalents") or {}
        for body, lst in eq.items():
            if isinstance(lst, list):
                for equiv in lst:
                    con.execute(
                        "INSERT INTO equivalents (standard_id, body, equivalent) VALUES (?,?,?)",
                        (std_id, body, equiv)
                    )

        # mechanical_properties
        mp_list = d.get("mechanical_properties") or []
        for mp in mp_list:
            if not isinstance(mp, dict):
                continue
            con.execute("""
                INSERT INTO mechanical_properties
                    (standard_id, property_class, tensile_strength_mpa, yield_strength_mpa,
                     hardness_min, hardness_max, proof_load_mpa)
                VALUES (?,?,?,?,?,?,?)
            """, (
                std_id,
                mp.get("property_class"),
                mp.get("tensile_strength_mpa"),
                mp.get("yield_strength_mpa"),
                mp.get("hardness_min"),
                mp.get("hardness_max"),
                mp.get("proof_load_mpa"),
            ))

        inserted += 1

    con.commit()
    con.close()

    if errors:
        print(f"\nWarnings ({len(errors)}):")
        for e in errors:
            print(f"  {e}")

    print(f"\nDone — {inserted} standards written to {DB_PATH}")

    # ── quick sanity report ───────────────────────────────────────────────────
    con2 = sqlite3.connect(DB_PATH)
    rows = con2.execute(
        "SELECT body, category, COUNT(*) FROM standards GROUP BY body, category ORDER BY body, category"
    ).fetchall()
    print(f"\n{'Body':<8} {'Category':<25} Count")
    print("-" * 40)
    for body, cat, cnt in rows:
        print(f"{body:<8} {cat:<25} {cnt}")
    print(f"\nTotal equivalents rows : {con2.execute('SELECT COUNT(*) FROM equivalents').fetchone()[0]}")
    print(f"Total mech-prop rows   : {con2.execute('SELECT COUNT(*) FROM mechanical_properties').fetchone()[0]}")
    con2.close()


if __name__ == "__main__":
    main()
