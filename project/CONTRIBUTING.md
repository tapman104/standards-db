# Contributing Guide

Thank you for contributing to the Fastener Standards Domain Database.

## Scope

This project curates structured engineering standard records (YAML + Markdown) and exports validated data for search and analytics.

## Contribution Types

You can contribute by:
- Adding new standards
- Correcting technical values
- Improving equivalence mappings
- Improving validation/build tooling
- Reporting data quality issues

## Folder and Naming Rules

- Place fastener records under [project/domains/mechanical/fasteners](domains/mechanical/fasteners)
- Keep body/type folder conventions intact (`iso`, `din`, `gost`, `indian`)
- Use lowercase file names with existing style patterns

## Record Quality Requirements

Every submitted record must:
- Conform to [project/schemas/standard.schema.yaml](schemas/standard.schema.yaml)
- Use `null` for non-applicable scalar fields
- Use empty arrays `[]` for non-applicable lists
- Provide source references in `sources`
- Set realistic `confidence` based on source quality

## Validation and Build

Before submitting, run from [project/build](build):

```bash
python validate.py
python build_sqlite.py
```

Expected:
- Validation passes without errors
- SQLite database builds successfully

## Pull Request Checklist

- [ ] Schema validation passes
- [ ] Source citations included and relevant
- [ ] No unrelated file churn
- [ ] Changes are limited to the intended domain
- [ ] Documentation updated if structure/rules changed

## Data Integrity Policy

- Do not invent technical values
- Prefer primary standards or authoritative references
- Mark uncertain fields with lower confidence and clear notes

## Review Expectations

Maintainers prioritize:
- Technical correctness
- Traceability to source material
- Consistency with existing data conventions

## Questions

Open an issue with:
- Standard identifier
- Affected fields
- Source reference
- Expected correction
