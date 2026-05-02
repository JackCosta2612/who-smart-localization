# who-smart-localization

Model-neutral Agent Skills for WHO SMART Guidelines localization work.

This repository is part of a one-month, 3 ECTS university NLP project connected to WHO SMART Guidelines localization. It currently contains the Country Profiling skill as the first implemented skill in a broader localization skill package. Examples and first tests are the next phase and should be treated as placeholders until real source material is added.

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

Status: implemented / MVP polish.

Creates a structured, source-backed country profile for a target health domain and DAK or SMART Guidelines scope. It supports document-only use from supplied sources and optional retrieval-assisted use when helper scripts are available.

Path: `skills/country-profiling/`

### Policy Comparison

Status: planned for later integration.

Compares WHO source content with local policy material and produces a traceable localization matrix.

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
python3 skills/country-profiling/scripts/validate_profile.py skills/country-profiling/examples/example-output-1.md
```

Policy comparison matrix validator:

```bash
python3 skills/policy-comparison/scripts/validate_matrix.py skills/policy-comparison/examples/example-output-1.md
```

Validators check structure only. They do not validate clinical correctness, policy correctness, country facts, or source interpretation.
