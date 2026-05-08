# Fastener Standards Domain Database (ISO, DIN, GOST, BIS)

A structured, machine-readable engineering standards repository for mechanical fasteners. This project organizes international fastener standards into YAML + Markdown records, validates them against a strict schema, and builds a searchable SQLite database for manufacturing, procurement, QA, and engineering automation.

Keywords: fastener standards database, ISO fastener standards, DIN standards, GOST standards, BIS standards, bolt standards, nut standards, washer standards, machine-readable standards, engineering compliance data.

## What This Project Is

This repository is a domain-organized standards knowledge base focused on fasteners under the mechanical domain.

It provides:
- Canonical YAML records for each standard
- Human-readable Markdown documents for each standard
- A strict schema for structural consistency
- Validation tooling for quality checks
- SQLite export for querying and integrations

## Project Structure

```text
├── project/
│   ├── build/
│   │   ├── validate.py
│   │   ├── build_sqlite.py
│   │   ├── schema.sql
│   │   └── sqlite/
│   │       └── standards.db
│   ├── domains/
│   │   ├── mechanical/
│   │   │   └── fasteners/
│   │   │       ├── iso/
│   │   │       ├── din/
│   │   │       ├── gost/
│   │   │       └── indian/
│   │   ├── electrical/
│   │   ├── materials/
│   │   ├── fluid/
│   │   └── manufacturing/
│   ├── schemas/
│   │   └── standard.schema.yaml
│   ├── CODE_OF_CONDUCT.md
│   ├── CONTRIBUTING.md
│   └── LEGAL.md
├── scripts/
│   └── generate_all.py
└── README.md
```

## Data Model (Fast Summary)

Each standard record includes normalized fields such as:
- Identity: standard, title, body, country, status
- Classification: category, sub_category
- Technical: dimensions, materials, surface_treatments, mechanical_properties
- Interoperability: equivalents (ISO/DIN/GOST/Indian)
- Compliance metadata: sources, legal_status, confidence, versioning

Schema source: [project/schemas/standard.schema.yaml](project/schemas/standard.schema.yaml)

## Quick Start

### 1) Requirements
- Python 3.9+
- PyYAML installed (`pip install pyyaml`)

### 2) Validate all standards
From [project/build](build):

```bash
python validate.py
```

Expected output: all YAML files pass validation.

### 3) Build SQLite database
From [project/build](build):

```bash
python build_sqlite.py
```

Output database:
- [project/build/sqlite/standards.db](project/build/sqlite/standards.db)

## How to Use the Data

### Browse standard files
Fastener files are grouped by body and type in:
- [project/domains/mechanical/fasteners](domains/mechanical/fasteners)

### Query SQLite quickly
Example SQL:

```sql
SELECT standard, title, body, category
FROM standards
WHERE body IN ('ISO', 'DIN')
ORDER BY standard;
```

### Integrate in applications
- Load YAML records for rule engines and metadata pipelines
- Use SQLite for dashboards, APIs, and compliance lookup tools
- Join equivalents and mechanical properties tables for cross-standard analysis

## Legal and Compliance

Please review:
- [project/LEGAL.md](project/LEGAL.md)

Important points:
- This project is an engineering reference dataset, not legal advice
- Standards bodies own official texts and trademarks
- Verify requirements against official, purchased/current standards before production use

## Contributing

Contributions are welcome. Start here:
- [project/CONTRIBUTING.md](project/CONTRIBUTING.md)

Please make sure all contributed records:
- Follow the schema exactly
- Include reliable technical sources
- Pass `python validate.py` before submission

## Code of Conduct

This project adopts a contributor conduct policy:
- [project/CODE_OF_CONDUCT.md](project/CODE_OF_CONDUCT.md)

## Maintainer Notes

If you expand the repository into new domains (electrical, materials, fluid, manufacturing), keep:
- A domain-first directory pattern
- Machine-readable canonical sources
- Validation-first workflow

## SEO Notes

This README intentionally includes high-intent technical terms used by engineers and sourcing teams, including ISO/DIN/GOST/BIS fastener standards, standards database, and machine-readable engineering data.
