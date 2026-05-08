#!/usr/bin/env python3
"""
Batch-generate standards markdown content for all fastener .md files.

Behavior:
- Scans project/domains/mechanical/fasteners/**/*.md
- Reads existing YAML frontmatter fields as seed context
- Skips files that already look complete (all required section headers + enough length)
- Writes generated markdown in-place
- Stores progress in .generation_state.json for resume after interruption

Requirements:
- pip install anthropic pyyaml
- set ANTHROPIC_API_KEY

Usage:
  python generate_all.py
  python generate_all.py --force
  python generate_all.py --limit 10
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

try:
    from anthropic import Anthropic
except Exception:
    Anthropic = None

ROOT = Path(__file__).resolve().parent
TARGET_GLOB = "project/domains/mechanical/fasteners/**/*.md"
STATE_FILE = ROOT / ".generation_state.json"

MODEL = "claude-opus-4-1-20250805"
MAX_TOKENS = 4000
REQUEST_DELAY_SECONDS = 1.0

REQUIRED_HEADERS = [
    "# Standard Overview",
    "# Cross References",
    "# Dimensions",
    "# Mechanical Properties",
    "# Materials",
    "# Surface Treatments",
    "# Marking Requirements",
    "# Testing Requirements",
    "# Designation Examples",
    "# Reliability Notes",
    "# Sources Consulted",
]

TEMPLATE = """---
standard: ""
title: ""
category: ""
sub_category: ""
body: ""
country: ""
status: ""
replaced_by: null
equivalent_gost: []
equivalent_iso: []
equivalent_din: []
equivalent_indian: []
confidence: ""
thread_range: ""
thread_tolerance: ""
product_grade: null
property_classes: []
max_temperature_c: null
single_use: false
source_type: researched_summary
legal_status: factual_cross_reference
doc_version: "2.0"
last_updated: "2026-05"
---

# Standard Overview
# Cross References
# Dimensions
# Mechanical Properties
# Materials
# Surface Treatments
# Marking Requirements
# Testing Requirements
# Designation Examples
# Reliability Notes
# Sources Consulted
"""

SYSTEM_PROMPT = """You are a technical standards database author.
Return ONLY completed markdown with YAML frontmatter. No preamble and no code fences.
Rules:
1. All prose must be original. Never copy standard text verbatim.
2. Dimensional values, property classes, standard numbers are factual and may be used.
3. Use null for missing scalar values and [] for missing lists.
4. confidence values: high, medium, low, or flag.
5. Fill every section completely.
6. If a value cannot be confirmed, write \"Not confirmed in available sources\".
7. For withdrawn standards, set replaced_by where known and mention withdrawal in overview.
8. For nyloc lock nuts: include max_temperature_c=120, HDG prohibited, max 5 reuse cycles.
9. For structural bolt systems intended for preloaded joints, set single_use=true.
10. Do not output placeholders, TODOs, or instruction comments.
11. Keep output valid markdown + valid YAML frontmatter.
"""


@dataclass
class Job:
    path: Path
    frontmatter: dict[str, Any]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def parse_frontmatter(md_text: str) -> dict[str, Any]:
    match = re.match(r"^---\n(.*?)\n---\n", md_text, re.DOTALL)
    if not match:
        return {}
    try:
        data = yaml.safe_load(match.group(1))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def has_required_sections(md_text: str) -> bool:
    return all(h in md_text for h in REQUIRED_HEADERS)


def looks_complete(md_text: str) -> bool:
    # Practical heuristic: all sections present + substantial body length.
    if not has_required_sections(md_text):
        return False
    return len(md_text) >= 1800


def discover_jobs() -> list[Job]:
    jobs: list[Job] = []
    for path in sorted(ROOT.glob(TARGET_GLOB)):
        text = read_text(path)
        fm = parse_frontmatter(text)
        jobs.append(Job(path=path, frontmatter=fm))
    return jobs


def load_state() -> dict[str, Any]:
    if not STATE_FILE.exists():
        return {"done": [], "failed": {}}
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data.setdefault("done", [])
            data.setdefault("failed", {})
            return data
    except Exception:
        pass
    return {"done": [], "failed": {}}


def save_state(state: dict[str, Any]) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def build_user_prompt(job: Job, current_text: str) -> str:
    fm = job.frontmatter or {}
    seed = {
        "standard": fm.get("standard"),
        "title": fm.get("title"),
        "category": fm.get("category"),
        "sub_category": fm.get("sub_category"),
        "body": fm.get("body"),
        "country": fm.get("country"),
        "status": fm.get("status"),
        "replaced_by": fm.get("replaced_by"),
        "equivalent_gost": fm.get("equivalent_gost"),
        "equivalent_iso": fm.get("equivalent_iso"),
        "equivalent_din": fm.get("equivalent_din"),
        "equivalent_indian": fm.get("equivalent_indian"),
        "confidence": fm.get("confidence"),
        "thread_range": fm.get("thread_range"),
        "thread_tolerance": fm.get("thread_tolerance"),
        "product_grade": fm.get("product_grade"),
        "property_classes": fm.get("property_classes"),
        "max_temperature_c": fm.get("max_temperature_c"),
        "single_use": fm.get("single_use"),
        "last_updated": fm.get("last_updated"),
    }

    return (
        "Complete this standards markdown file using the given schema and section structure.\n"
        "Use the frontmatter seed values where present and correct obvious gaps if needed.\n"
        "Preserve file's standard identity and body/country context.\n\n"
        f"Target file: {job.path.as_posix()}\n"
        f"Seed frontmatter JSON:\n{json.dumps(seed, ensure_ascii=False, indent=2)}\n\n"
        f"Template structure to fill:\n{TEMPLATE}\n"
        "Return the full file content only.\n"
    )


def generate_content(client: Any, prompt: str) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    parts = []
    for block in response.content:
        if getattr(block, "type", "") == "text":
            parts.append(block.text)
    return "".join(parts).strip() + "\n"


def validate_generated(text: str) -> list[str]:
    errs: list[str] = []
    if not text.startswith("---\n"):
        errs.append("Missing YAML frontmatter start")
    if not has_required_sections(text):
        errs.append("Missing one or more required section headers")

    # Ensure frontmatter is parseable.
    fm = parse_frontmatter(text)
    if not fm:
        errs.append("Unparseable or missing frontmatter")
    else:
        for key in ["standard", "title", "category", "sub_category", "body", "country", "status"]:
            if key not in fm:
                errs.append(f"Missing frontmatter key: {key}")

    return errs


def main() -> int:
    parser = argparse.ArgumentParser(description="Batch-generate standards markdown content")
    parser.add_argument("--force", action="store_true", help="Regenerate even if file looks complete")
    parser.add_argument("--limit", type=int, default=0, help="Process at most N files this run")
    parser.add_argument("--retry-failed", action="store_true", help="Only retry files in failed state")
    args = parser.parse_args()

    if Anthropic is None:
        print("ERROR: anthropic package is not installed. Run: pip install anthropic pyyaml", file=sys.stderr)
        return 2

    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY is not set", file=sys.stderr)
        return 2

    jobs = discover_jobs()
    if not jobs:
        print("No markdown files found under project/domains/mechanical/fasteners")
        return 0

    state = load_state()
    done: set[str] = set(state.get("done", []))
    failed: dict[str, str] = dict(state.get("failed", {}))

    if args.retry_failed:
        targets = [j for j in jobs if j.path.as_posix() in failed]
    else:
        targets = jobs

    client = Anthropic(api_key=api_key)

    processed = 0
    generated = 0
    skipped = 0

    for job in targets:
        rel = job.path.as_posix()

        if args.limit and processed >= args.limit:
            break

        text = read_text(job.path)

        if not args.force:
            if rel in done:
                print(f"SKIP (state done): {rel}")
                skipped += 1
                continue
            if looks_complete(text):
                print(f"SKIP (looks complete): {rel}")
                done.add(rel)
                if rel in failed:
                    del failed[rel]
                skipped += 1
                continue

        prompt = build_user_prompt(job, text)

        try:
            output = generate_content(client, prompt)
            validation_errors = validate_generated(output)
            if validation_errors:
                msg = "; ".join(validation_errors)
                failed[rel] = msg
                print(f"FAIL (validation): {rel} -> {msg}")
            else:
                write_text(job.path, output)
                done.add(rel)
                if rel in failed:
                    del failed[rel]
                generated += 1
                print(f"OK: {rel}")
        except Exception as exc:
            failed[rel] = str(exc)
            print(f"FAIL (exception): {rel} -> {exc}")

        processed += 1
        save_state({"done": sorted(done), "failed": failed})
        time.sleep(REQUEST_DELAY_SECONDS)

    save_state({"done": sorted(done), "failed": failed})

    print("\nRun summary")
    print(f"  processed: {processed}")
    print(f"  generated: {generated}")
    print(f"  skipped:   {skipped}")
    print(f"  failed:    {len(failed)}")
    print(f"  state:     {STATE_FILE.as_posix()}")

    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
