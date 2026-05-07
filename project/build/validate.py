"""
validate.py  —  Validate all YAML fastener records in project/data/yaml/
against the structural schema (no external dependencies; pure stdlib + PyYAML).

Usage:
    cd project/build
    python validate.py
"""
import sys, pathlib, yaml, json

ROOT = pathlib.Path(__file__).resolve().parent.parent
YAML_DIR = ROOT / "data" / "yaml"

REQUIRED_TOP = [
    "standard", "title", "category", "sub_category", "body", "country",
    "status", "confidence", "equivalents", "property_classes",
    "dimensions", "materials", "surface_treatments", "mechanical_properties",
    "marking", "testing", "designation_examples", "reliability_notes",
    "sources", "meta",
]
VALID_CATEGORIES = {
    "bolt", "nut", "washer", "socket_screw", "set_screw",
    "lock_nut", "thread_standard", "general_specification",
}
VALID_BODIES    = {"ISO", "GOST", "BIS", "DIN"}
VALID_STATUSES  = {"active", "withdrawn"}
VALID_CONFIDENCE = {"high", "medium", "flag"}

REQUIRED_EQUIVALENTS  = {"iso", "din", "gost", "indian"}
REQUIRED_DIMENSIONS   = {"head_type", "drive", "waf_notes", "length_range", "tolerance_grade"}
REQUIRED_MATERIALS    = {"primary", "stainless_variants", "notes"}
REQUIRED_SURFACE      = {"available", "prohibited", "coating_codes", "hydrogen_embrittlement_bake"}
REQUIRED_MARKING      = {"head_marking_required", "class_12_9_rule", "notes"}
REQUIRED_TESTING      = {"proof_load_test", "prevailing_torque_cycles", "standard_reference"}
REQUIRED_DESIGNATION  = {"gost", "iso", "din", "indian"}
REQUIRED_META         = {"source_type", "legal_status", "doc_version", "last_updated"}

MP_REQUIRED = {
    "property_class", "tensile_strength_mpa", "yield_strength_mpa",
    "hardness_min", "hardness_max", "proof_load_mpa",
}


def check(errors: list, path: str, condition: bool, msg: str):
    if not condition:
        errors.append(f"  [{path}] {msg}")


def validate_record(data: dict, filepath: str) -> list[str]:
    errors = []
    p = filepath

    # Top-level required keys
    for k in REQUIRED_TOP:
        check(errors, p, k in data, f"missing required key '{k}'")

    check(errors, p, data.get("category") in VALID_CATEGORIES,
          f"category '{data.get('category')}' not in {VALID_CATEGORIES}")
    check(errors, p, data.get("body") in VALID_BODIES,
          f"body '{data.get('body')}' not in {VALID_BODIES}")
    check(errors, p, data.get("status") in VALID_STATUSES,
          f"status '{data.get('status')}' not in {VALID_STATUSES}")
    check(errors, p, data.get("confidence") in VALID_CONFIDENCE,
          f"confidence '{data.get('confidence')}' not in {VALID_CONFIDENCE}")

    # Sub-objects
    for key, required_keys in [
        ("equivalents",        REQUIRED_EQUIVALENTS),
        ("dimensions",         REQUIRED_DIMENSIONS),
        ("materials",          REQUIRED_MATERIALS),
        ("surface_treatments", REQUIRED_SURFACE),
        ("marking",            REQUIRED_MARKING),
        ("testing",            REQUIRED_TESTING),
        ("designation_examples", REQUIRED_DESIGNATION),
        ("meta",               REQUIRED_META),
    ]:
        obj = data.get(key, {})
        if isinstance(obj, dict):
            for rk in required_keys:
                check(errors, p, rk in obj, f"'{key}.{rk}' missing")
        else:
            check(errors, p, False, f"'{key}' must be a mapping, got {type(obj).__name__}")

    # equivalents lists must be lists
    eq = data.get("equivalents", {})
    if isinstance(eq, dict):
        for body in REQUIRED_EQUIVALENTS:
            val = eq.get(body)
            check(errors, p, isinstance(val, list),
                  f"equivalents.{body} must be a list, got {type(val).__name__}")

    # mechanical_properties must be a list of mappings with required keys
    mp = data.get("mechanical_properties", [])
    check(errors, p, isinstance(mp, list), "mechanical_properties must be a list")
    if isinstance(mp, list):
        for i, entry in enumerate(mp):
            if not isinstance(entry, dict):
                errors.append(f"  [{p}] mechanical_properties[{i}] must be a mapping")
                continue
            for rk in MP_REQUIRED:
                check(errors, p, rk in entry,
                      f"mechanical_properties[{i}] missing '{rk}'")

    # reliability_notes and sources must be lists
    for field in ("reliability_notes", "sources", "property_classes"):
        val = data.get(field)
        check(errors, p, isinstance(val, list),
              f"'{field}' must be a list, got {type(val).__name__}")

    return errors


def main():
    all_errors = []
    files = sorted(YAML_DIR.rglob("*.yaml"))
    print(f"Validating {len(files)} YAML files in {YAML_DIR} ...\n")

    for f in files:
        try:
            with open(f, encoding="utf-8") as fh:
                data = yaml.safe_load(fh)
            errs = validate_record(data, f.relative_to(ROOT).as_posix())
            if errs:
                all_errors.extend(errs)
        except yaml.YAMLError as exc:
            all_errors.append(f"  [{f.relative_to(ROOT).as_posix()}] YAML parse error: {exc}")

    if all_errors:
        print(f"VALIDATION FAILED — {len(all_errors)} issue(s):\n")
        for e in all_errors:
            print(e)
        sys.exit(1)
    else:
        print(f"All {len(files)} files passed validation.")
        sys.exit(0)


if __name__ == "__main__":
    main()
