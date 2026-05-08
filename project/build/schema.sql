CREATE TABLE IF NOT EXISTS standards (
    id                        INTEGER PRIMARY KEY AUTOINCREMENT,
    standard                  TEXT NOT NULL UNIQUE,
    title                     TEXT,
    category                  TEXT,
    sub_category              TEXT,
    body                      TEXT,
    country                   TEXT,
    status                    TEXT,
    replaced_by               TEXT,
    confidence                TEXT,
    thread_range              TEXT,
    thread_tolerance          TEXT,
    product_grade             TEXT,
    max_temperature_c         INTEGER,
    single_use                INTEGER,
    head_type                 TEXT,
    drive                     TEXT,
    waf_notes                 TEXT,
    length_range              TEXT,
    tolerance_grade           TEXT,
    primary_materials         TEXT,
    stainless_variants        TEXT,
    materials_notes           TEXT,
    surface_available         TEXT,
    surface_prohibited        TEXT,
    coating_codes             TEXT,
    hydrogen_embrittlement_bake TEXT,
    head_marking_required     INTEGER,
    class_12_9_rule           TEXT,
    marking_notes             TEXT,
    proof_load_test           INTEGER,
    prevailing_torque_cycles  INTEGER,
    testing_standard_reference TEXT,
    designation_gost          TEXT,
    designation_iso           TEXT,
    designation_din           TEXT,
    designation_indian        TEXT,
    property_classes          TEXT,
    reliability_notes         TEXT,
    sources                   TEXT,
    source_type               TEXT,
    legal_status              TEXT,
    doc_version               TEXT,
    last_updated              TEXT,
    yaml_path                 TEXT,
    raw_record_json           TEXT
);

CREATE TABLE IF NOT EXISTS equivalents (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    standard_id   INTEGER NOT NULL REFERENCES standards(id),
    body          TEXT NOT NULL,
    equivalent    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS mechanical_properties (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    standard_id           INTEGER NOT NULL REFERENCES standards(id),
    property_class        TEXT,
    tensile_strength_mpa  INTEGER,
    yield_strength_mpa    INTEGER,
    hardness_min          TEXT,
    hardness_max          TEXT,
    proof_load_mpa        INTEGER
);

CREATE VIRTUAL TABLE IF NOT EXISTS standards_fts
USING fts5(standard, title, sub_category, category, content='standards', content_rowid='id');

CREATE INDEX IF NOT EXISTS idx_standards_body ON standards(body);
CREATE INDEX IF NOT EXISTS idx_standards_category ON standards(category);
CREATE INDEX IF NOT EXISTS idx_standards_standard ON standards(standard);
CREATE INDEX IF NOT EXISTS idx_equivalents_standard_id ON equivalents(standard_id);
CREATE INDEX IF NOT EXISTS idx_mech_props_standard_id ON mechanical_properties(standard_id);
