# Fastener Standards Cross-Reference Database

A normalized, machine-readable reference database covering metric fastener standards across four standards bodies: **GOST** (Soviet/Russian), **ISO** (International), **DIN** (German), and **IS/BIS** (Indian). Built for engineering cross-referencing, procurement substitution, RAG/AI retrieval, and SQLite/API ingestion.

---

## Overview

When working across international engineering contexts — Russian legacy plant, European procurement, Indian manufacturing — the same physical fastener may be specified under four different standard numbers. This database maps all of those equivalences in one place, with full technical content per standard: dimensions, mechanical properties, materials, surface treatments, marking, testing, designation strings, and reusability rules.

**65 standards documented. 4 standards bodies. 7 fastener categories.**

---

## Repository Structure

```
stanadard/
├── README.md                          ← this file
├── gost_crossref_research.md          ← source research document (Category 1)
├── gost_crossref_category2_socket_setscrew_locknut.md  ← source research (Category 2)
└── standards/
    ├── index.json                     ← machine-readable cross-reference index (all 65 standards)
    ├── gost/
    │   ├── bolts/                     ← 9 files
    │   ├── nuts/                      ← 2 files
    │   ├── washers/                   ← 2 files
    │   ├── socket_screws/             ← 1 file
    │   ├── set_screws/                ← 2 files
    │   ├── lock_nuts/                 ← 2 files
    │   ├── thread_standards/          ← 3 files
    │   └── general/                   ← 2 files
    ├── iso/
    │   ├── bolts/                     ← 4 files
    │   ├── nuts/                      ← 4 files
    │   ├── washers/                   ← 2 files
    │   ├── socket_screws/             ← 2 files
    │   └── set_screws/                ← 4 files
    ├── din/
    │   ├── bolts/                     ← 4 files
    │   ├── nuts/                      ← 4 files
    │   ├── washers/                   ← 2 files
    │   ├── socket_screws/             ← 1 file
    │   └── set_screws/                ← 4 files
    └── indian/
        ├── bolts/                     ← 5 files
        ├── nuts/                      ← 2 files
        ├── washers/                   ← 2 files
        ├── socket_screws/             ← 1 file
        └── set_screws/                ← 4 files
```

---

## Standards Covered

### GOST (Soviet / Russian Federation) — 23 files

#### Bolts (9)
| File | Standard | Title |
|------|----------|-------|
| `gost/bolts/7798-70.md` | GOST 7798-70 | Hex bolt, Grade B, partial thread — M6–M48 |
| `gost/bolts/7805-70.md` | GOST 7805-70 | Hex bolt, full thread — M1.6–M64 |
| `gost/bolts/7817-80.md` | GOST 7817-80 | Hex bolt, Grade A precision, partial thread — M1.6–M24 |
| `gost/bolts/15589-70.md` | GOST 15589-70 | Hex bolt, Grade C (black) — max class 5.8 |
| `gost/bolts/22353-77.md` | GOST 22353-77 | High-strength structural bolt, large WAF — class 10.9, single-use |
| `gost/bolts/r-52643-2006.md` | GOST R 52643-2006 | Structural bolt assembly general spec (modern RF) |
| `gost/bolts/r-52644-2006.md` | GOST R 52644-2006 | Structural bolt dimensions, large WAF (modern RF) |
| `gost/bolts/24379.0-80.md` | GOST 24379.0-80 | Foundation bolt — general specification |
| `gost/bolts/24379.1-80.md` | GOST 24379.1-80 | Foundation bolt — 7 types, M12–M125, up to 5000 mm |

#### Nuts (2)
| File | Standard | Title |
|------|----------|-------|
| `gost/nuts/5915-70.md` | GOST 5915-70 | Hex nut style 1, Grade B — M1.6–M64 |
| `gost/nuts/5927-70.md` | GOST 5927-70 | Hex nut style 1, Grade A — M1.6–M16 |

#### Washers (2)
| File | Standard | Title |
|------|----------|-------|
| `gost/washers/11371-78.md` | GOST 11371-78 | Plain washer — 200HV and 300HV, M1–M48 |
| `gost/washers/6402-70.md` | GOST 6402-70 | Spring lock washer (Grover) — 4 types, M2–M48, single-use |

#### Socket Screws (1)
| File | Standard | Title |
|------|----------|-------|
| `gost/socket_screws/11738-84.md` | GOST 11738-84 | Socket head cap screw (Allen bolt) — M1.6–M64, classes 8.8–12.9 |

#### Set Screws (2)
| File | Standard | Title |
|------|----------|-------|
| `gost/set_screws/11074-93.md` | GOST 11074-93 | Socket set screw, flat point — M1.6–M24, class 45H |
| `gost/set_screws/11075-93.md` | GOST 11075-93 | Socket set screw, dog point — M1.6–M24, full/half dog |

#### Lock Nuts (2)
| File | Standard | Title |
|------|----------|-------|
| `gost/lock_nuts/50592-93.md` | GOST 50592-93 | Nylon insert lock nut, low form — max 120°C, 5-cycle max |
| `gost/lock_nuts/11872-89.md` | GOST 11872-89 | Nylon insert lock nut, high form — max 120°C, 5-cycle max |

#### Thread Standards (3)
| File | Standard | Title |
|------|----------|-------|
| `gost/thread_standards/9150-2002.md` | GOST 9150-2002 | Metric thread basic profile (60°) — identical to ISO 68-1 |
| `gost/thread_standards/8724-2002.md` | GOST 8724-2002 | Metric thread diameters and pitches — identical to ISO 261/262 |
| `gost/thread_standards/24705-2004.md` | GOST 24705-2004 | Metric thread basic dimensions — identical to ISO 724 |

#### General Specifications (2)
| File | Standard | Title |
|------|----------|-------|
| `gost/general/1759.4-87.md` | GOST 1759.4-87 | Bolt/screw/stud mechanical properties — all classes 3.6–12.9 |
| `gost/general/1759.5-87.md` | GOST 1759.5-87 | Nut mechanical properties — classes 4–12 |

---

### ISO (International) — 16 files

#### Bolts (4)
| File | Standard | Title |
|------|----------|-------|
| `iso/bolts/4014.md` | ISO 4014 | Hex bolt, partial thread, grades A and B |
| `iso/bolts/4017.md` | ISO 4017 | Hex screw, full thread, grades A and B |
| `iso/bolts/4016.md` | ISO 4016 | Hex bolt, grade C (black) |
| `iso/bolts/7411.md` | ISO 7411 | High-strength structural bolt, large WAF |

#### Nuts (4)
| File | Standard | Title |
|------|----------|-------|
| `iso/nuts/4032.md` | ISO 4032 | Hex nut style 1, grades A and B |
| `iso/nuts/7040.md` | ISO 7040 | Nylon insert lock nut, low form |
| `iso/nuts/7041.md` | ISO 7041 | Nylon insert lock nut, high form |
| `iso/nuts/7042.md` | ISO 7042 | All-metal prevailing torque lock nut (Stover) — up to 300°C+ |

#### Washers (2)
| File | Standard | Title |
|------|----------|-------|
| `iso/washers/7089.md` | ISO 7089 | Plain washer, no chamfer, 200HV |
| `iso/washers/7090.md` | ISO 7090 | Plain washer, chamfered bore, 300HV |

#### Socket Screws (2)
| File | Standard | Title |
|------|----------|-------|
| `iso/socket_screws/4762.md` | ISO 4762 | Socket head cap screw — replaces DIN 912 |
| `iso/socket_screws/7380.md` | ISO 7380 | Socket button head screw — no GOST/DIN/IS equivalent |

#### Set Screws (4)
| File | Standard | Title |
|------|----------|-------|
| `iso/set_screws/4026.md` | ISO 4026 | Socket set screw, flat point |
| `iso/set_screws/4027.md` | ISO 4027 | Socket set screw, cone point — no GOST equivalent |
| `iso/set_screws/4028.md` | ISO 4028 | Socket set screw, dog point |
| `iso/set_screws/4029.md` | ISO 4029 | Socket set screw, cup point — no GOST equivalent |

---

### DIN (German) — 15 files

> All DIN fastener standards in this database are **withdrawn** (except DIN 127). They are documented for legacy drawing support and spare-parts procurement. New designs must use the ISO replacements.

#### Bolts (4)
| File | Standard | Replaced By |
|------|----------|-------------|
| `din/bolts/din-931.md` | DIN 931 | ISO 4014 — note WAF differences at M10/M12/M14/M22 |
| `din/bolts/din-933.md` | DIN 933 | ISO 4017 — dimensions identical |
| `din/bolts/din-601.md` | DIN 601 | ISO 4016 |
| `din/bolts/din-6914.md` | DIN 6914 | EN 14399-4 |

#### Nuts (4)
| File | Standard | Replaced By |
|------|----------|-------------|
| `din/nuts/din-934.md` | DIN 934 | ISO 4032 — dimensions identical |
| `din/nuts/din-985.md` | DIN 985 | ISO 7040 (nyloc low form) |
| `din/nuts/din-982.md` | DIN 982 | ISO 7041 (nyloc high form) |
| `din/nuts/din-980.md` | DIN 980 | ISO 7042 (all-metal lock nut) |

#### Washers (2)
| File | Standard | Replaced By |
|------|----------|-------------|
| `din/washers/din-125.md` | DIN 125 | ISO 7089 (Type A) / ISO 7090 (Type B) |
| `din/washers/din-127.md` | DIN 127 | Active — spring lock washer, widely referenced |

#### Socket Screws (1)
| File | Standard | Replaced By |
|------|----------|-------------|
| `din/socket_screws/din-912.md` | DIN 912 | ISO 4762 — dimensions identical; most-referenced legacy number |

#### Set Screws (4)
| File | Standard | Replaced By |
|------|----------|-------------|
| `din/set_screws/din-913.md` | DIN 913 | ISO 4026 (flat point) |
| `din/set_screws/din-914.md` | DIN 914 | ISO 4027 (cone point) |
| `din/set_screws/din-915.md` | DIN 915 | ISO 4028 (dog point) |
| `din/set_screws/din-916.md` | DIN 916 | ISO 4029 (cup point) |

---

### IS / BIS (Indian) — 14 files

#### Bolts (5)
| File | Standard | Title |
|------|----------|-------|
| `indian/bolts/is-1364-1.md` | IS 1364-1 | Hex bolt, partial thread — harmonised with ISO 4014 |
| `indian/bolts/is-1364-2.md` | IS 1364-2 | Hex screw, full thread — harmonised with ISO 4017 |
| `indian/bolts/is-1363-1.md` | IS 1363-1 | Hex bolt, grade C (black) — harmonised with ISO 4016 |
| `indian/bolts/is-3757.md` | IS 3757 | High-strength structural bolt — classes 8.8S and 10.9S |
| `indian/bolts/is-5624.md` | IS 5624 | Foundation bolts — straight/L/plate types |

#### Nuts (2)
| File | Standard | Title |
|------|----------|-------|
| `indian/nuts/is-1364-3.md` | IS 1364-3 | Hex nut style 1 — **declared identical to ISO 4032 by BIS** |
| `indian/nuts/is-7002.md` | IS 7002 | Nylon insert lock nut — covers **both** low and high form |

#### Washers (2)
| File | Standard | Title |
|------|----------|-------|
| `indian/washers/is-2016.md` | IS 2016 | Plain washer |
| `indian/washers/is-3063.md` | IS 3063 | Spring lock washer (Grover) |

#### Socket Screws (1)
| File | Standard | Title |
|------|----------|-------|
| `indian/socket_screws/is-2269.md` | IS 2269 | Socket head cap screw |

#### Set Screws (4)
| File | Standard | Title |
|------|----------|-------|
| `indian/set_screws/is-6094-1.md` | IS 6094-1 | Socket set screw, flat point |
| `indian/set_screws/is-6094-2.md` | IS 6094-2 | Socket set screw, cone point |
| `indian/set_screws/is-6094-3.md` | IS 6094-3 | Socket set screw, dog point |
| `indian/set_screws/is-6094-4.md` | IS 6094-4 | Socket set screw, cup point |

---

## File Format

Every standard file uses the same structure:

### YAML Frontmatter

Each file opens with a YAML block containing machine-readable metadata:

```yaml
---
standard: GOST 7798-70
title: "Hexagon Head Bolt, Product Grade B (Partial Thread)"
category: bolt
sub_category: hex_bolt_partial_thread
country: "USSR/Russia"
body: GOST
equivalent_iso:
  - ISO 4014
equivalent_din:
  - DIN 931
equivalent_indian:
  - IS 1364-1
confidence: high          # high | medium | low | flag
thread_range: "M6-M48"
property_classes:
  - "4.6"
  - "8.8"
  - "10.9"
source_type: researched_summary
legal_status: factual_cross_reference
doc_version: "2.0"
last_updated: "2026-05"
---
```

**YAML field reference:**

| Field | Description |
|-------|-------------|
| `standard` | Full standard designation (e.g., `GOST 7798-70`) |
| `title` | Descriptive title |
| `category` | Top-level type: `bolt`, `nut`, `washer`, `socket_screw`, `set_screw`, `lock_nut`, `thread_standard`, `general_specification` |
| `sub_category` | Specific variant |
| `body` | Standards body: `GOST`, `ISO`, `DIN`, `BIS` |
| `country` | Country or `International` |
| `equivalent_*` | Arrays of equivalent standard numbers per body |
| `confidence` | `high` = 3+ sources confirmed; `medium` = 2 sources or minor discrepancy; `flag` = expert verification needed |
| `thread_range` | Nominal diameter range (e.g., `"M1.6-M64"`) |
| `property_classes` | Array of available property classes |
| `max_temperature_c` | For temperature-sensitive components (nyloc nuts) |
| `status` | For DIN files: `withdrawn` or `active` |
| `replaced_by` | For withdrawn standards: the replacement standard |
| `source_type` | Always `researched_summary` |
| `legal_status` | Always `factual_cross_reference` |
| `doc_version` | Schema version (`"2.0"`) |

### Markdown Body (11 Sections)

All files follow the same 11-section order:

1. **Standard Overview** — what the standard covers, historical context, key notes
2. **Cross References** — table of equivalents per standards body with confidence level
3. **Dimensions** — thread range, head dimensions, product grade, tolerance
4. **Mechanical Properties** — property class table with tensile/yield/hardness values
5. **Materials** — steel grades, alloying requirements, stainless variants
6. **Surface Treatments** — coating codes, prohibited treatments (e.g., HDG on nyloc), hydrogen embrittlement bake procedure
7. **Marking Requirements** — head marking rules, class 12.9 emboss-only rule
8. **Testing Requirements** — test methods, acceptance criteria, proof load testing
9. **Designation Examples** — full designation strings in GOST / ISO / DIN / IS formats
10. **Reliability Notes** — flags, safety-critical warnings, known discrepancies
11. **Sources Consulted** — reference list

---

## index.json

`standards/index.json` is a flat JSON array of all 65 standards. Each entry contains:

```json
{
  "standard": "GOST 7798-70",
  "title": "Hexagon Head Bolt with Shank — Grade B",
  "category": "bolt",
  "sub_category": "hex_bolt_partial_thread",
  "body": "GOST",
  "country": "USSR/Russia",
  "path": "standards/gost/bolts/7798-70.md",
  "equivalents": {
    "iso": ["ISO 4014"],
    "din": ["DIN 931"],
    "indian": ["IS 1364-1"]
  }
}
```

The index is the entry point for any programmatic lookup. Load it to:
- Find all standards equivalent to a given standard number
- Filter by `category`, `body`, or `sub_category`
- Retrieve the file path to read the full technical document

---

## Cross-Reference Quick Lookup

### Hex Bolt (Partial Thread)
| GOST | ISO | DIN | IS |
|------|-----|-----|----|
| GOST 7817-80 (Grade A) | ISO 4014 | DIN 931 *(withdrawn)* | IS 1364-1 |
| GOST 7798-70 (Grade B) | ISO 4014 | DIN 931 *(withdrawn)* | IS 1364-1 |
| GOST 15589-70 (Grade C) | ISO 4016 | DIN 601 *(withdrawn)* | IS 1363-1 |

### Hex Bolt (Full Thread)
| GOST | ISO | DIN | IS |
|------|-----|-----|----|
| GOST 7805-70 | ISO 4017 | DIN 933 *(withdrawn)* | IS 1364-2 |

### Structural Bolt
| GOST | ISO | DIN | IS |
|------|-----|-----|----|
| GOST 22353-77 | ISO 7411 | DIN 6914 *(withdrawn)* / EN 14399-4 | IS 3757 |
| GOST R 52644-2006 | ISO 7411 | EN 14399-4 | IS 3757 |

### Hex Nut (Style 1)
| GOST | ISO | DIN | IS |
|------|-----|-----|----|
| GOST 5927-70 (Grade A) | ISO 4032 | DIN 934 *(withdrawn)* | IS 1364-3 |
| GOST 5915-70 (Grade B) | ISO 4032 | DIN 934 *(withdrawn)* | IS 1364-3 |

### Lock Nuts
| GOST | ISO | DIN | IS | Notes |
|------|-----|-----|-----|-------|
| GOST 50592-93 | ISO 7040 | DIN 985 *(withdrawn)* | IS 7002 | Nyloc, low form — max 120°C |
| GOST 11872-89 | ISO 7041 | DIN 982 *(withdrawn)* | IS 7002 | Nyloc, high form — max 120°C |
| *(none)* | ISO 7042 | DIN 980 *(withdrawn)* | *(none)* | All-metal — up to 300°C+ |

### Plain Washers
| GOST | ISO | DIN | IS |
|------|-----|-----|----|
| GOST 11371-78 (200HV) | ISO 7089 | DIN 125-A *(withdrawn)* | IS 2016 |
| GOST 11371-78 (300HV) | ISO 7090 | DIN 125-B *(withdrawn)* | IS 2016 |

### Spring Lock Washers
| GOST | ISO | DIN | IS |
|------|-----|-----|----|
| GOST 6402-70 | ISO 8738 | DIN 127 | IS 3063 |

### Socket Head Cap Screw
| GOST | ISO | DIN | IS |
|------|-----|-----|----|
| GOST 11738-84 | ISO 4762 | DIN 912 *(withdrawn)* | IS 2269 |

### Set Screws
| Point Type | GOST | ISO | DIN | IS | Notes |
|-----------|------|-----|-----|----|-------|
| Flat | GOST 11074-93 | ISO 4026 | DIN 913 *(withdrawn)* | IS 6094-1 | Lowest holding, minimal damage |
| Cone | *(none)* | ISO 4027 | DIN 914 *(withdrawn)* | IS 6094-2 | High holding, high shaft damage |
| Dog | GOST 11075-93 | ISO 4028 | DIN 915 *(withdrawn)* | IS 6094-3 | Highest holding, needs machined recess |
| Cup | *(none)* | ISO 4029 | DIN 916 *(withdrawn)* | IS 6094-4 | Most common worldwide, moderate damage |

---

## Key Technical Notes

### DIN Withdrawal
Every DIN fastener standard in this database (except DIN 127) has been formally withdrawn. The replacement in all cases is the corresponding ISO standard. For the most common legacy reference — **DIN 912** — the replacement is **ISO 4762**, with identical dimensions. New designs must not cite withdrawn DIN standards.

**Important exception — DIN 931 WAF:** DIN 931 and ISO 4014 differ in WAF (width across flats) at four sizes:

| Size | DIN 931 WAF | ISO 4014 WAF |
|------|-------------|--------------|
| M10 | 17 mm | 16 mm |
| M12 | 19 mm | 18 mm |
| M14 | 22 mm | 21 mm |
| M22 | 32 mm | 34 mm |

Verify socket/spanner compatibility before substituting ISO 4014 for DIN 931 at these sizes.

### IS 1364-3 Identity Declaration
BIS has formally declared **IS 1364-3 as identical to ISO 4032**. This is not merely harmonisation — it is a direct adoption. IS 1364-3 nuts are fully interchangeable with ISO 4032 nuts for all engineering purposes.

### IS 7002 Covers Both Lock Nut Forms
Unlike ISO (which separates nyloc nuts into two standards — ISO 7040 low form and ISO 7041 high form), **IS 7002 covers both forms in a single document**. Always specify "Low Form" or "High Form" explicitly when ordering under IS 7002.

### Nylon Insert Lock Nut Temperature Limit
GOST 50592-93, GOST 11872-89, ISO 7040, ISO 7041, DIN 985, DIN 982, IS 7002 — all nylon insert lock nuts share:
- **Maximum temperature:** 120°C continuous (PA6/PA66 insert degrades above this)
- **HDG prohibited:** Hot-dip galvanizing (450°C bath) destroys the nylon insert
- **Maximum reuse cycles:** 5 per ISO 2320 prevailing torque test protocol

For temperatures above 120°C or HDG assemblies, use **ISO 7042 / DIN 980** (all-metal lock nut).

### Class 12.9 Marking Rule
Property class 12.9 fasteners must be marked by **embossing or side-face stamping only**. Indented top-face marking creates stress concentrations that can initiate fatigue cracks at the mark. This applies across all standards bodies.

### Hydrogen Embrittlement Risk
Electroplated (acid-bath) fasteners of class 10.9 and 12.9 are susceptible to hydrogen embrittlement. Mandatory bake procedure: **190–210°C for a minimum of 4 hours** within 4 hours of plating, before any mechanical stress application.

### Structural Bolt Single-Use Rule
GOST 22353-77, GOST R 52644-2006, ISO 7411, DIN 6914, EN 14399-4, IS 3757 — all high-strength structural bolts are **single-use**. Once proof-load tightened into a friction-grip joint, they must not be removed and reused. Mark removed bolts for disposal.

### GOST Coating Codes
GOST fastener orders append a coating code to the designation string:

| Code | Coating |
|------|---------|
| 00 | No coating (black / as-rolled) |
| 01 | Zinc electroplate, 6 µm min |
| 03 | Cadmium plate (legacy — restricted use) |
| 12 | Phosphate + oil |
| 13 | Phosphate + grease |
| 40 | Hot-dip galvanized (HDG) |

### Set Screw GOST Gap
GOST has no confirmed standard number for cone point (ISO 4027) or cup point (ISO 4029) set screws. Russian engineering drawings reference ISO 4027 and ISO 4029 directly. This is flagged in the relevant files with `FLAG` confidence level.

---

## Usage

### Finding Equivalents for a Known Standard

**Option 1 — index.json lookup:**
```python
import json

with open("standards/index.json") as f:
    index = json.load(f)

# Find equivalents for GOST 7798-70
entry = next(e for e in index if e["standard"] == "GOST 7798-70")
print(entry["equivalents"])
# → {"iso": ["ISO 4014"], "din": ["DIN 931"], "indian": ["IS 1364-1"]}
print(entry["path"])
# → standards/gost/bolts/7798-70.md
```

**Option 2 — grep YAML frontmatter:**
```bash
grep -rl "ISO 4014" standards/ --include="*.md"
```

### Loading into SQLite

The YAML frontmatter and index.json are structured for direct import. Example schema:

```sql
CREATE TABLE standards (
    standard        TEXT PRIMARY KEY,
    title           TEXT,
    category        TEXT,
    sub_category    TEXT,
    body            TEXT,
    country         TEXT,
    path            TEXT,
    doc_version     TEXT,
    last_updated    TEXT
);

CREATE TABLE equivalents (
    standard        TEXT REFERENCES standards(standard),
    body            TEXT,   -- 'iso', 'din', 'indian', 'gost', 'astm'
    equivalent      TEXT
);
```

Parse `index.json` and the `equivalents` object of each entry to populate both tables.

### RAG / AI Retrieval

Each file is self-contained with YAML frontmatter for metadata filtering and structured markdown for chunked retrieval. Recommended chunking strategy:

- **Chunk 1:** YAML frontmatter (metadata + equivalents) — use for routing/filtering
- **Chunk 2:** Standard Overview + Cross References — use for identification queries
- **Chunk 3:** Dimensions + Mechanical Properties — use for technical specification queries
- **Chunk 4:** Surface Treatments + Marking + Testing — use for compliance queries
- **Chunk 5:** Designation Examples + Reliability Notes — use for ordering and engineering decision queries

---

## Legal and Intellectual Property

All content in this database is original writing. Standard numbers, dimensional values, material grades, and mechanical property values are treated as factual information not subject to copyright, consistent with:

- *Feist Publications v. Rural Telephone Service Co.* (US Supreme Court, 1991) — facts are not copyrightable
- EU Database Directive 96/9/EC — extracted facts do not infringe database right
- Indian Copyright Act 1957, Section 13 — facts and data in the public domain are not protected

No verbatim text from any published standard document has been reproduced. All descriptions, summaries, notes, and analyses are original.

---

## Source Documents

The research underlying this database is preserved in the two source documents at the root of the workspace:

- [gost_crossref_research.md](gost_crossref_research.md) — Category 1: hex bolts, nuts, washers, thread standards, mechanical properties. Version 2.0 with 14 sections including marking, surface treatments, materials, testing, designation strings, torque tables, and reusability.
- [gost_crossref_category2_socket_setscrew_locknut.md](gost_crossref_category2_socket_setscrew_locknut.md) — Category 2: socket head screws, set screws (4 point types), lock nuts (nylon insert and all-metal). Version 2.0 with sections D–J.

---

## Contributing / Extending

To add a new standard:

1. Create the file at the correct path: `standards/{body}/{category}/{number}.md`
2. Use the YAML frontmatter schema documented above
3. Include all 11 sections in order
4. Add a corresponding entry to `standards/index.json`
5. Update any existing files that cross-reference the new standard

To add a new standards body (e.g., ASTM, JIS, GB):
1. Create a new top-level folder under `standards/`
2. Mirror the category subfolder structure
3. Add `equivalent_{body}` arrays to relevant existing files
4. Add the new equivalents key to the `index.json` schema

---

*Database version 2.0 — May 2026*
