# who-smart-localization

Model-neutral Agent Skills for WHO SMART Guidelines localization work.

This repository is part of a one-month, 3 ECTS university NLP project connected to WHO SMART Guidelines localization. It currently contains the Country Profiling skill as the first implemented skill in a broader localization skill package. Real examples and first tests are still intentionally pending until source-backed examples are created.

## Project scope

The skills support preparation and review work for WHO SMART Guidelines and Digital Adaptation Kits (DAKs). They help organize sources, identify evidence gaps, and prepare structured outputs for human review.

They do not make clinical decisions, provide patient advice, draft final national policy, or replace WHO, national, legal, clinical, policy, or country experts.

## Repository structure

```text
.
├── README.md
├── SKILLS.md
├── docs/
│   └── repository-structure.md
├── shared/
│   └── assets/
└── skills/
    ├── country-profiling/
    │   ├── SKILL.md
    │   ├── README.md
    │   ├── context/
    │   ├── examples/
    │   ├── scripts/
    │   └── tests/
    └── policy-comparison/
        ├── SKILL.md
        ├── README.md
        ├── context/
        ├── examples/
        ├── scripts/
        └── tests/
```

## Current skills

### Country Profiling

Status: implemented / documentation pivot.

Creates a source-backed textual healthcare country profile covering country context, main health issues, health system organization, access and coverage, sanitary conditions, financing, workforce, infrastructure, digital health, equity, risks, and readiness for later policy comparison.

Path: `skills/country-profiling/`

### Policy Comparison

Status: migrated starting point / planned for later iteration.

Contains the previous policy-oriented country-profiling package as a starting point for the later policy-comparison skill.

Path: `skills/policy-comparison/`

## Basic workflow

```bash
git checkout main
git pull origin main
git checkout -b short-description
```

After editing:

```bash
git status
git add .
git commit -m "Short description of change"
git push -u origin short-description
```

Open a pull request on GitHub for team review before merging.

## Local checks

Country profile validator:

```bash
python3 skills/country-profiling/scripts/validate_profile.py --help
```

Policy comparison matrix validator:

```bash
python3 skills/policy-comparison/scripts/validate_profile.py --help
```

Validators check structure only. They do not validate clinical correctness, policy correctness, country facts, or source interpretation.
